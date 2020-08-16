import email
import imaplib
import tkinter as tk
from tkinter import ttk
from tkinter import *
from ttkthemes import ThemedTk

from PIL import Image, ImageTk
import os
import shutil

from settings import path_to_images

from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.models import load_model

class MainApplication(tk.Frame):
    """TWORZY INTERFEJS PROGRAMU
        PRZEKIEROWUJE DO KLASY KLIENT"""

    def __init__(self, parent, *args, **kwargs):
        # tk.Frame.__init__(self, parent, *args, **kwargs)
        tk.Frame.__init__(self, root)
        root.title("Animal monitoring system")
        self.button1 = ttk.Button(root, text="Display images", command=self.display_images).pack()
        self.progress_bar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
        self.progress_bar.pack()
        self.statusbar = tk.Label(root, text='Welcome', relief=SUNKEN, anchor=W, font='Times 10 italic')
        self.statusbar.pack(side=BOTTOM, fill=X)
        self.bytes = 0
        self.maxbytes = 0
        self.scrollFrame = ScrollFrame(self)
        self.client = Client()

    def display_images(self):
        path_train = path_to_images()
        file = "test"
        path_train = os.path.join(path_train, file)
        path_train = path_train.replace('\\', '/')

        self.progress_bar["value"] = 0
        num_dir = len([name for name in os.listdir(path_train) if os.path.isfile(os.path.join(path_train, name))])
        self.maxbytes = num_dir
        self.progress_bar["maximum"] = self.maxbytes
        self.bytes = 0

        if num_dir == 0:
            self.statusbar['text'] = 'Nothing new'
        else:
            self.statusbar['text'] = 'Loading...'
            for name in os.listdir(path_train):
                path_to_image = os.path.join(path_train, name)
                path_to_image = path_to_image.replace('\\', '/')
                im = Image.open(path_to_image).resize((250, 250))
                ph = ImageTk.PhotoImage(im)
                label = tk.Label(self.scrollFrame.viewPort, image=ph, borderwidth="1", relief="solid")
                label.image = ph
                label.pack()
                text = Classification_images(path_to_image)
                label1 = tk.Label(self.scrollFrame.viewPort, text=text.classifier())
                label1.pack()
                self.bytes += 1
                self.progress_bar["value"] = self.bytes
                self.progress_bar.update()
            self.scrollFrame.pack(side='top', fill='both', expand=True)
            self.statusbar['text'] = ' '

class ScrollFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)  # create a frame (self)

        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
        self.viewPort = tk.Frame(self.canvas, background="#ffffff")
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas_window = self.canvas.create_window((4, 4), window=self.viewPort, anchor="nw", tags="self.viewPort")
        # add view port frame to canvas

        self.viewPort.bind("<Configure>",
                           self.onFrameConfigure)  # bind an event whenever the size of the viewPort frame changes.
        self.canvas.bind("<Configure>",
                         self.onCanvasConfigure)  # bind an event whenever the size of the viewPort frame changes.

        self.onFrameConfigure(
            None)  # perform an initial stretch on render, otherwise the scroll region has a tiny border until the first resize

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox(
            "all"))  # whenever the size of the frame changes, alter the scroll region respectively.

    def onCanvasConfigure(self, event):
        '''Reset the canvas window to encompass inner frame when required'''
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window,
                               width=canvas_width)  # whenever the size of the canvas changes alter the window region respectively.

class FetchEmail(object):
    """ZAPISUJE ZALACZNIKI NIEPRZECZYTANYCH MAILI"""

    def __init__(self, username, password):
        self.username = username
        self.password = password
        domena = self.username.split('@')[1]
        domena = 'imap.poczta.' + domena
        imap = imaplib.IMAP4_SSL(domena, 993)
        imap.login(self.username, self.password)
        print("login accepted")
        imap.select('INBOX')

        # self.unread(imap)
        self.read(imap)

    def unread(self, imap):
        print('unread')

        status, response = imap.search(None, '(UNSEEN)')
        unread_msg_nums = response[0].split()

        # Print the count of all unread messages
        print("Unread messages: ", len(unread_msg_nums))

        typ, data = imap.search(None, 'UNSEEN')
        for num in data[0].split():
            typ, data = imap.fetch(num, '(RFC822)')
        imap.logout()

    def read(self, imap):
        path_train = path_to_images()
        file = "test"
        path_train = os.path.join(path_train, file)
        path_train = path_train.replace('\\', '/')
        path = path_train
        typ, data = imap.search(None, 'UNSEEN')
        for num in data[0].split():
            typ, data = imap.fetch(num, '(RFC822)')
            raw_email = data[0][1]  # converts byte literal to string removing b''
            raw_email_string = raw_email.decode('utf-8')
            email_message = email.message_from_string(raw_email_string)  # downloading attachments
            for part in email_message.walk():
                # this part comes from the snipped I don't understand yet...
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue
                fileName = part.get_filename()
                if bool(fileName):
                    filePath = os.path.join(path, fileName)
                    if not os.path.isfile(filePath):
                        fp = open(filePath, 'wb')
                        fp.write(part.get_payload(decode=True))
                        fp.close()
                        subject = str(email_message).split("Subject: ", 1)[1].split("\nTo:", 1)[0]

