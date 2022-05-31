import tkinter
import re
from tkinter import *
from PIL import Image, ImageTk

from tkinter import ttk
from tkinter import messagebox


from tkinter import filedialog
import os
import tkinter as tk #python3-pil.imagetk python3-imaging-tk


from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.applications.xception import Xception
from keras.models import load_model
from pickle import load
import numpy as np
from PIL import Image
#import matplotlib.pyplot as plt
import argparse
import pyttsx3
import time

def extract_features(filename, model):
        try:
            image = Image.open(filename)
            
        except:
            print("ERROR: Couldn't open image! Make sure the image path and extension is correct")
        image = image.resize((299,299))
        image = np.array(image)
        # for images that has 4 channels, we convert them into 3 channels
        if image.shape[2] == 4: 
            image = image[..., :3]
        image = np.expand_dims(image, axis=0)
        image = image/127.5
        image = image - 1.0
        feature = model.predict(image)
        return feature

def word_for_id(integer, tokenizer):
 for word, index in tokenizer.word_index.items():
     if index == integer:
         return word
 return None


def generate_desc(model, tokenizer, photo, max_length):
    in_text = 'start'
    for i in range(max_length):
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], maxlen=max_length)
        pred = model.predict([photo,sequence], verbose=0)
        pred = np.argmax(pred)
        word = word_for_id(pred, tokenizer)
        if word is None:
            break
        in_text += ' ' + word
        if word == 'end':
            break
    return in_text


#path = 'Flicker8k_Dataset/111537222_07e56d5a30.jpg'
max_length = 32
tokenizer = load(open("tokenizer.p","rb"))
model = load_model('models/model_9.h5')
xception_model = Xception(include_top=False, pooling="avg")

#photo = extract_features(img_path, xception_model)
#img = Image.open(img_path)

#description = generate_desc(model, tokenizer, photo, max_length)
#print("\n\n")
#print(description)
#plt.imshow(img)

##########
def generateButtonClick(imagePath):
    #captionLabel.configure(text = description[5:-3])
    photo = extract_features(str(imagePath), xception_model)
    img = Image.open(imagePath)
    img=img.resize((400,300), Image.ANTIALIAS)
    description = generate_desc(model, tokenizer, photo, max_length)
    Message = description[5:-3]
    #captionLabel.configure(text = "Caption: "+Message)
    return Message


def loadImage():
    fln=filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Image File", filetypes= (("JPG File","*.jpg"),("PNG File","*.png"),("All Files","*.*")))
    start_time = time.time()
    img=Image.open(fln)
    img.thumbnail((400,400))
    img=ImageTk.PhotoImage(img)
    lbl.configure(image=img)
    lbl.image=img
    captionMessage = generateButtonClick(fln)
    captionLabel.configure(text = captionMessage)
    print("--------------------------Time required:--------------------------")
    print("--- %s seconds ---" % (time.time() - start_time))
    #time.sleep(30)
    #Text_to_speech(captionMessage)
    ##text_speach=pyttsx3.init()
    #text_speach.say(in_text)
    ##text_speach.say(captionMessage)
    ##text_speach.runAndWait()

def Text_to_speech():
    cap = captionLabel.cget("text")
    text_speech=pyttsx3.init()
    text_speech.say(cap)
    #out.save('result.mp3')
    text_speech.runAndWait()
    #out=gTTS(text = cap)
    #out.save('result.mp3')
    #os.system('start result.mp3')

#def Exit():
    #self.destroy()
    
#root = Tk()
#root.title("Image Caption Generator")
#root.geometry('1100x600')

#app = Tk()
#app.title("Welcome")


#root.geometry('1100x600')

# Add image
#label = Label(root, image=bg)
#label.place(x = 0,y = 0)

#def resize_image(event):
#       new_width = event.width
#        new_height = event.height
#        image = copy_of_image.resize((new_width, new_height))
#        photo = ImageTk.PhotoImage(image)
#        label.config(image = photo)
#        label.image = photo #avoid garbage collection



