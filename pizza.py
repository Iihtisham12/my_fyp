from tkinter import *
from PIL import Image,ImageTk            #install pillow liabrary
from tkinter import messagebox
import sqlite3 as sq
from tkinter import ttk
from time import strftime
from docxtpl import DocxTemplate          #first install this liabrary
import datetime


cartitem =[]

class Login():

    
    # this function will show password in the password entry box
    def showpassword(self):
        if(self.root.pwd_chk.get()==1):
            self.root.entry_password.config(show="")
        else:
            self.root.entry_password.config(show="*")
    #end of show password function

    def login(self):
        if self.root.entry_username.get()=="" or self.root.entry_password.get()=="":
            messagebox.showerror("Error","All field are required",parent=self.root)
        else:
            try:
                self.root.username = self.root.entry_username.get()
                self.root.password =  self.root.entry_password.get()
                self.root.conn =sq.connect("DataBase/food_delivery.db")
                self.root.cursor = self.root.conn.cursor()
                self.root.cursor.execute("SELECT * FROM users where username=? and password =?",(self.root.username,self.root.password))
                self.root.rows = self.root.cursor.fetchone()
                if self.root.rows == None:

                    messagebox.showerror("Login Failed","Invalid credentials",parent=self.root)
                    self.root.entry_username.focus_set()
                else:
                    
                    self.root.destroy()
                    self.db_win =Tk()
                    self.obj = Dashboard(self.db_win)
                    self.obj.clock()
                    self.db_win.mainloop()
            

            except Exception as es:  
                print(f"Error is due to {es}")
            finally:
             self.root.conn.commit()
             self.root.conn.close()


                
       
    def register(self):
        self.root.destroy()
        self.reg_win =Tk()
        self.reg_obj =Registration(self.reg_win)
        self.reg_win.mainloop()

    #=========== Constructer of the class Lofin===============================================================
    def __init__(self,root):
        self.root = root
        self.root.title("Login form ")
        self.root.screen_width = self.root.winfo_screenwidth()
        self.root.screen_height =self.root.winfo_screenwidth()
        self.root.width = 400  # Width
        self.root.height = 500  # Height
        self.root.screen_width = self.root.winfo_screenwidth()        # Width of the screen
        self.root.screen_height = self.root.winfo_screenheight()      # Height of the screen
        # Calculate Starting X and Y coordinates for Window
        self.root.x = (self.root.screen_width / 2) - (self.root.width / 2)
        self.root.y = (self.root.screen_height / 2) - (self.root.height / 2)
        self.root.iconbitmap('icons/login.ico')
        self.root.geometry(f"{self.root.width}x{self.root.height}+{int(self.root.x)}+{int(self.root.y)}")
        self.root.resizable(False,False)
        #====================================================================================


        # Open login image 

        self.root.login_image =Image.open('icons/login.png')

       # resizing login image
        self.root.resized_login_image = self.root.login_image.resize((150,150),Image.ANTIALIAS)

        self.root.new_image = ImageTk.PhotoImage(self.root.resized_login_image)
      # creating label for resize_login_image

        self.root.login_image_label = Label(self.root,image=self.root.new_image ,text="Login Form",font=('Comic Sans',18,'bold'),compound="top",fg="orangered").place(x=120)

      # now creating  entry and lables for username and password
        self.root.username_lbl =Label(self.root,text="Username",font=("comicsans",12) ,fg="dodgerblue4").place(x=50,y=230)

        self.root.password_lbl =Label(self.root,text="Password",font=("comicsans",12),fg="dodgerblue4").place(x=50,y=300)
        self.root.entry_username = Entry(self.root,width=35,font=("comicsans",12))
        self.root.entry_username.focus_set()
        self.root.entry_username.place(x=50,y=250)

        self.root.pwd_value = StringVar()

        self.root.pwd_chk=IntVar(value=0)
      
        self.root.entry_password = Entry(self.root,width=35,show="*" ,textvariable=self.root.pwd_value,font=('comicsans',12))
        self.root.entry_password.place(x=50,y=320)





        #creating check boxes here
        self.root.show_pwd_chk=Checkbutton(self.root,text="Show password",command=self.showpassword,variable=self.root.pwd_chk,onvalue=1,offvalue=0,fg="dodgerblue4").place(x=50,y=360)
        

        # creating button here
        self.root.btn_font ="arial 22"
        self.root.login_btn = Button(self.root,text="Login",width=25,command=self.login,bg="limegreen").place(x=50,y=390)
        self.root.register_btn = Button(self.root,text="Register",width=20,command=self.register,bg="yellow").place(x=240,y=390,)

        # creating developer label here
        self.root.developer_lbl =Label(self.root,text="Developed By Team I Y I",font=("comicsans",14),fg="orangered").place(x=50,y=450)

class Registration():
   
    def clearfield(self):
        self.root.username_entry.delete(0,'end')
        self.root.email_entry.delete(0,'end')
        self.root.password_entry.delete(0,'end')
        self.root.confirm_password_entry.delete(0,'end')
        self.root.fullname_entry.delete(0,'end')

    def inserdata(self):
        self.root.username_entry.focus_set()
        if self.root.username_entry.get()=="" or self.root.email_entry.get()=="" or self.root.password_entry.get()=="" or self.root.confirm_password_entry.get()=="" or self.root.fullname_entry.get()=="":   
            messagebox.showerror("Error","All field are required",parent=self.root)
        elif self.root.password_entry.get()!=self.root.confirm_password_entry.get():
            messagebox.showerror("Password MissMatch","Password does not match",parent=self.root)
        else:
           
            try:
                self.root.username = self.root.username_entry.get()
                self.root.email =  self.root.email_entry.get()
                self.root.password =  self.root.password_entry.get()
                self.root.confirm_password =  self.root.confirm_password_entry.get()
                self.root.fullname =  self.root.fullname_entry.get()
                self.root.conn =sq.connect("DataBase/food_delivery.db")
                self.root.cursor = self.root.conn.cursor()

                insert_query ="INSERT INTO users(username,password,email,fullname) VALUES(?,?, ?, ?)"
                data = (self.root.username,self.root.password,self.root.email,self.root.fullname)
                inserted=self.root.cursor.execute(insert_query,data) 
                self.root.conn.commit() 
                if inserted:
                    messagebox.showinfo("Insertion Successelfull","Data has been inserted successelfully",parent=self.root)
                    self.clearfield()
                    self.loginform()
                else:
                    messagebox.showerror("Insertion failed","Data insertion failed!",parent=self.root)
            except Exception as es: 
                messagebox.showerror("Error",f"{es}",parent=self.root)
            finally:
                self.root.conn.close()
            
       


    def loginform(self):
        self.root.destroy()
        self.root.win=Tk()
        self.root.obj =Login(self.root.win)
        self.root.win.mainloop()
    def __init__(self,root):

        self.root = root
        
        self.root.fonts="Calibri 12"
        self.root.screen_width = self.root.winfo_screenwidth()
        self.root.screen_height = self.root.winfo_screenwidth()
        self.root.width = 500  # Width
        self.root.height = 400 # Height

        self.root.screen_width = self.root.winfo_screenwidth()  # Width of the screen
        self.root.screen_height = self.root.winfo_screenheight()  # Height of the screen

        # Calculate Starting X and Y coordinates for Window
        self.root.x = (self.root.screen_width / 2) - (self.root.width / 2)
        self.root.y = (self.root.screen_height / 2) - (self.root.height / 2)
        self.root.iconbitmap('icons/login.ico')
        self.root.geometry(f"{self.root.width}x{self.root.height}+{int(self.root.x)}+{int(self.root.y)}")
        self.root.title("Registration Form")

        self.root.resizable(False, False)

        # creating all label

        self.root.registration_lbl = Label(self.root, text="Registration Form",fg="darkorange" ,font=("Arial", 26, 'bold'))
        self.root.registration_lbl.place(x=180, y=20)
        self.root.username_lbl = Label(self.root, text="User Name:",fg="cyan2" , font=("Arial", 12))
        self.root.username_lbl.place(x=30, y=90)
        self.root.email_lbl = Label(self.root, text="Email:",fg="cyan2" , font=("Arial", 12))
        self.root.email_lbl.place(x=30, y=130)

        self.root.password_lbl = Label(self.root, text="Password:",fg="cyan2" , font=("Arial", 12))

        self.root.password_lbl.place(x=30, y=170)
        self.root.confirmpwd_lbl = Label(self.root, text="Confirm Password:",fg="cyan2" , font=("Arial", 12))

        self.root.confirmpwd_lbl.place(x=30, y=210)
        self.root.fullname_lbl = Label(self.root, text="Full Name:",fg="cyan2" , font=("Arial", 12))

        self.root.fullname_lbl.place(x=30, y=250)

        # creating entries

        self.root.username_entry = Entry(self.root, width=38,font=self.root.fonts,bg="springgreen",bd=2,relief=SUNKEN)
        self.root.username_entry.place(x=180, y=90)
        self.root.email_entry = Entry(self.root, width=38,font=self.root.fonts,bg="springgreen",bd=2,relief=SUNKEN)
        self.root.email_entry.place(x=180, y=130)
        self.root.password_entry = Entry(self.root, width=38,font=self.root.fonts,bg="springgreen",bd=2,relief=SUNKEN)
        self.root.password_entry.place(x=180, y=170)

        self.root.confirm_password_entry = Entry(self.root, width=38,font=self.root.fonts,bg="springgreen",bd=2,relief=SUNKEN)
        self.root.confirm_password_entry.place(x=180, y=210)

        self.root.fullname_entry = Entry(self.root, width=38,font=self.root.fonts,bg="springgreen",bd=2,relief=SUNKEN)
        self.root.fullname_entry.place(x=180, y=250)
        # creating buttons

        self.root.signup_btn = Button(self.root, width=20, text="Sign Up",command=self.inserdata,bg="limegreen")
        self.root.signup_btn.place(x=180, y=300)
        self.root.reset_btn = Button(self.root, width=20, text="Reset",command=self.clearfield,bg="gold")
        self.root.reset_btn.place(x=340, y=300)
        self.root.logi_btn = Button(self.root, text="Alread have an Account",command=self.loginform,bg="deepskyblue",width=20)
        self.root.logi_btn.place(x=340, y=340)

