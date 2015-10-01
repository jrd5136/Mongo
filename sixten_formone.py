from Tkinter import *
import Tkinter as tk
import re
import pymongo

# Class that creates the main query frame
# and performs DB operations using the pymongo driver for all the database operations

class App(object):
    

    def findRecord(self,field,searchString):
        try:
           
            client = pymongo.MongoClient('74.67.180.218',27017)
            client.prj.authenticate('appuser','ISTE610krt',source='prj')
            print "Server connection made     : ", client
        except pymongo.errors.ConnectionFailure, e:
            print "Could not connect to MongoDB: %s" % e
            print client

        print "Server connection made     : ", client
        db = client.prj
        
        print "Database connection made   : ", db

        tw = db.stack
        
        print "Collection connection made : ", tw
        
        count = 1
        self.resultList.delete(0,END)
        regx = re.compile(".*"+searchString+".*", re.IGNORECASE)
        for post in tw.find({field: regx},{'field':1, 'Title':1,'_id':0},limit=30):
    
            for item in post:
                self.resultList.grid(row=5, columnspan=3, sticky="WE", ipady=10, ipadx=10)
                temp1 = "  " + str(count) + ".  " + post['Title']
                count +=1
                self.resultList.insert(END, temp1)
                self.resultList.bind('<<ListboxSelect>>', self.onDouble)


# Function to connect to database

    def ConnectToDb(self):
        try:
            client = pymongo.MongoClient('74.67.180.218',27017)
            client.prj.authenticate('appuser','ISTE610krt',source='prj')
            print "Server connection made     : ", client 
            connMessage = "Connected successfully!!!"
            self.label = Label (master, text=connMessage)
            self.label.grid(row=2, column=0, pady=5, padx=5, sticky="WE")
            db = client.prj
            print "Database connection made   : ", db
            ab = 'This is a comment'
            c = '1' + ' ' + ab
            print c

        except pymongo.errors.ConnectionFailure, e:
            print "Could not connect to MongoDB: %s" % e
        
        print db.collection_names()
        print db.stack.find_one()
        print db.images.find_one()
        return connMessage

# Function to process the result list

    def onDouble(self, event):
        client = pymongo.MongoClient('74.67.180.218',27017)
        client.prj.authenticate('appuser','ISTE610krt',source='prj')
        
        db = client.prj
        tw = db.stack
        widget = event.widget
        selection = map(int,widget.curselection())
        value = widget.get(selection[0])
        value = re.sub('  [0-9]+.  ', '', value)
        tw.update({'Title': value },{'$set':{'counter': 0 }})
        subFrame = appwindow(self,value)

    def show(self):
        pass

# Function that initializes the main window

    def __init__(self, master):

        master.grid()
        master.title("Query Console")
        master.geometry("650x650")
       
        
        #Create label        
        self.projLabel = Label(master, text="Stack Overflow Questions",font = "Helvetica 16 bold italic")
        self.projLabel.grid(row=0, pady=5, sticky="W", columnspan=2)
        
        self.connectButton = Button( master, text="Connect!",command=self.ConnectToDb)
        self.connectButton.grid(row=1, column=0, pady=5, padx=5, sticky="W")
       

        self.entryVariable = StringVar()
        self.entry = Entry(master,textvariable=self.entryVariable,width=100)
        self.entry.grid(row=3, column=0, columnspan=1, pady=5, padx=3, sticky="W")
        self.entryVariable.set(u"Enter search text here.")


        self.searchButton = Button (master, text="Search",command=lambda:self.findRecord('Title',self.entry.get()))
        self.searchButton.grid(row=3, column=1, padx=5, pady=5, sticky="W")


        self.resultList = Listbox(master,width=50, height=29)
        self.resultList.grid(row=5, columnspan=5, sticky="WE")


        self.radio_var = IntVar()
        
        master.grid_columnconfigure(0,weight=1)
        master.resizable(True,False)
    

    def create_window(self):
        t = tk.Toplevel(self)

# Class that creates the main query frame
# and performs DB operations using the pymongo driver for all the database operations

class appwindow(tk.Toplevel):

