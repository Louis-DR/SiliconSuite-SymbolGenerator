import os
import re
from PIL import Image, ImageDraw, ImageFont

# Get the directory of the current script and of the fonts
script_directory = os.path.dirname(os.path.abspath(__file__))
font_directory   = os.path.join(script_directory, "../fonts")

# Font families and weights with paths to the font files
fonts = {
  "Arial": {
    'regular':              os.path.join(font_directory, "Arial/ArialMT.ttf"),
    'italic':               os.path.join(font_directory, "Arial/Arial-ItalicMT.ttf"),
    'bold':                 os.path.join(font_directory, "Arial/Arial-BoldMT.ttf"),
    'bold-italic':          os.path.join(font_directory, "Arial/Arial-BoldItalicMT.ttf"),
    'narrow':               os.path.join(font_directory, "Arial/ArialNarrow.ttf"),
    'narrow-italic':        os.path.join(font_directory, "Arial/ArialNarrow-Italic.ttf"),
    'narrow-bold':          os.path.join(font_directory, "Arial/ArialNarrow-Bold.ttf"),
    'narrow-bold-italic':   os.path.join(font_directory, "Arial/ArialNarrow-BoldItalic.ttf"),
  },
  "Comic Neue": {
    'regular':              os.path.join(font_directory, "Comic Neue/ComicNeue-Regular.ttf"),
    'italic':               os.path.join(font_directory, "Comic Neue/ComicNeue-RegularOblique.ttf"),
    'bold':                 os.path.join(font_directory, "Comic Neue/ComicNeue-Bold.ttf"),
    'bold-italic':          os.path.join(font_directory, "Comic Neue/ComicNeue-BoldOblique.ttf"),
    'light':                os.path.join(font_directory, "Comic Neue/ComicNeue-Light.ttf"),
    'light-italic':         os.path.join(font_directory, "Comic Neue/ComicNeue-LightOblique.ttf"),
    'angular':              os.path.join(font_directory, "Comic Neue/ComicNeueAngular-Regular.ttf"),
    'angular-italic':       os.path.join(font_directory, "Comic Neue/ComicNeueAngular-RegularOblique.ttf"),
    'angular-bold':         os.path.join(font_directory, "Comic Neue/ComicNeueAngular-Bold.ttf"),
    'angular-bold-italic':  os.path.join(font_directory, "Comic Neue/ComicNeueAngular-BoldOblique.ttf"),
    'angular-light':        os.path.join(font_directory, "Comic Neue/ComicNeueAngular-Light.ttf"),
    'angular-light-italic': os.path.join(font_directory, "Comic Neue/ComicNeueAngular-LightOblique.ttf"),
  },
  "Comic Sans": {
    'regular':              os.path.join(font_directory, "Comic Sans/ComicSansMS.ttf"),
    'italic':               os.path.join(font_directory, "Comic Sans/ComicSansMS-Italic.ttf"),
    'bold':                 os.path.join(font_directory, "Comic Sans/ComicSansMS-Bold.ttf"),
    'bold-italic':          os.path.join(font_directory, "Comic Sans/ComicSansMS-BoldItalic.ttf"),
  },
  "Consolas": {
    'regular':              os.path.join(font_directory, "Consolas/Consolas.ttf"),
    'italic':               os.path.join(font_directory, "Consolas/Consolas-Italic.ttf"),
    'bold':                 os.path.join(font_directory, "Consolas/Consolas-Bold.ttf"),
    'bold-italic':          os.path.join(font_directory, "Consolas/Consolas-ItalicBold.ttf"),
  },
  "Courier New": {
    'regular':              os.path.join(font_directory, "Courier New/Courier New.ttf"),
    'italic':               os.path.join(font_directory, "Courier New/Courier New Italic.ttf"),
    'bold':                 os.path.join(font_directory, "Courier New/Courier New Bold.ttf"),
    'bold-italic':          os.path.join(font_directory, "Courier New/Courier New Bold Italic.ttf"),
  },
  "Garamond": {
    'regular':              os.path.join(font_directory, "Garamond/AGaramondLT-Regular.ttf"),
    'italic':               os.path.join(font_directory, "Garamond/AGaramondLT-Italic.ttf"),
    'bold':                 os.path.join(font_directory, "Garamond/AGaramondLT-Bold.ttf"),
    'bold-italic':          os.path.join(font_directory, "Garamond/AGaramondLT-BoldItalic.ttf"),
    'semibold':             os.path.join(font_directory, "Garamond/AGaramondLT-Semibold.ttf"),
    'semibold-italic':      os.path.join(font_directory, "Garamond/AGaramondLT-SemiboldItalic.ttf"),
    'titling':              os.path.join(font_directory, "Garamond/AGaramondLT-Titling.ttf"),
  },
  "Georgia": {
    'regular':              os.path.join(font_directory, "Georgia/Georgia.ttf"),
    'italic':               os.path.join(font_directory, "Georgia/Georgia-Italic.ttf"),
    'bold':                 os.path.join(font_directory, "Georgia/Georgia-Bold.ttf"),
    'bold-italic':          os.path.join(font_directory, "Georgia/Georgia-BoldItalic.ttf"),
  },
  "Helvetica": {
    'regular':              os.path.join(font_directory, "Helvetica/Helvetica.ttf"),
    'italic':               os.path.join(font_directory, "Helvetica/Helvetica-Oblique.ttf"),
    'bold':                 os.path.join(font_directory, "Helvetica/Helvetica-Bold.ttf"),
    'bold-italic':          os.path.join(font_directory, "Helvetica/Helvetica-BoldOblique.ttf"),
    'light':                os.path.join(font_directory, "Helvetica/Helvetica-Light.ttf"),
    'light-italic':         os.path.join(font_directory, "Helvetica/Helvetica-LightOblique.ttf"),
  },
  "Lato": {
    'black':                os.path.join(font_directory, "Lato/Lato-Black.ttf"),
    'black-italic':         os.path.join(font_directory, "Lato/Lato-BlackItalic.ttf"),
    'heavy':                os.path.join(font_directory, "Lato/Lato-Heavy.ttf"),
    'heavy-italic':         os.path.join(font_directory, "Lato/Lato-HeavyItalic.ttf"),
    'bold':                 os.path.join(font_directory, "Lato/Lato-Bold.ttf"),
    'bold-italic':          os.path.join(font_directory, "Lato/Lato-BoldItalic.ttf"),
    'semibold':             os.path.join(font_directory, "Lato/Lato-Semibold.ttf"),
    'semibold-italic':      os.path.join(font_directory, "Lato/Lato-SemiboldItalic.ttf"),
    'medium':               os.path.join(font_directory, "Lato/Lato-Medium.ttf"),
    'medium-italic':        os.path.join(font_directory, "Lato/Lato-MediumItalic.ttf"),
    'regular':              os.path.join(font_directory, "Lato/Lato-Regular.ttf"),
    'italic':               os.path.join(font_directory, "Lato/Lato-Italic.ttf"),
    'light':                os.path.join(font_directory, "Lato/Lato-Light.ttf"),
    'light-italic':         os.path.join(font_directory, "Lato/Lato-LightItalic.ttf"),
    'thin':                 os.path.join(font_directory, "Lato/Lato-Thin.ttf"),
    'thin-italic':          os.path.join(font_directory, "Lato/Lato-ThinItalic.ttf"),
    'hairline':             os.path.join(font_directory, "Lato/Lato-Hairline.ttf"),
    'hairline-italic':      os.path.join(font_directory, "Lato/Lato-HairlineItalic.ttf"),
  },
  "Open Sans": {
    'regular':              os.path.join(font_directory, "Open Sans/open-sans.regular.ttf"),
    'italic':               os.path.join(font_directory, "Open Sans/open-sans.italic.ttf"),
    'bold':                 os.path.join(font_directory, "Open Sans/open-sans.bold.ttf"),
    'bold-italic':          os.path.join(font_directory, "Open Sans/open-sans.bold-italic.ttf"),
    'extrabold':            os.path.join(font_directory, "Open Sans/open-sans.extrabold.ttf"),
    'extrabold-italic':     os.path.join(font_directory, "Open Sans/open-sans.extrabold-italic.ttf"),
    'light':                os.path.join(font_directory, "Open Sans/open-sans.light.ttf"),
    'light-italic':         os.path.join(font_directory, "Open Sans/open-sans.light-italic.ttf"),
    'semibold':             os.path.join(font_directory, "Open Sans/open-sans.semibold.ttf"),
    'semibold-italic':      os.path.join(font_directory, "Open Sans/open-sans.semibold-italic.ttf"),
  },
  "Playfair Display": {
    'regular':              os.path.join(font_directory, "Playfair Display/PlayfairDisplay-Regular.ttf"),
    'italic':               os.path.join(font_directory, "Playfair Display/PlayfairDisplay-Italic.ttf"),
    'bold':                 os.path.join(font_directory, "Playfair Display/PlayfairDisplay-Bold.ttf"),
    'bold-italic':          os.path.join(font_directory, "Playfair Display/PlayfairDisplay-BoldItalic.ttf"),
    'black':                os.path.join(font_directory, "Playfair Display/PlayfairDisplay-Black.ttf"),
    'black-italic':         os.path.join(font_directory, "Playfair Display/PlayfairDisplay-BlackItalic.ttf"),
  },
  "Roboto Condensed": {
    'regular':              os.path.join(font_directory, "Roboto Condensed/RobotoCondensed-Regular.ttf"),
    'italic':               os.path.join(font_directory, "Roboto Condensed/RobotoCondensed-Italic.ttf"),
    'bold':                 os.path.join(font_directory, "Roboto Condensed/RobotoCondensed-Bold.ttf"),
    'bold-italic':          os.path.join(font_directory, "Roboto Condensed/RobotoCondensed-BoldItalic.ttf"),
    'light':                os.path.join(font_directory, "Roboto Condensed/RobotoCondensed-Light.ttf"),
    'light-italic':         os.path.join(font_directory, "Roboto Condensed/RobotoCondensed-LightItalic.ttf"),
  },
  "Roboto Slab": {
    'regular':              os.path.join(font_directory, "Roboto Slab/RobotoSlab-Regular.ttf"),
    'bold':                 os.path.join(font_directory, "Roboto Slab/RobotoSlab-Bold.ttf"),
    'light':                os.path.join(font_directory, "Roboto Slab/RobotoSlab-Light.ttf"),
    'thin':                 os.path.join(font_directory, "Roboto Slab/RobotoSlab-Thin.ttf"),
  },
  "Roboto": {
    'regular':              os.path.join(font_directory, "Roboto/roboto.regular.ttf"),
    'italic':               os.path.join(font_directory, "Roboto/roboto.italic.ttf"),
    'black':                os.path.join(font_directory, "Roboto/roboto.black.ttf"),
    'black-italic':         os.path.join(font_directory, "Roboto/roboto.black-italic.ttf"),
    'bold':                 os.path.join(font_directory, "Roboto/roboto.bold.ttf"),
    'bold-italic':          os.path.join(font_directory, "Roboto/roboto.bold-italic.ttf"),
    'light':                os.path.join(font_directory, "Roboto/roboto.light.ttf"),
    'light-italic':         os.path.join(font_directory, "Roboto/roboto.light-italic.ttf"),
    'medium':               os.path.join(font_directory, "Roboto/roboto.medium.ttf"),
    'medium-italic':        os.path.join(font_directory, "Roboto/roboto.medium-italic.ttf"),
    'thin':                 os.path.join(font_directory, "Roboto/roboto.thin.ttf"),
    'thin-italic':          os.path.join(font_directory, "Roboto/roboto.thin-italic.ttf"),
  },
  "Source Code Pro": {
    'regular':              os.path.join(font_directory, "Source Code Pro/SourceCodePro-Regular.ttf"),
    'black':                os.path.join(font_directory, "Source Code Pro/SourceCodePro-Black.ttf"),
    'bold':                 os.path.join(font_directory, "Source Code Pro/SourceCodePro-Bold.ttf"),
    'semibold':             os.path.join(font_directory, "Source Code Pro/SourceCodePro-Semibold.ttf"),
    'light':                os.path.join(font_directory, "Source Code Pro/SourceCodePro-Light.ttf"),
    'extralight':           os.path.join(font_directory, "Source Code Pro/SourceCodePro-ExtraLight.ttf"),
  },
  "Source Sans Pro": {
    'regular':              os.path.join(font_directory, "Source Sans Pro/source-sans-pro.regular.ttf"),
    'italic':               os.path.join(font_directory, "Source Sans Pro/source-sans-pro.italic.ttf"),
    'black':                os.path.join(font_directory, "Source Sans Pro/source-sans-pro.black.ttf"),
    'black-italic':         os.path.join(font_directory, "Source Sans Pro/source-sans-pro.black-italic.ttf"),
    'bold':                 os.path.join(font_directory, "Source Sans Pro/source-sans-pro.bold.ttf"),
    'bold-italic':          os.path.join(font_directory, "Source Sans Pro/source-sans-pro.bold-italic.ttf"),
    'extralight':           os.path.join(font_directory, "Source Sans Pro/source-sans-pro.extralight.ttf"),
    'extralight-italic':    os.path.join(font_directory, "Source Sans Pro/source-sans-pro.extralight-italic.ttf"),
    'light':                os.path.join(font_directory, "Source Sans Pro/source-sans-pro.light.ttf"),
    'light-italic':         os.path.join(font_directory, "Source Sans Pro/source-sans-pro.light-italic.ttf"),
    'semibold':             os.path.join(font_directory, "Source Sans Pro/source-sans-pro.semibold.ttf"),
    'semibold-italic':      os.path.join(font_directory, "Source Sans Pro/source-sans-pro.semibold-italic.ttf"),
  },
  "Tahoma": {
    'regular':              os.path.join(font_directory, "Tahoma/Tahoma.ttf"),
    'bold':                 os.path.join(font_directory, "Tahoma/Tahoma-Bold.ttf"),
  },
  "Times New Roman": {
    'regular':              os.path.join(font_directory, "Times New Roman/Times New Roman.ttf"),
    'italic':               os.path.join(font_directory, "Times New Roman/Times New Roman Italic.ttf"),
    'bold':                 os.path.join(font_directory, "Times New Roman/Times New Roman Bold.ttf"),
    'bold-italic':          os.path.join(font_directory, "Times New Roman/Times New Roman Bold Italic.ttf"),
  },
  "Ubuntu": {
    'regular':              os.path.join(font_directory, "Ubuntu/Ubuntu-R.ttf"),
    'italic':               os.path.join(font_directory, "Ubuntu/Ubuntu-RI.ttf"),
    'bold':                 os.path.join(font_directory, "Ubuntu/Ubuntu-B.ttf"),
    'bold-italic':          os.path.join(font_directory, "Ubuntu/Ubuntu-BI.ttf"),
    'light':                os.path.join(font_directory, "Ubuntu/Ubuntu-L.ttf"),
    'light-italic':         os.path.join(font_directory, "Ubuntu/Ubuntu-LI.ttf"),
    'medium':               os.path.join(font_directory, "Ubuntu/Ubuntu-M.ttf"),
    'medium-italic':        os.path.join(font_directory, "Ubuntu/Ubuntu-MI.ttf"),
  },
  "Ubuntu Mono": {
    'regular':              os.path.join(font_directory, "UbuntuMono/UbuntuMono-R.ttf"),
    'italic':               os.path.join(font_directory, "UbuntuMono/UbuntuMono-RI.ttf"),
    'bold':                 os.path.join(font_directory, "UbuntuMono/UbuntuMono-B.ttf"),
    'bold-italic':          os.path.join(font_directory, "UbuntuMono/UbuntuMono-BI.ttf"),
  },
  "Verdana": {
    'regular':              os.path.join(font_directory, "Verdana/VerdanaPro-Regular.ttf"),
    'italic':               os.path.join(font_directory, "Verdana/VerdanaPro-Italic.ttf"),
    'black':                os.path.join(font_directory, "Verdana/VerdanaPro-Black.ttf"),
    'black-italic':         os.path.join(font_directory, "Verdana/VerdanaPro-BlackItalic.ttf"),
    'bold':                 os.path.join(font_directory, "Verdana/VerdanaPro-Bold.ttf"),
    'bold-italic':          os.path.join(font_directory, "Verdana/VerdanaPro-BoldItalic.ttf"),
    'semi-bold':            os.path.join(font_directory, "Verdana/VerdanaPro-SemiBold.ttf"),
    'semi-bold-italic':     os.path.join(font_directory, "Verdana/VerdanaPro-SemiBoldItalic.ttf"),
    'light':                os.path.join(font_directory, "Verdana/VerdanaPro-Light.ttf"),
    'light-italic':         os.path.join(font_directory, "Verdana/VerdanaPro-LightItalic.ttf"),
  },
  "Verdana Condensed": {
    'regular':              os.path.join(font_directory, "Verdana/VerdanaPro-CondRegular.ttf"),
    'italic':               os.path.join(font_directory, "Verdana/VerdanaPro-CondItalic.ttf"),
    'black':                os.path.join(font_directory, "Verdana/VerdanaPro-CondBlack.ttf"),
    'black-italic':         os.path.join(font_directory, "Verdana/VerdanaPro-CondBlackItalic.ttf"),
    'bold':                 os.path.join(font_directory, "Verdana/VerdanaPro-CondBold.ttf"),
    'bold-italic':          os.path.join(font_directory, "Verdana/VerdanaPro-CondBoldItalic.ttf"),
    'light':                os.path.join(font_directory, "Verdana/VerdanaPro-CondLight.ttf"),
    'light-italic':         os.path.join(font_directory, "Verdana/VerdanaPro-CondLightItalic.ttf"),
    'semi-bold':            os.path.join(font_directory, "Verdana/VerdanaPro-CondSemiBold.ttf"),
    'semi-bold-italic':     os.path.join(font_directory, "Verdana/VerdanaPro-CondSemiBoldItalic.ttf"),
  }
}