class Dashboard():
    def logout(self):
        
        self.root.destroy()
        self.root.win = Tk()
        self.root.obj=Login(self.root.win)
        self.root.mainloop()

    def clock(self):
        self.time=strftime("%I:%M:%S:%p")
        self.day = strftime("%A")
        self.date = strftime("%d-%m-%Y")
        self.root.time_lbl.config(text=self.time)
        self.root.day_lbl.config(text=self.day)
        self.root.date_lbl.config(text=self.date)
        self.root.time.after(1000,self.clock)

    def vegpizza(self):

      
        self.root.destroy()
        self.db_win =Tk()
        self.obj = Vegpizza(self.db_win)
        self.obj.clock()
        self.db_win.mainloop()

    def nonvegpizza(self):
      
        self.root.destroy()
        self.db_win =Tk()
        self.obj =NonVegpizza(self.db_win)
        self.obj.clock()
        self.db_win.mainloop()
    
    def specialchicken(self):
       
        self.root.destroy()
        self.db_win =Tk()
        self.obj = SpecialChicken(self.db_win)
        self.obj.clock()
        self.db_win.mainloop()
    
    def colddrinks(self):
    
        self.root.destroy()
        self.db_win =Tk()
        self.obj = Colddrinks(self.db_win)
        self.obj.clock()
        self.db_win.mainloop()





    def __init__(self,root):
        self.root = root
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenwidth()
        self.width = 1366  # Width
        self.height = 768  # Height
        
        self.screen_width = self.root.winfo_screenwidth()  # Width of the screen
        self.screen_height = self.root.winfo_screenheight()  # Height of the screen

        # Calculate Starting X and Y coordinates for Window
        self.x = (self.screen_width / 2) - (self.width / 2)
        self.y = (self.screen_height / 2) - (self.height / 2)




        self.root.iconbitmap('icons/login.ico')
        self.root.geometry(f"{self.width}x{self.height}+{int(self.x)}+{int(self.y)}")
        self.root.title("DashBoard Form")
        self.root.state('zoomed')
        self.root.resizable(False,False)
        #creating frame and labels
        self.root.top_frame = Frame(self.root,width =1366,bg="darkorange",height=180,borderwidth =5,relief =SUNKEN,pady=10)
        self.root.top_frame.place(x=0,y=0)
        self.root.top_lable=Label(self.root.top_frame,text="Online Pizza Delivery Mangement System",font=("Arial ",24,"bold"),bg="darkorange",fg="white")
        self.root.top_lable.place(x=20,y=50)
        self.root.time=Label(self.root.top_frame,text="Time",font=("Arial",22,"bold"),bg="darkorange",fg="white")
        self.root.time.place(x=1050,y=50)
        self.root.time_lbl = Label(self.root.top_frame,text="00:00:00 AM",font=("Arial ",22,"bold"),background="darkorange",fg="white")
        self.root.time_lbl.place(x=1150,y=50)
        self.root.day_lbl = Label(self.root.top_frame,text="Day",font=("Arial ",22,"bold"),background="darkorange",fg="white")
        self.root.day_lbl.place(x=1150,y=0)

        self.root.date_lbl = Label(self.root.top_frame,text="Date",font=("Arial ",22,"bold"),background="darkorange",fg="white")
        self.root.date_lbl.place(x=1150,y=100)


        #=========== Labels for Pizza images===========================
        self.root.inner_frame = Frame(self.root,width =1200,height=350,bg="red",borderwidth =5,relief =SUNKEN,pady=10)
        self.root.inner_frame.place(x=100,y=250)
        

        self.root.vegpizza_image = Image.open('icons/veg.png')
        self.root.vp_resize = self.root.vegpizza_image.resize((250,200))
        self.root.vp_new_img =ImageTk.PhotoImage(self.root.vp_resize)
        self.root.vegpizza_btn =Button(self.root.inner_frame,font=("Arial",22),image=self.root.vp_new_img,text="Veg Pizza",cursor="hand2",compound="top",command=self.vegpizza)
        self.root.vegpizza_btn.place(x=20,y=20)
        


        self.root.non_vegpizza_image = Image.open('icons/Non.png')
        self.root.p_resize = self.root.non_vegpizza_image.resize((250,200))
        self.root.p_new_img =ImageTk.PhotoImage(self.root.p_resize)
        self.root.nonveg_btn =Button(self.root.inner_frame,font=("Arial",22),image=self.root.p_new_img,text="Non Veg Pizza",cursor="hand2",compound="top",command=self.nonvegpizza)
        self.root.nonveg_btn.place(x=320,y=20)


        self.root.specialchicken_image = Image.open('icons/chiken.png')
        self.root.spc_resize = self.root.specialchicken_image.resize((250,200))
        self.root.spc_new_img =ImageTk.PhotoImage(self.root.spc_resize)
        self.root.spc_btn =Button(self.root.inner_frame,font=("Arial",22),image=self.root.spc_new_img,text="Special Chicken",cursor="hand2",compound="top",command=self.specialchicken)
        self.root.spc_btn.place(x=620,y=20) 

        self.root.colddrink_image = Image.open('icons/extra.png')
        self.root.cd_resize = self.root.colddrink_image.resize((250,200))
        self.root.cd_new_img =ImageTk.PhotoImage(self.root.cd_resize)
        self.root.cd_btn =Button(self.root.inner_frame,font=("Arial",22),image=self.root.cd_new_img,text="Cold Drinks",cursor="hand2",compound="top",command=self.colddrinks)
        self.root.cd_btn.place(x=920,y=20) 
        self.root.logout_btn = Button(self.root,text="LogOut",width=15,height=1,bg="red" ,fg="white",font=("arial black",12,"bold"),command=self.logout)
        self.root.logout_btn.place(x=1120,y=200)

