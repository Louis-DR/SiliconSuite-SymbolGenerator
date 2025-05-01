import argparse

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
