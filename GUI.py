from sentence import Sentence
from tkinter import *
from tkinter import messagebox
from tracker import Tracker
import sys, re

########################################
### our main GUI for the typing test ###
class GUI:
    def __init__(self, numOfSentences: int) -> None:
        #variable declaration
        self.myTracker = Tracker()
        self.numOfSentences: int = numOfSentences
        self.count = 0
        self.wordsTyped: int = 0        
        self.wordNum: int = None
        # for the GUI:
        self.root: Tk = None                # the window
        self.label1: Label = None           # the top label
        self.source: Label = None           # the string label
        self.textEntry: Text = None         # the user's entry to type in
        self.label2:Label = None            # The label for the image
        self.replayButton: Button = None    # button to replay the game
        self.__createGUI()


    def __createGUI(self):
        # GUI config 
        self.root = Tk()
        self.root.geometry('1000x520')
        self.root.title('Typing Practice')
        self.root.protocol("WM_DELETE_WINDOW", self.__onClosing)

        #configure the label that displays the starting message
        self.label1 = Label(self.root, text="Type to start...", height=3, font="Courier 11")
        self.label1.pack()

        # configure the label that displays the source string
        self.source = self.WrappingLabel(self.root)
        self.source.config(width=90, height=5, font="Courier 12 bold", anchor="w")
        self.source.pack()

        self.__fetchSentence()

        # configure the text entry
        self.textEntry = Text(self.root, width=90, height = 1,
            font="Courier 12 bold", bg="white", fg="blue", pady=3, padx=3)
        self.textEntry.pack()
        self.textEntry.bind('<Key>', self.__firstKeyHit)
        self.textEntry.bind('<KeyRelease-space>', self.__spaceAndEnterHit)
        self.textEntry.bind('<KeyRelease-Return>', self.__spaceAndEnterHit)

        # add a space between the entry text and the next label
        space = Label(self.root, height=1).pack()

        # configure image and the label that contains it
        img = PhotoImage(file="typing.png")
        self.label2 = Label(self.root, image=img).pack()

        # configure the replayButton
        self.replayButton = Button(self.label1, text="PLAY AGAIN", height=2, width=14, command=lambda:self.__replay())
        self.replayButton.config(bg="brown", fg="white", font="Courier 10 bold")

        # publish the GUI
        self.root.mainloop()


    def __fetchSentence(self):
        sentence: Sentence = self.myTracker.getNewSentence()
        line = sentence.getString()
        self.wordNum = len(re.findall(r'\w+', line))
        self.source.config(text=line)

    def __firstKeyHit(self, event):
        self.textEntry.unbind('<Key>')
        self.label1.config(text="")
        self.myTracker.startTiming()

    def __spaceAndEnterHit(self, event):
        self.wordsTyped = len(re.findall(r'\w+', self.textEntry.get('1.0', END)))
        errorsAt = self.myTracker.checkError(self.textEntry.get('1.0', END))
        self.__highlightErrors(errorsAt)
        if self.wordsTyped == self.wordNum:
            self.count += 1
            self.textEntry.delete('1.0', END)
            if self.count == self.numOfSentences:
                self.__end()
            else:
                self.__fetchSentence()

    def __highlightErrors(self, errorsAt):
        self.textEntry.tag_remove('found', '1.0', END) 
        if (len(errorsAt) > 0):
            for mistake in errorsAt:
                idx = '1.0'
                while 1:
                    idx = self.textEntry.search(mistake, idx, nocase=1, stopindex=END)
                    if not idx: break
                    lastidx = '%s+%dc' % (idx, len(mistake))
                    self.textEntry.tag_add('found', idx, lastidx) 
                    idx = lastidx
                #mark located string as red
                self.textEntry.tag_config('found', foreground='red')
                
            
    def __onClosing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            sys.exit(0)

    def __end(self):
        self.myTracker.doneTiming()
        self.textEntry.destroy()
        result = self.myTracker.getFinalResult()
        self.source.config(text = result, font = "Courier 20 bold", height=3, anchor="center")
        self.replayButton.grid(row=0, column=1, padx=10, pady=10)

    def __replay(self): 
        self.root.destroy()
        WelcomeGUI()
        
    def __from_rgb(self, rgb):
        # translates an rgb tuple of int to a tkinter friendly color code
        return "#%02x%02x%02x" % rgb   


    # A label that automatically wrap to the size
    class WrappingLabel(Label):
        def __init__(self, master=None, **kwargs):
            Label.__init__(self, master, **kwargs)
            self.bind('<Configure>', lambda e: self.config(wraplength=self.winfo_width()))




####################################################################################
### A welcome GUI where the user chooses the desired number of sentences to type ###
class WelcomeGUI:
    def __init__(self) -> None:
        # GUI config
        self.root = Tk()
        self.root.geometry('500x480')
        self.root.title('Typing Practice')

        label1 = Label(self.root, text="Please choose the number of sentences",
                       height=4, font="Courier 12 bold")
        label1.pack()

        for i in range(1, 9):
            newButton = self.__createButton(5*i)
            space = Label()
            newButton.pack()
            space.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.__onClosing)
        self.root.mainloop()


    def __createButton(self, num):
        buttonText = str(num) + " sentences"
        button = Button(self.root, text=buttonText,
                        fg="white", bg="brown", width=10,
                        command=lambda:self.__buttonCommand(num))
        return button

    def __buttonCommand(self, num):
        self.root.destroy()
        GUI(num)

    def __onClosing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            sys.exit(0)




##########################
########## MAIN ##########
##########################
if __name__ == "__main__":
    WelcomeGUI()