class Vegpizza():
    
    def confirm_order(self):
        self.root.destroy()
        self.win = Tk()
        self.obj=OrderDetails(self.win)
        self.win.mainloop()
    
    def addmore(self):

        self.root.destroy()
        self.win=Tk()
        self.obj=Dashboard(self.win)
    
        self.obj.clock()
        self.win.mainloop()
        
    
    def sum_of_total(self,item=""):
        self.root.sum_of_total =0
        for row in self.root.table.get_children(item) :
            self.root.sum_of_total=self.root.sum_of_total+self.root.table.item(row)['values'][4]
        

    def logout(self):
        
        self.root.destroy()
        self.root.win = Tk()
        self.root.obj=Login(self.root.win)
        self.root.mainloop()
    def add_delex(self):
        if self.root.sb1.get()==0:
            messagebox.showerror("Error","Please select quantity to add")
        elif self.root.v1.get()==0:
            messagebox.showerror("Error","Please select size")
        else:
            self.item_name ="Delux Veggie"
            self.size=""
            self.quantity = int(self.root.sb1.get())
            self.price =0
           
            if self.root.v1.get()==20:
                global size
                global price
                self.size="Larg"
                self.price =650
              

            elif self.root.v1.get()==10:
                
                self.size ="Meduim"
                self.price=450
            else:
                
                self.size="Regular"
                self.price =250
            self.total = self.quantity * self.price
            invoice_list=[self.item_name,self.size,self.quantity,self.price,self.total]
            self.root.table.insert('',0,values =invoice_list)
            cartitem.append(invoice_list)
            self.subtotal = sum(item[4]for item in cartitem)
            self.root.sub_total_lbl =Label(self.root,text="Your Total Bill:"+str(self.subtotal),font=("cooper black",22,"bold"),bg="limegreen")
            self.root.sub_total_lbl.place(x=900,y=700)
            
            
    #==================================================================

    def add_veg_vegenza(self):
        if self.root.sb2.get()==0:
            messagebox.showerror("Error","Please select quantity to add")
        elif self.root.v2.get()==0:
            messagebox.showerror("Error","Please select size")
        else:
            self.item_name ="Veg Vegenza"
            self.size=""
            self.quantity = int(self.root.sb2.get())
            self.price =0
           
            if self.root.v2.get()==20:
                global size
                global price
                self.size="Larg"
                self.price =600
              

            elif self.root.v2.get()==10:
                
                self.size ="Meduim"
                self.price=400
            else:
                
                self.size="Regular"
                self.price =250
            self.total = self.quantity * self.price
            invoice_list=[self.item_name,self.size,self.quantity,self.price,self.total]
            self.root.table.insert('',0,values =invoice_list)
            cartitem.append(invoice_list)
            self.subtotal = sum(item[4]for item in cartitem)
            self.root.sub_total_lbl =Label(self.root,text="Your Total Bill:"+str(self.subtotal),font=("cooper black",22,"bold"),bg="limegreen")
            self.root.sub_total_lbl.place(x=900,y=700)

            
   
      #=====================================================================================================

    def add_pepper5(self):
        if self.root.sb3.get()==0:
            messagebox.showerror("Error","Please select quantity to add")
        elif self.root.v3.get()==0:
            messagebox.showerror("Error","Please select size")
        else:
            self.item_name ="5 Pepper Pizza"
            self.size=""
            self.quantity = int(self.root.sb3.get())
            self.price =0
           
            if self.root.v3.get()==20:
                global size
                global price
                self.size="Larg"
                self.price =550
              

            elif self.root.v3.get()==10:
                
                self.size ="Meduim"
                self.price=385
            else:
                
                self.size="Regular"
                self.price =225
            self.total = self.quantity * self.price
            invoice_list=[self.item_name,self.size,self.quantity,self.price,self.total]
            self.root.table.insert('',0,values =invoice_list)
            cartitem.append(invoice_list)
            self.subtotal = sum(item[4]for item in cartitem)
            self.root.sub_total_lbl =Label(self.root,text="Your Total Bill:"+str(self.subtotal),font=("cooper black",22,"bold"),bg="limegreen")
            self.root.sub_total_lbl.place(x=900,y=700)
            






    def clock(self):
        self.time=strftime("%I:%M:%S:%p")
        self.day = strftime("%A")
        self.date = strftime("%d-%m-%Y")
        self.root.time_lbl.config(text=self.time)
        self.root.day_lbl.config(text=self.day)
        self.root.date_lbl.config(text=self.date)
        self.root.time.after(1000,self.clock)

        


    def __init__(self,root):
        
        self.root = root
        root.overrideredirect(1)
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenwidth()
        self.width = 1366  # Width
        self.height = 768  # Height
    
        self.screen_width = self.root.winfo_screenwidth()  # Width of the screen
        self.screen_height = self.root.winfo_screenheight()  # Height of the screen

        # Calculate Starting X and Y coordinates for Window
        self.x = (self.screen_width / 2) - (self.width / 2)
        self.y = (self.screen_height / 2) - (self.height / 2)




        self.root.iconbitmap('icons/login.ico')
        self.root.geometry(f"{self.width}x{self.height}+{int(self.x)}+{int(self.y)}")
        self.root.title("Veg Pizza Form")
        self.root.state('zoomed')
        self.root.resizable(False,False)
        #creating frame and labels
        self.root.top_frame = Frame(self.root,width =1366,bg="darkorange",height=180,borderwidth =5,relief =SUNKEN,pady=10)
        self.root.top_frame.place(x=0,y=0)
        self.root.top_lable=Label(self.root.top_frame,text="Online Pizza Delivery Mangement System",font=("Arial ",24,"bold"),bg="darkorange",fg="white")
        self.root.top_lable.place(x=20,y=50)
        self.root.time=Label(self.root.top_frame,text="Time",font=("Arial",22,"bold"),bg="darkorange",fg="white")
        self.root.time.place(x=1050,y=50)
        self.root.time_lbl = Label(self.root.top_frame,text="00:00:00 AM",font=("Arial ",22,"bold"),background="darkorange",fg="white")
        self.root.time_lbl.place(x=1150,y=50)
        self.root.day_lbl = Label(self.root.top_frame,text="Day",font=("Arial ",22,"bold"),background="darkorange",fg="white")
        self.root.day_lbl.place(x=1150,y=0)

        self.root.date_lbl = Label(self.root.top_frame,text="Date",font=("Arial ",22,"bold"),background="darkorange",fg="white")
        self.root.date_lbl.place(x=1150,y=100)


        #=========== Labels for Pizza images===========================
        self.root.inner_frame = Frame(self.root,width =1366,height=1600,bg="red",borderwidth =5,relief =SUNKEN,pady=10)
        self.root.inner_frame.place(x=100,y=250)
        self.root.c=Canvas(self.root.inner_frame,height=400,width=1200)
        self.root.c.pack()
       #================ Delux pizza ====================================
        self.root.c.create_rectangle(20, 10, 550, 130,width=2,fill="#aae2d7")
        self.delu=PhotoImage(file="icons/deluxe.png")
        self.root.c.create_image(80,70,image=self.delu)
        self.root.c.create_text(250,40,text="Deluxe Veggie",fill="#000000",font=("Cooper Black",20))
        self.root.c.create_text(450,40,text="Rs.450/Rs.650/Rs.250",fill="#ff3838",font=("default",14,'bold'))
        self.root.v1=IntVar()
        self.root.sb1=IntVar()
        self.root.med1=Radiobutton(self.root.inner_frame,text = "Medium",value=10,variable=self.root.v1)
        self.root.med1.place(x=155,y=70)
        self.root.larg1 = Radiobutton(self.root.inner_frame, text = "Large",value = 20, variable =self.root.v1)
        self.root.larg1.place(x=255,y=70)
        self.root.reg1 = Radiobutton(self.root.inner_frame, text = "Regular",value = 30, variable =self.root.v1)
        self.root.reg1.place(x=355,y=70)
        self.root.c.create_text(190,110,text="Quantity : ",fill="#000000",font=("default",12))
        self.root.qty1=Spinbox(self.root.inner_frame,from_=0 ,to=1000,bg="#0b1335",fg="white",font=("arial",13,"bold"),textvariable=self.root.sb1)
        self.root.qty1.place(x=225,y=100)
        self.root.add1=Button(self.root.inner_frame,text="Add to Cart",bg="#0b1335",cursor="hand2",fg="white",bd=4,font=("default",12,'bold'),command=self.add_delex)
        self.root.add1.place(x=440,y=70)
        #==========veg vegganza ====================================================
        self.root.c.create_rectangle(20, 130, 550, 260,width=2,fill="#aae2d7")
        self.vag=PhotoImage(file="icons/extravaganza.png")
        self.root.c.create_image(80,190,image=self.vag)
        self.root.c.create_text(250,150,text="Veg Vaganza",fill="#000000",font=("Cooper Black",20))
        self.root.c.create_text(450,150,text="Rs.400/Rs.600/Rs.250",fill="#ff3838",font=("default",14,'bold'))  
        self.root.v2=IntVar()
        self.root.sb2=IntVar()
        self.root.med2=Radiobutton(self.root.inner_frame,text = "Medium",value=10,variable=self.root.v2)
        self.root.med2.place(x=155,y=180)
        self.root.larg2 = Radiobutton(self.root.inner_frame, text = "Large",value = 20,variable=self.root.v2)
        self.root.larg2.place(x=255,y=180)
        self.root.reg2 = Radiobutton(self.root.inner_frame, text = "Regular",value = 30, variable=self.root.v2)
        self.root.reg2.place(x=355,y=180)
        self.root.c.create_text(190,230,text="Quantity : ",fill="#000000",font=("default",12))
        self.root.qty2=Spinbox(self.root.inner_frame,textvariable=self.root.sb2,from_=0 ,to=1000,bg="#0b1335",fg="white",font=("arial",11,"bold"))
        self.root.qty2.place(x=225,y=220)
        self.root.add2=Button(self.root.inner_frame,text="Add to cart",bg="#0b1335",cursor="hand2",fg="white",bd=4,font=("default",12,'bold'),command=self.add_veg_vegenza)
        self.root.add2.place(x=440,y=200)


        self.root.c.create_rectangle(20, 260, 550, 390,width=2,fill="#aae2d7")
        self.root.pep=PhotoImage(file="icons/5-pepper-veg-pizza.png")
        self.root.c.create_image(80,320,image=self.root.pep)
        self.root.c.create_text(250,290,text="5 Pepper",fill="#000000",font=("Cooper Black",20))
        self.root.c.create_text(450,290,text="Rs.385/Rs.550/Rs.225",fill="#ff3838",font=("default",14,'bold'))
        self.root.v3=IntVar()
        self.root.sb3=IntVar()
        self.med3=Radiobutton(self.root.inner_frame,text = "Medium",value=10,variable=self.root.v3)
        self.med3.place(x=155,y=315)
        self.larg3 = Radiobutton(self.root.inner_frame, text = "Large",value = 20,variable=self.root.v3)
        self.larg3.place(x=255,y=315)
        self.reg3 = Radiobutton(self.root.inner_frame, text = "Regular",value = 30,variable=self.root.v3 )
        self.reg3.place(x=355,y=315)


        self.root.c.create_text(190,360,text="Quantity : ",fill="#000000",font=("default",12))
        self.root.qty3=Spinbox(self.root.inner_frame,from_=0 ,to=1000,bg="#0b1335",fg="white",font=("arial",11,"bold"),textvariable=self.root.sb3)
        self.root.qty3.place(x=225,y=350)

        self.root.add3=Button(self.root.inner_frame,text="Add to Cart",bg="#0b1335",cursor="hand2",fg="white",bd=4,font=("default",12,'bold'),command=self.add_pepper5)
        self.root.add3.place(x=440,y=340)

      
     
      #================== Table ======================================================
        self.root.columns=('item','size','qty','price','total')
        self.root.table = ttk.Treeview(self.root.inner_frame,columns=self.root.columns,show="headings",height=19)
        self.root.table.place(x=550,y=10)
        self.root.style= ttk.Style()

        self.root.style.configure('Treeview.Heading',font=('arial',12,"bold"))
        self.root.style.configure("Treeview",font=('comicsans',12))
        self.root.table.heading('item',text="Items Name",anchor=CENTER,)
        self.root.table.heading('size',text="Size",anchor=CENTER)
        self.root.table.heading('qty',text="Quantity",anchor=CENTER)
        self.root.table.heading('price',text="Price",anchor=CENTER)
        self.root.table.heading('total',text="Total",anchor=CENTER)
        self.root.table.column('item',width=200,anchor=CENTER)
        self.root.table.column('size',width=120,anchor=CENTER)
        self.root.table.column('qty',width=100,anchor=CENTER)
        self.root.table.column('price',width=100,anchor=CENTER)
        self.root.table.column('total',width=120,anchor=CENTER)
        
        
    

      
        #==================== Button====================================================

        self.root.logout_btn = Button(self.root,text="LogOut",width=15,height=1,bg="red" ,fg="white",font=("arial black",12,"bold"),command=self.logout)
        self.root.logout_btn.place(x=1140,y=200)
        self.root.addmore=Button(self.root,text="Add more",command=self.addmore,width=15,height=1,bg="limegreen",fg="white",font=("arial black",12,"bold"))
        self.root.addmore.place(x=750,y=200)
        self.root.confirm_order = Button(self.root,text="Confirm Order",command=self.confirm_order,width=15,height=1,bg="blue",fg="white",font=("arial black",12,"bold"))
        self.root.confirm_order.place(x=950,y=200)
        
