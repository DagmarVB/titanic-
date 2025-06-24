import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandastable import Table # library for embedding tables in tkinter using pandas dataframes
import titanicGetData # module that retrieves the data for plotting or display

"""
Project description: build a tkinter GUI that allows a user to chose specifications (gender, age, class)
for Titanic passengers. According to the given specifications the user can then
a.) have a pie chart plotted for the survival ratio (using matplotlib) or
b.) have a list of passengers displayed with the given specifications (using pandastable).
"""


class BuildGui(tk.Tk):
    """build tkinter interface"""

    def __init__(self, *args, **kwargs):
        """declare class attributes and build the interface"""

        super().__init__(*args, **kwargs)
        # declare class attributes:
        self.image = tk.PhotoImage(file="titanicImage.gif")
        self.gendervar = tk.StringVar(None, "all")
        self.agevar1 = tk.IntVar()
        self.agevar2 = tk.IntVar()
        self.agevar3 = tk.IntVar()
        self.agevar4 = tk.IntVar()
        self.agevarU = tk.IntVar()
        self.classvar = tk.StringVar(None, "all")

        # build GUI window and header:
        self.title("Titanic Passengers Survival")
        self.geometry("950x720")
        self.resizable(width=False, height=False)
        self.header = tk.Label(self, text="Survival statistics of Titanic passengers",
                               font=("Calibri", "16"), padx=10, pady=15)
        self.header.grid(row=0, column=0, columnspan=3, sticky="ew")
        self.leftspace = tk.Label(self, text="   ") # empty column for formatting
        self.leftspace.grid(row=1, column=0)

        # build plot/display area and insert background picture:
        self.plotframe = tk.Frame()
        self.plotframe.grid(row=1, column=2, sticky="ew")
        self.setBackground()

        # build menu:
        self.createMenu()

        # create the interface:
        self.mainloop()

    def createMenu(self):
        """create the menu panel for the interface"""

        i = 1  # parameter for all padx und pady entries
        # build menu frame, make it non-resizable and build a header
        menuframe = tk.Frame(self)
        menuframe.grid(row=1, column=1, sticky="nsew")
        menuframe.rowconfigure(1, weight=0)
        menuframe.columnconfigure(0, weight=0)
        menuheader = tk.Label(menuframe, text="Select passenger specs:", font=("Calibri", "12"), padx=5, pady=5)
        menuheader.grid(row=0, column=0, columnspan=1, sticky="nsew")

        # build "Gender" label frame, enable gender selection via radiobutton widget:
        lfGender = tk.LabelFrame(menuframe, font=("Calibri", "11"), text="Gender")
        lfGender.grid(row=1, column=0, sticky="new", padx=i, pady=i)
        rbGenderF = tk.Radiobutton(lfGender, font=("Calibri", "11"), variable=self.gendervar, value="female", text="female")
        rbGenderF.grid(row=0, column=0, sticky="nsw", padx=i, pady=i)
        rbGenderM = tk.Radiobutton(lfGender, font=("Calibri", "11"), variable=self.gendervar, value="male", text="male")
        rbGenderM.grid(row=1, column=0, sticky="nsw", padx=i, pady=i)
        rbGenderA = tk.Radiobutton(lfGender, font=("Calibri", "11"), variable=self.gendervar, value="all", text="all")
        rbGenderA.grid(row=2, column=0, sticky="nsw", padx=i, pady=i)

        # build "Age" label frame, enable age selection via checkbutton widget:
        lfAge = tk.LabelFrame(menuframe, font=("Calibri", "11"), text="Age")
        lfAge.grid(row=2, column=0, sticky="new", padx=i, pady=i)
        cbAge1 = tk.Checkbutton(lfAge, font=("Calibri", "11"), variable=self.agevar1, text="<16")
        cbAge1.grid(row=0, column=0, sticky="nsw", padx=i, pady=i)
        cbAge2 = tk.Checkbutton(lfAge, font=("Calibri", "11"), variable=self.agevar2, text="16-35")
        cbAge2.grid(row=1, column=0, sticky="nsw", padx=i, pady=i)
        cbAge3 = tk.Checkbutton(lfAge, font=("Calibri", "11"), variable=self.agevar3, text="36-55")
        cbAge3.grid(row=2, column=0, sticky="nsw", padx=i, pady=i)
        cbAge4 = tk.Checkbutton(lfAge, font=("Calibri", "11"), variable=self.agevar4, text=">55")
        cbAge4.grid(row=3, column=0, sticky="nsw", padx=i, pady=i)
        cbAgeU = tk.Checkbutton(lfAge, font=("Calibri", "11"), variable=self.agevarU, text="unknown")
        cbAgeU.grid(row=4, column=0, sticky="nsw", padx=i, pady=i)

        # build "Class" label frame, enable class selection via radiobutton widget:
        lfClass = tk.LabelFrame(menuframe, font=("Calibri", "11"), text="Class")
        lfClass.grid(row=3, column=0, sticky="new", padx=i, pady=i)
        rbClass1 = tk.Radiobutton(lfClass, font=("Calibri", "11"), variable=self.classvar, value="1", text="1st")
        rbClass1.grid(row=0, column=0, sticky="nsw", padx=i, pady=i)
        rbClass2 = tk.Radiobutton(lfClass, font=("Calibri", "11"), variable=self.classvar, value="2", text="2nd")
        rbClass2.grid(row=1, column=0, sticky="nsw", padx=i, pady=i)
        rbClass3 = tk.Radiobutton(lfClass, font=("Calibri", "11"), variable=self.classvar, value="3", text="3rd")
        rbClass3.grid(row=2, column=0, sticky="nsw", padx=i, pady=i)
        rbClassA = tk.Radiobutton(lfClass, font=("Calibri", "11"), variable=self.classvar, value="all", text="all")
        rbClassA.grid(row=3, column=0, sticky="nsw", padx=i, pady=i)

        # "Select all passengers" button
        bSelectAll = tk.Button(menuframe, font=("Calibri", "11"), text="Select all passengers", command=self.selectAll)
        bSelectAll.grid(row=4, column=0, sticky="new", padx=i, pady=i)

        # "Plot survival ratio" button
        bPlot = tk.Button(menuframe, font=("Calibri", "11"), text="Plot survival ratio", command=self.plot)
        bPlot.grid(row=5, column=0, sticky="new", padx=i, pady=i)

        # "Display passenger list" button
        bList = tk.Button(menuframe, font=("Calibri", "11"), text="Display passenger list", command=self.display)
        bList.grid(row=6, column=0, sticky="new", padx=i, pady=i)

        # "Clear" button
        bClear = tk.Button(menuframe, font=("Calibri", "11"), text="Clear", command=self.setBackground)
        bClear.grid(row=7, column=0, sticky="new", padx=i, pady=i)

        # "Close" button
        bClose = tk.Button(menuframe, font=("Calibri", "11"), text="Close", command=self.quit)
        bClose.grid(row=8, column=0, sticky="new", padx=i, pady=i)

    def setBackground(self):
        """empty plot/display area and load the background image"""

        # remove everything that might be displayed in the plot area
        for widgets in self.plotframe.winfo_children():
            widgets.destroy()

        # load background image
        background = tk.Label(self.plotframe, image=self.image)
        background.grid(row=0, column=0, padx=15, pady=15)

    def selectAll(self):
        """set all variables to True or "all" in order to select all passengers"""

        self.gendervar.set("all")
        self.classvar.set("all")
        self.agevar1.set(1)
        self.agevar2.set(1)
        self.agevar3.set(1)
        self.agevar4.set(1)
        self.agevarU.set(1)

    def plot(self):
        """plot passenger survival ratio as a pie chart in the plot/display area"""

        # if no age group has been selected, show message box and end function
        if self.agevar1.get()==0 and self.agevar2.get()==0 and self.agevar3.get()==0\
                and self.agevar4.get()==0 and self.agevarU.get()==0:
            messagebox.showinfo("No age group selected", "Please make an age selection")
            return

        # remove everything that might be displayed in the plot area
        for widgets in self.plotframe.winfo_children():
            widgets.destroy()

        # prepare figure, axis and canvas for the plot
        figure = plt.Figure()
        ax = figure.add_subplot(111)
        canvas = FigureCanvasTkAgg(figure, master=self.plotframe) # create canvas as matplotlib drawing area
        canvas.get_tk_widget().grid(column=0, row=0, sticky="nsew",padx=15, pady=15)  # Get reference to tk_widget

        # get relevant passengers dataset, number of survivors and number of fatalities
        # by calling the getData function in the titanicGetData module:
        data, survivors, fatalities = titanicGetData.getData(self.gendervar.get(),
                                                          self.agevar1.get(),
                                                          self.agevar2.get(),
                                                          self.agevar3.get(),
                                                          self.agevar4.get(),
                                                          self.agevarU.get(),
                                                          self.classvar.get())

        # for testing and better control, print return values:
        print(f"{survivors} suvivors, {fatalities} fatalities\n{data}")

        # create the pie chart showing the survival ratio for passenger specification:
        labels = "Survivors", "Fatalities"
        sizes = [survivors, fatalities]
        ax.pie(sizes, labels=labels, autopct="%1.1f%%")
        plt.show()

    def display(self):
        """display passenger list as a table in the plot/display area"""

        # if no age group has been selected, show message box and end function
        if self.agevar1.get()==0 and self.agevar2.get()==0 and self.agevar3.get()==0\
                and self.agevar4.get()==0 and self.agevarU.get()==0:
            messagebox.showinfo("No age group selected", "Please make an age selection")
            return

        # remove everything that might be displayed in the plot area
        for widgets in self.plotframe.winfo_children():
            widgets.destroy()

        # prepare display frame for the passenger list
        displayframe = tk.LabelFrame(self.plotframe, text="Passenger list", font=("Calibri","12"))
        displayframe.grid(column=0, row=0,padx=15, pady=15)

        # get relevant passengers dataset, number of survivors and number of fatalities
        # by calling the getData function in the titanicGetData module:
        data, survivors, fatalities = titanicGetData.getData(self.gendervar.get(),
                                                       self.agevar1.get(),
                                                       self.agevar2.get(),
                                                       self.agevar3.get(),
                                                       self.agevar4.get(),
                                                       self.agevarU.get(),
                                                       self.classvar.get())

        # create the table containing the passenger data
        table = Table(displayframe, dataframe=data, editable = False, font=("Calibri","11"),
                      width="670", height="550")#, showstatusbar=True, showtoolbar=True)
        table.show()

        # create the display frame:
        self.mainloop()


# on execution, create an instance of the BuildGui class, i.e. start the program:
if __name__ == "__main__":
    run = BuildGui()