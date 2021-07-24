from tkinter import messagebox
from tkinter import * 
from tkinter import ttk
import PIL
from PIL import ImageTk
from PIL import Image
import mysql.connector
import cv2

class Details:
    def __init__(self,root,**kwargs):
        self.root = root
        pad=3
        self.root.geometry("1350x1080+10+0")
        root.geometry("{0}x{1}+0+0".format(
            root.winfo_screenwidth()-pad, root.winfo_screenheight()-pad))
        root.bind('<Escape>',self.toggle_geom)  
        self.root.title("Add details")


        self.var_name= StringVar()
        self.var_id= StringVar()
        self.var_age= StringVar()
        self.var_dob= StringVar()
        self.var_gen= StringVar()
        self.var_field= StringVar()
        self.var_address= StringVar()
        self.var_reli= StringVar()
        self.var_phone= StringVar()
        self.var_nati= StringVar()





        img = Image.open(r"Images\face.jpg")
        img = img.resize((2050,1380))
        self.photo = ImageTk.PhotoImage(img)

        bglbl = Label(self.root,image=self.photo)
        bglbl.place(width=2050,height=1380)
        tittlelbl = Label(bglbl,text="FACE DETECTION RECORDS AND SYSTEM",font=("Sans Serif",20,"bold"),fg="dark blue")
        tittlelbl.place(x=0, y=0, width=2050,height=40)

        back = Button(bglbl,cursor="hand2",text="Back",background="white",fg="dark blue" ,font=("Sans Serif",10,"bold"),command=root.destroy)
        back.place(x=0,y=0,width=150,height=40)

        bg_frame = Frame(bglbl,bd=2)
        bg_frame.place(x=50,y=50,width=1200,height=700)

        l_frame = LabelFrame(bg_frame,bd=2,relief=RIDGE,text="Add Details and Information",font=("Sans Serif",20,"bold"),fg="dark blue")
        l_frame.place(x=50,y=50,width=560,height=600)

        r_frame = LabelFrame(bg_frame,bd=2,relief=RIDGE,text="Details and Search",font=("Sans Serif",20,"bold"),fg="dark blue")
        r_frame.place(x=600,y=50,width=560,height=600)

        search_frame = LabelFrame(r_frame,bd=4,bg="white",relief=RIDGE,text="Search..",font=("Sans Serif",20,"bold"))
        search_frame.place(x=0,y=0,width=550,height=100)

        search_lbl = Label(search_frame,text="Search",font=("Sans Serif",12,"bold"),bg="black",fg="white")
        search_lbl.grid(row=0,column=0,padx=5,pady=5,sticky=W)
        search_box = ttk.Combobox(search_frame,font=("Sans Serif",12,"bold"),width=10,state="readonly")
        search_box["values"]=("Select Search By","ID","AGE","FIELD STATUS","GENDER")
        search_box.current(0)
        search_box.grid(row=0,column=1,padx=5,pady=5,sticky=W)
        search_entry = ttk.Entry(search_frame,text="Search",font=("Sans Serif",12,"bold"),width=20)
        search_entry.grid(row=0,column=2,padx=5,pady=5,sticky=W)
        search_btn = Button(search_frame,text="Search",font=("Sans Serif",12,"bold"),bg="black",fg="white",cursor="hand2",width=10)
        search_btn.grid(row=0,column=3)
        
        table_frame = Frame(r_frame,bd=4,relief=RIDGE)
        table_frame.place(x=0,y=105,width=550,height=450)
        scroll_x = Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y = Scrollbar(table_frame,orient=VERTICAL)
        self.details_table = ttk.Treeview(table_frame,column=("NAME","ID","AGE","DOB","GENDER","ADDRESS","NATIONALITY","PHONE","RELIGION","FIELD STATUS","PHOTO"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.details_table.xview)
        scroll_y.config(command=self.details_table.yview)

        self.details_table.heading("NAME",text="NAME")
        self.details_table.heading("ID",text="ID")
        self.details_table.heading("AGE",text="AGE")
        self.details_table.heading("DOB",text="DOB")
        self.details_table.heading("GENDER",text="GENDER")
        self.details_table.heading("ADDRESS",text="ADDRESS")
        self.details_table.heading("NATIONALITY",text="NATIONALITY")
        self.details_table.heading("PHONE",text="PHONE")
        self.details_table.heading("RELIGION",text="RELIGION")
        self.details_table.heading("FIELD STATUS",text="FIELD STATUS")
        self.details_table.heading("PHOTO",text="PHOTO")
        self.details_table["show"]="headings"

        self.details_table.column("NAME",width=100)
        self.details_table.column("ID",width=100)
        self.details_table.column("AGE",width=100)
        self.details_table.column("DOB",width=100)
        self.details_table.column("GENDER",width=100)
        self.details_table.column("ADDRESS",width=100)
        self.details_table.column("NATIONALITY",width=100)
        self.details_table.column("PHONE",width=100)
        self.details_table.column("RELIGION",width=100)
        self.details_table.column("FIELD STATUS",width=100)
        self.details_table.column("PHOTO",width=100)
        
        

        self.details_table.pack(fill=BOTH,expand=1)
        self.details_table.bind("<ButtonRelease>",self.cursor_focus)
        self.get_data()




        name_lbl = Label(l_frame,text="NAME",font=("Sans Serif",12,"bold"))
        name_lbl.grid(row=0,column=0,padx=10,pady=10,sticky=W)
        name_entry = ttk.Entry(l_frame,text="NAME",font=("Sans Serif",12,"bold"),width=20,textvariable=self.var_name)
        name_entry.grid(row=0,column=1,padx=10,pady=10,sticky=W)

        id_lbl = Label(l_frame,text="ID",font=("Sans Serif",12,"bold"))
        id_lbl.grid(row=1,column=0,padx=10,pady=10,sticky=W)
        id_entry = ttk.Entry(l_frame,text="ID",font=("Sans Serif",12,"bold"),width=20,textvariable=self.var_id)
        id_entry.grid(row=1,column=1,padx=10,pady=10,sticky=W)

        address_lbl = Label(l_frame,text="ADDRESS",font=("Sans Serif",12,"bold"))
        address_lbl.grid(row=2,column=0,padx=10,pady=10,sticky=W)
        address_entry = ttk.Entry(l_frame,text="ADDRESS",font=("Sans Serif",12,"bold"),width=25,textvariable=self.var_address)
        address_entry.grid(row=2,column=1,padx=10,pady=10,sticky=W)

        religion_lbl = Label(l_frame,text="RELIGION",font=("Sans Serif",12,"bold"))
        religion_lbl.grid(row=3,column=0,padx=10,pady=10,sticky=W)
        religion_box = ttk.Combobox(l_frame,font=("Sans Serif",12,"bold"),width=20,state="readonly",textvariable=self.var_reli)
        religion_box["values"]=("Select..","Islam","Hindu","Christian","Buddism")
        religion_box.current(0)
        religion_box.grid(row=3,column=1,padx=10,pady=10,sticky=W)

        dob_lbl = Label(l_frame,text="DOB",font=("Sans Serif",12,"bold"))
        dob_lbl.grid(row=4,column=0,padx=10,pady=10,sticky=W)
        dob_entry = ttk.Entry(l_frame,text="DOB",font=("Sans Serif",12,"bold"),textvariable=self.var_dob)
        dob_entry.grid(row=4,column=1,padx=10,pady=10,sticky=W)

        gender_lbl = Label(l_frame,text="GENDER",font=("Sans Serif",12,"bold"))
        gender_lbl.grid(row=5,column=0,padx=10,pady=10,sticky=W)
        gender_box = ttk.Combobox(l_frame,font=("Sans Serif",12,"bold"),width=18,state="readonly",textvariable=self.var_gen)
        gender_box["values"]=("Select gender","Male","Female","Transgender")
        gender_box.current(0)
        gender_box.grid(row=5,column=1,padx=10,pady=10,sticky=W)

        nationality_lbl = Label(l_frame,text="NATIONALITY",font=("Sans Serif",12,"bold"))
        nationality_lbl.grid(row=6,column=0,padx=10,pady=10,sticky=W)
        nationality_entry = ttk.Entry(l_frame,text="NATIONALITY",font=("Sans Serif",12,"bold"),textvariable=self.var_nati)
        nationality_entry.grid(row=6,column=1,padx=10,pady=10,sticky=W)

        age_lbl = Label(l_frame,text="AGE",font=("Sans Serif",12,"bold"))
        age_lbl.grid(row=7,column=0,padx=10,pady=10,sticky=W)
        age_entry = ttk.Entry(l_frame,text="AGE",font=("Sans Serif",12,"bold"),textvariable=self.var_age)
        age_entry.grid(row=7,column=1,padx=10,pady=10,sticky=W)


        field_lbl = Label(l_frame,text="FIELD STATUS",font=("Sans Serif",12,"bold"))
        field_lbl.grid(row=8,column=0,padx=10,pady=10,sticky=W)
        field_box = ttk.Combobox(l_frame,font=("Sans Serif",12,"bold"),width=18,state="readonly",textvariable=self.var_field)
        field_box["values"]=("Select Field Status","CEO","Manager","Sr.Developer","Jr.Developer","Jr.Software Engineer","Sr.Software Engineer","Graphics Designer","Software Tester","Sales Manager","Executive Manager","Co-owner","Project Advisor","HR","Admin panel","Intern","Sales Leader","Trainee","Helper","General Worker")
        field_box.current(0)
        field_box.grid(row=8,column=1,padx=10,pady=10,sticky=W)
        
        phone_lbl = Label(l_frame,text="PHONE",font=("Sans Serif",12,"bold"))
        phone_lbl.grid(row=9,column=0,padx=10,pady=10,sticky=W)
        phone_entry = ttk.Entry(l_frame,text="PHONE",font=("Sans Serif",12,"bold"),textvariable=self.var_phone)
        phone_entry.grid(row=9,column=1,padx=10,pady=10,sticky=W)

        self.var_rad = StringVar()
        rad_btn = ttk.Radiobutton(l_frame,text="Take Photo Sample",value="Yes",variable=self.var_rad)
        rad_btn.grid(row=10,column=0)
        
        rad_btn1 = ttk.Radiobutton(l_frame,text="No Photo Sample",value="NO",variable=self.var_rad)
        rad_btn1.grid(row=10,column=1)

        btn_frame = Frame(l_frame,bd=4,relief=RIDGE)
        btn_frame.place(x=0,y=490,width=545,height=40)

        save_btn = Button(btn_frame,text="Save",font=("Sans Serif",12,"bold"),command=self.add_data,bg="black",fg="white",cursor="hand2",width=13)
        save_btn.grid(row=0,column=0)

        edit_btn = Button(btn_frame,text="Edit",font=("Sans Serif",12,"bold"),command=self.update_data,bg="black",fg="white",cursor="hand2",width=13)
        edit_btn.grid(row=0,column=1)

        delete_btn = Button(btn_frame,text="Delete",font=("Sans Serif",12,"bold"),command=self.delete_data,bg="black",fg="white",cursor="hand2",width=13)
        delete_btn.grid(row=0,column=2)

        reset_btn = Button(btn_frame,text="Reset",font=("Sans Serif",12,"bold"),command=self.reset_data,bg="black",fg="white",cursor="hand2",width=12)
        reset_btn.grid(row=0,column=3)

        btn_frame1 = Frame(l_frame,bd=4,relief=RIDGE)
        btn_frame1.place(x=0,y=520,width=560,height=40)

        takep_btn = Button(btn_frame1,text="Capture Photo",command =self.generate_data,font=("Sans Serif",12,"bold"),bg="black",fg="white",cursor="hand2",width=27)
        takep_btn.grid(row=0,column=0)
        updatep_btn = Button(btn_frame1,text="Upadate Captured Photo",font=("Sans Serif",12,"bold"),bg="black",fg="white",cursor="hand2",width=27)
        updatep_btn.grid(row=0,column=1)

    def toggle_geom(self,event):
        geom=self.root.winfo_geometry()
        print(geom,self._geom)
        self.root.geometry(self._geom)
        self._geom=geom


    def add_data(self):
        if self.var_name.get()=="" or self.var_id.get()== "" or self.var_age==""or self.var_address=="" or self.var_dob==""or self.var_phone=="" or self.var_gen=="Select gender"or self.var_nati=="" or self.var_reli =="Select.." or self.var_field=="Select Field Status":
            messagebox.showerror("ERROR!","All must be filled!!",parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="localhost",username="root",password="#",database="face_detection")
                my_cursr=conn.cursor()
                my_cursr.execute("insert into details values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(
                                                                                             self.var_name.get(),
                                                                                             self.var_id.get(),
                                                                                             self.var_age.get(),
                                                                                             self.var_dob.get(),
                                                                                             self.var_gen.get(),
                                                                                             self.var_address.get(),
                                                                                             self.var_nati.get(),
                                                                                             self.var_phone.get(),
                                                                                             self.var_reli.get(),
                                                                                             self.var_field.get(),
                                                                                             self.var_rad.get()
                                                                                             ))
                conn.commit()
                self.get_data()
                conn.close()
                messagebox.showinfo("Success", "Successfully information added",parent=self.root)                                                                             
            except Exception as es:
                messagebox.showerror("Error!",f"Due to: {str(es)}",parent=self.root)

    def get_data(self):
        conn = mysql.connector.connect(host="localhost",username="root",password="#",database="face_detection")
        my_cursr=conn.cursor()
        my_cursr.execute("Select * from details")
        data = my_cursr.fetchall()

        if len(data) !=0:
            self.details_table.delete(*self.details_table.get_children())
            for i in data:
                self.details_table.insert("",END,values=i)
            conn.commit()
        conn.close()

    def cursor_focus(self,event=''):
        cursr_focus=self.details_table.focus()
        content = self.details_table.item(cursr_focus)
        data = content["values"]

        self.var_name.set(data[0]),
        self.var_id.set(data[1]),
        self.var_age.set(data[2]),
        self.var_dob.set(data[3]),
        self.var_gen.set(data[4]),
        self.var_address.set(data[5]),
        self.var_nati.set(data[6]),
        self.var_phone.set(data[7]),
        self.var_reli.set(data[8]),
        self.var_field.set(data[9]),
        self.var_rad.set(data[10])



    def update_data(self):
        if self.var_name.get()=="" or self.var_id.get()== "" or self.var_age==""or self.var_address=="" or self.var_dob==""or self.var_phone=="" or self.var_gen=="Select gender"or self.var_nati=="" or self.var_reli =="Select.." or self.var_field=="Select Field Status":
            messagebox.showerror("ERROR!","All must be filled!!",parent=self.root)
        else:
            try:
                update = messagebox.askyesno("Update","Do you want to make changes?",parent=self.root)
                if update > 0:
                    conn = mysql.connector.connect(host="localhost",username="root",password="#",database="face_detection")
                    my_cursr=conn.cursor()
                    my_cursr.execute("Update details set name=%s,age=%s,dob=%s,gender=%s,address=%s,nationality=%s,phone=%s,religion=%s,fields=%s,Photosample=%s where id=%s",(

                                                                                                                                                              self.var_name.get(),
                                                                                                                                                              self.var_age.get(),
                                                                                                                                                              self.var_dob.get(),
                                                                                                                                                              self.var_gen.get(),
                                                                                                                                                              self.var_address.get(),
                                                                                                                                                              self.var_nati.get(),
                                                                                                                                                              self.var_phone.get(),
                                                                                                                                                              self.var_reli.get(),
                                                                                                                                                              self.var_field.get(),
                                                                                                                                                              self.var_rad.get(),
                                                                                                                                                              self.var_id.get()
                                                                                                                                                              ))
                else:
                    if not update:
                        return
                messagebox.showinfo("Success!","Successfully Updated data",parent=self.root)
                conn.commit()
                self.get_data()
                conn.close()
            except Exception as es:
                messagebox.showerror("Error!",f"Due to: {str(es)}",parent=self.root) 


    def delete_data(self):
        if self.var_id.get()== "":
            messagebox.showerror("Error","ID must be required",parent=self.root)
        else:
            try:
                delete = messagebox.askyesno("Delete","Are you sure you want to delete this?",parent=self.root)
                if delete > 0:
                    conn = mysql.connector.connect(host="localhost",username="root",password="#",database="face_detection")
                    my_cursr=conn.cursor()
                    sql = "delete from details where id=%s"
                    val = (self.var_id.get(),)
                    my_cursr.execute(sql,val)
                else:
                    if not delete:
                        return
                messagebox.showinfo("Success!","Successfully deleted data",parent=self.root)
                conn.commit()
                self.get_data()
                conn.close() 
            except Exception as es:
                messagebox.showerror("Error!",f"Due to: {str(es)}",parent=self.root) 


    def reset_data(self):
        self.var_name.set("")
        self.var_id.set("")
        self.var_age.set("")
        self.var_dob.set("")
        self.var_gen.set("Select gender")
        self.var_address.set("")
        self.var_nati.set("")
        self.var_phone.set("")
        self.var_reli.set("Select..")
        self.var_field.set("Select Field Status")
        self.var_rad.set("")


    def generate_data(self):
        if self.var_name.get()=="" or self.var_id.get()== "" or self.var_age==""or self.var_address=="" or self.var_dob==""or self.var_phone=="" or self.var_gen=="Select gender"or self.var_nati=="" or self.var_reli =="Select.." or self.var_field=="Select Field Status":
            messagebox.showerror("ERROR!","All must be filled!!",parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="localhost",username="root",password="#",database="face_detection")
                my_cursr=conn.cursor()
                my_cursr.execute("Select * from details")
                result = my_cursr.fetchall()
                idd = 0
                for i in result:
                    idd +=1
                my_cursr.execute("update details set name=%s,age=%s,dob=%s,gender=%s,address=%s,nationality=%s,phone=%s,religion=%s,fields=%s,Photosample=%s where id=%s",(

                                                                                                                                                              self.var_name.get(),
                                                                                                                                                              self.var_age.get(),
                                                                                                                                                              self.var_dob.get(),
                                                                                                                                                              self.var_gen.get(),
                                                                                                                                                              self.var_address.get(),
                                                                                                                                                              self.var_nati.get(),
                                                                                                                                                              self.var_phone.get(),
                                                                                                                                                              self.var_reli.get(),
                                                                                                                                                              self.var_field.get(),
                                                                                                                                                              self.var_rad.get(),
                                                                                                                                                              self.var_id.get()
                                                                                                                                                              ))
                conn.commit()
                self.get_data
                self.reset_data
                conn.close()
                face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

                def face_crop(img):
                    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                    face = face_classifier.detectMultiScale(gray,1.3,5)
                    for (x,y,w,h) in face:
                        face_crop = img[y:y+h,x:x+w]
                        return face_crop
                cap = cv2.VideoCapture(0)
                img_id = 0
                while True:
                    ret,myframe = cap.read()
                    if face_crop(myframe) is not None:
                        img_id +=1
                        faces = cv2.resize(face_crop(myframe),(450,450))
                        faces = cv2.cvtColor(faces,cv2.COLOR_BGR2GRAY)
                        file_path = "photos/user."+str(idd)+"."+str(img_id)+".jpg"
                        cv2.imwrite(file_path,faces)
                        cv2.putText(faces,str(img_id),(50,50),cv2.FONT_HERSHEY_COMPLEX,2,(0,255,0),2)
                        cv2.imshow("Face detection",faces)
                    if cv2.waitKey(1)==13 or int(img_id)==30:
                        break
                cap.release()
                cv2.destroyAllWindows()
                messagebox.showinfo("Photo","Generating Photo datasets completed!!!! ")
            except Exception as es:
                messagebox.showerror("Error!",f"Due to: {str(es)}",parent=self.root)
                    
                                                                                                                                                                 

        






if __name__ == "__main__":
    root=Tk()
    obj = Details(root)
    root.mainloop()