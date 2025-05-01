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

To generate the symbol schematic from this descriptor file, run the following command in your terminal :

```bash
symbol-generator simple_buffer.sss
```

This will create the following SVG file named `simple_buffer.svg` :

![simple_buffer.svg](example/simple_buffer.svg)
