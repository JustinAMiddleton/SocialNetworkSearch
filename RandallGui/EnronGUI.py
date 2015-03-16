'''
Created on Feb 16, 2015

@author: Randy
'''
from Tkinter import *
class App:
    
    def __init__(self, master):
        attribute1 = "Attribute 1"
        attribute2 = "Attribute 2"
        attribute3 = "Attribute 3"
        attribute4 = "Attribute 4"
        attribute5 = "Attribute 5"
        
        self.v1 = IntVar()
        self.v2 = IntVar()
        self.v3 = IntVar()
        self.v4 = IntVar()
        self.v5 = IntVar()
        
        frame = Frame(master)
        frame.pack()
        master.title("Whistleblower Dataset Analysis")
        master.geometry('300x230-625+200')   
        Label(frame, text="File Location: ").grid(row=0, column=0, pady=4)
        fileLocation = Entry(frame)
        fileLocation.configure(width=14)
        fileLocation.grid(row=0, column=3)
        browse = Button(frame, text="Browse")
        browse.configure(width=10)
        browse.grid(row=0, column=5)

        Label(frame, text=attribute1).grid(row=1)
        Button(frame, text="Define Attribute", command=self.defineAttribute).grid(row=1, column=3,
                                             sticky=W, pady=4)
        Button(frame, text="X", command=self.resetAttribute).grid(row=1, column=4, padx=4)
        attr1Weight = StringVar(frame)
        attr1Weight.set("Weight")
        weight = OptionMenu(frame, attr1Weight, "High", "Medium", "Low")
        weight.grid(row=1, column=5)

        Label(frame, text=attribute2).grid(row=2, pady=4)
        Button(frame, text="Define Attribute", command=self.defineAttribute).grid(row=2, column=3,
                                                           sticky=W, pady=4)
        Button(frame, text="X", command=self.resetAttribute).grid(row=2, column=4, padx=4)
        attr2Weight = StringVar(frame)
        attr2Weight.set("Weight")
        weight = OptionMenu(frame, attr2Weight, "High", "Medium", "Low")
        weight.grid(row=2, column=5)

        Label(frame, text=attribute3).grid(row=3, pady=4)
        Button(frame, text="Define Attribute", command=self.defineAttribute).grid(row=3, column=3,
                                                           sticky=W, pady=4)
        Button(frame, text="X", command=self.resetAttribute).grid(row=3, column=4, padx=4)
        attr3Weight = StringVar(frame)
        attr3Weight.set("Weight")
        weight = OptionMenu(frame, attr3Weight, "High", "Medium", "Low")
        weight.grid(row=3, column=5)

        Label(frame, text=attribute4).grid(row=4, pady=4)
        Button(frame, text="Define Attribute", command=self.defineAttribute).grid(row=4, column=3,
                                                           sticky=W, pady=4)
        Button(frame, text="X", command=self.resetAttribute).grid(row=4, column=4, padx=4)
        attr4Weight = StringVar(frame)
        attr4Weight.set("Weight")
        weight = OptionMenu(frame, attr4Weight, "High", "Medium", "Low")
        weight.grid(row=4, column=5)
        
        Label(frame, text=attribute5).grid(row=5, pady=4)
        Button(frame, text="Define Attribute", command=self.defineAttribute).grid(row=5, column=3,
                                                            sticky=W, pady=4)
        Button(frame, text="X", command=self.resetAttribute).grid(row=5, column=4, padx=4)
        attr5Weight = StringVar(frame)
        attr5Weight.set("Weight")
        weight = OptionMenu(frame, attr5Weight, "High", "Medium", "Low")
        weight.grid(row=5, column=5)
        
        searchButton = Button(frame, text="Search").grid(row=7, column=3, sticky=W, padx=20)
    
    def defineAttribute(self):
        self.toplevel= Toplevel()
        self.toplevel.title('Define Attribute')
        self.toplevel.geometry('450x210-160+200')
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
#         Radiobutton(frame, text="Positive", variable=self.v1)
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
        
        Label(frame, text="Word 5: ").grid(row=5, column=0, sticky=E)
        e5 = Entry(frame)
        e5.grid(row=5, column=1)
        
        var5 = StringVar(self.toplevel)
        var5.set("Weight")
        weight = OptionMenu(frame, var5, "High", "Medium", "Low")
        weight.grid(row=5, column=2)
        self.pos5 = Radiobutton(frame, text="Positive", variable=self.v5, value=1, indicatoron=0)
        self.pos5.grid(row=5, column=3)
        self.neg5 = Radiobutton(frame, text="Negative", variable=self.v5, value=2, indicatoron=0)
        self.neg5.grid(row=5, column=4)
        
        Button(frame, text="Save").grid(row=6, column=2, pady=4)
        
    def resetAttribute(self):
        self.pos1.deselect()
        self.neg1.deselect()
        self.pos2.deselect()
        self.neg2.deselect()
        self.pos3.deselect()
        self.neg3.deselect()
        self.pos4.deselect()
        self.neg4.deselect()
        self.pos5.deselect()
        self.neg5.deselect()
root=Tk()
app = App(root)
root.mainloop()