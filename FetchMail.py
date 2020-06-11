import email
import imaplib
import tkinter as tk
from PIL import Image, ImageTk
import os
import shutil

class MainApplication(tk.Frame):

    path = ''

    def __init__(self, parent, *args, **kwargs):
        # tk.Frame.__init__(self, parent, *args, **kwargs)
        tk.Frame.__init__(self, root)
        root.title("Name")
        bg_image = tk.PhotoImage(file="background-869596_1280.png")
        # background = tk.Label(image=bg_image)
        # background.image = bg_image
        # background.pack()
        self.scrollFrame = ScrollFrame(self)

        script_path = os.path.abspath(__file__) 
        script_dir = os.path.split(script_path)[0] 
        path_dirname = script_dir.replace('\\', '/')
        rel_path = "classification_images/cats_and_dogs_filtered/train/cats"
        path = os.path.join(path_dirname, rel_path)
        path = path.replace('\\', '/')
        
        i = 0
        for name in os.listdir(path):
            # image = tk.PhotoImage(path + "/" + name)
            # DetectionImage.detection()
            # im = Image.open(path + "/" + name).resize((250, 250))
            path_to_image = os.path.join(path, name)
            path_to_image = path_to_image.replace('\\', '/')
            im = Image.open(path_to_image).resize((250,250))
            ph = ImageTk.PhotoImage(im)
            label = tk.Label(self.scrollFrame.viewPort, image=ph, borderwidth="1", relief="solid")
            label.image = ph
            label.pack()

        self.scrollFrame.pack(side='top', fill='both', expand=True)

        self.client = Client()

    def printMsg(self, msg):
        print(msg)
'''
    #tutaj było def logowanie()
    def login(self):
        try:
            imap = imaplib.IMAP4_SSL("imap.poczta.onet.pl", 993)
            print(self.email.get(), self.password.get(), 'login try in Main')
            imap.login(self.email.get(), self.password.get())
            print("Login accepted")
            self.message['text'] = 'Login accepted'
            self.screen.after(1000, self.screen.destroy)
        except:
            print(self.email.get(), self.password.get(), 'login except in Main')
            print("An exception occurred")
            self.message['text'] = 'Incorrect email or password'  # invalid?

    # def get_label(self, variable):
    #    self.variable = variable
    #    return self.variable.get()

    def printuj(self):
        print(self.textA.get())

    def _show_value(*pargs):
        # print(*pargs)
        return(root.globalgetvar(pargs[0]))

    def recupere(self):
        "Function to get the variable"
        dev = self.dev_var.get()
        return self.dev_var.set(dev)

    def show_output(self, event):
        print(self.entry_var.get())
'''
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

    # TODO: połaczyć z CNN
    filePath = ''

    def unread(username, password):
        imap = imaplib.IMAP4_SSL("imap.poczta.onet.pl", 993)
        imap.login(username, password)
        imap.select('INBOX')

        status, response = imap.search(None, '(UNSEEN)')
        unread_msg_nums = response[0].split()

        # Print the count of all unread messages
        print("Unread messages: ", len(unread_msg_nums))

        typ, data = imap.search(None, 'UNSEEN')
        for num in data[0].split():
            typ, data = imap.fetch(num, '(RFC822)')
        imap.logout()

    def read(username, password):
        #TODO: sprawdzic czy działa zapisywanie i optwieranie path
        imap = imaplib.IMAP4_SSL("imap.poczta.onet.pl", 993)
        imap.login(username, password)
        print("login accepted")
        imap.select("INBOX")
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
                    filePath = os.path.join(MainApplication.path, fileName)
                    if not os.path.isfile(filePath):
                        fp = open(filePath, 'wb')
                        fp.write(part.get_payload(decode=True))
                        fp.close()
                        # subject = str(email_message).split("Subject: ", 1)[1].split("\nTo:", 1)[0]
                    #  print('Downloaded "{file}" from email titled "{subject}" with UID {uid}.'.format(file=fileName, subject=subject,uid=latest_email_uid.decode('utf-8')))
            '''for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1].decode('utf-8'))
                    email_subject = msg['subject']
                    email_from = msg['from']
                    print('From : ' + email_from + '\n')
                    print('Subject : ' + email_subject + '\n')
                    print(msg.get_payload(decode=True))'''

class Client(object):

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
        Client.ID_default = Client.ID_default + 1
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
            self.client(self.email.get(), self.password.get())
        except:
            print("An exception occurred")
            self.message['text'] = 'Incorrect email or password'

class CNN(object):
    # TODO: sprawdzić czy działa

    def __init__(self):
        import keras
        import tensorflow as tf

        try:
            self.sess = tf.compat.v1.Session()
            self.model = keras.models.load_model('convnet_cifar10.kerasave')
            self.classifier()
        except:
            exec(open('settings.py').read())
            exec(open("functions.py").read())
            exec(open("sample_images.py").read())
            exec(open("model.py").read())
            exec(open("model_analysis.py").read())
            exec(open("init_training.py").read())
            exec(open("long_training.py").read())
            exec(open("short_training.py").read())
            self.classifier()

    def classifier(self):
        # TODO: sprawdzic czy działa cała funkcja: plik z maila, klasyfikacja zgodna z modelem, przeniesienie do pliku

        exec(open("functions.py").read())
        import numpy as np

        _, _, _, _, labels = setup_load_cifar()

        self.image = tf.io.read_file(FetchEmail.filePath)
        # self.img = tf.io.read_file('C:/Users/julia/Documents/bioinformatyka/classification_images/cats_and_dogs_filtered/cat.1.jpg')
        self.img = tf.image.decode_jpeg(self.image, channels=3)
        self.img.set_shape([None, None, 3])
        self.img = tf.image.resize(self.img, (32, 32))
        from keras.preprocessing import image
        self.img = image.img_to_array(self.img)  # convert to numpy array
        self.img = np.expand_dims(self.img, 0)  # make 'batch' of 1

        self.pred = self.model.predict(self.img)
        self.pred = labels["label_names"][np.argmax(self.pred)]
        print(self.pred)
        shutil.move(self.image, MainApplication.path+self.pred)




# server = 'imap.poczta.onet.pl'
username = 'mgrphototrap@onet.pl'
password = 'Mgr.Photo.Trap.1'
# folder = 'C:/Users/julia/Documents/bioinformatyka/mgr'

if __name__ == "__main__":
    root = tk.Tk()
    bg_image = tk.PhotoImage(file="background-869596_1280.png")
    MainApplication(root, bg=bg_image).pack(side="top", fill="both", expand=True)
    # background = tk.Label(image=bg_image)
    # background.image = bg_image
    # background.pack()

    root.mainloop()
