# SpeedRead ![](demo.gif)

## About

Speed reader written in python. It reads text from the clipboard content (or xsel/xclip output). Supports some command line arguments and you can navigate within the text with the arrow keys.

I made this to integrate in my i3wm + zathura pdf reader workflow. zathura can copy text to the clipboard with a simple mouse selection, then just use a keybind to call the package with: `$ python -m speedread`. Fast and Easy.


## Usage

Install with:

`$ pip install --user speedread`

Options:

> SpeedRead [-h] [-w WPM] [-xclip] [-xsel] [-cb]
>
> optional arguments:
>   -h, --help         show this help message and exit
>   -w WPM, --wpm WPM  words per Minute
>   -xclip, --xclip    use output from `$ xclip -o`
>   -xsel, --xsel      use output from `$ xsel`
>   -cb, --clipboard   use clipboard content

Additionally it also support some key binds:
- j / k : decrease / increase wpm
- h / l : go backward / forward one word
Same idea with arrow keys


## Integration with i3wm

Add this line to your i3wm config file:

`for_window [class="Speedread"] floating enable`

Them add a line to call this package with a key bind:

`bindsym <KEY> python -m speedread &> /dev/null`


### DOTOs

- [x] Add more command line arguments
- [ ] Make it prettier
- [ ] Make it WM independent
- [ ] Add option to read from STDIN
- [ ] Select text in pdf without using the mouse


