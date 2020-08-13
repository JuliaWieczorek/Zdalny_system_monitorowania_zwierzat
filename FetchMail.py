import email
import imaplib
import tkinter as tk
from typing import List, Union

from PIL import Image, ImageTk
import os
import shutil

from settings import path_to_images

import pandas as pd
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
        bg_image = tk.PhotoImage(file="background-869596_1280.png")
        self.button1 = tk.Button(root, text="Display images", command=self.display_images).pack()
        self.scrollFrame = ScrollFrame(self)
        self.client = Client()

    def printMsg(self, msg):
        print(msg)

    def display_images(self):
        path_train = path_to_images()
        file = "test"
        path_train = os.path.join(path_train, file)
        path_train = path_train.replace('\\', '/')
        i = 0
        for name in os.listdir(path_train):
            # image = tk.PhotoImage(path + "/" + name)
            # DetectionImage.detection()
            # im = Image.open(path + "/" + name).resize((250, 250))
            path_to_image = os.path.join(path_train, name)
            path_to_image = path_to_image.replace('\\', '/')
            Classification_images(path_to_image)
            im = Image.open(path_to_image).resize((250, 250))
            # CNN(path_to_image) #TODO: CNN
            ph = ImageTk.PhotoImage(im)
            label = tk.Label(self.scrollFrame.viewPort, image=ph, borderwidth="1", relief="solid")
            label.image = ph
            label.pack()
        self.scrollFrame.pack(side='top', fill='both', expand=True)

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
    """ZAPISUJE ZAlACZNIKI NIEPRZECZYTANYCH MAILI"""

    # TODO: połaczyć z CNN
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

        # script_path = os.path.abspath(__file__)
        # script_dir = os.path.split(script_path)[0]
        # path_dirname = script_dir.replace('\\', '/')
        # rel_path = "classification_images/cats_and_dogs_filtered/test"
        # path = os.path.join(path_dirname, rel_path)
        # filePath = path.replace('\\', '/')
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
    """LOGOWANIE DO MAILA"""

    ID_default = 1
    list_of_clients = []

    def __init__(self):
        # self.screen = tk.Tk()
        self.screen = tk.Toplevel()
        self.screen.title("Log in")  # panel logowania
        # Gets the requested values of the height and widht.
        windowWidth = root.winfo_reqwidth()
        windowHeight = root.winfo_reqheight()
        positionRight = int(self.screen.winfo_screenwidth() / 2 - windowWidth / 2)
        positionDown = int(self.screen.winfo_screenheight() / 2 - windowHeight / 2)
        # Positions the window in the center of the page.
        self.screen.geometry("250x160+{}+{}".format(positionRight, positionDown))
        self.screen.configure(background='dim gray')
        # screen.geometry("210x170")
        self.screen.grid_columnconfigure(0, weight=1)
        self.screen.grid_rowconfigure(0, weight=1)
        tk.Label(self.screen, text=' ', bg='dim gray').grid(column=0, row=1)

        tk.Label(self.screen, text="email", bg='dim gray').grid(column=0, row=2)
        self.email = tk.Entry(self.screen, width=20)
        self.email.grid(column=1, row=2)

        tk.Label(self.screen, text='password', bg='dim gray').grid(column=0, row=3)
        self.password = tk.Entry(self.screen, width=20)
        self.password.grid(column=1, row=3)

        tk.Label(self.screen, text=' ', bg='dim gray').grid(column=4, row=4)
        tk.Button(self.screen, text="Log in", command=self.log_in, bg='AntiqueWhite2').grid(columnspan=4, row=5)

        self.message = tk.Label(self.screen, bg='dim gray')
        self.message.grid(columnspan=4, row=7)

        # self.screen.call('wm', 'attributes', '.', '-topmost', '1')

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
        self.classifier()

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
        # TODO: sprawdzic czy działa cala funkcja: plik z maila,  przeniesienie do pliku
        # load the image
        img = self.load_image(self.img)
        # load model
        # model = load_model('final_model.h5')
        model = load_model('model.h5')
        # predict the class
        result = model.predict(img)
        if result[0] == [1.]:
            print('dog')
        else:
            print('cat')


# server = 'imap.poczta.onet.pl'
# username = 'mgrphototrap@onet.pl'
# password = 'Mgr.Photo.Trap.1'

# e: photo.trap@onet.pl
# h: mgr.Photo.Trap.1
path = 'images'
if __name__ == "__main__":
    root = tk.Tk()
    bg_image = tk.PhotoImage(file="background-869596_1280.png")
    path = path_to_images()
    MainApplication(root, bg=bg_image).pack(side="top", fill="both", expand=True)
    # background = tk.Label(image=bg_image)
    # background.image = bg_image
    # background.pack()

    root.mainloop()
