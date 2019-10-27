import tkinter as tk
import re


class DisplayApp:
    
    """ GUI displaying words in the canvas center with a delay. 
    """

    GEOMETRY = '1200x700'
    BG_COLOR = 'black'

    FONT = 'Consolas'
    FONT_SIZE = 20
    FONT_COLOR = 'white'

    EOS_PATTERN = re.compile('.+\.$')

    def __init__(self, text, wpm=200, end_of_sentence_delay=None, wpm_step=10):

        self.text = text

        self.wpm = wpm
        self.wpm_step = wpm_step

        # self.text_delay = self._wpm_to_delay(wpm)
        self.eos_delay = end_of_sentence_delay
        if self.eos_delay is None:
            self.eos_delay = self.text_delay

        self.root = tk.Tk()
        self.root.configure(background=self.BG_COLOR)
        self.root.geometry(self.GEOMETRY)

        self._setup_text_label()
        self._setup_wpm_label()

        # WPM speed change.
        self.arr_up = tk.Frame(self.root, width=100, height=100, bg='red')
        self.arr_up.bind('<Button-1>', self._increase_wpm)
        self.arr_up.pack()

        self.arr_down = tk.Frame(self.root, width=100, height=100, bg='green')
        self.arr_down.bind('<Button-1>', self._decrease_wpm)
        self.arr_down.pack()


        self.root.after(self.text_delay, self._show_next_word)
        self.root.mainloop()

    @property
    def wpm(self):
        return self._wpm
    
    @wpm.setter
    def wpm(self, value):
        # Automatically sets delay between two actions.
        self._wpm = int(value)
        self.text_delay = 60 * 1000 // value

    def _change_text(self, text):
        self.txt_var.set(text)

    def _show_next_word(self):
        try:
            new_text = next(self.text)
        except StopIteration:
            self.txt_var.set('')
        else:
            self._change_text(new_text)
            delay = self.eos_delay if self._eof_found(new_text) else self.text_delay
            self.root.after(delay, self._show_next_word)

    def _eof_found(self, text):
        return self.EOS_PATTERN.match(text)     

    def _pause_on_eos(self):
        self.root(after(self.eos_delay, self._show_next_word))

    def _setup_text_label(self):
        self.txt_var = tk.StringVar()
        self.msg = tk.Label(self.root, 
                            textvariable=self.txt_var, 
                            anchor=tk.CENTER, 
                            font=(self.FONT, self.FONT_SIZE),
                            bg=self.BG_COLOR,
                            fg=self.FONT_COLOR)
        self.msg.place(relx=.5, rely=.5, anchor=tk.CENTER)

    def _setup_wpm_label(self):
        self.wpm_var = tk.IntVar()
        self.msg = tk.Label(self.root,
                            textvariable=self.wpm_var,
                            anchor=tk.CENTER,
                            font=(self.FONT, self.FONT_SIZE),
                            bg=self.BG_COLOR,
                            fg=self.FONT_COLOR)
        self.wpm_var.set(self.wpm)
        self.msg.pack()

    def _increase_wpm(self, event):
        self.wpm += self.wpm_step
        self._update_wpm_display()

    def _decrease_wpm(self, event):
        self.wpm -= self.wpm_step
        self._update_wpm_display()

    def _update_wpm_display(self):
        self.wpm_var.set(self.wpm)
