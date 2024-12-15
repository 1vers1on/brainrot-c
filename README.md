# Brainrot Translator - README

## Overview
**Brainrot Translator** is a tool for transforming C code into a humorous "Brainrot" dialect and vice versa. This utility applies token-based translation to C keywords and common identifiers, replacing them with "brainrot" equivalents. Additionally, the tool can reverse the Brainrot dialect back into valid C code.

## Features
- **Transform C Code to Brainrot Dialect**: Replaces C keywords and identifiers with playful equivalents.
- **Reverse Brainrot to C Code**: Restores the original C code from its Brainrot-translated form.
- **Syntax-Aware Formatting**: Retains proper code indentation and spacing for both transformations.
- **Support for Preprocessor Directives and Comments**: Handles C-style comments and preprocessor directives during tokenization.

## Installation
1. Clone the repository or copy the code to your local machine.
2. Ensure you have Python 3.x installed.
3. Save the script as `brainrot_translator.py`.

## Usage
Run the tool from the command line using Python.

### Arguments
- `--transform`: Transforms C code into Brainrot.
- `--reverse`: Reverses Brainrot back into C code.
- `<input_file>`: The path to the input file containing the code.
- `-o`, `--output`: (Optional) Path to the output file for saving the result. If omitted, the result is printed to the console.

### Example Commands
#### Transform C Code to Brainrot:
```bash
python brainrot_translator.py --transform example.c -o transformed.c
```

#### Reverse Brainrot to C Code:
```bash
python brainrot_translator.py --reverse transformed.c -o original.c
```

#### Without Output File:
```bash
python brainrot_translator.py --transform example.c
```

## How It Works
1. **Tokenization**: The input code is scanned and broken into tokens (keywords, identifiers, operators, etc.) using regular expressions.
2. **Transformation**:
   - **C to Brainrot**: Matches tokens with the `brainrot_keywords` and `brainrot_identifiers` mappings to substitute values.
   - **Brainrot to C**: Reverses substitutions using the same mappings.
3. **Code Generation**: Reconstructs the code from the transformed tokens while preserving indentation and spacing.

## Translation Rules
### Keywords
| C Keyword      | Brainrot Equivalent |
|----------------|----------------------|
| `if`           | `rizzing`           |
| `else`         | `sussy`             |
| `return`       | `mew`               |
| `while`        | `ohio`              |
| `int`          | `omega`             |
| `void`         | `fein`              |
| (And more...)  |                    |

### Identifiers
| Common Identifier | Brainrot Equivalent |
|-------------------|----------------------|
| `printf`          | `yap`               |
| `malloc`          | `grind`             |
| `free`            | `dip`               |
| `i`               | `rizz`              |
| `temp`            | `sus`               |
| (And more...)     |                    |

## Error Handling
- Unrecognized characters are reported to `stderr` and ignored during processing.
- Comments and whitespace are skipped in the tokenization step.

## Contributing
Feel free to suggest new mappings for the Brainrot dialect or improvements to the code. Fork the project, make your changes, and submit a pull request.

## License
This project is released under the MIT License.

Enjoy "brainrotting" your C code! 🎉
