import threading
import tkinter as TK
from tkinter import filedialog, messagebox
from tkinter.messagebox import showerror, askyesno

import ttkbootstrap as ttk
from PIL import Image, ImageTk

import ImageProcessing


"""The topic of this program is applying convolutions to discrete signals, the discrete signals in this case being 
the images we can edit. There are several different convolutions and filters the program allows you to play around 
with.
To install ttkboostrap: pip install ttkbootstrap
To install Python Pillow: python3 -m pip install --upgrade pip
                        python3 -m pip install --upgrade Pillow """

"""Authors: David Lara
    Jomar Veloso"""

filepath = ""
WIDTH = 750
HEIGHT = 560
photo_image = None
filtered_image = None

"""To run the program, make sure that ttkbootstrap is installed, as well as the PILLOW image library. After that, 
simply just run the main.py file in an IDE in order to run the program. ImageProcessing.py is a file that contains file 
definitions used in providing image filtering capabilities to the GUI."""


class MainWindow(TK.Tk):
    """Main driver for the GUI"""

    def __init__(self):

        super().__init__()

        self.title("Image Editor V1")
        self.resizable(0, 0)
        self.geometry("510x580+300+110")
        # Set up the left frame that will house the buttons for the program
        self.leftFrame = ttk.Frame(self, width=200, height=600)
        self.leftFrame.pack(side="left", fill="y")
        # Set up the canvas that will display the images
        self.canvas = ttk.Canvas(self, width=WIDTH, height=HEIGHT)
        self.canvas.pack()

        self.image_filters = ["Sobel Edge Detected", "Color Inversion", "Black and White", "Gaussian Blur", "Sharpen"]
        # Set up the dropdown containing the image filters
        self.filter_combobox = ttk.Combobox(self.leftFrame, values=self.image_filters, width=15)
        self.filter_combobox.pack(pady=5, padx=10)

        # Added threading so that the GUI doesn't hang while the 'extremely' fast image processing occurs
        self.filter_combobox.bind("<<ComboboxSelected>>",
                                  lambda event: threading.Thread(self.apply_filter(self.filter_combobox.get())))

        self.image_icon = ttk.PhotoImage(file='saveicon.png').subsample(12, 12)
        self.load_icon = ttk.PhotoImage(file='loadicon-removebg-preview.png').subsample(12, 12)

        save_button = ttk.Button(self.leftFrame, image=self.image_icon, bootstyle="light", command=self.save_image)
        save_button.pack(pady=10)

        load_button = ttk.Button(self.leftFrame, image=self.load_icon, bootstyle="light", command=self.load_image)
        load_button.pack(pady=10)

    def apply_filter(self, grabbed_filter):
        """Apply filters to an image, catches an attribute error if there is no image on the canvas to apply a filter"""
        try:
            global filepath, photo_image, filtered_image
            if grabbed_filter == self.image_filters[0]:
                img = ImageProcessing.edge_detector(filepath)
            elif grabbed_filter == self.image_filters[1]:
                img = ImageProcessing.image_inversion(filepath)
            elif grabbed_filter == self.image_filters[2]:
                img = ImageProcessing.greyscale_image(filepath)
            elif grabbed_filter == self.image_filters[3]:
                img = ImageProcessing.gaussian_blur(filepath)
            elif grabbed_filter == self.image_filters[4]:
                img = ImageProcessing.sharpen_image(filepath)

            new_width = int((WIDTH / 2))
            filtered_image = img.resize((new_width, HEIGHT), Image.LANCZOS)
            photo_image = ImageTk.PhotoImage(filtered_image)
            # Place the image onto the canvas
            self.canvas.create_image(0, 0, anchor="nw", image=photo_image)



        except AttributeError:
            showerror(title='Error', message="Cannot apply a filter to an empty image!")
        except:
            showerror(title='Error', message="Unknown Error, consult your nearest programmer!")

    def load_image(self):
        """Load an image from your local filesystem. Allowed filetypes are .jpg, .jpeg, .png, .gif and bitmap files"""
        global filepath
        filepath = filedialog.askopenfilename(title="Open Image File",
                                              filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp")])
        if filepath:
            global image, photo_image
            image = Image.open(filepath)
            new_width = int((WIDTH / 2))
            image = image.resize((new_width, HEIGHT), Image.LANCZOS)

            image = ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, anchor="nw", image=image)

    def save_image(self):
        """Save an image to the desired location"""
        global filepath, photo_image, image
        #Update the screen
        self.update()

        if filepath:
            image = filtered_image

        file_path = filedialog.asksaveasfilename(defaultextension=".jpg")

        if filepath:
            if askyesno(title='Save Image', message='Do you want to save this image?'):
                # save the image to a file
                image.save(filepath)

    def quit_program(self):
        """Quit the program, gracefully"""
        if messagebox.askokcancel("Quit", "Do you really want to exit the program?"):
            self.destroy()


if __name__ == "__main__":
    application = MainWindow()
    application.protocol("WM_DELETE_WINDOW", application.quit_program)
    application.mainloop()
