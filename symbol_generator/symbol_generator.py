import re
import argparse
import importlib.resources
import yaml
import collections.abc
from jinja2 import Environment
from symbol_generator.font_character_widths import font_character_widths

# Function to recursively update a dictionary
def update_recursive(dictionary, update):
  for key, value in update.items():
    if isinstance(value, collections.abc.Mapping):
      dictionary[key] = update_recursive(dictionary.get(key, {}), value)
    else:
      dictionary[key] = value
  return dictionary

def main():

  # Parse command line arguments
  argparser = argparse.ArgumentParser(description='Generate the SVG symbol of a hardware component from a description file.')
  argparser.add_argument('input_file', help='Path to the symbol description file.')
  argparser.add_argument("--scale", "-s", dest="scale", help="Scaling factor of the SVG.", default=1, type=float)
  argparser.add_argument("--theme", "-t", dest="theme_file", help="Path to a custom theme YAML file to override default settings.", default=None) # Default is None, load default theme first
  args = argparser.parse_args()

  # Read input file
  input_description = None
  try:
    with open(args.input_file, 'r') as input_file:
      input_description = input_file.read()
  except FileNotFoundError:
    print(f"ERROR: Input file not found at '{args.input_file}'.")
    exit(1)
  except Exception as exception:
    print(f"ERROR: Failed to read input file: {exception}.")
    exit(1)

  # Load default theme from package resources
  default_theme = None
  try:
    default_theme_ref = importlib.resources.files('symbol_generator').joinpath('default_theme.yaml')
    with importlib.resources.as_file(default_theme_ref) as default_theme_path:
      with open(default_theme_path, 'r') as theme_file:
        default_theme = yaml.safe_load(theme_file)
  except FileNotFoundError:
    print(f"ERROR: Default theme file 'default_theme.yaml' not found in package.")
    exit(1)
  except yaml.YAMLError as exception:
    print(f"ERROR: Default theme file is not a valid YAML file: {exception}.")
    exit(1)
  except Exception as exception:
    print(f"ERROR: Failed to load default theme file: {exception}.")
    exit(1)

  # Initialize theme with default theme
  theme = default_theme

  # Load custom theme file if provided and merge it into the default theme
  if args.theme_file:
    custom_theme = None
    try:
      with open(args.theme_file, 'r') as theme_file:
        custom_theme = yaml.safe_load(theme_file)
      if custom_theme:
        theme = update_recursive(theme, custom_theme)
    except FileNotFoundError:
      print(f"ERROR: Custom theme file not found at '{args.theme_file}'.")
      exit(1)
    except yaml.YAMLError as exception:
      print(f"ERROR: Custom theme file is not a valid YAML file: {exception}.")
      exit(1)
    except Exception as exception:
      print(f"ERROR: Failed to load custom theme file: {exception}.")
      exit(1)

  # Extract parameters from the final merged theme
  layout_config = theme['layout']
  font_config   = theme['fonts']
  color_config  = theme['colors']
  shapes_config = theme['shapes']

  # Drawing parameters (now loaded from theme)
  title_height           = layout_config['title_height']
  title_margin           = layout_config['title_margin']
  subtitle_height        = layout_config['subtitle_height']
  subtitle_margin        = layout_config['subtitle_margin']
  ports_height           = layout_config['ports_height']
  ports_label_margin     = layout_config['ports_label_margin']
  box_padding_top        = layout_config['box_padding_top']
  box_padding_bottom     = layout_config['box_padding_bottom']
  box_padding_sides      = layout_config['box_padding_sides']
  port_arrow_length      = layout_config['port_arrow_length']
  svg_padding            = layout_config['svg_padding']
  arrow_triangle_length  = shapes_config['arrow_triangle_length']
  arrow_triangle_height  = shapes_config['arrow_triangle_height']
  bus_line_distance      = shapes_config['bus_line_distance']
  bus_line_size          = shapes_config['bus_line_size']

  # Variables used in the SVG template
  template_variables = {}

  # Scale factor
  template_variables['scale'] = float(args.scale)

  # Colors
  template_variables['colors'] = color_config

  # Shapes
  template_variables['shapes'] = shapes_config

  # Font attributes (now structured per element)
  template_variables['fonts'] = font_config

  # Get width in pixels of text with specific font
  def get_text_width(text:str, font_name:str, font_weight:str="normal", font_size:int=6) -> int:
    # Check if the primary font family exists
    if font_name not in font_character_widths:
      print(f"WARNING: Font family '{font_name}' not found in character width data. Using estimated width based on font size.")
      # Calculate width using the formula for all characters
      width = len(text) * (font_size * 0.6)
      return int(round(width * 1.1))

    # Font family exists, try to get specific widths
    width = 0
    try:
      char_widths = font_character_widths[font_name][font_weight][font_size]
    except KeyError:
      # Handle missing weight/size combination for the existing font family
      print(f"WARNING: Font configuration '{font_name}' (Weight: {font_weight}, Size: {font_size}) not found. Using estimated width based on font size.")
      width = len(text) * (font_size * 0.6)
      return int(round(width * 1.1))

    # Font family, weight, and size combination exists, proceed character by character
    for character in text:
      char_width = char_widths.get(character)
      if char_width is None:
        # Handle missing character within the font data
        print(f"WARNING: Character '{character}' not found in width data for font '{font_name}' (Weight: {font_weight}, Size: {font_size}). Using estimated width for this character.")
        # Estimate width for the missing character (e.g., using space or formula)
        char_width = char_widths.get(' ', font_size * 0.6)
      width += char_width

    return int(round(width*1.1))

  # Process the descriptor line by line
  lines = input_description.strip().split('\n')

  # Parse the first two lines for title and subtitle
  template_variables['title']    = {'label':lines.pop(0).strip()}
  template_variables['subtitle'] = {'label':lines.pop(0).strip()}

  # Width in pixels of each line of the schematic
  line_widths    = []
  title_width    = get_text_width(
                     template_variables['title']['label'],
                     template_variables['fonts']['title']['family'],
                     template_variables['fonts']['title']['weight'],
                     template_variables['fonts']['title']['size']
                   )
  subtitle_width = get_text_width(
                     template_variables['subtitle']['label'],
                     template_variables['fonts']['subtitle']['family'],
                     template_variables['fonts']['subtitle']['weight'],
                     template_variables['fonts']['subtitle']['size']
                   )
  line_widths.append(title_width)
  line_widths.append(subtitle_width)

  # Parse the next lines for ports
  template_variables['ports'] = {'left':[], 'right':[]}
  template_variables['number_port_lines'] = 0
  empty_port = {'label':"", 'direction':"", 'width':""}
  line_re = re.compile(r"(?:([-=<>]{2,})\s+(\w+))?\s*(?:(\w+)\s+([-=<>]{2,}))?")
  while lines:
    template_variables['number_port_lines'] += 1
    line        = lines.pop(0).strip()
    line_parse  = line_re.search(line)
    line_groups = line_parse.groups()
    left_arrow  = line_groups[0]
    left_label  = line_groups[1]
    right_label = line_groups[2]
    right_arrow = line_groups[3]
    # Left side ports
    if left_arrow:
      direction = "input" if '>' in left_arrow else "output"
      width     = "bus"   if '=' in left_arrow else "bit"
      port = {
        'label':     left_label,
        'direction': direction,
        'width':     width
      }
      template_variables['ports']['left'].append(port)
    else:
      template_variables['ports']['left'].append(empty_port)
    # Right side ports
    if right_arrow:
      direction = "input" if '<' in right_arrow else "output"
      width     = "bus"   if '=' in right_arrow else "bit"
      port = {
        'label':     right_label,
        'direction': direction,
        'width':     width
      }
      template_variables['ports']['right'].append(port)
    else:
      template_variables['ports']['right'].append(empty_port)
    # Line width
    line_width = ports_label_margin
    if left_label is not None:
      line_width += get_text_width(
                      left_label,
                      template_variables['fonts']['port']['family'],
                      template_variables['fonts']['port']['weight'],
                      template_variables['fonts']['port']['size']
                    )
    if right_label is not None:
      line_width += get_text_width(
                      right_label,
                      template_variables['fonts']['port']['family'],
                      template_variables['fonts']['port']['weight'],
                      template_variables['fonts']['port']['size']
                    )
    line_widths.append(line_width)

  # Box dimensions
  template_variables['box'] = {}
  template_variables['box']['width'] = int(
      max(line_widths)
    + box_padding_sides * 2
  )
  template_variables['box']['height'] = int(
      box_padding_top
    + title_height
    + title_margin
    + subtitle_height
    + subtitle_margin
    + ports_height * template_variables['number_port_lines']
    + box_padding_bottom
  )

  # Box position
  template_variables['box']['x'] = int(
      port_arrow_length
    + svg_padding
  )
  template_variables['box']['y'] = int(
      svg_padding
  )

  # Title
  template_variables['title']['x'] = int(
      template_variables['box']['x']
    + template_variables['box']['width'] / 2
  )
  template_variables['title']['y'] = int(
      template_variables['box']['y']
    + box_padding_top
    + title_height / 2
  )
  template_variables['subtitle']['x'] = int(
      template_variables['title']['x']
  )
  template_variables['subtitle']['y'] = int(
      template_variables['title']['y']
    + title_height / 2
    + title_margin
    + subtitle_height / 2
  )

  # Position of the arrows
  template_variables['arrows'] = {}
  template_variables['arrows']['length'] = port_arrow_length
  template_variables['arrows']['x_left'] = int(
      template_variables['box']['x']
  )
  template_variables['arrows']['x_right'] = int(
      template_variables['box']['x']
    + template_variables['box']['width']
  )

  template_variables['arrows']['triangle'] = {}
  template_variables['arrows']['triangle']['length'] = arrow_triangle_length
  template_variables['arrows']['triangle']['height'] = arrow_triangle_height
  template_variables['arrows']['triangle']['left_path']  = f"l +{arrow_triangle_length} +{arrow_triangle_height/2} v -{arrow_triangle_height} z"
  template_variables['arrows']['triangle']['right_path'] = f"l -{arrow_triangle_length} +{arrow_triangle_height/2} v -{arrow_triangle_height} z"
  template_variables['arrows']['busline'] = {}
  template_variables['arrows']['busline']['distance'] = bus_line_distance
  template_variables['arrows']['busline']['size']     = bus_line_size

  # Position of the ports
  template_variables['ports']['y_start'] = int(
      template_variables['subtitle']['y']
    + subtitle_height / 2
    + subtitle_margin
  )
  template_variables['ports']['x_left'] = int(
      template_variables['box']['x']
    + box_padding_sides
  )
  template_variables['ports']['x_right'] = int(
      template_variables['box']['x']
    + template_variables['box']['width']
    - box_padding_sides
  )
  port_y = int(
      template_variables['ports']['y_start']
    + ports_height / 2
  )
  for port_line_index in range(template_variables['number_port_lines']):
    template_variables['ports']['left' ][port_line_index]['y'] = port_y
    template_variables['ports']['right'][port_line_index]['y'] = port_y
    port_y += ports_height

  # SVG dimensions
  template_variables['width'] = int(
      template_variables['box']['width']
    + port_arrow_length * 2
    + svg_padding * 2
  )
  template_variables['height'] = int(
      template_variables['box']['height']
    + svg_padding * 2
  )

  # Jinja2 environment
  env = Environment()

  # Load template from package resources
  template_ref = importlib.resources.files('symbol_generator').joinpath('symbol.svg.j2')
  with importlib.resources.as_file(template_ref) as svg_template_path:
      with open(svg_template_path, 'r') as svg_template:
          # Generate output SVG string
          output_str = env.from_string(svg_template.read()).render(template_variables)

          # Remove trailing whitespaces from lines
          output_str = re.sub(r' +\n', '\n', output_str)

          # Determine output path (e.g., same name as input but with .svg)
          output_path = args.input_file.rsplit('.', 1)[0] + ".svg"

          # Write output file
          with open(output_path, 'w') as output_file:
              output_file.write(output_str)
          print(f"Symbol successfully generated at '{output_path}'.")

if __name__ == "__main__":
    main()