class NonVegpizza():
    
    def confirm_order(self):
        self.root.destroy()
        self.win = Tk()
        self.obj=OrderDetails(self.win)
        self.win.mainloop()
    def addmore(self):

        self.root.destroy()
        self.win=Tk()
        self.obj=Dashboard(self.win)
        self.obj.clock()
        self.win.mainloop()
        
    
    def sum_of_total(self,item=""):
        self.root.sum_of_total =0
        for row in self.root.table.get_children(item) :
            self.root.sum_of_total=self.root.sum_of_total+self.root.table.item(row)['values'][4]
        

    def logout(self):
       
        self.root.destroy()
        self.root.win = Tk()
        self.root.obj=Login(self.root.win)
        self.root.mainloop()
    def add_non_veg_supreme(self):
        if self.root.sb1.get()==0:
            messagebox.showerror("Error","Please select quantity to add")
        elif self.root.v1.get()==0:
            messagebox.showerror("Error","Please select size")
        else:
            self.item_name ="Non Veg supreme"
            self.size=""
            self.quantity = int(self.root.sb1.get())
            self.price =0
           
            if self.root.v1.get()==20:
                global size
                global price
                self.size="Larg"
                self.price =650
              

            elif self.root.v1.get()==10:
                
                self.size ="Meduim"
                self.price=450
            else:
                
                self.size="Regular"
                self.price =250
            self.total = self.quantity * self.price
            invoice_list=[self.item_name,self.size,self.quantity,self.price,self.total]
            self.root.table.insert('',0,values =invoice_list)
            cartitem.append(invoice_list)
            self.subtotal = sum(item[4]for item in cartitem)
            self.root.sub_total_lbl =Label(self.root,text="Your Total Bill:"+str(self.subtotal),font=("cooper black",22,"bold"),bg="limegreen")
            self.root.sub_total_lbl.place(x=900,y=700)
            
            
    #==================================================================

    def add_chicken_tikka(self):
        if self.root.sb2.get()==0:
            messagebox.showerror("Error","Please select quantity to add")
        elif self.root.v2.get()==0:
            messagebox.showerror("Error","Please select size")
        else:
            self.item_name ="Chicken Tikka"
            self.size=""
            self.quantity = int(self.root.sb2.get())
            self.price =0
           
            if self.root.v2.get()==20:
                global size
                global price
                self.size="Larg"
                self.price =600
              

            elif self.root.v2.get()==10:
                
                self.size ="Meduim"
                self.price=400
            else:
                
                self.size="Regular"
                self.price =250
            self.total = self.quantity * self.price
            invoice_list=[self.item_name,self.size,self.quantity,self.price,self.total]
            self.root.table.insert('',0,values =invoice_list)
            cartitem.append(invoice_list)
            self.subtotal = sum(item[4]for item in cartitem)
            self.root.sub_total_lbl =Label(self.root,text="Your Total Bill:"+str(self.subtotal),font=("cooper black",22,"bold"),bg="limegreen")
            self.root.sub_total_lbl.place(x=900,y=700)
            
   
      #=====================================================================================================

    def add_chicken_sausage(self):
        if self.root.sb3.get()==0:
            messagebox.showerror("Error","Please select quantity to add")
        elif self.root.v3.get()==0:
            messagebox.showerror("Error","Please select size")
        else:
            self.item_name ="Chicken Sausage"
            self.size=""
            self.quantity = int(self.root.sb3.get())
            self.price =0
           
            if self.root.v3.get()==20:
                global size
                global price
                self.size="Larg"
                self.price =550
              

            elif self.root.v3.get()==10:
                
                self.size ="Meduim"
                self.price=385
            else:
                
                self.size="Regular"
                self.price =225
            self.total = self.quantity * self.price
            invoice_list=[self.item_name,self.size,self.quantity,self.price,self.total]
            self.root.table.insert('',0,values =invoice_list)
            cartitem.append(invoice_list)
            self.subtotal = sum(item[4]for item in cartitem)
            self.root.sub_total_lbl =Label(self.root,text="Your Total Bill:"+str(self.subtotal),font=("cooper black",22,"bold"),bg="limegreen")
            self.root.sub_total_lbl.place(x=900,y=700)
            
        






    def clock(self):
        self.time=strftime("%I:%M:%S:%p")
        self.day = strftime("%A")
        self.date = strftime("%d-%m-%Y")
        self.root.time_lbl.config(text=self.time)
        self.root.day_lbl.config(text=self.day)
        self.root.date_lbl.config(text=self.date)
        self.root.time.after(1000,self.clock)

        


    def __init__(self,root):
        
        self.root = root
       # root.overrideredirect(1)
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenwidth()
        self.width = 1366  # Width
        self.height = 768  # Height
    
        self.screen_width = self.root.winfo_screenwidth()  # Width of the screen
        self.screen_height = self.root.winfo_screenheight()  # Height of the screen

        # Calculate Starting X and Y coordinates for Window
        self.x = (self.screen_width / 2) - (self.width / 2)
        self.y = (self.screen_height / 2) - (self.height / 2)




        self.root.iconbitmap('icons/login.ico')
        self.root.geometry(f"{self.width}x{self.height}+{int(self.x)}+{int(self.y)}")
        self.root.title("Non Veg Pizza Form")
        self.root.state('zoomed')
        self.root.resizable(False,False)
        #creating frame and labels
        self.root.top_frame = Frame(self.root,width =1366,bg="darkorange",height=180,borderwidth =5,relief =SUNKEN,pady=10)
        self.root.top_frame.place(x=0,y=0)
        self.root.top_lable=Label(self.root.top_frame,text="Online Pizza Delivery Mangement System",font=("Arial ",24,"bold"),bg="darkorange",fg="white")
        self.root.top_lable.place(x=20,y=50)
        self.root.time=Label(self.root.top_frame,text="Time",font=("Arial",22,"bold"),bg="darkorange",fg="white")
        self.root.time.place(x=1050,y=50)
        self.root.time_lbl = Label(self.root.top_frame,text="00:00:00 AM",font=("Arial ",22,"bold"),background="darkorange",fg="white")
        self.root.time_lbl.place(x=1150,y=50)
        self.root.day_lbl = Label(self.root.top_frame,text="Day",font=("Arial ",22,"bold"),background="darkorange",fg="white")
        self.root.day_lbl.place(x=1150,y=0)

        self.root.date_lbl = Label(self.root.top_frame,text="Date",font=("Arial ",22,"bold"),background="darkorange",fg="white")
        self.root.date_lbl.place(x=1150,y=100)


        #=========== Labels for Pizza images===========================
        self.root.inner_frame = Frame(self.root,width =1366,height=1600,bg="red",borderwidth =5,relief =SUNKEN,pady=10)
        self.root.inner_frame.place(x=100,y=250)
        self.root.c=Canvas(self.root.inner_frame,height=400,width=1200)
        self.root.c.pack()
       #================ Non veg supreme pizza ====================================
        self.root.c.create_rectangle(20, 10, 550, 130,width=2,fill="#aae2d7")
        self.delu=PhotoImage(file="icons/Non-Veg_Supreme.png")
        self.root.c.create_image(80,70,image=self.delu)
        self.root.c.create_text(250,40,text="Non veg Supreme",fill="#000000",font=("Cooper Black",16))
        self.root.c.create_text(450,40,text="Rs.450/Rs.650/Rs.250",fill="#ff3838",font=("default",14,'bold'))
        self.root.v1=IntVar()
        self.root.sb1=IntVar()
        self.root.med1=Radiobutton(self.root.inner_frame,text = "Medium",value=10,variable=self.root.v1)
        self.root.med1.place(x=155,y=70)
        self.root.larg1 = Radiobutton(self.root.inner_frame, text = "Large",value = 20, variable =self.root.v1)
        self.root.larg1.place(x=255,y=70)
        self.root.reg1 = Radiobutton(self.root.inner_frame, text = "Regular",value = 30, variable =self.root.v1)
        self.root.reg1.place(x=355,y=70)
        self.root.c.create_text(190,110,text="Quantity : ",fill="#000000",font=("default",12))
        self.root.qty1=Spinbox(self.root.inner_frame,from_=0 ,to=1000,bg="#0b1335",fg="white",font=("arial",13,"bold"),textvariable=self.root.sb1)
        self.root.qty1.place(x=225,y=100)
        self.root.add1=Button(self.root.inner_frame,text="Add to Cart",bg="#0b1335",cursor="hand2",fg="white",bd=4,font=("default",12,'bold'),command=self.add_non_veg_supreme)
        self.root.add1.place(x=440,y=70)
        #========== Chicken tikka ====================================================
        self.root.c.create_rectangle(20, 130, 550, 260,width=2,fill="#aae2d7")
        self.vag=PhotoImage(file="icons/nonChicken_Tikka.png")
        self.root.c.create_image(80,190,image=self.vag)
        self.root.c.create_text(250,150,text="Chicken Tikka",fill="#000000",font=("Cooper Black",16))
        self.root.c.create_text(450,150,text="Rs.400/Rs.600/Rs.250",fill="#ff3838",font=("default",14,'bold'))  
        self.root.v2=IntVar()
        self.root.sb2=IntVar()
        self.root.med2=Radiobutton(self.root.inner_frame,text = "Medium",value=10,variable=self.root.v2)
        self.root.med2.place(x=155,y=180)
        self.root.larg2 = Radiobutton(self.root.inner_frame, text = "Large",value = 20,variable=self.root.v2)
        self.root.larg2.place(x=255,y=180)
        self.root.reg2 = Radiobutton(self.root.inner_frame, text = "Regular",value = 30, variable=self.root.v2)
        self.root.reg2.place(x=355,y=180)
        self.root.c.create_text(190,230,text="Quantity : ",fill="#000000",font=("default",12))
        self.root.qty2=Spinbox(self.root.inner_frame,textvariable=self.root.sb2,from_=0 ,to=1000,bg="#0b1335",fg="white",font=("arial",11,"bold"))
        self.root.qty2.place(x=225,y=220)
        self.root.add2=Button(self.root.inner_frame,text="Add to cart",bg="#0b1335",cursor="hand2",fg="white",bd=4,font=("default",12,'bold'),command=self.add_chicken_tikka)
        self.root.add2.place(x=440,y=200)


        self.root.c.create_rectangle(20, 260, 550, 390,width=2,fill="#aae2d7")
        self.root.pep=PhotoImage(file="icons/non-Chicken_Sausage.png")
        self.root.c.create_image(80,320,image=self.root.pep)
        self.root.c.create_text(250,290,text="Chicken Sausage",fill="#000000",font=("Cooper Black",16))
        self.root.c.create_text(450,290,text="Rs.385/Rs.550/Rs.225",fill="#ff3838",font=("default",14,'bold'))
        self.root.v3=IntVar()
        self.root.sb3=IntVar()
        self.med3=Radiobutton(self.root.inner_frame,text = "Medium",value=10,variable=self.root.v3)
        self.med3.place(x=155,y=315)
        self.larg3 = Radiobutton(self.root.inner_frame, text = "Large",value = 20,variable=self.root.v3)
        self.larg3.place(x=255,y=315)
        self.reg3 = Radiobutton(self.root.inner_frame, text = "Regular",value = 30,variable=self.root.v3 )
        self.reg3.place(x=355,y=315)


        self.root.c.create_text(190,360,text="Quantity : ",fill="#000000",font=("default",12))
        self.root.qty3=Spinbox(self.root.inner_frame,from_=0 ,to=1000,bg="#0b1335",fg="white",font=("arial",11,"bold"),textvariable=self.root.sb3)
        self.root.qty3.place(x=225,y=350)

        self.root.add3=Button(self.root.inner_frame,text="Add to Cart",bg="#0b1335",cursor="hand2",fg="white",bd=4,font=("default",12,'bold'),command=self.add_chicken_sausage)
        self.root.add3.place(x=440,y=340)

      
      #========== customer details ==================================

        self.root.c_name =Label(self.root,text="Customer Name",font=("arial",12,"bold"))
        self.root.c_name.place(x=100,y=190)
        self.root.c_entry = Entry(self.root,width=20 ,font=("arial",12,"bold"))
        self.root.c_entry.place(x=100,y=220)
      #================== Table ======================================================
        self.root.columns=('item','size','qty','price','total')
        self.root.table = ttk.Treeview(self.root.inner_frame,columns=self.root.columns,show="headings",height=19)
        self.root.table.place(x=550,y=10)
        self.root.style= ttk.Style()

        self.root.style.configure('Treeview.Heading',font=('arial',12,"bold"))
        self.root.style.configure("Treeview",font=('comicsans',12))
        self.root.table.heading('item',text="Items Name",anchor=CENTER,)
        self.root.table.heading('size',text="Size",anchor=CENTER)
        self.root.table.heading('qty',text="Quantity",anchor=CENTER)
        self.root.table.heading('price',text="Price",anchor=CENTER)
        self.root.table.heading('total',text="Total",anchor=CENTER)
        self.root.table.column('item',width=200,anchor=CENTER)
        self.root.table.column('size',width=120,anchor=CENTER)
        self.root.table.column('qty',width=100,anchor=CENTER)
        self.root.table.column('price',width=100,anchor=CENTER)
        self.root.table.column('total',width=120,anchor=CENTER)
        
        
    
      #==================== Button====================================================

        self.root.logout_btn = Button(self.root,text="LogOut",width=15,height=1,bg="red" ,fg="white",font=("arial black",12,"bold"),command=self.logout)
        self.root.logout_btn.place(x=1140,y=200)
        self.root.addmore=Button(self.root,text="Add more",command=self.addmore,width=15,height=1,bg="limegreen",fg="white",font=("arial black",12,"bold"))
        self.root.addmore.place(x=750,y=200)
        self.root.confirm_order = Button(self.root,text="Confirm Order",width=15,height=1,bg="blue",fg="white",font=("arial black",12,"bold"),command=self.confirm_order)
        self.root.confirm_order.place(x=950,y=200)
           