class Dashboard:
    def __init__(self):
        self.frame = Tk()
        self.frame.wm_iconbitmap("collegeLogo.ico")
        self.frame.geometry("1100x600")
        #self.frame.configure(bg='#f0f0f0')
        img =Image.open('login.jpg')
        bg = ImageTk.PhotoImage(img)
        label = Label(self.frame, image=bg)
        label.place(x = 0,y = 0)
        self.frame.title("Image Caption Generator - Home")
        title = tkinter.Label(self.frame, text = " Image Caption Generator ", font = 'Impact 40',fg='white',bg='#5a92fa',relief='raised')
        title.grid(column=0, row=1, padx=100, pady=10)
        title.place(x=260,y=50)
        
        Frame_login=Frame(self.frame,bg="white")
        Frame_login.place(x=300 ,y=180,height=320,width=500)
        title=Label(Frame_login,text="Welcome..!",font=("Impact",35,"bold"),fg="#5a92fa",bg="white").place(x=70,y=20)
        
        
        
        ###image = Image.open("login.jpg")
        ###copy_of_image = image.copy()
        #resize_image = image.resize((300, 125))
        ###photo = ImageTk.PhotoImage(image)
        ###label = ttk.Label(root, image = photo)
        ###label.bind('<Configure>', resize_image)
        ###label.pack(fill=BOTH, expand = YES)
        ##Label(self.frame, image=photo).pack()
        #Label(self.frame, bg="#f0f0f0", text="Welcome!!!", font=("Arial", 35)).pack(pady=15)
        #Button(self.frame, bg="#5a92fa", text = "Login", fg="white", font=("times new roman", 15), #command = self.onClick).place(x=240,y=445)
        #Button(self.frame, bg="#5a92fa", text = "Home", fg="white", font=("times new roman", 15), #command = self.backClick).place(x=350,y=445)
        ##
        register = Button(self.frame, bg="#5a92fa", text = "Register", fg="white", font=("times new roman", 17), command = self.registerClick)
        register.place(x=390,y=475)
        login = Button(self.frame, bg="#5a92fa", text = "Login", fg="white", font=("times new roman", 17), command = self.loginClick)
        login.place(x=600,y=475)
        
        self.frame.mainloop()

    def registerClick(self):
        self.frame.destroy()
        RegistrationPage()

    def loginClick(self):
        self.frame.destroy()
        LoginPage()


class RegistrationPage:
    def __init__(self):
        self.frame = Tk()
        self.frame.wm_iconbitmap("collegeLogo.ico")
        self.frame.geometry("1100x600")
        #self.frame.configure(bg='#f0f0f0')
        img =Image.open('login.jpg')
        bg = ImageTk.PhotoImage(img)
        label = Label(self.frame, image=bg)
        label.place(x = 0,y = 0)
        self.frame.title("Image Caption Generator - Registration")
        #Label(self.frame, bg="#f0f0f0", text="Registration Page", font=("Arial", 35)).pack(pady=50)
        Frame_login=Frame(self.frame,bg="white")
        Frame_login.place(x=150,y=150,height=320,width=500)
        title=Label(Frame_login,text="New? Register Here",font=("Impact",35,"bold"),fg="#5a92fa",bg="white").place(x=70,y=20)

        Label(Frame_login, anchor = "w", bg="white", fg="grey", text = "Email Address", font = ("Goudy old style", 15)).place(x=70,y=120)
        self.uname = StringVar()
        Entry(Frame_login, textvariable=self.uname, font=("times new roman", 15), bg="lightgray").place(x=70,y=150,width=350,height=35)
        Label(Frame_login, anchor = "w", bg="white", fg="grey", text = "Password", font = ("Goudy old style", 15)).place(x=70,y=200)
        self.pword = StringVar()
        Entry(Frame_login, textvariable=self.pword, font=("times new roman", 15),bg="lightgray", show="*", width=25).place(x=70,y=230,width=350,height=35)

        Button(self.frame, bg="#5a92fa", text = "Register", fg="white", font=("times new roman", 15), command = self.onClick).place(x=240,y=445)
        Button(self.frame, bg="#5a92fa", text = "Home", fg="white", font=("times new roman", 15), command = self.backClick).place(x=350,y=445)

        self.frame.mainloop()

    def onClick(self):
        if self.emailValidation(self.uname.get()) and self.pwordValidation(self.pword.get()):
            self.f = open('credentials.txt','a')
            self.f.write(self.uname.get()+' '+self.pword.get()+'\n')
            self.f.close()
            messagebox.showinfo("Registration Successful","Now you can Login!")
            self.frame.destroy()
            LoginPage()
        else:
            #InvalidMsgPage()
            messagebox.showwarning("Invalid Email or Password!", "Your email should be a valid one\nand your password must contain a uppercase,\na lowercase, a digit, a special symbol and of length\n6-15 characters.")
            self.frame.destroy()
            RegistrationPage()
    def emailValidation(self, email):
        if re.fullmatch(r'\b[a-z0-9_]+@[a-z0-9]+\.[a-z]{2,3}\b', email):
            return True
        else:
            return False

    def pwordValidation(self, pword):
        self.regex = '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,15}$'
        if re.fullmatch(re.compile(self.regex), pword):
            return True
        else:
            return False
    
    def backClick(self):
        self.frame.destroy()
        Dashboard()

    
