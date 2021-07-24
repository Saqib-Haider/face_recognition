from tkinter import *
from tkinter import ttk
import tkinter
import datetime
from time import strftime, time
import PIL
from PIL import ImageTk
from PIL import Image
from detail import Details
import os
from train import Train
from face import Face

class Face_system:
    def __init__(self,root,**kwargs):
        self.root = root
        pad=3
        self.root.geometry("1350x1080+10+0")
        root.geometry("{0}x{1}+0+0".format(
            root.winfo_screenwidth()-pad, root.winfo_screenheight()-pad))
        root.bind('<Escape>',self.toggle_geom)  
        self.root.title("Face Detection System")

        img = Image.open(r"Images\face.jpg")
        img = img.resize((2050,1380))
        self.photo = ImageTk.PhotoImage(img)

        bglbl = Label(self.root,image=self.photo)
        bglbl.place(width=2050,height=1380)
        tittlelbl = Label(bglbl,text="FACE DETECTION RECORDS AND SYSTEM",font=("Sans Serif",20,"bold"),fg="dark blue")
        tittlelbl.place(x=0, y=0, width=2050,height=40)


        img1 = Image.open(r"Images\decimal.jpg")
        img1 = img1.resize((250,200))
        self.photo1 = ImageTk.PhotoImage(img1)
        b1 = Button(bglbl,image=self.photo1,cursor="hand2",command=self.add_details)
        b1.place(x=50,y=50,width=250,height=200)
        b1lbl = Button(bglbl,text="Add Details",font=("Sans Serif",20,"bold"),command=self.add_details,cursor="hand2",bg="#00ddff",fg="white")
        b1lbl.place(x=50,y=230,width=250,height=40)

        img2 = Image.open(r"Images\single.jpg")
        img2 = img2.resize((250,200))
        self.photo2 = ImageTk.PhotoImage(img2)
        b2 = Button(bglbl,image=self.photo2,cursor="hand2",command=self.face_data)
        b2.place(x=350,y=50,width=250,height=200)
        b2lbl = Button(bglbl,text="Detect Face",font=("Sans Serif",20,"bold"),command=self.face_data,cursor="hand2",bg="#00ddff",fg="white")
        b2lbl.place(x=350,y=230,width=250,height=40)

        img3 = Image.open(r"Images\train data.png")
        img3 = img3.resize((250,200))
        self.photo3 = ImageTk.PhotoImage(img3)
        b3 = Button(bglbl,image=self.photo3,cursor="hand2",command=self.train_data)
        b3.place(x=50,y=450,width=250,height=200)
        b3lbl = Button(bglbl,text="Train data",font=("Sans Serif",20,"bold"),command=self.train_data,cursor="hand2",bg="#00ddff",fg="white")
        b3lbl.place(x=50,y=650,width=250,height=40)

        img4 = Image.open(r"Images\record.jpg")
        img4 = img4.resize((250,200))
        self.photo4 = ImageTk.PhotoImage(img4)
        b4 = Button(bglbl,image=self.photo4,cursor="hand2",command=self.open_img)
        b4.place(x=350,y=450,width=250,height=200)
        b4lbl = Button(bglbl,text="Records",font=("Sans Serif",20,"bold"),cursor="hand2",bg="#00ddff",fg="white",command=self.open_img)
        b4lbl.place(x=350,y=650,width=250,height=40)

        img5 = Image.open(r"Images\monitoring.jfif")
        img5 = img5.resize((250,200))
        self.photo5 = ImageTk.PhotoImage(img5)
        b5 = Button(bglbl,image=self.photo5,cursor="hand2",command=self.open_file)
        b5.place(x=650,y=50,width=250,height=200)
        b5lbl = Button(bglbl,text="Monitoring",font=("Sans Serif",20,"bold"),cursor="hand2",bg="#00ddff",fg="white",command=self.open_file)
        b5lbl.place(x=650,y=230,width=250,height=40)

        img6 = Image.open(r"Images\exit.jpg")
        img6 = img6.resize((250,200))
        self.photo6 = ImageTk.PhotoImage(img6)
        b6 = Button(bglbl,image=self.photo6,cursor="hand2",command=self.exit_soft)
        b6.place(x=650,y=450,width=250,height=200)
        b6lbl = Button(bglbl,text="Exit",font=("Sans Serif",20,"bold"),cursor="hand2",bg="#00ddff",fg="white",command=self.exit_soft)
        b6lbl.place(x=650,y=650,width=250,height=40)

        def time():
            stime = strftime("%H:%M:%S %p")
            lbl.config(text = stime)
            lbl.after(1000, time)
        lbl = Label(tittlelbl,font=("Sans Serif",10,"bold"),background="white",fg="dark blue")
        lbl.place(x=0,y=0,width=110,height=50)
        time()

    def toggle_geom(self,event):
        geom=self.root.winfo_geometry()
        print(geom,self._geom)
        self.root.geometry(self._geom)
        self._geom=geom
    
    def open_img(self):
        os.startfile("photos")
    
    def add_details(self):
        self.new_window= Toplevel(self.root)
        self.soft=Details(self.new_window)
    
    def train_data(self):
        self.new_window= Toplevel(self.root)
        self.soft=Train(self.new_window)

    def face_data(self):
        self.new_window= Toplevel(self.root)
        self.soft=Face(self.new_window)
    
    def open_file(self):
        os.startfile("monitor.csv")

    def exit_soft(self):
        self.exit_soft = tkinter.messagebox.askyesno("Face Recognization","Are you sure you want to exit?", parent=self.root)
        if self.exit_soft > 0:
            self.root.destroy()
        else:
            return

        




if __name__ == "__main__":
    root=Tk()
    obj = Face_system(root)
    root.mainloop()