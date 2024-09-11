# Mighty Macro-Machine

Ambitious mouse & keyboard macro language with a built-in recorder and playback. Each line within the script is computed on a frame (think frames per second). Multiple statements can be on a singular frame by using the `next (->)` symbol.

So far, the language supports variable and function declarations, function calls, basic arithmetic, comparisons, and processing built-in functions. Blank / empty lines are ignored and not processed, this is to allow for more elegant formatting of code.

## Example

Below is an example of how to program utilizing Mighty. This shows how to declare variables, call functions, and declare a function `test` and call it with an argument. Lastly the `->` symbol is used to imply that defining both `x` and `y` should happen on the same frame and without pause.

```
x: int = 5
  -> y: float = 10.5
print(x + y)
print("Hello World!")

func test(value: int) {
    print(value)
}

test(x + x)
```

## Outline

### Built-in Functions

- [x] Print: `print(*args)`, displays to console what is passed.
- [x] Wait: `wait(duration: int)`, waits `duration` of frames.
- [ ] Mouse
  - [x] Move: `mpos(x: int, y: int)`
  - [x] Click: `mclick(button_id: 'left' | 'right' | 'middle', randomize: bool)`
  - [ ] Drag