class Client(object):
    """
    PANEL LOGOWANIA
    LOGOWANIE DO MAILA
    """

    ID_default = 1
    list_of_clients = []

    def __init__(self):
        self.screen = tk.Toplevel(root)
        self.screen.title("Log in")
        # Gets the requested values of the height and width.
        windowWidth = root.winfo_reqwidth()
        windowHeight = root.winfo_reqheight()
        positionRight = int(self.screen.winfo_screenwidth() / 2 - windowWidth / 2)
        positionDown = int(self.screen.winfo_screenheight() / 2 - windowHeight / 2)
        # Positions the window in the center of the page.
        self.screen.geometry("250x160+{}+{}".format(positionRight, positionDown))
        # screen.geometry("210x170")
        self.screen.grid_columnconfigure(0, weight=1)
        self.screen.grid_rowconfigure(0, weight=1)
        tk.Label(self.screen, text=' ').grid(column=0, row=1)

        tk.Label(self.screen, text="email").grid(column=0, row=2)
        self.email = ttk.Entry(self.screen, width=20)
        self.email.grid(column=1, row=2)

        tk.Label(self.screen, text='password').grid(column=0, row=3)
        self.password = ttk.Entry(self.screen, width=20, show='*')
        self.password.grid(column=1, row=3)

        tk.Label(self.screen, text='show password').grid(column=0, row=4)
        self.var = tk.IntVar()
        self.bt = tk.Checkbutton(self.screen, command=self.mark, offvalue=0, onvalue=1, variable=self.var)
        self.bt.grid(column=1, row=4)

        tk.Label(self.screen, text=' ').grid(column=4, row=4)
        # tk.Button(self.screen, text="Log in", command=self.log_in, bg='AntiqueWhite2').grid(columnspan=4, row=5)
        ttk.Button(self.screen, text="Log in", command=self.log_in).grid(columnspan=4, row=5)


        # self.message = tk.Label(self.screen, bg='dim gray')
        self.message = ttk.Label(self.screen)
        self.message.grid(columnspan=4, row=8)

        # self.screen.call('wm', 'attributes', '.', '-topmost', '1')

    def mark(self):
        """show password- change '*' into letters"""
        if self.var.get() == 1:
            self.password.configure(show="")
        elif self.var.get() == 0:
            self.password.configure(show="*")

    def client(self, mail, password):
        self.client_ID = Client.ID_default
        print(self.client_ID)
        Client.ID_default = Client.ID_default + 1
        print(Client.client_ID)
        self.mail = mail
        self.password = password
        self.__class__.list_of_clients.append(self)

    def log_in(self):
        try:
            mail = self.email.get()
            domena = mail.split('@')[1]
            domena = 'imap.poczta.'+domena
            imap = imaplib.IMAP4_SSL(domena, 993)
            imap.login(self.email.get(), self.password.get())
            print("Login accepted")
            self.message['text'] = 'Login accepted'
            self.screen.after(1000, self.screen.destroy)
            FetchEmail(self.email.get(), self.password.get())
            # self.client(self.email.get(), self.password.get())
        except:
            print("An exception occurred")
            self.message['text'] = 'Incorrect email or password'

class Classification_images(object):

    def __init__(self, img):
        self.img = img

        # load and prepare the image
    def load_image(self, filename):
        # load the image
        path_train = path_to_images()
        path_file = os.path.join(path_train, 'test')
        path_file = os.path.join(path_file, filename)
        path_file = path_file.replace('\\', '/')
        img = load_img(path_file, target_size=(224, 224))
        # convert to array
        img = img_to_array(img)
        # reshape into a single sample with 3 channels
        img = img.reshape(1, 224, 224, 3)
        # center pixel data
        img = img.astype('float32')
        img = img - [123.68, 116.779, 103.939]
        return img

    # load an image and predict the class
    def classifier(self):
        # load the image
        img = self.load_image(self.img)
        # load model
        model = load_model('final_model.h5')
        # model = load_model('model.h5')
        # predict the class
        result = model.predict(img)
        self.clas = tk.StringVar()
        if result[0] > [0.5]:
            self.clas = 'dog'
            dest = "images/final/dogs"
            shutil.move(self.img, dest)
        else:
            self.clas = 'cat'
            dest = "images/final/cats"
            shutil.move(self.img, dest)
        return (self.clas)


# server = 'imap.poczta.onet.pl'
# e: photo.trap@onet.pl
# h: mgr.Photo.Trap.1
# path = 'images'
if __name__ == "__main__":
    root = ThemedTk(theme="clearlooks")
    path = path_to_images()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
