from tkinter import messagebox
from tkinter import * 
from tkinter import ttk
import PIL
from PIL import ImageTk
from PIL import Image
import mysql.connector
import cv2
import os
import numpy as np

class Train:
    def __init__(self,root,**kwargs):
        self.root = root
        pad=3
        self.root.geometry("1350x1080+10+0")
        root.geometry("{0}x{1}+0+0".format(
            root.winfo_screenwidth()-pad, root.winfo_screenheight()-pad))
        root.bind('<Escape>',self.toggle_geom) 
        self.root.title("Train data")


        img = Image.open(r"Images\face.jpg")
        img = img.resize((2050,1380))
        self.photo = ImageTk.PhotoImage(img)

        bglbl = Label(self.root,image=self.photo)
        bglbl.place(width=2050,height=1380)
        tittlelbl = Label(bglbl,text="FACE DETECTION RECORDS AND SYSTEM",font=("Sans Serif",20,"bold"),fg="dark blue")
        tittlelbl.place(x=0, y=0, width=2050,height=40)

        back = Button(bglbl,cursor="hand2",text="Back",background="white",fg="dark blue",font=("Sans Serif",10,"bold"),command=root.destroy)
        back.place(x=0,y=0,width=150,height=40)

        img1 = Image.open(r"Images\train.jfif")
        img1 = img1.resize((750,300),Image.ANTIALIAS)
        self.photo1 = ImageTk.PhotoImage(img1)
        b1 = Button(bglbl,image=self.photo1)
        b1.place(x=10,y=50,width=750,height=300)
        b1lbl = Button(bglbl,text="Train Data",font=("Sans Serif",20,"bold"),cursor="hand2",bg="grey",fg="white",command = self.train_face)
        b1lbl.place(x=10,y=310,width=750,height=40)

    def toggle_geom(self,event):
        geom=self.root.winfo_geometry()
        print(geom,self._geom)
        self.root.geometry(self._geom)
        self._geom=geom

    def train_face(self):
        data_dir =("photos")
        path = [os.path.join(data_dir,file) for file in os.listdir(data_dir)]
        faces = []
        ids = []
        try:
            for img in path:
                image = Image.open(img).convert('L') #Gray Scale
                npimg = np.array(image)
                id = int(os.path.split(img)[1].split('.')[1])

                faces.append(npimg)
                ids.append(id)
                cv2.imshow("Training",npimg)
                cv2.waitKey(1)==13
                
            ids = np.array(ids)
            
            cls = cv2.face.LBPHFaceRecognizer_create()
            cls.train(faces,ids)
            cls.write("Classifier.xml")
            cv2.destroyAllWindows
            messagebox.showinfo("Results","Training datasets completed!")
        except Exception as es:
                messagebox.showerror("Error!",f"Due to: {str(es)}",parent=self.root)






if __name__ == "__main__":
    root=Tk()
    obj = Train(root)
    root.mainloop()