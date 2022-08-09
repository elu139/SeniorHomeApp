# To-do list:
# 1. Figuring out how to code the back button to go to a different page
# 2. Formatting

import os
from tkinter import *
from backend import *

root = Tk()
root.title('Springfield Senior Home')
root.geometry("600x800")

# Takes in apt # and displays all visitors in that apt who aren't signed in


def enter():
    message.config(text="")
    number = int(aptNumber.get())
    match apts.get_apt(number):
        case Success():
            visitorList.delete(0, END)
            apt = apts.get_apt(number).unwrap()
            if not apt.visitors:
                message.config(
                    text="There are no registered visitors for this apartment.")
            else:
                hasVisitors = True
                for visitor in apt.visitors:
                    if (visitor, number) not in allVisitors.visitors:
                        visitorList.insert(END, visitor)
                        hasVisitors = False
                if(hasVisitors):
                    message.config(
                        text="All visitors registered for this apartment are currently signed in.")
        case Failure():
            visitorList.delete(0, END)
            message.config(
                text="Please enter a valid apartment number.\nAsk help from the guard if necessary.")

# Signs in the selected visitor


def signIn():
    number = int(aptNumber.get())
    name = visitorList.get(ANCHOR)
    allVisitors.sign_in(name, number)
    if not visitorList.curselection():
        message.config(text="Please select a visitor to sign in.")
    else:
        message.config(text=name + " has successfully signed in.")
        visitorList.delete(ANCHOR)

# Help message that appears when help button is clicked


def help():
    message.config(text="To sign in, enter the apartment number of the visitor.\n \
Click 'Enter'.\nYou will see a list of all the registered visitors who are not signed in in the box above.\n \
Click on the visitor that you want to sign in.\nClick 'Sign in'.\n \
If you don't see your name, you are currently signed in,\nor you need to register yourself as a visitor in the homepage.")

# I don't know how to go back to the home page so I will make the app close for now


def back():
    root.destroy()
    os.system("python3 tkHome.py")


# Code for how the app appears
title = Label(root, text="Sign In", font=("Helvetica", 20))
title.pack(side=TOP, pady=5)

apts = ApartmentDatabase("./data/apts.json")
allVisitors = VisitorManager(apts, "./visitor-logs/")

prompt = Label(root, text="Enter apartment #:")
prompt.pack()

aptNumber = Entry(root, width=10)
aptNumber.pack()

enterButton = Button(root, text="Enter", command=enter)
enterButton.pack(pady=5)

visitorList = Listbox(root)
visitorList.pack(pady=10)

signInButton = Button(root, text="Sign in", command=signIn)
signInButton.pack(pady=5)

helpButton = Button(root, text="Help", command=help)
helpButton.pack(pady=5)

backButton = Button(root, text="Back", command=back)
backButton.pack(pady=5)

global message
message = Label(root, text="")
message.pack(pady=5)

root.mainloop()