class OrderDetails():

    def payment(self):
        self.root.destroy()
        self.win = Tk()
        self.obj= Payment(self.win)
        self.win.mainloop()
    
    
    def addmore(self):
        self.root.destroy()
        self.win = Tk()
        self.obj = Dashboard(self.win)
        self.obj.clock()
        self.win.mainloop()
    def __init__(self,root):
        
        self.root=root
        self.root.title("Order Details Form")
        self.root.geometry("1366x768")
        self.root.resizable(False, False)
        self.root.ordf1=Frame(self.root,height=150,width=1366)
        self.root.c=Canvas(self.root.ordf1,height=150,width=1366)
        self.root.c.pack()
        
  
        self.root.ordf2=Frame(self.root,height=618,width=1366)
        self.root.c=Canvas(self.root.ordf2,height=800,width=1366)
        self.root.c.pack()
        self.root.logo1=PhotoImage(file="icons/pizzamain.png")
        self.root.c.create_image(683,309,image=self.root.logo1)
        self.root.log=Label(self.root.ordf2,text="YOUR ORDER",bg="#9db1f2",font=("Cooper Black",22))
        self.root.log.place(x=450,y=4)
        self.root.c.create_rectangle(250, 50, 800, 500,fill="#d3ede6",outline="white",width=6)
    
      
        self.root.pay=Button(self.root.ordf2,text="Pay",bg="#0b1335",cursor="hand2",fg="white",bd=5,font=("default",18,'bold'),command=self.payment)
        self.root.pay.place(x=900,y=300)
        self.root.exi=Button(self.root.ordf2,text="Add more",bg="#0b1335",cursor="hand2",fg="white",bd=5,font=("default",18,'bold'),command=self.addmore)
        self.root.exi.place(x=1070,y=300)
        self.root.c.create_text(525,80,text="Items\tSize\tQty\tPrice\tTotal",font=("cooper black",18))
        self.root.c.create_text(525,90,text="____________________________________________",font=("cooper black",18))
        y =100
        for i in cartitem: 
            y+=30
            item_name = i[0]
            size = i[1]
            quantity = i[2]
            price = i[3]
            total=i[4]
            
            
            s=f"{item_name}\t{size}\t{quantity}\t{price}\t{total}"
            self.root.c.create_text(525,y,text=s,font=("default",16))
            self.subtotal = sum(item[4]for item in cartitem)
            self.root.sub_total_lbl =Label(self.root,text="Your Total Bill:"+str(self.subtotal),font=("cooper black",22,"bold"))
            self.root.sub_total_lbl.place(x=900,y=230)
     
            
            
        self.root.ordf2.pack(fill=BOTH,expand=1)

class Payment():

    def genrate_inovice(self):
        if len(cartitem)==0:
            messagebox.showerror("Error","Please Add item to the cart first")
        elif self.root.customername_entry.get()=="" or self.root.mobile_entry.get()=="" or self.root.address_entry.get('1.0','end')=="" or self.root.payment_entry.get()=="":
            messagebox.showerror("Erro","All field are required")
        else:
            self.date=datetime.datetime.now().strftime("%d-%m-%Y")
            doc = DocxTemplate('template\invoiceTemp.docx')
            self.customernname=self.root.customername_entry.get()
            self.customermobile=self.root.mobile_entry.get()
            self.customer_address=self.root.address_entry.get('1.0','end')
            self.payment_method = self.root.payment_entry.get()
            self.subtotal = sum(item[4]for item in cartitem)
            doc.render({
                "name":self.customernname,
                "mobile":self.customermobile,
                "address":self.customer_address,
                "cartitem":cartitem,
                "subtotal":self.subtotal,
                "date":self.date,
                "pm":self.payment_method,


            })
            #pat="Invoices\\"

            #doc_name=f"{self.customernname}_invoice_{datetime.datetime.now().strftime('%d-%m-%Y :%I:%m:%s:%p')}.docx"
            doc.save(f'Invoices\{self.customernname}_ivoice.docx')
            self.clearfield()
            cartitem.clear()
            messagebox.showinfo("Bill Info",f"{self.customernname} your bill is genrated successfully")
            self.root.destroy()
            self.win = Tk()
            self.obj=Dashboard(self.win)
            self.obj.clock()
            self.win.mainloop()


    def clearfield(self):
        self.root.customername_entry.delete(0,'end')
        self.root.mobile_entry.delete(0,'end')
        self.root.payment_entry.delete(0,'end')
        self.root.address_entry.delete('1.0','end')
        
        

    


    def __init__(self,root):

        self.root = root
        
        self.root.fonts="Calibri 12"
        self.root.screen_width = self.root.winfo_screenwidth()
        self.root.screen_height = self.root.winfo_screenwidth()
        self.root.width = 550  # Width
        self.root.height = 500 # Height

        self.root.screen_width = self.root.winfo_screenwidth()  # Width of the screen
        self.root.screen_height = self.root.winfo_screenheight()  # Height of the screen

        # Calculate Starting X and Y coordinates for Window
        self.root.x = (self.root.screen_width / 2) - (self.root.width / 2)
        self.root.y = (self.root.screen_height / 2) - (self.root.height / 2)
        self.root.iconbitmap('icons/login.ico')
        self.root.geometry(f"{self.root.width}x{self.root.height}+{int(self.root.x)}+{int(self.root.y)}")
        self.root.title("Payment Form")

        self.root.resizable(False, False)

        # creating all label

        self.root.Payment_lbl = Label(self.root, text="Payment Form", font=("Arial Black", 26,),fg="limegreen")
        self.root.Payment_lbl.place(x=180, y=20)
        self.root.customername_lbl = Label(self.root, text="Customer Name:", font=("Arial", 12))
        self.root.customername_lbl.place(x=30, y=90)
        self.root.mobile_lbl = Label(self.root, text="Mobile:", font=("Arial", 12))
        self.root.mobile_lbl.place(x=30, y=130)

        self.root.address_lbl = Label(self.root, text="Address:", font=("Arial", 12))

        self.root.address_lbl.place(x=30, y=250)
        self.root.payment_method = Label(self.root, text="Payment method:", font=("Arial", 12))

        self.root.payment_method.place(x=30, y=170)
        

        # creating entries
       
        self.root.customername_entry = Entry(self.root, width=38,font=self.root.fonts)
        self.root.customername_entry.place(x=180, y=90)
 
        self.root.mobile_entry = Entry(self.root, width=38,font=self.root.fonts)
        self.root.mobile_entry.place(x=180, y=130)
      
        self.method=["Cash On Delivery"]
        self.root.payment_entry = ttk.Combobox(self.root, width=36,font=self.root.fonts,values=self.method)
        self.root.payment_entry.insert(0,"Select Payment Method")
        self.root.payment_entry.place(x=180, y=170)
        self.root.address_entry = Text(self.root, width=38,font=self.root.fonts,height=8)
        self.root.address_entry.place(x=180, y=210)

       

       

        self.root.submit_btn = Button(self.root, width=15, text="Submit",bg="limegreen",fg="white",font=('arial black',10,"bold"),command=self.genrate_inovice)
        self.root.submit_btn.place(x=180, y=380)
        self.root.reset_btn = Button(self.root, width=15, text="Reset",command=self.clearfield,bg='yellow',fg="black",font=('arial black',10,'bold'))
        self.root.reset_btn.place(x=350, y=380)
        
