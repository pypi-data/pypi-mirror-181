# Deskpanel

Simple library to display useful information on the desktop.

## Installation

```commandline
pip install deskpanel
```

## Usage

```python
import os
from src.deskpanel import Panel

OUTER = 30  # padding around screen borders
GUTTER = 20  # gutter between rows and columns

# if you use these panels once 
# then an initial wallpaper is saved in "wallpaper/saved"
saved_wallpaper = None
if os.path.exists("wallpaper/saved"):
    saved_wallpaper = os.listdir("wallpaper/saved")[0]

panel1 = Panel(outer=OUTER, gutter=GUTTER)
panel1.set_position("left", "top")  # position in 3/3 grid
panel1.set_padding(30)  # padding around text
panel1.set_font("fonts/Poppins.ttf")  # path to font (only TTF)
panel1.set_text("Very useful information goes here", color="#fff")  # content
panel1.set_background("#000000c0")  # background with opacity

# use same outer and gutter for different panels for valid layout
panel2 = Panel(outer=OUTER, gutter=GUTTER)
panel2.set_position("left", "top")  # position in 3/3 grid
panel2.set_padding(30)  # padding around text
panel2.set_font("fonts/Poppins.ttf")  # path to font (only TTF)
panel2.set_text("Very useful information goes here", color="#fff")  # panel content
panel2.set_background("#000000c0")  # background with opacity

# rendering panels
Panel.render([panel1, panel2], saved_wallpaper)
```

