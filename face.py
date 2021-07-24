from tkinter import messagebox
from tkinter import * 
from tkinter import ttk
import PIL
from PIL import ImageTk
from PIL import Image
import mysql.connector
import cv2
from datetime import datetime
from time import strftime

class Face:
    def __init__(self,root,**kwargs):
        self.root = root
        pad=3
        self.root.geometry("1350x1080+10+0")
        root.geometry("{0}x{1}+0+0".format(
            root.winfo_screenwidth()-pad, root.winfo_screenheight()-pad))
        root.bind('<Escape>',self.toggle_geom) 
        self.root.title("Face Recognization System")


        img = Image.open(r"Images\face.jpg")
        img = img.resize((2050,1380))
        self.photo = ImageTk.PhotoImage(img)

        bglbl = Label(self.root,image=self.photo)
        bglbl.place(width=2050,height=1380)
        tittlelbl = Label(bglbl,text="FACE DETECTION RECORDS AND SYSTEM",font=("Sans Serif",20,"bold"),fg="dark blue")
        tittlelbl.place(x=0, y=0, width=2050,height=40)

        back = Button(bglbl,cursor="hand2",text="Back",background="white",fg="dark blue", font=("Sans Serif",10,"bold"),command=root.destroy)
        back.place(x=0,y=0,width=150,height=40)   


        img1 = Image.open(r"Images\detect.jfif")
        img1 = img1.resize((750,400),Image.ANTIALIAS)
        self.photo1 = ImageTk.PhotoImage(img1)
        b1 = Button(bglbl,image=self.photo1)
        b1.place(x=0,y=40,width=750,height=400)
        b1lbl = Button(bglbl,text="Detect Face",font=("Sans Serif",20,"bold"),cursor="hand2",bg="brown",fg="white",command=self.face_recog)
        b1lbl.place(x=400,y=390,width=150,height=40)

    def toggle_geom(self,event):
        geom=self.root.winfo_geometry()
        print(geom,self._geom)
        self.root.geometry(self._geom)
        self._geom=geom

    
    def monitoring (self,n,i,g,f):
        with open("monitor.csv","r+",newline="\n") as r:
            myDataList= r.readlines()
            name_list=[]
            for line in myDataList:
                entry =line.split((","))
                name_list.append(entry[0])
            if ((n not in name_list) and (i not in name_list) and (g not in name_list) and (f not in name_list)):
                now = datetime.now()
                d1 = now.strftime("%d/%m/%Y")
                dt = now.strftime("%H:%M:%S")
                r.writelines(f"\n{i},{n},{g},{f},{dt},{d1}, Arrived")




    def face_recog(self):
        def boundary(img,classifier,sF,mN,color,text,cls):
            gray_image = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            features = classifier.detectMultiScale(gray_image,1.1,10)

            coord =[]
            for (x,y,w,h) in features:
                cv2.rectangle(img,(x,y),(x+w, y+h),(0,255,0),3)
                id,predict= cls.predict(gray_image[y:y+h,x:x+w])
                confidence =int((100*(1-predict/300)))

                conn = mysql.connector.connect(host="localhost",username="root",password="#",database="face_detection")
                my_cursr=conn.cursor()
                my_cursr.execute("Select name from details where id="+str(id))
                n = my_cursr.fetchone()
                n = "+".join(n)

                my_cursr.execute("Select id from details where id="+str(id))
                i = my_cursr.fetchone()
                i = "+".join(i)

                my_cursr.execute("Select gender from details where id="+str(id))
                g = my_cursr.fetchone()
                g = "+".join(g)

                my_cursr.execute("Select fields from details where id="+str(id))
                f = my_cursr.fetchone()
                f = "+".join(f)



                if confidence > 77:
                    cv2.putText(img,f"Name:{n}",(x,y-75),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),3)
                    cv2.putText(img,f"Id:{i}",(x,y-55),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),3)
                    cv2.putText(img,f"Gender:{g}",(x,y-30),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),3)
                    cv2.putText(img,f"Field:{f}",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),3)
                    self.monitoring(n,i,g,f)
                else:
                    cv2.rectangle(img,(x,y),(x + w, y + h),(0,0,255),3)
                    cv2.putText(img,"Unknow!! Not Registered",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                
                coord =[x,y,w,h]
            return coord

        def recognize(img,cls,faceCascade):
            coord = boundary(img,faceCascade,1.1,10,(255,25,255),"Face",cls)
            return img
        
        faceCascade= cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        cls = cv2.face.LBPHFaceRecognizer_create()
        cls.read("Classifier.xml")

        video_cap = cv2.VideoCapture(0)
        while True:
            ret,img =video_cap.read()
            img = recognize(img,cls,faceCascade)
            cv2.imshow("Welcome to face recognizer",img)

            if cv2.waitKey(1)==13:
                break
        video_cap.release()
        cv2.destroyAllWindows()
            
      

                    



if __name__ == "__main__":
    root=Tk()
    obj = Face(root)
    root.mainloop()