#!/usr/bin/python

import argparse
import subprocess
import tkinter as tk


class SpeedRead(tk.Frame):
    def __init__(self, master=None, wpm=300, label_config={}):
        super().__init__(master)
        self.master = master
        self.pack()
        # get word list from clipboard
        words = split_text(xsel_get())
        times = calc_times(words, wpm)
        self.words = zip(words, times)
        # write first word to window
        start = format_word(words[0]) if words else ("Empty Clipboard")
        self.text = tk.Label(self, text=start, **label_config)
        self.text.pack()
        # wait a little and start updating
        self.after(1000, self.update)

    def update(self):
        # Update text until generator is consumed
        try:
            word, time = next(self.words)
            word = format_word(word)
            self.text.configure(text=word)
            self.after(time, self.update)
        except StopIteration:
            self.after(2500, self.quit)

    def quiet():
        self.destroy()


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
    args = parser.parse_args()
    return args


def clipboard_get():
    root = tk.Tk()
    root.withdraw()
    clip = root.clipboard_get()
    return clip


def xsel_get():
    proc = subprocess.Popen("xsel", stdout=subprocess.PIPE)
    clip = proc.stdout.read()
    return clip


def split_text(text):
    return [word.decode("utf-8") for word in text.split() if word]


def time_per_word(word, base_time):
    # the mean length of a English word is 5.1
    lenght_factor = 1 / 5.1
    coefficient = len(word) * lenght_factor
    # shouldn't return a value smaller than base_time
    return int(coefficient * base_time) if coefficient > 1 else base_time


def calc_times(words, wpm):
    # map function requires arguments of the same length
    base_time = int(1000 * 60 / wpm)
    base_times = [base_time] * len(words)
    return map(time_per_word, words, base_times)


def format_word(word, text_config={}):
    middle = len(word) // 2
    return f"|\n {word} \n|"


def main():

    args = parse_args()

    label_config = {
        "bg": "#2F343F",
        "height": 8,
        "width": 24,
        "fg": "#E52B50",
        "font": ("Helvetica", "32"),
    }

    root = tk.Tk(className="SpeedRead")
    root.bind("<KeyRelease-q>", quit)
    root.bind("<KeyRelease-Q>", quit)

    app = SpeedRead(master=root, wpm=args.wpm, label_config=label_config)
    app.mainloop()


if __name__ == "__main__":
    main()
