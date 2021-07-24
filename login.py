import tkinter
from tkinter import messagebox
from tkinter import * 
from tkinter import ttk
import mysql.connector
import datetime
from time import strftime, time
import PIL
from PIL import ImageTk
from PIL import Image
from detail import Details
import os
from train import Train
from face import Face


def main():
    win = Tk()
    app = Login(win)
    win.mainloop()

class Login:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1350x1080+15+15")
        self.root.title("Login")


        img = Image.open(r"Images\face.jpg")
        img = img.resize((2050,1380))
        self.photo = ImageTk.PhotoImage(img)

        bglbl = Label(self.root,image=self.photo)
        bglbl.place(width=1350,height=1080)
        tittlelbl = Label(bglbl,text="FACE DETECTION RECORDS AND SYSTEM",font=("Sans Serif",20,"bold"),fg="dark blue")
        tittlelbl.place(x=0, y=0, width=1350,height=40)

        main_frame = Frame(self.root,bg ="black")
        main_frame.place(x=500,y=200,width=350,height=550)


        img1 = Image.open(r"Images\login.png")
        img1 = img1.resize((150,150), Image.ANTIALIAS)
        self.photo1 = ImageTk.PhotoImage(img1)
        lblimg1 =Label(image=self.photo1,bg="white",borderwidth=0)
        lblimg1.place(x=600,y=200,width=150,height=150)

        get_star =Label(main_frame,text = "Getting Started",fg="white",background="black",font=("Sans Serif",14,"bold"))
        get_star.place(x=110,y=150)

        username =Label(main_frame,text = "Username",fg="white",background="black",font=("Sans Serif",12,"bold"))
        username.place(x=70,y=190)

        self.txtusr = ttk.Entry(main_frame,font=("Sans Serif",12,"bold"))
        self.txtusr.place(x=40,y=220,width=250)


        password =Label(main_frame,text = "Password",fg="white",background="black",font=("Sans Serif",12,"bold"))
        password.place(x=70,y=260)

        self.txtpass = ttk.Entry(main_frame,font=("Sans Serif",12,"bold"),show="*")
        self.txtpass.place(x=40,y=290,width=250)


        img2 = Image.open(r"Images\icon1.png")
        img2 = img2.resize((30,30), Image.ANTIALIAS)
        self.photo2 = ImageTk.PhotoImage(img2)
        lblimg2 =Label(image=self.photo2,bg="white",borderwidth=0)
        lblimg2.place(x=540,y=390,width=30,height=30)

        img3 = Image.open(r"Images\pass.jfif")
        img3 = img3.resize((30,30), Image.ANTIALIAS)
        self.photo3 = ImageTk.PhotoImage(img3)
        lblimg3 =Label(image=self.photo3,bg="white",borderwidth=0)
        lblimg3.place(x=540,y=460,width=30,height=30)

        log_b = Button(main_frame,font=("Sans Serif",12,"bold"),bd=3,relief=RIDGE,text="Login",fg="white",bg="red",command=self.login)
        log_b.place(x=110,y=330,width=120,height=30)

        reg_b = Button(main_frame,font=("Sans Serif",10,"bold"),borderwidth=0,relief=RIDGE,text="Registration",fg="white",bg="black",activebackground="red",activeforeground="white",command=self.register_win )
        reg_b.place(x=20,y=380,width=220,height=20)

        forg_b = Button(main_frame,font=("Sans Serif",10,"bold"),borderwidth=0,relief=RIDGE,text="Forgot Password?",fg="white",bg="black",activebackground="red",activeforeground="white",command=self.forgot_pass)
        forg_b.place(x=40,y=400,width=220,height=20)

    def toggle_geom(self,event):
        geom=self.root.winfo_geometry()
        print(geom,self._geom)
        self.root.geometry(self._geom)
        self._geom=geom
    
    
    def login(self):
        if self.txtusr.get()=="" or self.txtpass.get()=="":
            messagebox.showerror("Error!","Must provide entry")
        else:
            conn = mysql.connector.connect(host="localhost",username="root",password="#",database="face_detection")
            my_cursr=conn.cursor()
            my_cursr.execute("Select * from register where username=%s and password=%s",(
                                                                                        self.txtusr.get(),
                                                                                        self.txtpass.get()
                                                                                    ))

            row = my_cursr.fetchone()
            if row ==None:
                messagebox.showerror("Error!!","Invalid username & password")
            else:
                open_win = messagebox.askyesno("YesNo","Access only Admin")
                if open_win >0 :
                    self.new_window = Toplevel(self.root)
                    self.app = Face_system(self.new_window)
                else:
                    if not open_win:
                        return
            
            conn.commit()
            conn.close()


    def reset_pass(self):
        if self.sq_box.get()=="Select":
            messagebox.showerror("Error!!","Please Select the security question",parent=self.root2)
        elif self.sa_ent.get()=="":
            messagebox.showerror("Error!!","Please answer the question",parent=self.root2)
        elif self.newpass_ent.get()=="":
            messagebox.showerror("Error!!","Please enter the new password",parent=self.root2)
        else:
            conn = mysql.connector.connect(host="localhost",username="root",password="#",database="face_detection")
            my_cursr=conn.cursor()
            query = ("Select * from register where username=%s and secq=%s and seca=%s")
            value =(self.txtusr.get(),self.sq_box.get(),self.sa_ent.get(),)
            my_cursr.execute(query,value)
            row = my_cursr.fetchone()
            if row == None:
                messagebox.showerror("Error!!","Please enter the correct answer",parent=self.root2)
            else:
                quer = ("update register set password=%s where username=%s")
                valu = (self.newpass_ent.get(),self.txtusr.get())
                my_cursr.execute(quer,valu)
                
                conn.commit()
                conn.close()
                messagebox.showinfo("Success","Successfully reset password!",parent=self.root2)
                self.root2.destroy()



        

    def forgot_pass(self):
        if self.txtusr.get()=="":
            messagebox.showerror("Error!!","Please enter the username to reset password")
        else:
            conn = mysql.connector.connect(host="localhost",username="root",password="#",database="face_detection")
            my_cursr=conn.cursor()
            query=("Select * from register where username=%s")
            value =(self.txtusr.get(),)
            my_cursr.execute(query,value)
            row = my_cursr.fetchone()
            if row == None:
                messagebox.showerror("Error!!","Please enter valid username")
            else:
                conn.close()
                self.root2 = Toplevel()
                self.root2.title("Forget Password")
                self.root2.geometry("340x450+610+170")


                l1 = Label(self.root2,text="Forgot Password",font=("Sans Serif",20,"bold"),fg="red",bg="black")
                l1.place(x=0,y=20,relwidth=1)

                sq_lbl = Label(self.root2,text="Security Question",font=("Sans Serif",10,"bold"),fg="black",bg="white")
                sq_lbl.place(x=50,y=80)

                self.sq_box = ttk.Combobox(self.root2,font=("Sans Serif",10,"bold"),state="readonly")
                self.sq_box["values"]=("Select","Your First School","Your Favourite Club","Your Pet's name","Your Hometown","Your Birthplace")
                self.sq_box.current(0)
                self.sq_box.place(x=50,y=110,width=250,height=40)

                sa_lbl = Label(self.root2,text="Security Answer",font=("Sans Serif",10,"bold"),fg="black",bg="white")
                sa_lbl.place(x=50,y=150)

                self.sa_ent = ttk.Entry(self.root2,text="Security Answer",font=("Sans Serif",10,"bold"))
                self.sa_ent.place(x=50,y=180,width=250,height=40)

                newpass_lbl = Label(self.root2,text="NEW PASSWORD",font=("Sans Serif",10,"bold"),fg="black",bg="white")
                newpass_lbl.place(x=50,y=220)

                self.newpass_ent = ttk.Entry(self.root2,text="NEW PASSWORD",font=("Sans Serif",10,"bold"),show="*")
                self.newpass_ent.place(x=50,y=250,width=250,height=40)

                b1 = Button(self.root2,text="Rest Password",font=("Sans Serif",10,"bold"),bg="red",fg="white",command=self.reset_pass)
                b1.place(x=120,y=300)



    
    
    def register_win(self):
        self.new_window = Toplevel(self.root)
        self.app = Register(self.new_window)