# Functions and sub methods for all the database operations and UI components creation

    def find(self,key):
        try:
            
            client = pymongo.MongoClient('74.67.180.218',27017)
            client.prj.authenticate('appuser','ISTE610krt',source='prj')
            print "Server connection made     : ", client 
        except pymongo.errors.ConnectionFailure, e:
            print "Could not connect to MongoDB: %s" % e
        db = client.prj #myFirstDb is the DB I am trying to connect to
        print "Database connection made   : ", db
        tw = db.stack
        print "Collection connection made : ", tw

    def __init__(self, origional, key):
      
        try:
            
            client = pymongo.MongoClient('74.67.180.218',27017)
            client.prj.authenticate('appuser','ISTE610krt',source='prj')
            print "Server connection made     : ", client
        except pymongo.errors.ConnectionFailure, e:
            print "Could not connect to MongoDB: %s" % e

        db = client.prj
        print "Database connection made   : ", db
        tw = db.stack
        print "Collection connection made : ", tw
        images = db.images
        print "Collection connection made : ", images

        
        self.origional_frame = origional
        tk.Toplevel.__init__(self)
        self.title("Question Details")

        self.grid()
        
        self.configure(background="white")

        #Create form label
        projLabel = Label(self, text="Stack Overflow Question Details", background="white", font = "Helvetica 16 bold italic")
        projLabel.pack()
        projLabel.grid(row=0, pady=5, sticky="W", columnspan=4)

        #Create title label
        titleLabel = Label(self, text="Title:", background="white", anchor=N)
        titleLabel.grid(row=1, padx=5, pady=5, sticky="W", column=0)

        #Create the field to hold the title of the docuemnt
        
        for post in tw.find({'Title':key}):
            ids = post['PostId']

            for m in tw.find({'PostId':ids}):
                    titleText = StringVar()
                    titleText.set (post['Title'])
                    titleText = Label(self, textvariable=titleText,
                                      justify=LEFT, background="white",
                                      padx=5, pady=5)
                    titleText.grid(row=1, column=1, columnspan=3, sticky="W")


        #Create body label
        bodyLabel = Label(self, text="Body:", background="white", anchor=N)
        bodyLabel.grid(row=2, padx=5, pady=5, sticky="W", column=0)
        

        #Create the field to hold the body of the docuemnt
        for post in tw.find({'Title':key}):
            ids = post['PostId']
            for m in tw.find({'PostId':ids}):
                T = Text(self, height=4, width=70,font=("Helvetica",13))
                T.insert(END,post['BodyMarkdown'])
                T.grid(row=2, padx=5, pady=5, sticky="W", column=1,columnspan=4)
        
        #Create date label
        dateLabel = Label(self, text="Create Date:", background="white")
        dateLabel.grid(row=3, padx=5, pady=5, sticky="W", column=0)

        #Create the field to hold the post date of the doc
        for post in tw.find({'Title':key}):
            ids = post['PostId']
            for m in tw.find({'PostId':ids}):
                dateText = StringVar()
                dateText.set (post['PostCreationDate'])
                dateText = Label(self, textvariable=dateText, justify=LEFT, background="white")
                dateText.grid(row=3, column=1, columnspan=3, sticky="W", padx=5, pady=5)

        #Create the tags label
        tagLabel = Label ( self, text="Tags:", justify=LEFT, background="white", anchor=N)
        tagLabel.grid(row=4, column=0, sticky="W")
        index = 1
        for post in tw.find({'Title':key}):
            tags = [post['Tag1'],post['Tag2'],post['Tag3'],post['Tag4'],post['Tag5']]

            for i in tags:
                for item in db.images.find({'tag':i}):
                    str = 'img/'+item['image']
                    print str
                    photoImage =PhotoImage(file=str)
                    imageLabel = Label(self, image=photoImage, anchor=N, background="white")
                    imageLabel.grid(row=4, column= index, sticky="NSWE")
                    imageLabel.image = photoImage
                    index = index+1

                    

        commentLabel = Label(self, text="Add/Edit Comments",
                             background="white", padx=5, pady=5, font=(20),
                             anchor=W, justify=LEFT)
        commentLabel.grid(row=5, pady=5, sticky="W", columnspan=4)

        commentLabel = Label (self, text="Comment:", background="white",
                              anchor=W)
        commentLabel.grid(row=6, column=0, sticky=W)

        commentEntry = Entry (self, bg="Gainsboro", width=50)
        commentEntry.grid(row=6, column=1, columnspan=4, sticky=W)
        
        i= 0
        saveButton = Button(self, text="Save", anchor=S, command=lambda:self.updateDoc(commentEntry.get(),post['PostId']))
        saveButton.grid(row=7, rowspan=2, column=1, sticky="W")

        saveButton = Button(self, text="Close", anchor=S, command=self.closeWindow)
        saveButton.grid(row=7, rowspan=2, column=2, sticky="W")

        commentLabel = Label (self, text="Comments", background="white",
                      anchor=W,font = "Helvetica 16 bold italic")
        commentLabel.grid(row=10, column=0, sticky=W)

        list=[]
        for post in tw.find({'Title':key}):
            ids = post['PostId']
            for m in tw.find({'PostId':ids}):
                rowindex=11
                for key,value in m.iteritems():
                    if key.startswith('comment'):
                        print value
                        commentLabel = Label(self, text=value,
                        background="white", padx=5, pady=5, font=(20),
                        anchor=W, justify=LEFT)
                        commentLabel.grid(row=rowindex, pady=5, sticky="W", columnspan=4)
                        rowindex = rowindex + 1


    def closeWindow(self):
        self.destroy()

# Function that inserts new comment feild to the db

    def updateDoc(self, comment, postid):
        try:
            client = pymongo.MongoClient('74.67.180.218',27017)
            client.prj.authenticate('appuser','ISTE610krt',source='prj')
        except pymongo.errors.ConnectionFailure, e:
            print "Could not connect to MongoDB: %s" % e

        count = 0
        db = client.prj
        tw = db.stack
        print postid
        
        for i in tw.find({'PostId':postid}):
            print i
            print tw.update({'PostId': postid },{'$inc':{'counter': 1 }})
            print i['counter']

            print tw.update({'PostId': postid },{'$set':{'comment'+str(i['counter']): comment }},upsert=False)


# main method

if __name__ == '__main__':
    master = Tk()
    app = App(master)
    mainloop()