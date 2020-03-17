import email
import imaplib
import os
import tkinter as tk
from PIL import Image, ImageTk
#from time import time
#from imageai.Detection import ObjectDetection
import os

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        # tk.Frame.__init__(self, parent, *args, **kwargs)
        tk.Frame.__init__(self, root)
        root.title("Name")
        bg_image = tk.PhotoImage(file="background-869596_1280.png")
        #background = tk.Label(image=bg_image)
        #background.image = bg_image
        #background.pack()
        self.scrollFrame = ScrollFrame(self)
        path = 'C:/Users/julia/Documents/bioinformatyka/magisterka/images/'
        #number = len(os.listdir(path))
        #frame = tk.Frame(root).pack()
        #canvas = tk.Canvas(frame, bg='cornsilk4', width=n * number, height=n * number)
        #canvas.pack(expand='yes', fill='both')
        #canvas.create_image(50, 10, image=bg_image, anchor='nw')
        i = 0
        for name in os.listdir(path):
            # image = tk.PhotoImage(path + "/" + name)
            # DetectionImage.detection()
            im = Image.open(path + "/" + name).resize((250, 250))
            ph = ImageTk.PhotoImage(im)
            label = tk.Label(self.scrollFrame.viewPort, image=ph, borderwidth="1", relief="solid")
            label.image = ph
            label.pack()


            #c = tk.Canvas(canvas, width=n, height=n)
            #c.create_image(n / 2, n / 2, image=ph)
            #canvas.create_window(0, n * i, window=c)
            #i += 1
        self.scrollFrame.pack(side='top', fill='both', expand=True)
        '''
        vsb = tk.Scrollbar(frame, orient="vertical")
        vsb.pack(side='right', fill='y')
        vsb.config(command=canvas.yview)
        canvas.config(width=n * number, height=n * number)
        canvas.config(yscrollcommand=vsb.set, scrollregion=canvas.bbox('all'))
        canvas.pack(side='left', expand=True, fill='both')
        self.parent = parent
    
        # Gets the requested values of the height and widht.
        windowWidth = root.winfo_reqwidth()
        windowHeight = root.winfo_reqheight()
        positionRight = int(root.winfo_screenwidth()/8 - windowWidth/8)
        positionDown = int(root.winfo_screenheight()/8 - windowHeight/8)
        # Positions the window in the center of the page.
        root.geometry("1000x800+{}+{}".format(positionRight, positionDown)) # jeszcze jest za nisko :/
    '''
        self.logowanie()

    def printMsg(self, msg):
        print(msg)

    def logowanie(self):
        #self.screen = tk.Tk()
        self.screen = tk.Toplevel()
        self.screen.title("Log in") #panel logowania
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
        tk.Button(self.screen, text="Log in", command=self.login, bg='AntiqueWhite2').grid(columnspan=4, row=5)
        self.message = tk.Label(self.screen,  bg='dim gray')
        self.message.grid(columnspan=4 , row=7)
        #self.screen.call('wm', 'attributes', '.', '-topmost', '1')

    def login(self):
        try:
            imap = imaplib.IMAP4_SSL("imap.poczta.onet.pl", 993)
            imap.login(self.email.get(), self.password.get())
            print("Login accepted")
            self.message['text'] = 'Login accepted'
            self.screen.after(1000, self.screen.destroy)
        except:
            print("An exception occurred")
            self.message['text'] = 'Incorrect email or password' #invalid?

class ScrollFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent) # create a frame (self)

        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")          #place canvas on self
        self.viewPort = tk.Frame(self.canvas, background="#ffffff")   #place a frame on the canvas, this frame will hold the child widgets
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview) #place a scrollbar on self
        self.canvas.configure(yscrollcommand=self.vsb.set)           #attach scrollbar action to scroll of canvas

        self.vsb.pack(side="right", fill="y")                                       #pack scrollbar to right of self
        self.canvas.pack(side="left", fill="both", expand=True)          #pack canvas to left of self and expand to fil
        self.canvas_window = self.canvas.create_window((4,4), window=self.viewPort, anchor="nw", tags="self.viewPort")
        #add view port frame to canvas


        self.viewPort.bind("<Configure>", self.onFrameConfigure) #bind an event whenever the size of the viewPort frame changes.
        self.canvas.bind("<Configure>", self.onCanvasConfigure)  #bind an event whenever the size of the viewPort frame changes.

        self.onFrameConfigure(None) #perform an initial stretch on render, otherwise the scroll region has a tiny border until the first resize

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))                 #whenever the size of the frame changes, alter the scroll region respectively.

    def onCanvasConfigure(self, event):
        '''Reset the canvas window to encompass inner frame when required'''
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width = canvas_width)            #whenever the size of the canvas changes alter the window region respectively.



class FetchEmail():
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
                    filePath = os.path.join('C:/Users/julia/Documents/bioinformatyka/mgr', fileName)
                    if not os.path.isfile(filePath):
                        fp = open(filePath, 'wb')
                        fp.write(part.get_payload(decode=True))
                        fp.close()
                        #subject = str(email_message).split("Subject: ", 1)[1].split("\nTo:", 1)[0]
                    #  print('Downloaded "{file}" from email titled "{subject}" with UID {uid}.'.format(file=fileName, subject=subject,uid=latest_email_uid.decode('utf-8')))
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1].decode('utf-8'))
                    email_subject = msg['subject']
                    email_from = msg['from']
                    print('From : ' + email_from + '\n')
                    print('Subject : ' + email_subject + '\n')
                    print(msg.get_payload(decode=True))
'''
class DetectionImage():
    def detection(self):
        execution_path = os.getcwd()

        detector = ObjectDetection()
        detector.setModelTypeAsRetinaNet()
        detector.setModelPath(os.path.join(execution_path, "resnet50_coco_best_v2.0.1.h5"))
        detector.loadModel()
        detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path, "image.jpg"),
                                                     output_image_path=os.path.join(execution_path, "imagenew.jpg"))

        for eachObject in detections:
            print(eachObject["name"], " : ", eachObject["percentage_probability"])

'''
server = 'imap.poczta.onet.pl'
username = 'mgrphototrap@onet.pl'
password = 'Mgr.Photo.Trap.1'
folder = 'C:/Users/julia/Documents/bioinformatyka/mgr'

if __name__ == "__main__":
    root = tk.Tk()
    bg_image = tk.PhotoImage(file="background-869596_1280.png")
    MainApplication(root, bg=bg_image).pack(side="top", fill="both", expand=True)
    # background = tk.Label(image=bg_image)
    # background.image = bg_image
    # background.pack()

    root.mainloop()
