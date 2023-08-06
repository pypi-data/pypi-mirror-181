from tkinter import Tk, Label,  Button, Frame, E, W

font = 'Arial'
label_text_size = 16
text_text_size = 10


class ConfirmUrl:

    def __init__(self, instance_url: str):
        self.confirm = False
        self.root = Tk()
        self.frame = Frame()
        self.frame.pack()
        self.root.title('Metagen GUI')
        self.description = Label(self.frame, text=f'Should be fixtures imported into:\n{instance_url} ',
                                 font=(font, text_text_size), padx=5)
        self.description.grid(row=0, column=0, sticky=W + E)

        self.button_frame = Frame(self.frame)
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        self.button_frame.grid(row=1, column=0, sticky=W + E)

        self.yes = Button(self.button_frame, text='Yes', font=(font, text_text_size), command=self.yes_click)
        self.yes.grid(row=0, column=0, pady=5, padx=2)

        self.no = Button(self.button_frame, text='No', font=(font, text_text_size), command=self.end)
        self.no.grid(row=0, column=1, pady=5, padx=2)

        self.root.mainloop()

    def yes_click(self):
        self.confirm = True
        self.root.destroy()

    def end(self):
        self.root.destroy()
