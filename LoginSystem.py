import random
import string
from tkinter import *
import tkinter
import os
import mysql.connector
from captcha.image import ImageCaptcha

connectiondb = mysql.connector.connect(host="sql6.freemysqlhosting.net",user="sql6467182",passwd="EpTAlfs8ns",database="sql6467182")
mycur = connectiondb.cursor()
#setting default role as (user)
userRole = "user"



def main_display():
    global root
    root = Tk()
    root.config(bg="white")
    root.title("Log-IN Portal") #Name of the App (Top bar)
    root.geometry("1400x750") # Resolution of the Window
    Label(root, text='Welcome to Log In', bd=20, font=('arial', 20, 'bold'), relief="groove", fg="white",bg="blue", width=300).pack()
    Label(root, text="").pack()
    Button(root, text='Log In', height="1", width="20", bd=8, font=('arial', 12, 'bold'), relief="groove", fg="white",bg="blue",command=login).pack()
    Label(root, text="").pack()
    Button(root, text='Exit', height="1", width="20", bd=8, font=('arial', 12, 'bold'), relief="groove", fg="white",bg="blue", command=exit).pack()
    Label(root, text="").pack()

def login():
    global root2
    root2 = Toplevel(root)
    root2.title("Account Login")
    root2.geometry("1400x750")
    root2.config(bg="white")

    #global variables so that they can be used outside the function
    global username_verification
    global password_verification

    Label(root2, text='Log In', bd=5, font=('arial', 12, 'bold'), relief="groove", fg="white",bg="blue", width=300).pack()
    #to get inputs as strings
    username_verification = StringVar()
    password_verification = StringVar()

    Label(root2, text="").pack()
    Label(root2, text="Username :", fg="black", font=('arial', 12, 'bold')).pack()
    Entry(root2, textvariable=username_verification).pack()
    Label(root2, text="").pack()

    Label(root2, text="Password :", fg="black", font=('arial', 12, 'bold')).pack()
    Entry(root2, textvariable=password_verification, show="*").pack()
    Label(root2, text="").pack()

    Button(root2, text="Login", bg="blue", fg='white', relief="groove", font=('arial', 12, 'bold'),command=login_verification).pack()
    Label(root2, text="")


def login_verification():
    global userRole
    #get user_verification and pass_verification as strings
    user_verification = username_verification.get()
    pass_verification = password_verification.get()

    sql = "select * from usertable where username = %s and password = %s"

    #get username and password inputs from GUI
    mycur.execute(sql, [user_verification, pass_verification])
    results = mycur.fetchall()

    #Get role of the logged in user
    Query = "SELECT a.role FROM (select * from usertable where username = %s) as a"

    #[user_verification] will be swapped with %s
    mycur.execute(Query , [user_verification])
    roleofuser = mycur.fetchone()

    #save it in UserRole to print it later on
    #[0] to get it as a string
    userRole = roleofuser[0]
    #if what the user wrote matches what is in the database run logged(), else run failed()

    if results:
        for i in results:
            captchaWindow()
            break
    else:
        failed()
    return userRole

def createCaptcha():
    global captcha_text
    image = ImageCaptcha(width=280, height=90)
    captcha_text = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
    data = image.generate(captcha_text)
    image.write(captcha_text, "CAPTCHA.png")
    return

def captchaWindow():
    global root3,captcha_verification,Photo, label
    root3 = Toplevel(root2)
    root3.title("Account Login")
    root3.geometry("750x400")
    root3.config(bg="white")

    createCaptcha()
    Photo = tkinter.PhotoImage(file="CAPTCHA.png")

    Label(root3, text="Captcha :", fg="black", font=('arial', 12, 'bold')).pack()
    captcha_verification = StringVar()
    Entry(root3, textvariable=captcha_verification).pack()
    # REFERENCE to the image (must always be there)
    label = Label(root3, image=Photo)
    label.image = Photo  # keep a reference!
    label.pack()
    Label(root3, text="").pack()
    Button(root3, text="Submit", bg="blue", fg='white', relief="groove", font=('arial', 12, 'bold'),command=captchaVerification).pack()
    Label(root3, text="").pack()
    Button(root3, text="Refresh", bg="blue", fg='white', relief="groove", font=('arial', 12, 'bold'),command = lambda: refreshCaptcha(label)).pack()


def captchaVerification():
    global captcha_verification
    captcha_verification = captcha_verification.get()
    if captcha_verification == captcha_text:
        logged()
    else:
        print("Wrong Captcha!")
        print(captcha_text)
        print(captcha_verification)


def refreshCaptcha(label):
    global Photo,captcha_verification
    createCaptcha()
    Photo = tkinter.PhotoImage(file="CAPTCHA.png")
    label.configure(image=Photo)





def logged():
    global logged_message
    logged_message = Toplevel(root3)
    logged_message.title("Welcome")
    logged_message.geometry("500x100")
    Label(logged_message, text="Login Successfully!... Welcome {} ".format(username_verification.get()), fg="green", font="bold").pack()
    Label(logged_message, text="").pack()
    Button(logged_message, text="Logout", bg="blue", fg='white', relief="groove", font=('arial', 12, 'bold'), command=logged_destroy).pack()
    Label(logged_message, text=userRole).pack()

def failed():
    global failed_message
    failed_message = Toplevel(root2)
    failed_message.title("Invalid")
    failed_message.geometry("500x100")
    Label(failed_message, text="Invalid Username or Password", fg="red", font="bold").pack()
    Label(failed_message, text="").pack()
    Button(failed_message,text="Ok", bg="blue", fg='white', relief="groove", font=('arial', 12, 'bold'), command=failed_destroy).pack()

def Exit():
    wayOut = tkinter.messagebox.askquestion("Login System", "Do you want to exit the system")
    if wayOut =='yes':
        root.destroy()

def logged_destroy():
    logged_message.destroy()
    root2.destroy()

def failed_destroy():
    failed_message.destroy()



main_display()
root.mainloop()


print("Program Run Succesfully!")