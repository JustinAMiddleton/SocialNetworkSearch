'''
Created on Feb 18, 2015

@author: Randy
'''
from Tkinter import *
class App():
    attribute1 = "Attribute 1"
    defAtt = "Define Attribute"
    #words = list["yo", "whats", "up", "dawg"]
    
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        master.title("Whistleblower Analysis")
        master.geometry('-625+200')

        Label(frame, text="Attributes").grid(row=0, column=0, pady=4)
        Label(frame, text="Web Sites").grid(row=0, column=3)
        
        Label(frame, text=self.attribute1).grid(row=1, column=0)
        Button(frame, text=self.defAtt, command=self.defineAttribute).grid(
                            row=1, column=1, pady=4)
        Button(frame, text="X", command=self.resetAttribute).grid(row=1, column=2, padx=5)
        
        Label(frame, text="Attribute 2").grid(row=2, column=0)
        Button(frame, text=self.defAtt, command=self.defineAttribute).grid(
                            row=2, column=1, pady=4)
        Button(frame, text="X", command=self.resetAttribute).grid(row=2, column=2, padx=5)
        
        Label(frame, text="Attribute 3").grid(row=3, column=0)
        Button(frame, text=self.defAtt, command=self.defineAttribute).grid(
                            row=3, column=1, pady=4)
        Button(frame, text="X").grid(row=3, column=2, padx=5)
        
        Button(frame, text="Search", command=self.displayResults).grid(row=4, column=1)
        Button(frame, text="Stop").grid(row=5, column=1, pady=4)
        
        var=StringVar(master)
        var.set("Select Date")
        option = OptionMenu(frame, var, "Live Stream", "Last 30 Days",
                            "Last 90 Days", "Past Year").grid(row=4, column=3)
        
        self.v1 = IntVar()
        self.v2 = IntVar()
        self.v3 = IntVar()
        self.v4 = IntVar()
        
        var1 = IntVar()
        Checkbutton(frame, text="Twitter", variable=var1).grid(row=1,
                            column=3, sticky=W, padx=15)
        var2 = IntVar()
        Checkbutton(frame, text="Google+", variable=var2).grid(row=2,
                            column=3, sticky=W, padx=15)
        
    def defineAttribute(self):
        self.toplevel= Toplevel()
        self.toplevel.title('Define Attribute')
        self.toplevel.geometry('450x180-160+200')
        self.toplevel.focus_set()
        frame = Frame(self.toplevel)
        frame.pack()
        
        Label(frame, text="Attribute Name: ").grid(row=0, column=0)
        self.attribute1 = Entry(frame)
        self.attribute1.grid(row=0, column=1)
        
        Label(frame, text="Word 1: ").grid(row=1, column=0, sticky=E)
        #self.attr1Word1 = self.words[0]
        self.attr1Word1 = Entry(frame)
        self.attr1Word1.grid(row=1, column=1)
        
        var1 = StringVar(self.toplevel)
        var1.set("Weight")
        weight = OptionMenu(frame, var1, "High", "Medium", "Low")
        weight.grid(row=1, column=2)
        self.pos1 = Radiobutton(frame, text="Positive", variable=self.v1, value=1, indicatoron=0)
        self.pos1.grid(row=1, column=3, padx=4)
        self.neg1 = Radiobutton(frame, text="Negative", variable=self.v1, value=2, indicatoron=0)
        self.neg1.grid(row=1, column=4, padx=4)
        
        Label(frame, text="Word 2: ").grid(row=2, column=0, sticky=E)
        self.e2 = Entry(frame)
        self.e2.grid(row=2, column=1)
        
        var2 = StringVar(self.toplevel)
        var2.set("Weight")
        weight = OptionMenu(frame, var2, "High", "Medium", "Low")
        weight.grid(row=2, column=2)
        self.pos2 = Radiobutton(frame, text="Positive", variable=self.v2, value=1, indicatoron=0)
        self.pos2.grid(row=2, column=3)
        self.neg2 = Radiobutton(frame, text="Negative", variable=self.v2, value=2, indicatoron=0)
        self.neg2.grid(row=2, column=4)
        
        Label(frame, text="Word 3: ").grid(row=3, column=0, sticky=E)
        e3 = Entry(frame)
        e3.grid(row=3, column=1)
        
        var3 = StringVar(self.toplevel)
        var3.set("Weight")
        weight = OptionMenu(frame, var3, "High", "Medium", "Low")
        weight.grid(row=3, column=2)
        self.pos3 = Radiobutton(frame, text="Positive", variable=self.v3, value=1, indicatoron=0)
        self.pos3.grid(row=3, column=3)
        self.neg3 = Radiobutton(frame, text="Negative", variable=self.v3, value=2, indicatoron=0)
        self.neg3.grid(row=3, column=4)
        
        Label(frame, text="Word 4: ").grid(row=4, column=0, sticky=E)
        e4 = Entry(frame)
        e4.grid(row=4, column=1)
        
        var4 = StringVar(self.toplevel)
        var4.set("Weight")
        weight = OptionMenu(frame, var4, "High", "Medium", "Low")
        weight.grid(row=4, column=2)
        self.pos4 = Radiobutton(frame, text="Positive", variable=self.v4, value=1, indicatoron=0)
        self.pos4.grid(row=4, column=3)
        self.neg4 = Radiobutton(frame, text="Negative", variable=self.v4, value=2, indicatoron=0)
        self.neg4.grid(row=4, column=4)
        
        Button(frame, text="Save", command=self.saveWords).grid(row=5, column=2, pady=4)
        
    def testResize(self):
        Button(self.frame, text="Search")

    def resetAttribute(self):
        self.pos1.deselect()
        self.neg1.deselect()
        self.pos2.deselect()
        self.neg2.deselect()
        self.pos3.deselect()
        self.neg3.deselect()
        self.pos4.deselect()
        self.neg4.deselect()
        
    def saveWords(self):
        #words = list(self.attr1Word1, self.e2)
        self.toplevel.destroy()
        
    def displayResults(self):
        resultsPage = Toplevel()
        resultsPage.title("Results")
        resultsPage.focus_set()
        resultsFrame = Frame(resultsPage)
        resultsFrame.pack()
        
        Label(resultsFrame, text="Top Results").grid(row=0, column=1)
        Label(resultsFrame, text="Users").grid(row=1, column=0)
        Label(resultsFrame, text="Score").grid(row=1, column=1)
        Label(resultsFrame, text="View Links").grid(row=1, column=2)
        
root=Tk()
app = App(root)
root.mainloop()