class Register:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1350x1080+15+15")
        self.root.title("Register")

        self.var_name = StringVar()
        self.var_usname = StringVar()
        self.var_email = StringVar()
        self.var_pass = StringVar()
        self.var_cpass = StringVar()
        self.var_sq = StringVar()
        self.var_sa = StringVar()


        img = Image.open(r"Images\face.jpg")
        img = img.resize((1350,1080))
        self.photo = ImageTk.PhotoImage(img)

        bglbl = Label(self.root,image=self.photo)
        bglbl.place(width=1350,height=1080)
        tittlelbl = Label(bglbl,text="FACE DETECTION RECORDS AND SYSTEM",font=("Sans Serif",20,"bold"),fg="dark blue")
        tittlelbl.place(x=0, y=0, width=1350,height=40)

        reg_frame = Frame(self.root,bg="white")
        reg_frame.place(x=500,y=100,width=800,height=650)

        reg_lbl = Label(reg_frame,text="REGISTRATION HERE",font=("Sans Serif",20,"bold"),fg="green",bg="white")
        reg_lbl.place(x=30,y=10)

        name_lbl = Label(reg_frame,text="NAME",font=("Sans Serif",14,"bold"),fg="black",bg="white")
        name_lbl.place(x=20,y=70)

        name_ent = ttk.Entry(reg_frame,text="NAME",font=("Sans Serif",14,"bold"),textvariable=self.var_name)
        name_ent.place(x=20,y=100,width=250,height=40)

        usnam_lbl = Label(reg_frame,text="USERNAME",font=("Sans Serif",14,"bold"),fg="black",bg="white",)
        usnam_lbl.place(x=20,y=170)

        usnam_ent = ttk.Entry(reg_frame,text="USERNAME",font=("Sans Serif",14,"bold"),textvariable=self.var_usname)
        usnam_ent.place(x=20,y=200,width=250,height=40)

        sq_lbl = Label(reg_frame,text="Security Question",font=("Sans Serif",14,"bold"),fg="black",bg="white")
        sq_lbl.place(x=20,y=270)

        sq_box = ttk.Combobox(reg_frame,font=("Sans Serif",14,"bold"),state="readonly",textvariable=self.var_sq)
        sq_box["values"]=("Select","Your First School","Your Favourite Club","Your Pet's name","Your Hometown","Your Birthplace")
        sq_box.current(0)
        sq_box.place(x=20,y=300,width=250,height=40)

        sa_lbl = Label(reg_frame,text="Security Answer",font=("Sans Serif",14,"bold"),fg="black",bg="white")
        sa_lbl.place(x=20,y=370)

        sa_ent = ttk.Entry(reg_frame,text="Security Answer",font=("Sans Serif",14,"bold"),textvariable=self.var_sa)
        sa_ent.place(x=20,y=400,width=250,height=40)


        email_lbl = Label(reg_frame,text="EMAIL",font=("Sans Serif",14,"bold"),fg="black",bg="white")
        email_lbl.place(x=420,y=70)

        email_ent = ttk.Entry(reg_frame,text="EMAIL",font=("Sans Serif",14,"bold"),textvariable=self.var_email)
        email_ent.place(x=420,y=100,width=250,height=40)


        pass_lbl = Label(reg_frame,text="PASSWORD",font=("Sans Serif",14,"bold"),fg="black",bg="white")
        pass_lbl.place(x=420,y=170)

        pass_ent = ttk.Entry(reg_frame,text="PASSWORD",font=("Sans Serif",14,"bold"),show="*",textvariable=self.var_pass)
        pass_ent.place(x=420,y=200,width=250,height=40)

        cpass_lbl = Label(reg_frame,text="CONFIRM PASSWORD",font=("Sans Serif",14,"bold"),fg="black",bg="white")
        cpass_lbl.place(x=420,y=270)

        cpass_ent = ttk.Entry(reg_frame,text="CONFIRM PASSWORD",font=("Sans Serif",14,"bold"),show="*",textvariable=self.var_cpass)
        cpass_ent.place(x=420,y=300,width=250,height=40)

        self.var_chk = IntVar()
        chk_btn = Checkbutton(reg_frame,font=("Sans Serif",12,"bold"),text="I agree to the Terms & Conditions",bg="white",onvalue=1,offvalue=0,variable=self.var_chk)
        chk_btn.place(x=20,y=450)


        img1 = Image.open(r"Images\register.jfif")
        img1 = img1.resize((200,100),Image.ANTIALIAS)
        self.photo1 = ImageTk.PhotoImage(img1)
        b1 = Button(reg_frame,image=self.photo1,cursor="hand2",bd=0,command=self.register_data)
        b1.place(x=50,y=500,width=200,height=100)


        img2 = Image.open(r"Images\login1.jpg")
        img2 = img2.resize((200,100),Image.ANTIALIAS)
        self.photo2 = ImageTk.PhotoImage(img2)
        b2 = Button(reg_frame,image=self.photo2,cursor="hand2",bd=0,command=self.login_now)
        b2.place(x=450,y=500,width=200,height=100)

    
    def register_data(self):
        if self.var_name.get()=="" or self.var_usname.get()=="" or self.var_pass.get()=="" or self.var_cpass.get()=="" or self.var_sq.get()=="Select" or self.var_sa.get()=="" or self.var_email.get()=="":
            messagebox.showerror("Error!!","All information must be filled")
        elif self.var_pass.get() != self.var_cpass.get():
            messagebox.showerror("Error!!","Passwords do not match with confirm password")
        elif self.var_chk.get()==0:
            messagebox.showerror("Error!!","Please agree to terms & conditions")
        else:
            conn = mysql.connector.connect(host="localhost",username="root",password="#",database="face_detection")
            my_cursr=conn.cursor()
            query = ("Select * from register where email=%s")
            value =(self.var_email.get(),)
            my_cursr.execute(query,value)
            row = my_cursr.fetchone()
            if row !=None:
                messagebox.showerror("Error!","User already exists with this email")
            else:
                my_cursr.execute("insert into register values(%s,%s,%s,%s,%s,%s,%s)",(
                                                                                      self.var_name.get(),
                                                                                      self.var_usname.get(),
                                                                                      self.var_email.get(),
                                                                                      self.var_pass.get(),
                                                                                      self.var_cpass.get(),
                                                                                      self.var_sq.get(),
                                                                                      self.var_sa.get()
                                                                                    ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success","Register Successfully!!")

    def login_now(self):
        self.root.destroy()

            
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
    main()