class LoginPage:
    def __init__(self):
        self.frame = Tk()
        self.frame.wm_iconbitmap("collegeLogo.ico")
        self.frame.geometry("1100x600")
        #self.frame.configure(bg='#f0f0f0')
        im =Image.open('login.jpg')
        bg = ImageTk.PhotoImage(im)
        label = Label(self.frame, image=bg)
        label.place(x = 0,y = 0)
        self.frame.title("Image Caption Generator - Login")
        #Label(self.frame, bg="#f0f0f0", text="Login Page", font=("Arial", 35)).pack(pady=40)
        Frame_login=Frame(self.frame,bg="white")
        Frame_login.place(x=150,y=150,height=320,width=500)
        title=Label(Frame_login,text="Login Here",font=("Impact",35,"bold"),fg="#5a92fa",bg="white").place(x=70,y=20)
        
        Label(Frame_login, anchor = "w", bg="white", fg="grey", text = "Username", font = ("Goudy old style", 15)).place(x=70,y=95)
        self.uname = StringVar()
        Entry(Frame_login, textvariable=self.uname, font=("times new roman", 15), width=25, bg="lightgray").place(x=70,y=130,width=350,height=35)
        Label(Frame_login, anchor = "w", bg="white", fg="grey", text = "Password", font = ("Goudy old style", 15), width = 36).place(x=70,y=170)
        self.pword = StringVar()
        Entry(Frame_login, textvariable=self.pword, font=("times new roman", 15), bg="lightgray", show="*", width=25).place(x=70,y=200, width=350,height=35)

        Button(self.frame, bg="#5a92fa", text = "Login", fg="white", font=("times new roman", 15), command = self.onClick).place(x=240,y=445)
        
        Button(self.frame, bg="#5a92fa", text = "Home", fg="white", font=("times new roman", 15), command = self.backClick).place(x=350,y=445)
        
        Button(self.frame, bg="white", text = "Forget Password?", fg="#5a92fa", font=("times new roman", 13), command = self.frgt_pwrdClick).place(x=420,y=400)

        
        self.frame.mainloop()

    def onClick(self):
        if self.validCredentials():
            self.frame.destroy()
            LoggedInPage()
        else:
            messagebox.showerror("Error","Wrong username or password")
            self.frame.destroy()
            LoginPage()
            

    def backClick(self):
        self.frame.destroy()
        Dashboard()

    def validCredentials(self):
        self.f = open('credentials.txt', 'r')
        for line in self.f:
            f_email, f_pword = line.split()
            if f_email == self.uname.get() and f_pword == self.pword.get():
                self.f.close()
                return True
        self.f.close()
        return False
    
    def frgt_pwrdClick(self):
        self.frame.destroy()
        Frgt_pwrdPage()


