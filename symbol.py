import re
import argparse
from .font_character_widths import font_character_widths

# Parse command line arguments
parser = argparse.ArgumentParser(description='Generate the SVG symbol of a hardware component from a description file.')
parser.add_argument('input_file', help='Path to the symbol description file.')
args = parser.parse_args()

# Read input file
input_description = None
try:
  with open(args.input_file, 'r') as input_file:
    input_description = input_file.read()
except FileNotFoundError:
  print(f"Error: Input file not found at '{args.input_file}'.")
  exit(1)
except Exception as exception:
  print(f"Error reading input file: {exception}.")
  exit(1)

# Drawing parameters
title_height           = 10 # Height of the title
title_margin           =  0 # Bottom margin of the title
subtitle_height        =  8# Height of the subtitle
subtitle_margin        =  5 # Bottom margin of the subtitle
ports_height           = 10 # Height of each port line
ports_label_margin     = 10 # Margin between ports of either sides
box_padding_top        =  2 # Box top padding
box_padding_bottom     =  5 # Box bottom padding
box_padding_sides      =  2 # Box bottom padding
box_height_padding     = 10 # Box vertical padding
port_arrow_length      = 20 # Length of the port arrows
arrow_triangle_length  =  6 # Length of the port arrows
arrow_triangle_height  =  4 # Length of the port arrows
bus_line_distance      =  5 # Distance from end of line and the angled line
bus_line_size          =  2 # Distance from line to each end of the angled line
svg_padding            =  5 # Padding for the top, bottom, left, and right

# Variables used in the SVG template
template_variables = {}

# Font attributes
font_name = "helvetica"
fonts = {
  'title': {
    'weight': "bold",
    'size': 8
  },
  'subtitle': {
    'weight': "normal",
    'size': 6
  },
  'port': {
    'weight': "normal",
    'size': 6
  }
}
template_variables['font_family'] = font_name
template_variables['fonts']       = fonts

# Get width in pixels of text with specific font
def get_text_width(text:str, font_name:str="helvetica", font_weight:str="normal", font_size:int=6) -> int:
  width = 0
  for character in text:
    width += font_character_widths[font_name][font_weight][font_size][character]
  return int(round(width*1.1))

# Process the descriptor line by line
lines = input_description.strip().split('\n')

# Parse the first two lines for title and subtitle
template_variables['title']    = {'label':lines.pop(0).strip()}
template_variables['subtitle'] = {'label':lines.pop(0).strip()}

# Width in pixels of each line of the schematic
line_widths    = []
title_width    = get_text_width(template_variables['title'   ]['label'], font_name, fonts['title'   ]['weight'], fonts['title'   ]['size'])
subtitle_width = get_text_width(template_variables['subtitle']['label'], font_name, fonts['subtitle']['weight'], fonts['subtitle']['size'])
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
    line_width += get_text_width(left_label, font_name, fonts['port']['weight'], fonts['port']['size'])
  if right_label is not None:
    line_width += get_text_width(right_label, font_name, fonts['port']['weight'], fonts['port']['size'])
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

