# SpeedRead ![](demo.gif)

## About

Speed reader written in python. It reads text from the clipboard content (xsel output). Right now, it just supports wpm argument, but I plan to expand this latter.

I made this to integrate in my i3wm + zathura pdf reader workflow. zathura can copy text to the clipboard with a mouse selection, then just use a keybind to call the package with: `$ python -m speedread`.

## Usage

Install with:

`$ pip install --user speedread`

Add this line to your i3wm config file:

`for_window [class="Speedread"] floating enable`

bind with i3wm or sxhkd

### DOTOs

- [ ] Add more command line arguments
- [ ] Make it WM independent
- [ ] Add option to read from stdin
- [ ] Select text without using the mouse (?)