class SpecialChicken():
    
    def confirm_order(self):
        self.root.destroy()
        self.win = Tk()
        self.obj=OrderDetails(self.win)
        self.win.mainloop()
    
    def addmore(self):

        self.root.destroy()
        self.win=Tk()
        self.obj=Dashboard(self.win)
    
        self.obj.clock()
        self.win.mainloop()
        
    
    def sum_of_total(self,item=""):
        self.root.sum_of_total =0
        for row in self.root.table.get_children(item) :
            self.root.sum_of_total=self.root.sum_of_total+self.root.table.item(row)['values'][4]
        

    def logout(self):
        
        self.root.destroy()
        self.root.win = Tk()
        self.root.obj=Login(self.root.win)
        self.root.mainloop()
    def add_roasted(self):
        if self.root.sb1.get()==0:
            messagebox.showerror("Error","Please select quantity to add")
        elif self.root.v1.get()==0:
            messagebox.showerror("Error","Please select size")
        else:
            self.item_name ="Roasted Chicken"
            self.size=""
            self.quantity = int(self.root.sb1.get())
            self.price =0
           
            if self.root.v1.get()==20:
                global size
                global price
                self.size="Larg"
                self.price =650
              

            elif self.root.v1.get()==10:
                
                self.size ="Meduim"
                self.price=450
            else:
                
                self.size="Regular"
                self.price =250
            self.total = self.quantity * self.price
            invoice_list=[self.item_name,self.size,self.quantity,self.price,self.total]
            self.root.table.insert('',0,values =invoice_list)
            cartitem.append(invoice_list)
            self.subtotal = sum(item[4]for item in cartitem)
            self.root.sub_total_lbl =Label(self.root,text="Your Total Bill:"+str(self.subtotal),font=("cooper black",22,"bold"),bg="limegreen")
            self.root.sub_total_lbl.place(x=900,y=700)
            
            
    #==================================================================

    def add_chicken_metaball(self):
        if self.root.sb2.get()==0:
            messagebox.showerror("Error","Please select quantity to add")
        elif self.root.v2.get()==0:
            messagebox.showerror("Error","Please select size")
        else:
            self.item_name ="Chicken Metaballs"
            self.size=""
            self.quantity = int(self.root.sb2.get())
            self.price =0
           
            if self.root.v2.get()==20:
                global size
                global price
                self.size="Larg"
                self.price =600
              

            elif self.root.v2.get()==10:
                
                self.size ="Meduim"
                self.price=400
            else:
                
                self.size="Regular"
                self.price =250
            self.total = self.quantity * self.price
            invoice_list=[self.item_name,self.size,self.quantity,self.price,self.total]
            self.root.table.insert('',0,values =invoice_list)
            cartitem.append(invoice_list)
            self.subtotal = sum(item[4]for item in cartitem)
            self.root.sub_total_lbl =Label(self.root,text="Your Total Bill:"+str(self.subtotal),font=("cooper black",22,"bold"),bg="limegreen")
            self.root.sub_total_lbl.place(x=900,y=700)
            
   
      #=====================================================================================================

    def add_boneless(self):
        if self.root.sb3.get()==0:
            messagebox.showerror("Error","Please select quantity to add")
        elif self.root.v3.get()==0:
            messagebox.showerror("Error","Please select size")
        else:
            self.item_name ="Boneless Chicken "
            self.size=""
            self.quantity = int(self.root.sb3.get())
            self.price =0
           
            if self.root.v3.get()==20:
                global size
                global price
                self.size="Larg"
                self.price =550
              

            elif self.root.v3.get()==10:
                
                self.size ="Meduim"
                self.price=385
            else:
                
                self.size="Regular"
                self.price =225
            self.total = self.quantity * self.price
            invoice_list=[self.item_name,self.size,self.quantity,self.price,self.total]
            self.root.table.insert('',0,values =invoice_list)
            cartitem.append(invoice_list)
            self.subtotal = sum(item[4]for item in cartitem)
            self.root.sub_total_lbl =Label(self.root,text="Your Total Bill:"+str(self.subtotal),font=("cooper black",22,"bold"),bg="limegreen")
            self.root.sub_total_lbl.place(x=900,y=700)
            






    def clock(self):
        self.time=strftime("%I:%M:%S:%p")
        self.day = strftime("%A")
        self.date = strftime("%d-%m-%Y")
        self.root.time_lbl.config(text=self.time)
        self.root.day_lbl.config(text=self.day)
        self.root.date_lbl.config(text=self.date)
        self.root.time.after(1000,self.clock)

        


    def __init__(self,root):
        
        self.root = root
        root.overrideredirect(1)
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenwidth()
        self.width = 1366  # Width
        self.height = 768  # Height
    
        self.screen_width = self.root.winfo_screenwidth()  # Width of the screen
        self.screen_height = self.root.winfo_screenheight()  # Height of the screen

        # Calculate Starting X and Y coordinates for Window
        self.x = (self.screen_width / 2) - (self.width / 2)
        self.y = (self.screen_height / 2) - (self.height / 2)




        self.root.iconbitmap('icons/login.ico')
        self.root.geometry(f"{self.width}x{self.height}+{int(self.x)}+{int(self.y)}")
        self.root.title("Special Chicken Form")
        self.root.state('zoomed')
        self.root.resizable(False,False)
        #creating frame and labels
        self.root.top_frame = Frame(self.root,width =1366,bg="darkorange",height=180,borderwidth =5,relief =SUNKEN,pady=10)
        self.root.top_frame.place(x=0,y=0)
        self.root.top_lable=Label(self.root.top_frame,text="Online Pizza Delivery Mangement System",font=("Arial ",24,"bold"),bg="darkorange",fg="white")
        self.root.top_lable.place(x=20,y=50)
        self.root.time=Label(self.root.top_frame,text="Time",font=("Arial",22,"bold"),bg="darkorange",fg="white")
        self.root.time.place(x=1050,y=50)
        self.root.time_lbl = Label(self.root.top_frame,text="00:00:00 AM",font=("Arial ",22,"bold"),background="darkorange",fg="white")
        self.root.time_lbl.place(x=1150,y=50)
        self.root.day_lbl = Label(self.root.top_frame,text="Day",font=("Arial ",22,"bold"),background="darkorange",fg="white")
        self.root.day_lbl.place(x=1150,y=0)

        self.root.date_lbl = Label(self.root.top_frame,text="Date",font=("Arial ",22,"bold"),background="darkorange",fg="white")
        self.root.date_lbl.place(x=1150,y=100)


        #=========== Labels for Pizza images===========================
        self.root.inner_frame = Frame(self.root,width =1366,height=1600,bg="red",borderwidth =5,relief =SUNKEN,pady=10)
        self.root.inner_frame.place(x=100,y=250)
        self.root.c=Canvas(self.root.inner_frame,height=400,width=1200)
        self.root.c.pack()
       #================ Delux pizza ====================================
        self.root.c.create_rectangle(20, 10, 550, 130,width=2,fill="#aae2d7")
        self.delu=PhotoImage(file="icons/roasted.png")
        self.root.c.create_image(80,70,image=self.delu)
        self.root.c.create_text(250,40,text="Roasted Chicken",fill="#000000",font=("Cooper Black",15))
        self.root.c.create_text(450,40,text="Rs.450/Rs.650/Rs.250",fill="#ff3838",font=("default",14,'bold'))
        self.root.v1=IntVar()
        self.root.sb1=IntVar()
        self.root.med1=Radiobutton(self.root.inner_frame,text = "Medium",value=10,variable=self.root.v1)
        self.root.med1.place(x=155,y=70)
        self.root.larg1 = Radiobutton(self.root.inner_frame, text = "Large",value = 20, variable =self.root.v1)
        self.root.larg1.place(x=255,y=70)
        self.root.reg1 = Radiobutton(self.root.inner_frame, text = "Regular",value = 30, variable =self.root.v1)
        self.root.reg1.place(x=355,y=70)
        self.root.c.create_text(190,110,text="Quantity : ",fill="#000000",font=("default",12))
        self.root.qty1=Spinbox(self.root.inner_frame,from_=0 ,to=1000,bg="#0b1335",fg="white",font=("arial",13,"bold"),textvariable=self.root.sb1)
        self.root.qty1.place(x=225,y=100)
        self.root.add1=Button(self.root.inner_frame,text="Add to Cart",bg="#0b1335",cursor="hand2",fg="white",bd=4,font=("default",12,'bold'),command=self.add_roasted)
        self.root.add1.place(x=440,y=70)
        #==========veg vegganza ====================================================
        self.root.c.create_rectangle(20, 130, 550, 260,width=2,fill="#aae2d7")
        self.vag=PhotoImage(file="icons/chicken-meatballs.png")
        self.root.c.create_image(80,190,image=self.vag)
        self.root.c.create_text(250,150,text="Chicken Metaballs",fill="#000000",font=("Cooper Black",15))
        self.root.c.create_text(450,150,text="Rs.400/Rs.600/Rs.250",fill="#ff3838",font=("default",14,'bold'))  
        self.root.v2=IntVar()
        self.root.sb2=IntVar()
        self.root.med2=Radiobutton(self.root.inner_frame,text = "Medium",value=10,variable=self.root.v2)
        self.root.med2.place(x=155,y=180)
        self.root.larg2 = Radiobutton(self.root.inner_frame, text = "Large",value = 20,variable=self.root.v2)
        self.root.larg2.place(x=255,y=180)
        self.root.reg2 = Radiobutton(self.root.inner_frame, text = "Regular",value = 30, variable=self.root.v2)
        self.root.reg2.place(x=355,y=180)
        self.root.c.create_text(190,230,text="Quantity : ",fill="#000000",font=("default",12))
        self.root.qty2=Spinbox(self.root.inner_frame,textvariable=self.root.sb2,from_=0 ,to=1000,bg="#0b1335",fg="white",font=("arial",11,"bold"))
        self.root.qty2.place(x=225,y=220)
        self.root.add2=Button(self.root.inner_frame,text="Add to cart",bg="#0b1335",cursor="hand2",fg="white",bd=4,font=("default",12,'bold'),command=self.add_chicken_metaball)
        self.root.add2.place(x=440,y=200)


        self.root.c.create_rectangle(20, 260, 550, 390,width=2,fill="#aae2d7")
        self.root.pep=PhotoImage(file="icons/Boneless-Chicken-wings-192x192.png")
        self.root.c.create_image(80,320,image=self.root.pep)
        self.root.c.create_text(250,290,text="Boneless Chicken",fill="#000000",font=("Cooper Black",15))
        self.root.c.create_text(450,290,text="Rs.385/Rs.550/Rs.225",fill="#ff3838",font=("default",14,'bold'))
        self.root.v3=IntVar()
        self.root.sb3=IntVar()
        self.med3=Radiobutton(self.root.inner_frame,text = "Medium",value=10,variable=self.root.v3)
        self.med3.place(x=155,y=315)
        self.larg3 = Radiobutton(self.root.inner_frame, text = "Large",value = 20,variable=self.root.v3)
        self.larg3.place(x=255,y=315)
        self.reg3 = Radiobutton(self.root.inner_frame, text = "Regular",value = 30,variable=self.root.v3 )
        self.reg3.place(x=355,y=315)


        self.root.c.create_text(190,360,text="Quantity : ",fill="#000000",font=("default",12))
        self.root.qty3=Spinbox(self.root.inner_frame,from_=0 ,to=1000,bg="#0b1335",fg="white",font=("arial",11,"bold"),textvariable=self.root.sb3)
        self.root.qty3.place(x=225,y=350)

        self.root.add3=Button(self.root.inner_frame,text="Add to Cart",bg="#0b1335",cursor="hand2",fg="white",bd=4,font=("default",12,'bold'),command=self.add_boneless)
        self.root.add3.place(x=440,y=340)

      
     
      #================== Table ======================================================
        self.root.columns=('item','size','qty','price','total')
        self.root.table = ttk.Treeview(self.root.inner_frame,columns=self.root.columns,show="headings",height=19)
        self.root.table.place(x=550,y=10)
        self.root.style= ttk.Style()

        self.root.style.configure('Treeview.Heading',font=('arial',12,"bold"))
        self.root.style.configure("Treeview",font=('comicsans',12))
        self.root.table.heading('item',text="Items Name",anchor=CENTER,)
        self.root.table.heading('size',text="Size",anchor=CENTER)
        self.root.table.heading('qty',text="Quantity",anchor=CENTER)
        self.root.table.heading('price',text="Price",anchor=CENTER)
        self.root.table.heading('total',text="Total",anchor=CENTER)
        self.root.table.column('item',width=200,anchor=CENTER)
        self.root.table.column('size',width=120,anchor=CENTER)
        self.root.table.column('qty',width=100,anchor=CENTER)
        self.root.table.column('price',width=100,anchor=CENTER)
        self.root.table.column('total',width=120,anchor=CENTER)
        
        
    

      
        #==================== Button====================================================

        self.root.logout_btn = Button(self.root,text="LogOut",width=15,height=1,bg="red" ,fg="white",font=("arial black",12,"bold"),command=self.logout)
        self.root.logout_btn.place(x=1140,y=200)
        self.root.addmore=Button(self.root,text="Add more",command=self.addmore,width=15,height=1,bg="limegreen",fg="white",font=("arial black",12,"bold"))
        self.root.addmore.place(x=750,y=200)
        self.root.confirm_order = Button(self.root,text="Confirm Order",command=self.confirm_order,width=15,height=1,bg="blue",fg="white",font=("arial black",12,"bold"))
        self.root.confirm_order.place(x=950,y=200)
        
