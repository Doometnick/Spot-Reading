import tkinter as tk
import re


class DisplayApp:
    
    """ GUI displaying words in the canvas center with a delay. 
    """

    WIDTH = 1200
    HEIGHT = 700
    BG_COLOR_TOP = '#002633'
    BG_COLOR = 'black'

    FONT = 'Consolas'
    FONT_SIZE = 20
    FONT_COLOR = 'white'

    EOS_PATTERN = re.compile('.+\.$')

    def __init__(self, text, wpm=200, end_of_sentence_delay=None, wpm_step=10):

        self.text = text

        self.wpm = wpm
        self.wpm_step = wpm_step

        self.eos_delay = end_of_sentence_delay
        if self.eos_delay is None:
            self.eos_delay = self._text_delay

        self.root = tk.Tk()
        self.root.wm_title('Spot Reading')
        self.root.configure(background=self.BG_COLOR)
        self.root.geometry(f'{self.WIDTH}x{self.HEIGHT}')

        self.topbar = tk.Frame(self.root, width=self.WIDTH, height=50, bg=self.BG_COLOR_TOP)
        self.topbuttonbar = tk.Frame(self.root, width=self.WIDTH, height=50, bg=self.BG_COLOR_TOP)
        self.bottom = tk.Frame(self.root, width=self.WIDTH, height=50, bg=self.BG_COLOR)
        
        self._setup_wpm_label()
        self._setup_wpm_change_buttons()
        self._setup_center_text()

        self.topbar.pack(fill='both')
        self.topbuttonbar.pack(fill='both')
        self.bottom.pack()
        
        self.root.after(self._text_delay, self._show_next_word)
        self.root.mainloop()

    @property
    def wpm(self):
        return self._wpm
    
    @wpm.setter
    def wpm(self, value):
        # Automatically update delay between two subsequent words.
        self._wpm = int(value)
        self._text_delay = 60 * 1000 // value

    def _change_text(self, text):
        self.txt_var.set(text)

    def _show_next_word(self):
        try:
            new_text = next(self.text)
        except StopIteration:
            self.txt_var.set('')
        else:
            self._change_text(new_text)
            delay = self.eos_delay if self._eof_found(new_text) else self._text_delay
            self.root.after(delay, self._show_next_word)

    def _eof_found(self, text):
        return self.EOS_PATTERN.match(text)     

    def _pause_on_eos(self):
        self.root(after(self.eos_delay, self._show_next_word))

    def _setup_center_text(self):
        self.txt_var = tk.StringVar()
        self.msg = tk.Label(self.root, 
                            textvariable=self.txt_var, 
                            anchor=tk.CENTER, 
                            font=(self.FONT, self.FONT_SIZE),
                            bg=self.BG_COLOR,
                            fg=self.FONT_COLOR)
        self.msg.place(relx=.5, rely=.5, anchor=tk.CENTER)

    def _setup_wpm_label(self):
        self.wpm_var = tk.StringVar()
        self.msg = tk.Label(self.topbar,
                            textvariable=self.wpm_var,
                            anchor=tk.CENTER,
                            font=(self.FONT, self.FONT_SIZE),
                            bg=self.BG_COLOR_TOP,
                            fg=self.FONT_COLOR)
        self._update_wpm_display()
        self.msg.pack()
    
    def _setup_wpm_change_buttons(self):
        wpm_down_btn = tk.Button(
            self.topbuttonbar, text='--', command=self._decrease_wpm)
        wpm_down_btn.config(height=1, width=10)
        wpm_down_btn.place(relx=.46, rely=.5, anchor=tk.CENTER)
        
        wpm_up_btn = tk.Button(
            self.topbuttonbar, text='++', command=self._increase_wpm)
        wpm_up_btn.config(height=1, width=10)
        wpm_up_btn.place(relx=.54, rely=.5, anchor=tk.CENTER)

    def _increase_wpm(self):
        self.wpm += self.wpm_step
        self._update_wpm_display()

    def _decrease_wpm(self):
        self.wpm -= self.wpm_step
        self._update_wpm_display()

    def _update_wpm_display(self):
        self.wpm_var.set(f'wpm: {self.wpm}')
