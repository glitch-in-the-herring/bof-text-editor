# Markup Syntax

The intermediary file consists of two major sections: the header and the content. 

## Header
The header defines the variables that are used by the editor. Variables are defined like so:
```
%VARIABLE_NAME_1="string value"
%VARIABLE_NAME_2=0x123
%VARIABLE_NAME_3=12345
```

Hexadecimal integers must begin with `0x`, otherwise they are considered to be decimal integers. Special characters in a string value must be escaped. Currently only two variables are used:
* `%PTSIZE`: Size of the pointer table. If not specified, defaults to 512.
* `%TARGET`: Output target for the editor, whether in patch mode or overwritte mode. If not specified, defaults to output.bin.

## Content
### Strings
Strings are marked at the start with a caret (`^`) and at the end with a dollar sign (`$`). The caret automatically adds a pointer to the pointer table at that location, while the dollar sign automatically adds a zero-byte (`0x00`) at that location. Whitespace between strings is ignored. Exaple:
```
^This is a string!$^This is another string$
^This is another string in a new line$
```

### Safe Characters
Safe characters are characters that are not used for syntactic purposes. The following table gives a list of safe characters:

| Character(s) | Name |
|-------|------|
|`A-Z` | Uppercase letters|
|`a-z`| Lowercase letters|
|`0-9`| Digits |
|` `| Space
|`(` | Left parenthesis |
|`)` | Right parenthesis |
|`,` | Comma |
|`-` | Dash |
|`.` | Period|
|`/` | Slash|
|`?` | Question mark|
|`!` | Exclamation mark|
|`+` | Plus sign|
|`~` | Tilde|
|`&` | Ampersand|
|`'` | Single quote|
|`:` | Colon|
|`"` | Double quote|
|`;` | Semicolon|
|`%` | Percent sign|

Anything not found in here may either be a part of the markup's syntax, or an entirely unrecognized character.

### Newline and End-of-Line Characters
This markup language is sensitive to newlines in the text. Newlines are translated to literal newlines in the game. Exceptions include:

* Newlines between strings (any newline after `$` and before `^` is ignored)
* Newlines inside tags and blocks (any newline between either  square brackets `[` or `]` and the tag definition)
* A pipe `|` before a newline indicates that the current text box is over and the text should continue in a new text box. The pipe can only be used at the end of a line.
* A backslash `\` before a newline indicates that there should be a zero byte `0x00` at the current location. The backslash can only be used at the end of a line.

### Pointers
Pointers are automatically generated based on the position of the carets `^`. To force a pointer to point to the current location, use the at sign `@`. 

### Formatting
#### Pause
`#` adds a pause at the current location
#### Color
`[color=color_name]text[/color]` adds color to the text between the tags. Valid options (case-insensitive) are:
* `Purple`
* `Red`
* `Cyan`
* `Yellow`
* `Pink`
* `Green`
* `Black`
#### Effect
`[effect]text[/effect=effect_name]` adds an effect to the text between the tags. Valid options (case-insensitive) are:
* `SHK_S`
* `SHK_L`
* `SHK_P`
* `BIG0_S`
* `BIG1_S`
* `BIG2_S`
* `BIG0_L`
* `BIG1_L`
* `BIG2_L`
* `BIG0_P`
* `BIG1_P`
* `BIG2_P`
* `SML0_S`
* `SML1_S`
* `SML2_S`
* `SML0_L`
* `SML1_L`
* `SML2_L`
* `SML0_P`
* `SML1_P`
* `SML2_P`
* `WAV_L`
* `WAV_H`
* `JMP0`
* `JMP1`
* `JMP2`

### Macro
#### Textbox macro
`[TB POS VIS]` sets the position and appearance of the textbox. The argument `POS` defines the position of the textbox, while the argument `VIS` defines the appearance of the textbox. Valid options (case-insensitive) are:
* `POS`
    * `BM`: Bottom-mid
    * `MM`: Mid-mid
    * `TM`: Top-mid
    * `TL`: Top-left
    * `TR`: Top-right
    * `BL`: Bottom-left
    * `BR`: Bottom-right
* `VIS`
    * `NV`: Normal and visible
    * `SV`: Small and visible
    * `NI`: Normal and invisible

#### Party name macro
`[PARTY MEMBER]` is a placeholder for a party member's actual name. Valid options (case-insensitive) are:
* `RYU`
* `NINA`
* `GARR`
* `TEEPO`
* `REI`
* `MOMO`
* `PECO`

#### Symbol macro
`[SYMBOL BYTE]` is substituted with the byte given as the argument.

#### Duration mcaro
`[DUR BYTE]` sets the duration a textbook appears. The valid range for the duration is `0` to `255`.
