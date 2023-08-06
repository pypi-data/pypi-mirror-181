# Fun with Unicode braille characters

_tldr; I made a library. The whole canvas is just an int. Still can't feel it through the screen._

The other day I was thinking about showing live data in a simple way for a little library I've been coming up with for using async streams in Python.
I played around with using the Unicode bar characters ▁▂▃▄▅▆▇█, but I didn't particularly like their look.
So while searching for a better alternative, I came across the Unicode braille characters  (⠄⠂⠆⠇⠏⠋⠛⠟, etc.).
I thought they looked nice enough, and was pleasantly surprised to find that implementing something to draw with them was actually a pretty fun puzzle, full of wondrous possibilities in low-level bit twiddling.

Historically, the braille characters were used only in a 6-dot configuration, making up a grid of 2x3 dots.
The Unicode standard has since expanded this to 8-dot configurations, allowing the representation of 2x4 dots in a single character.
This is pretty cool because it allows us a greater deal of information density than the bar characters allow.
Though there's 8 levels of bar characters and braille only goes up to 4 dots high, braille allows us greater horizontal resolution, as you can represent 2 samples of an X dimension in a single character.

Here's what I mean:

```
# (1 2 3 4 5 6 7 8 8 7 6 5 4 3 2 1) - 16 characters for 16 samples

▁▂▃▄▅▆▇█▇▆▅▄▃▂▁

# (1 2 3 4 5 6 7 8 8 7 6 5 4 3 2 1) - 8 characters for 16 samples

⣀⡠⠔⠊⠑⠢⢄⣀


# Or, using just the more restricted vertical resolution of braille characters:

# (1 2 3 4 4 3 2 1) - 4 characters for 8 samples
⡠⠊⠑⢄
```

Also, I just think it looks nicer.

So anyway - looking at the code points for the characters, some ideas started to form in my head.
This is more attributable to the Unicode folks who designed the braille characters than me, but I thought it was pretty cool.
The first code point for the braille characters is 0x2800, which is `0b1010000000000000` in binary.
From there, if you add (or `or`) a number such as 2, 4, 8, 16, 32, 64, or 128, you get a character with a single dot:

```python
In [1]: chr(0x2800 + 2)
Out[1]: '⠂'

In [2]: chr(0x2800 + 4)
Out[2]: '⠄'

In [3]: chr(0x2800 + 8)
Out[3]: '⠈'

In [4]: chr(0x2800 + 16)
Out[4]: '⠐'
```

The significance of this is clear when you look at the binary representation of integers which are powers of 2:

```python
In [5]: bin(2)
Out[5]: '0b10'

In [6]: bin(4)
Out[6]: '0b100'

In [7]: bin(8)
Out[7]: '0b1000'

In [8]: bin(16)
Out[8]: '0b10000'
```

The binary representation of these numbers is just a single 1 in a different position. You can get these numbers by shifting a 1 to the left by the number of positions you want to shift it.

```python
In [9]: bin(1 << 1)
Out[9]: '0b10'

In [10]: bin(1 << 2)
Out[10]: '0b100'

In [11]: bin(1 << 3)
Out[11]: '0b1000'
```

So you could create for instance a dictionary mapping (x, y) coordinates within a character to the number you need to add to the base code point to get the character with the dot in the right place, and it'd look like this:

```python
coords_braille_mapping = {
    (0, 3): 1 << 0,
    (0, 2): 1 << 1,
    (0, 1): 1 << 2,
    (0, 0): 1 << 6,
    (1, 3): 1 << 3,
    (1, 2): 1 << 4,
    (1, 1): 1 << 5,
    (1, 0): 1 << 7,
}
```

And then get each of the characters like this:

```python
In [12]: chr(0x2800 + tup_to_braille_offset[(0, 3)])
Out[12]: '⠈'

In [13]: chr(0x2800 + tup_to_braille_offset[(0, 2)])
Out[13]: '⠐'
```

(N.B. the pattern is broken by the bottom 2 dots, presumably because the original braille characters were only 2x3 dots, and the Unicode standard wanted to keep the order for those. This tripped me up a bit initially, but doesn't change much in the grand scheme of things)

Pretty neat, huh?
It goes further than that - it turns out that the secret to everything braille unicode is to think about it in binary representations.
You may have guessed it by now, but the characters representing each combination of dots is just the codepoint for the base character OR'd with the characters for each individual dot.
So say you have these 3 characters:

```
Operation       |   Decimal |   Binary              |   Braille
0x2800 | 1 << 4	|	10256	|	0b10100000010000	|	⠐
0x2800 | 1 << 1	|	10242	|	0b10100000000010	|	⠂
0x2800 | 1 << 7	|	10368	|	0b10100010000000	|	⢀
```

They each correspond to a single dot in a braille character. If you OR them together, you get the character for the combination of those dots:

```python

In [14]: chr(0x2800 | 1 << 4 | 1 << 1 | 1 << 7)
Out[14]: '⢒'
```

Clever! We can use this to represent any combination of dots in a braille character.
If we're feeling fancy enough to use `reduce` and `operator.or_`, we can build a helper function that gives us the character for any combination of dots in just one line:

```python
import operator
from functools import reduce

BRAILLE_RANGE_START = 0x2800

coords_braille_mapping = {
    (0, 3): 1 << 0,
    (0, 2): 1 << 1,
    (0, 1): 1 << 2,
    (0, 0): 1 << 6,
    (1, 3): 1 << 3,
    (1, 2): 1 << 4,
    (1, 1): 1 << 5,
    (1, 0): 1 << 7,
}


def coords_to_braille(*coords: tuple[int, int]) -> str:
    return chr(reduce(operator.or_, [coords_braille_mapping[tup] for tup in coords], BRAILLE_RANGE_START))


print(coords_to_braille((0, 0), (1, 0)))  # ⣀
print(coords_to_braille((0, 0), (1, 0), (1, 3), (1, 2)))  # ⣘
```

And now we can use this to build a function that takes a list of samples and returns a string of braille characters representing those samples.
A couple of tricky parts are to correctly spread out the samples; each character represents 2 samples, not just one.

```python

def sparkline(
    data: Sequence[float],
    width: int = 60,
    min_val: int | None = None,
    max_val: int | None = None,
) -> str:
    """Return a sparkline of the given data, with the given width."""
    if not data:
        return " " * width

    _min_val = min(data) if min_val is None else min_val
    _max_val = max(data) if max_val is None else max_val
    scale = _max_val - _min_val
    if scale == 0:
        scale = 1

    chars = []
    for left, right in zip(data[::2], data[1::2]):
        val_left = math.floor((left - _min_val) / scale * 3)
        val_right = math.floor((right - _min_val) / scale * 3)

        ch = coords_braille_mapping[(0, val_left)] | coords_braille_mapping[(1, val_right)]
        chars.append(chr(BRAILLE_RANGE_START | ch))

    if len(data) % 2:
        val = math.floor((data[-1] - _min_val) / scale * 3)
        chars.append(chr(BRAILLE_RANGE_START | coords_braille_mapping[(0, val)]))
    if len(chars) > width:
        chars = chars[:width]
    elif len(chars) < width:
        chars = [" " * (width - len(chars))] + chars
    return "".join(chars)

```

