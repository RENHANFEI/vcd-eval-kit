__author__ = 'Hanfei'

import os
import time
from random import choice, random, shuffle, sample
from tkinter import *
from PIL import Image, ImageTk


class Evaluation(object):
    def __init__(self):
        super(Evaluation, self).__init__()

        self.__images = list(range(32))
        self.__models = ['equal', 'sinc']
        self.__apertures = [3, 5]    # pinhole size
        self.__degrees = [300, 320]
        self.__test_num = 12
        self.__adapt_num = 4    # 12 * 8 + 4 = 100 comparisons for one subject


    def evaluate(self):

        pairs = []

        for image_idx in sample(self.__images, self.__test_num):
            for model in self.__models:
                for aperture in self.__apertures:
                    for degree in self.__degrees:
                        param1 = (str(image_idx), model, str(aperture), str(degree))
                        param2 = (str(image_idx), choice(self.__models), 
                            str(choice(self.__apertures)), str(degree))
                        # avoid evaluation between two same images
                        while param2 == param1:
                            param2 = (str(image_idx), choice(self.__models), 
                            str(choice(self.__apertures)), str(degree))
                        # shuffle two images
                        param1, param2 = (param1, param2) if random() < 0.5 \
                            else (param2, param1)

                        pairs.append((param1, param2))

        adaptation = sample(pairs, self.__adapt_num)
        pairs.extend(adaptation)
        pairs = list(reversed(pairs))
        root = Tk()
        app = Window(pairs, self.__adapt_num, root)
        root.mainloop()


class Window(Frame):

    def __init__(self, pairs, adapt_num, master=None):

        self.__image_dir = 'simulation'
        self.__image_suffix = '.png'

        self.__pairs = pairs
        self.__pair_num = len(pairs)
        self.__pair_idx = 0
        self.__adapt_num = adapt_num


        self.__scales = {-3: 'Much worse', -2: 'Worse', -1: 'Slightly worse', 
                          0: 'The same', 1: 'Slightly better', 2: 'Better', 
                          3: 'Much better'}

        self.__instruction = 'Compared with (a), (b) is ?'
        self.__confirm = 'Confirm'

        self.__btn = None
        self.__radio_var = StringVar()

        self.__record = []
        self.__records = []

        Frame.__init__(self, master)
        self.master = master
        self.__init_window()
        self.__update_images()


    def __init_window(self):

        self.master.title('Simulation Image Evaluation')
        self.grid()


    def __update_images(self):

        param1, param2 = self.__pairs[self.__pair_idx]
        self.__record = list(param1 + param2)

        filename1 = '_'.join(param1) + self.__image_suffix
        filename2 = '_'.join(param2) + self.__image_suffix
        path1 = os.path.join(self.__image_dir, filename1)
        path2 = os.path.join(self.__image_dir, filename2)

        # display images
        load1 = Image.open(path1)
        load1 = load1.resize((376, 376))
        render1 = ImageTk.PhotoImage(load1)
        im1 = Label(self, text='(a)', image=render1, compound=TOP, font=('Arial', 18))
        im1.image = render1
        im1.grid(row=0, rowspan=10, column=0, padx=10, pady=10)

        load2 = Image.open(path2)
        load2 = load2.resize((376, 376))
        render2 = ImageTk.PhotoImage(load2)
        im2 = Label(self, text='(b)', image=render2, compound=TOP, font=('Arial', 18))
        im2.image = render2
        im2.grid(row=0, rowspan=10, column=1, padx=10, pady=10)
        
        # set instruction
        instruction = Label(self, text=self.__instruction, font=('Arial', 18))
        instruction.grid(row=0, column=2, padx=10, pady=5)

        # set radio buttons
        row = 1
        for scale, scale_text in self.__scales.items():
            radio = Radiobutton(self, text=scale_text, variable=self.__radio_var, value=scale, 
                                font=('Arial', 16), command=self.__selected)
            radio.grid(row=row, column=2, sticky=W, padx=20)
            row += 1

        # set confirm button
        self.__btn = Button(self, text=self.__confirm, font=('Arial', 16), 
                     width=15, height=2, state=DISABLED, command=self.__go_next)

        self.__btn.grid(row=row, column=2, sticky=W, padx=20)


    def __selected(self):
        
        self.__btn.configure(state=NORMAL)


    def __go_next(self):

        if self.__pair_idx >= self.__pair_num - 1:
            self.__record.append(str(self.__radio_var.get()))
            self.__records.append(','.join(self.__record))
            records = '\n'.join(self.__records)
            filename = str(int(time.time())) + '.csv'
            with open(filename, 'w') as f:
                f.write(records)
            exit()

        if self.__pair_idx >= self.__adapt_num:
            self.__record.append(str(self.__radio_var.get()))
            self.__records.append(','.join(self.__record))

        self.__radio_var.set(None)
        self.__pair_idx += 1
        self.__update_images()
        self.__btn.configure(state=DISABLED)




if __name__ == '__main__':
    evaluation = Evaluation()
    evaluation.evaluate()
