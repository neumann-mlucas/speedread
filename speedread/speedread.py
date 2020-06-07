#!/usr/bin/python

import argparse
import subprocess
from itertools import accumulate
import tkinter as tk


class SpeedRead(tk.Frame):
    def __init__(
        self, master=None, wpm=300, clipboard_get=None, big_label={}, small_label={},
    ):
        super().__init__(master)
        self.master = master

        # FUTURE: PUT BINDS INTO A FUNCTION

        # Go forward and backward in words
        self.master.bind("<Key-l>", self.next_word)
        self.master.bind("<Left>", self.next_word)
        self.master.bind("<Key-h>", self.previous_word)
        self.master.bind("<Right>", self.previous_word)
        # Increase and decrease wpm
        self.master.bind("<Key-k>", self.inc_wpm)
        self.master.bind("<Up>", self.inc_wpm)
        self.master.bind("<Key-j>", self.dec_wpm)
        self.master.bind("<Down>", self.dec_wpm)
        # Exit program
        self.master.bind("<KeyRelease-q>", quit)
        self.master.bind("<KeyRelease-Q>", quit)

        self.pack()

        self.wpm = wpm
        self.words = split_text(clipboard_get())
        self.length = len(self.words) if self.words else 1
        self.index = 0

        # write first word to window
        start = format_word(self.words[0]) if self.words else ("Empty Clipboard")
        self.text = tk.Label(self, text=start, **big_label)
        self.text.pack()

        # write info
        start = format_info(0, self.length, self.wpm)
        self.info = tk.Label(self, text=start, **small_label)
        self.info.pack()

        # wait a little and start updating
        self.after(500, self.update)

    def update(self):
        # Increase index and Update text until get IndexError
        try:
            idx, wpm = self.index, self.wpm
            word = self.words[idx]

            info = format_info(idx, self.length, wpm)
            time = time_per_word(word, wpm)
            word = format_word(word)

            self.index += 1

            self.info.configure(text=info)
            self.text.configure(text=word)
            self.after(time, self.update)

        except IndexError:
            self.after(1000, self.quit)

    def next_word(self, event=None):
        self.index += 2

    def previous_word(self, event=None):
        self.index -= 2

    def inc_wpm(self, event=None):
        self.wpm += 10

    def dec_wpm(self, event=None):
        self.wpm -= 10


def parse_args():

    parser = argparse.ArgumentParser(
        prog="SpeedRead",
        description="""Speed reader python package. Reads clipboard
        contents and displays it, one word at a time, in a new window""",
        epilog="""You can quit the windows pressing q or Q. For bug report
        and more information:
        https://github.com/neumann-mlucas/speedread""",
    )
    parser.add_argument(
        "-w", "--wpm", action="store", default=300, type=int, help="Words per Minute",
    )

    parser.add_argument(
        "-xclip",
        "--xclip",
        action="store_true",
        default=False,
        help="Use output from xclip -o",
    )
    parser.add_argument(
        "-xsel",
        "--xsel",
        action="store_true",
        default=False,
        help="Use output from xsel",
    )
    parser.add_argument(
        "-cb",
        "--clipboard",
        action="store_true",
        default=True,
        help="Use clipboard content",
    )
    args = parser.parse_args()

    if args.xclip:
        args.clipboard_get = xclip_get
    elif args.xsel:
        args.clipboard_get = xsel_get
    else:
        args.clipboard_get = tkinter_get

    return args


def tkinter_get():
    root = tk.Tk()
    root.withdraw()
    clip = root.clipboard_get()
    # must return a regular string
    return clip.decode("utf-8") if isinstance(clip, bytes) else clip


def xclip_get():
    proc = subprocess.Popen(["xclip", "-out"], stdout=subprocess.PIPE)
    clip = proc.stdout.read()
    # must return a regular string
    return clip.decode("utf-8") if isinstance(clip, bytes) else clip


def xsel_get():
    proc = subprocess.Popen("xsel", stdout=subprocess.PIPE)
    clip = proc.stdout.read()
    # must return a regular string
    return clip.decode("utf-8") if isinstance(clip, bytes) else clip


def split_text(text):
    return [word for word in text.split() if word]


def time_per_word(word, wpm, lenght_factor=0.196):
    # the mean length of a English word is 5.1 (or  1 / 0.196)
    base_time = int(60_000 / wpm)
    coefficient = len(word) * lenght_factor
    # shouldn't return a value smaller than base_time
    return int(coefficient * base_time) if coefficient > 1 else base_time


def format_word(word):
    return f"|\n {word} \n|"


def format_info(idx, total, wpm):
    porcentage = f"{100 * idx / total:5.0f}"
    # return f" WPM : {wpm} {' '*158} {porcentage}% "
    bar = "-" * 76
    return f"{bar}\n WPM : {wpm} {' ' * 58} {porcentage}% "


def main():

    big_label = {
        "bg": "#2F343F",
        "height": 4,
        "width": 32,
        "fg": "#E52B50",
        "font": ("Helvetica", "32", "bold"),
    }

    small_label = {
        "bg": "#2F343F",
        "fg": "#E52B50",
        "height": 2,
        "font": ("Monospace", "12"),
    }

    args = parse_args()
    root = tk.Tk(className="SpeedRead")

    app = SpeedRead(
        master=root,
        wpm=args.wpm,
        clipboard_get=args.clipboard_get,
        big_label=big_label,
        small_label=small_label,
    )
    app.mainloop()


if __name__ == "__main__":
    main()