class Frgt_pwrdPage:
    def __init__(self):
        self.frame = Tk()
        self.frame.wm_iconbitmap("collegeLogo.ico")
        self.frame.geometry("1100x600")
        #self.frame.configure(bg='#f0f0f0')
        img =Image.open('login.jpg')
        bg = ImageTk.PhotoImage(img)
        label = Label(self.frame, image=bg)
        label.place(x = 0,y = 0)
        self.frame.title("Image Caption Generator - Forgot Password")
        Label(self.frame, fg='white',bg='#5a92fa', text="Find your Password here!", font=("Goudy old style", 20)).pack(pady=65)

        Label(self.frame, anchor = "w",fg='white',bg='#5a92fa', text = "Email Address", font = ("Goudy old style", 13)).place(x=210,y=180)
        self.uname = StringVar()
        Entry(self.frame, textvariable=self.uname, font=("sans-serif", 17), width=25).place(x=210,y=210)

        Button(self.frame, text = "Find Password", fg='white',bg='#5a92fa', font=("Goudy old style", 14), padx=7,pady=2, command = self.onClick).place(x=290,y=290)

        self.frame.mainloop()


    def onClick(self):
        self.pword = self.findPassword()
        if self.pword != -1:
            messagebox.showinfo("Your Password is",self.pword)
            self.frame.destroy()
            LoginPage()
            
        else:
            messagebox.showinfo("No Matches","Entered user doesn't exist")
            self.frame.destroy()
            LoginPage()

    def findPassword(self):
        self.f = open('credentials.txt', 'r')
        for line in self.f:
            f_email, f_pword = line.split()
            if f_email == self.uname.get():
                self.f.close()
                return f_pword
        self.f.close()
        return -1


class LoggedInPage:
    def __init__(self):
        self.frame = Tk()
        self.frame.wm_iconbitmap("collegeLogo.ico")
        self.frame.geometry("1100x800")
        #self.frame.configure(bg='#f0f0f0')
        img =Image.open('login.jpg')
        bg = ImageTk.PhotoImage(img)
        label = Label(self.frame, image=bg)
        label.place(x = 0,y = 0)
        self.frame.title("Image Caption Generator")
        #master=tkinter.Tk()
        #master.resizable(width=True,height=True)
        #master.configure(borderwidth='6',background='sky blue',relief='groove')
        title = tkinter.Label(self.frame, text = " Upload Your Image Here... ", font = 'Arial 15',fg='white',bg='navy blue',relief="raised", padx=5,pady=2)
        title.grid(column=0, row=1, padx=100, pady=10)
        title.place(x=450,y=20)
        
        Caption = tkinter.Label(self.frame, text = " Caption: ", font = 'arial 13 ',fg='white', bg='navy blue',borderwidth=3, relief="raised")
        Caption.place(x=150, y=540)

        global captionLabel
        captionLabel = tkinter.Label(self.frame, text = "", font = 'arial 16',fg='black', bg='white',borderwidth=1, relief="sunken")
        captionLabel.place(x=270,y=540)
        
        global lbl
        lbl=tkinter.Label(self.frame, bg='white',borderwidth=0)
        lbl.place(x=270, y=120)

        
        uploadButton=tkinter.Button(self.frame, text=" Upload Image ", command = loadImage, font = 'arial 10 bold',bg='white',fg='navy blue')
        uploadButton.place(x=270, y=85)
        
	

        #voiceButton=tkinter.Button(master, text=" Voice Caption ", command = text_speach, font = 'arial 10 bold', bg ='white smoke')
        #voiceButton.place(x=450, y=540)

        generateVoice=tkinter.Button(self.frame, text="Generate Audio Caption", command = Text_to_speech, font = 'arial 10 bold',bg='white',fg='navy blue' ,padx=5,pady=2)
        generateVoice.place(x=270, y=580)
        
        
        #exit=tkinter.Button(self.frame, text="Logout", command = Exit, font = 'arial 9 bold', bg = 'Red')
        #exit.place(x=250, y=580)
        #Label(self.frame, bg="#f0f0f0", text="Welcome!\n\nYou have successfully logged in!", font=("Arial", 35)).pack(pady=50)
        Button(self.frame, text = "Logout",bg='white',fg='navy blue', font=("Arial", 10), padx=5,pady=2, command = self.onClick).place(x=550,y=620)
    
        self.frame.mainloop()

    def onClick(self):
        self.frame.destroy()
        LoginPage()

Dashboard()