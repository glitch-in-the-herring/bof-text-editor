# Breath of Fire Text Editor
Extractor and markup intermediary for editing text sections found in Breath of Fire III and IV.

## Installing
1. Download [Python](https://www.python.org/downloads/)
2. When installing Python, make sure that "Add Python 3.xx" is ticked
3. Open a command prompt window
4. Type `python -m pip install git+https://github.com/glitch-in-the-herring/bof-text-editor`

## Usage
### Extractor
To obtain the markup representation of the text section in an .EMI file, run:
```
bof3-text extract FILENAME [-o OUT]
```
The argument `-o` specifies the optional output filename.

### Editor
The editor lets you patch an existing .EMI file or output the translated text section into a separate binary file. To patch an existing .EMI file, make sure that the correct filename is specified in the `%TARGET` variable, and run:

```
bof3-text edit FILENAME [-c]
```
The argument `-c` is an optional flag that tells the editor to perform the patch on a copy instead of the original file.

To create a new binary file, run:
```
bof3-text edit FILENAME -n
```

## Syntax
For information about the syntax of the intermediary markup, see [SYNTAX.MD]()
