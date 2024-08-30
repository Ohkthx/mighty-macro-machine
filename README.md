# Mighty Macro-Machine

Ambitious mouse & keyboard macro language with a built-in recorder and playback. Each line within the script is computed on a frame (think frames per second). Multiple statements can be on a singular frame by using the `next (->)` symbol.

## Outline

### Menus

#### Buttons

- [ ] Record action
- [ ] Playback action
- [ ] Stop action
  - [ ] Stop hotkey
- [ ] Load Script
- [ ] Save Script

#### Fields

- [ ] Randomness (0 is none, decimal form)
- [ ] Script record / playback delay (milliseconds)

#### Toggles

### Lexer

#### Tokens

- [ ] Identifier - Variable names, A-Z 0-9
- [ ] Operator
- [ ] Literal
- [ ] Keyword
- [ ] Indent
- [ ] Dedent
- [ ] EOL (End of Line) - '\n', Completion of the frame
- [ ] Comment - '//' not considered during processing.
- [ ] Delimiter
- [ ] Colon
- [ ] Comma

#### Operators

- [ ] +, -, /, *, **, % - Arithmetic
- [ ] +=, -=, /=, */ - Arithmetic + Assignment
- [ ] -> - Next, this indicates the following statement should be on same frame.
- [ ] = - Assignment
- [ ] ==, !=, >, <, >=, <= - Comparison

#### Keywords

- [ ] if, else
- [ ] for, while
- [ ] func

#### Delimiters

- [ ] () - Function calls, holds parameters.
- [ ] [] - Subscripts for 
- [ ] {}

### Built-in Functions

- [ ] Mouse
  - [ ] Move
  - [ ] Click
  - [ ] Hold
  - [ ] Release
- [ ] Keybord
  - [ ] Click
  - [ ] Hold
  - [ ] Release