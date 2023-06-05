# Human Readable Regex

This is a Python library that provides a collection of classes for constructing regular expressions.
It aims to simplify the process of creating and maintaining complex regex patterns by providing
intuitive and reusable elements.

## Installation

You can install the library using pip:

```shell
pip install human-re
```

## Usage

Here's an example of how to create a regular expression pattern using the human-re library:

```python
from human_re import Regex, Literal, Or, Letter, Digit

# Create a basic pattern to match hex-colors
hex_color_regex = Regex(
    Literal("#"),
    Or(
        Digit(),
        Letter("a", "f"),
        times=(3, 6)
    )
).compile()
# the resulting regex will be r'(\#((\d|[A-Fa-f]){6}|(\d|[A-Fa-f]){3}))'

assert hex_color_regex.match("#fff")
assert hex_color_regex.match("#1ed99e")
assert hex_color_regex.match("#1eg99e") is None
assert hex_color_regex.match("red") is None
```

## Documentation

The documentation for the library can be found in the /docs directory. Or just visit it [here](...). It provides an
overview of the available elements, their constructors, and examples of usage.

<details>
  <summary><strong>Overview Regex Elements</strong></summary>

- [And](./docs/src/elements/and_.html)
- [Anything](...)
- [Boundary](...)
- [Digit](...)
- [EndOfString](...)
- [Integer](...)
- [Letter](...)
- [Literal](...)
- [LiteralSet](...)
- [Multiple](...)
- [Named](...)
- [Not](...)
- [Optional](...)
- [Or](...)
- [Regex](...)
- [RegexPattern](...)
- [StartOfString](...)
- [Whitespace](...)

</details>

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)