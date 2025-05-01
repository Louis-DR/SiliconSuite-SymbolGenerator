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
