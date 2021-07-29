"""
The GUI will interact with a separate backend Python script to provide functionality

Dependencies:
pip3 install tkcalendar
"""
#Libraries
from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime as dt

#Constants
PROGRAM_NAME = "Ernest-Badger"
BACKGROUND_COLOUR = "light green"
FRAME_BG_COLOUR = "light green"


class MainWindow(): #Class for the Main Window
    def __init__(self, master): 
        self.master = master
        self.master.title(PROGRAM_NAME) #Set window title
        self.master.geometry("300x300") #Set window size
        self.master.configure(background=BACKGROUND_COLOUR)
        self.title = Label(self.master, text = PROGRAM_NAME, font=('Arial',20),bg=BACKGROUND_COLOUR)
        self.title.pack(fill='x',pady=5)
        self.frame = Frame(self.master, bg=FRAME_BG_COLOUR)
        date = dt.now() #Get current date
        #Creates and styles the data picker
        self.calendar = Calendar(self.frame, selectmode= "day",year=date.year,month=date.month,day=date.day,showweeknumbers=False,\
            selectforeground="white",selectbackground="red",normalbackground="white",weekendbackground="white",headersbackground="light blue",bordercolor="light blue")
        self.calendar.pack(fill='x',pady=3,padx=10)
        self.submit = ttk.Button(self.frame,text="Fetch Data",style=f"white/{BACKGROUND_COLOUR}.TButton",command=self.submit)
        self.submit.pack(fill='x',pady=3,padx=60)
        self.frame.pack(fill='both',pady=5)
        self.message = Label(self.master,bg=BACKGROUND_COLOUR,text="Select a date to request data for")
        self.message.pack(fill='x',pady=5)

    def submit(self):
        date = self.calendar.get_date() #Gets the date selected in the GUI calendar
        self.message.configure(text = f"Data requested for: {date}") #Displays a success message in the GUI
        r_date = dt.strptime(date,"%d/%m/%Y").strftime("%Y%m%d") #Converts the date into the same format as the CSV file naming scheme
        print(f"Request data for: {r_date}") #This is where a request to the backend will be made

#If the program is running as a standalone script (not as part of another script)
if __name__ == "__main__":
    app = Tk()
    style = ttk.Style(app)
    style.theme_use('clam') #Changes the style of the GUI
    MainWindow(app) #Creates a new main window
    app.mainloop() #Displays the GUI