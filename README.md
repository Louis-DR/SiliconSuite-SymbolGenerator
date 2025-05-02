# SiliconSuite-SymbolGenerator

Generate symbol schematics for hardware IP cores.

## Installation

To install the package using pip, run the following command:

```bash
pip install siliconsuite-symbol-generator
```

## Example

The tool takes a symbol descriptor file in a custom format as input. The first line is the title, it should be the human readable name of the component. The second line is the subtitle, it should be the programming name of the component. All the other lines describe ports.

Each port has a label (without spaces) and is characterized by an arrow. The arrow comes before the label for the ports on the left side, and the opposite for the right side. The arrow direction indicates the direction of the port (input or output), and the line indicates the bus type (`-` for a single bit and `=` for multi-bit). On each line, there can be ports on either sides, both, or neither to jump a line.

Here is an example of a simple symbol descriptor file named `simple_buffer.sss` :

```sss
Simple Buffer
valid_ready_simple_buffer
-> clock
-> resetn
<- empty               full ->
=> write_data     read_data =>
-> write_valid   read_valid ->
<- write_ready   read_ready <-
```

To generate the symbol schematic from this descriptor file, run the following command in your terminal. Note that you can use the `--scale` argument to apply a scaling factor to the whole schematic. A scaling factor of 3 or 4 is recommended for most usecases.

```bash
symbol-generator simple_buffer.sss --scale 4
```

This will create the following SVG file named `simple_buffer.svg` :

![simple_buffer.svg](https://raw.githubusercontent.com/Louis-DR/SiliconSuite-SymbolGenerator/refs/heads/master/example/simple_buffer.svg)

Note that if you view this readme in a website or application that doesn't support dark mode correctly (such as PyPI), the example diagram might not be visible. Dark mode support can be disabled when generating the diagram (see section below).

If multiple files are provided (with a list or a wildcard pattern), each descriptor will be processed individually and rendered in the corresponding location.

## Theme

The visual appearance of the generated symbol (e.g., padding, font sizes, arrow dimensions, colors) can be customized through a YAML theme file. The tool comes with a default theme (`default_theme.yaml`) located within the package.

You can create your own theme file and specify only the settings you want to change. Any settings omitted from your custom theme file will retain their values from the default theme. Use the `--theme` or `-t` command-line argument to specify your custom theme file:

```bash
symbol-generator input.sss --theme path/to/your/theme.yaml
```

Refer to the `default_theme.yaml` file in the package source for the available options and their structure.

## Dark mode

By default, the SVG symbol will be generated with a CSS style that automatically inverts the luminance of all colors when the SVG is viewed in dark mode. This can be disabled by passing the command-line argument `--no-dark-mode`.