# Font sizes to measure
font_sizes = [4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20]

# Characters to measure
characters = [
  '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
  'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
  'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
  ' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~'
]

# Use Pillow to get the width of a single character using the specified font
def get_text_width(character:str, font:ImageFont.FreeTypeFont) -> int:
  dummy_image  = Image.new('RGB', (1,1))
  draw_context = ImageDraw.Draw(dummy_image)
  width        = draw_context.textlength(text=character, font=font)
  return int(round(width))

# Initialize the main dictionary to store all font metrics
font_character_widths = {}

print("Measuring font character widths.")

# Iterate through each font family
for font_family, weights in fonts.items():
  print(f"  Processing font family: {font_family}.")
  font_character_widths[font_family] = {}
  # Iterate through each weight
  for font_weight, font_path in weights.items():
    print(f"    Processing font weight: {font_weight}.")
    font_character_widths[font_family][font_weight] = {}
    # Check if the font file exists before proceeding
    if not os.path.exists(font_path):
      print(f"      WARNING: Font file not found at {font_path}. Skipping weight '{font_weight}'.")
      continue # Skip this font weight if the file is missing
    # Iterate through each font size
    for font_size in font_sizes:
      print(f"      Processing font size: {font_size}.")
      font_character_widths[font_family][font_weight][font_size] = {}
      try:
        # Load the font file for the current size
        font_object = ImageFont.truetype(font_path, font_size)
        # Iterate through each character
        for character in characters:
          # Calculate the width of the character
          width = get_text_width(character, font_object)
          # Store the width in the data structure
          font_character_widths[font_family][font_weight][font_size][character] = width
      except Exception as exception:
        # Handle potential errors during font loading or processing
        print(f"      ERROR: could not process font {font_path} at size {font_size}: {exception}.")
        # Assign an empty dictionary to indicate failure for this size/weight
        font_character_widths[font_family][font_weight][font_size] = {}

# Define the path for the output Python file, relative to the script directory
output_file_path = os.path.join(script_directory, 'font_character_widths.py')
print(f"Writing font metrics to {output_file_path}.")

# Write the generated dictionary to the output file
try:
  with open(output_file_path, 'w', encoding='utf-8') as output_file:
    # Write the header to the output file
    output_file.write("# This file is auto-generated by font_charachter_widths.py.\n")
    output_file.write("# It contains pre-calculated character widths for various fonts and sizes.\n\n")
    # Format the font metrics data for better readability
    font_character_widths_string = f"font_character_widths = {font_character_widths}"
    font_character_widths_string = re.sub(r"\s*(\d+:)", r"\n\g<1>", font_character_widths_string)
    font_character_widths_string = re.sub(r"('[a-zA-Z][a-zA-Z0-9_-]+':)", r"\n\g<1>", font_character_widths_string)
    # Write the formatted font metrics data to the output file
    output_file.write(font_character_widths_string)
    output_file.write("\n")
  print("Successfully wrote font metrics.")
except IOError as exception:
  print(f"ERROR: could not write to output file {output_file_path}: {exception}.")