class Colddrinks():
    
    def confirm_order(self):
        self.root.destroy()
        self.win = Tk()
        self.obj=OrderDetails(self.win)
        self.win.mainloop()
    
    def addmore(self):

        self.root.destroy()
        self.win=Tk()
        self.obj=Dashboard(self.win)
    
        self.obj.clock()
        self.win.mainloop()
        
    
    def sum_of_total(self,item=""):
        self.root.sum_of_total =0
        for row in self.root.table.get_children(item) :
            self.root.sum_of_total=self.root.sum_of_total+self.root.table.item(row)['values'][4]
        

    def logout(self):
        
        self.root.destroy()
        self.root.win = Tk()
        self.root.obj=Login(self.root.win)
        self.root.mainloop()
    def add_coke(self):
        if self.root.sb1.get()==0:
            messagebox.showerror("Error","Please select quantity to add")
        elif self.root.v1.get()==0:
            messagebox.showerror("Error","Please select size")
        else:
            self.item_name ="Coka Cola"
            self.size=""
            self.quantity = int(self.root.sb1.get())
            self.price =0
           
            if self.root.v1.get()==20:
                global size
                global price
                self.size="Larg"
                self.price =180
              

            elif self.root.v1.get()==10:
                
                self.size ="Meduim"
                self.price=140
            else:
                
                self.size="Regular"
                self.price =40
            self.total = self.quantity * self.price
            invoice_list=[self.item_name,self.size,self.quantity,self.price,self.total]
            self.root.table.insert('',0,values =invoice_list)
            cartitem.append(invoice_list)
            self.subtotal = sum(item[4]for item in cartitem)
            self.root.sub_total_lbl =Label(self.root,text="Your Total Bill:"+str(self.subtotal),font=("cooper black",22,"bold"),bg="limegreen")
            self.root.sub_total_lbl.place(x=900,y=700)
            
            
    #==================================================================

    def add_dew(self):
        if self.root.sb2.get()==0:
            messagebox.showerror("Error","Please select quantity to add")
        elif self.root.v2.get()==0:
            messagebox.showerror("Error","Please select size")
        else:
            self.item_name ="Mountain Dew"
            self.size=""
            self.quantity = int(self.root.sb2.get())
            self.price =0
           
            if self.root.v2.get()==20:
                global size
                global price
                self.size="Larg"
                self.price =180
              

            elif self.root.v2.get()==10:
                
                self.size ="Meduim"
                self.price=140
            else:
                
                self.size="Regular"
                self.price =40
            self.total = self.quantity * self.price
            invoice_list=[self.item_name,self.size,self.quantity,self.price,self.total]
            self.root.table.insert('',0,values =invoice_list)
            cartitem.append(invoice_list)
            self.subtotal = sum(item[4]for item in cartitem)
            self.root.sub_total_lbl =Label(self.root,text="Your Total Bill:"+str(self.subtotal),font=("cooper black",22,"bold"),bg="limegreen")
            self.root.sub_total_lbl.place(x=900,y=700)
            
   
      #=====================================================================================================

    def add_pepsi(self):
        if self.root.sb3.get()==0:
            messagebox.showerror("Error","Please select quantity to add")
        elif self.root.v3.get()==0:
            messagebox.showerror("Error","Please select size")
        else:
            self.item_name ="Pepsi Cola"
            self.size=""
            self.quantity = int(self.root.sb3.get())
            self.price =0
           
            if self.root.v3.get()==20:
                global size
                global price
                self.size="Larg"
                self.price =180
              

            elif self.root.v3.get()==10:
                
                self.size ="Meduim"
                self.price=140
            else:
                
                self.size="Regular"
                self.price =40
            self.total = self.quantity * self.price
            invoice_list=[self.item_name,self.size,self.quantity,self.price,self.total]
            self.root.table.insert('',0,values =invoice_list)
            cartitem.append(invoice_list)
            self.subtotal = sum(item[4]for item in cartitem)
            self.root.sub_total_lbl =Label(self.root,text="Your Total Bill:"+str(self.subtotal),font=("cooper black",22,"bold"),bg="limegreen")
            self.root.sub_total_lbl.place(x=900,y=700)
            






    def clock(self):
        self.time=strftime("%I:%M:%S:%p")
        self.day = strftime("%A")
        self.date = strftime("%d-%m-%Y")
        self.root.time_lbl.config(text=self.time)
        self.root.day_lbl.config(text=self.day)
        self.root.date_lbl.config(text=self.date)
        self.root.time.after(1000,self.clock)

        


    def __init__(self,root):
        
        self.root = root
        root.overrideredirect(1)
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenwidth()
        self.width = 1366  # Width
        self.height = 768  # Height
    
        self.screen_width = self.root.winfo_screenwidth()  # Width of the screen
        self.screen_height = self.root.winfo_screenheight()  # Height of the screen

        # Calculate Starting X and Y coordinates for Window
        self.x = (self.screen_width / 2) - (self.width / 2)
        self.y = (self.screen_height / 2) - (self.height / 2)




        self.root.iconbitmap('icons/login.ico')
        self.root.geometry(f"{self.width}x{self.height}+{int(self.x)}+{int(self.y)}")
        self.root.title("Cold Drinks Form")
        self.root.state('zoomed')
        self.root.resizable(False,False)
        #creating frame and labels
        self.root.top_frame = Frame(self.root,width =1366,bg="darkorange",height=180,borderwidth =5,relief =SUNKEN,pady=10)
        self.root.top_frame.place(x=0,y=0)
        self.root.top_lable=Label(self.root.top_frame,text="Online Pizza Delivery Mangement System",font=("Arial ",24,"bold"),bg="darkorange",fg="white")
        self.root.top_lable.place(x=20,y=50)
        self.root.time=Label(self.root.top_frame,text="Time",font=("Arial",22,"bold"),bg="darkorange",fg="white")
        self.root.time.place(x=1050,y=50)
        self.root.time_lbl = Label(self.root.top_frame,text="00:00:00 AM",font=("Arial ",22,"bold"),background="darkorange",fg="white")
        self.root.time_lbl.place(x=1150,y=50)
        self.root.day_lbl = Label(self.root.top_frame,text="Day",font=("Arial ",22,"bold"),background="darkorange",fg="white")
        self.root.day_lbl.place(x=1150,y=0)

        self.root.date_lbl = Label(self.root.top_frame,text="Date",font=("Arial ",22,"bold"),background="darkorange",fg="white")
        self.root.date_lbl.place(x=1150,y=100)


        #=========== Labels for Pizza images===========================
        self.root.inner_frame = Frame(self.root,width =1366,height=1600,bg="red",borderwidth =5,relief =SUNKEN,pady=10)
        self.root.inner_frame.place(x=100,y=250)
        self.root.c=Canvas(self.root.inner_frame,height=400,width=1200)
        self.root.c.pack()
       #================ Delux pizza ====================================
        self.root.c.create_rectangle(20, 10, 550, 130,width=2,fill="#aae2d7")
        self.delu=PhotoImage(file="icons/coke.png")
        self.root.c.create_image(80,70,image=self.delu)
        self.root.c.create_text(250,40,text="Coca Cola",fill="#000000",font=("Cooper Black",15))
        self.root.c.create_text(450,40,text="Rs.140/Rs.180/Rs.40",fill="#ff3838",font=("default",14,'bold'))
        self.root.v1=IntVar()
        self.root.sb1=IntVar()
        self.root.med1=Radiobutton(self.root.inner_frame,text = "Medium",value=10,variable=self.root.v1)
        self.root.med1.place(x=155,y=70)
        self.root.larg1 = Radiobutton(self.root.inner_frame, text = "Large",value = 20, variable =self.root.v1)
        self.root.larg1.place(x=255,y=70)
        self.root.reg1 = Radiobutton(self.root.inner_frame, text = "Regular",value = 30, variable =self.root.v1)
        self.root.reg1.place(x=355,y=70)
        self.root.c.create_text(190,110,text="Quantity : ",fill="#000000",font=("default",12))
        self.root.qty1=Spinbox(self.root.inner_frame,from_=0 ,to=1000,bg="#0b1335",fg="white",font=("arial",13,"bold"),textvariable=self.root.sb1)
        self.root.qty1.place(x=225,y=100)
        self.root.add1=Button(self.root.inner_frame,text="Add to Cart",bg="#0b1335",cursor="hand2",fg="white",bd=4,font=("default",12,'bold'),command=self.add_coke)
        self.root.add1.place(x=440,y=70)
        #==========veg vegganza ====================================================
        self.root.c.create_rectangle(20, 130, 550, 260,width=2,fill="#aae2d7")
        self.vag=PhotoImage(file="icons/Dew.png")
        self.root.c.create_image(80,190,image=self.vag)
        self.root.c.create_text(250,150,text="Mountain Dew",fill="#000000",font=("Cooper Black",15))
        self.root.c.create_text(450,150,text="Rs.140/Rs.180/Rs.40",fill="#ff3838",font=("default",14,'bold'))  
        self.root.v2=IntVar()
        self.root.sb2=IntVar()
        self.root.med2=Radiobutton(self.root.inner_frame,text = "Medium",value=10,variable=self.root.v2)
        self.root.med2.place(x=155,y=180)
        self.root.larg2 = Radiobutton(self.root.inner_frame, text = "Large",value = 20,variable=self.root.v2)
        self.root.larg2.place(x=255,y=180)
        self.root.reg2 = Radiobutton(self.root.inner_frame, text = "Regular",value = 30, variable=self.root.v2)
        self.root.reg2.place(x=355,y=180)
        self.root.c.create_text(190,230,text="Quantity : ",fill="#000000",font=("default",12))
        self.root.qty2=Spinbox(self.root.inner_frame,textvariable=self.root.sb2,from_=0 ,to=1000,bg="#0b1335",fg="white",font=("arial",11,"bold"))
        self.root.qty2.place(x=225,y=220)
        self.root.add2=Button(self.root.inner_frame,text="Add to cart",bg="#0b1335",cursor="hand2",fg="white",bd=4,font=("default",12,'bold'),command=self.add_dew)
        self.root.add2.place(x=440,y=200)


        self.root.c.create_rectangle(20, 260, 550, 390,width=2,fill="#aae2d7")
        self.root.pep=PhotoImage(file="icons/pepsi.png")
        self.root.c.create_image(80,320,image=self.root.pep)
        self.root.c.create_text(250,290,text="Pepsi ",fill="#000000",font=("Cooper Black",15))
        self.root.c.create_text(450,290,text="Rs.140/Rs.180/Rs.40",fill="#ff3838",font=("default",14,'bold'))
        self.root.v3=IntVar()
        self.root.sb3=IntVar()
        self.med3=Radiobutton(self.root.inner_frame,text = "Medium",value=10,variable=self.root.v3)
        self.med3.place(x=155,y=315)
        self.larg3 = Radiobutton(self.root.inner_frame, text = "Large",value = 20,variable=self.root.v3)
        self.larg3.place(x=255,y=315)
        self.reg3 = Radiobutton(self.root.inner_frame, text = "Regular",value = 30,variable=self.root.v3 )
        self.reg3.place(x=355,y=315)


        self.root.c.create_text(190,360,text="Quantity : ",fill="#000000",font=("default",12))
        self.root.qty3=Spinbox(self.root.inner_frame,from_=0 ,to=1000,bg="#0b1335",fg="white",font=("arial",11,"bold"),textvariable=self.root.sb3)
        self.root.qty3.place(x=225,y=350)

        self.root.add3=Button(self.root.inner_frame,text="Add to Cart",bg="#0b1335",cursor="hand2",fg="white",bd=4,font=("default",12,'bold'),command=self.add_pepsi)
        self.root.add3.place(x=440,y=340)

      
     
      #================== Table ======================================================
        self.root.columns=('item','size','qty','price','total')
        self.root.table = ttk.Treeview(self.root.inner_frame,columns=self.root.columns,show="headings",height=19)
        self.root.table.place(x=550,y=10)
        self.root.style= ttk.Style()

        self.root.style.configure('Treeview.Heading',font=('arial',12,"bold"))
        self.root.style.configure("Treeview",font=('comicsans',12))
        self.root.table.heading('item',text="Items Name",anchor=CENTER,)
        self.root.table.heading('size',text="Size",anchor=CENTER)
        self.root.table.heading('qty',text="Quantity",anchor=CENTER)
        self.root.table.heading('price',text="Price",anchor=CENTER)
        self.root.table.heading('total',text="Total",anchor=CENTER)
        self.root.table.column('item',width=200,anchor=CENTER)
        self.root.table.column('size',width=120,anchor=CENTER)
        self.root.table.column('qty',width=100,anchor=CENTER)
        self.root.table.column('price',width=100,anchor=CENTER)
        self.root.table.column('total',width=120,anchor=CENTER)
        
        
    

      
        #==================== Button====================================================

        self.root.logout_btn = Button(self.root,text="LogOut",width=15,height=1,bg="red" ,fg="white",font=("arial black",12,"bold"),command=self.logout)
        self.root.logout_btn.place(x=1140,y=200)
        self.root.addmore=Button(self.root,text="Add more",command=self.addmore,width=15,height=1,bg="limegreen",fg="white",font=("arial black",12,"bold"))
        self.root.addmore.place(x=750,y=200)
        self.root.confirm_order = Button(self.root,text="Confirm Order",command=self.confirm_order,width=15,height=1,bg="blue",fg="white",font=("arial black",12,"bold"))
        self.root.confirm_order.place(x=950,y=200)            


if __name__=="__main__":
    root =Tk()
    obj = Login(root)
    root.mainloop()