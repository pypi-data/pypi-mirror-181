# importations
import tkinter
import time
import threading
import sys
#intialization
itv = 1

# class
class wheel:
    # thefunctiontoUse↓
    def setupwheel(self, list):
        self.root = tkinter.Tk()
        self.root.title('Wheel')
        self.root.minsize(300, 300)
        self.isloop = False
        self.newloop = False
        self.btn_start = tkinter.Button(
            self.root, text='start', command=self.newtaskT)
        self.btn_start.place(x=90, y=125, width=50, height=50)

        self.btn_stop = tkinter.Button(
            self.root, text='stop', command=self.newtaskF)
        self.btn_stop.place(x=160, y=125, width=50, height=50)

        self.btn1 = tkinter.Button(self.root, text=list[0], bg='white')
        self.btn1.place(x=20, y=20, width=50, height=50)

        self.btn2 = tkinter.Button(self.root, text=list[1], bg='white')
        self.btn2.place(x=90, y=20, width=50, height=50)

        self.btn3 = tkinter.Button(self.root, text=list[2], bg='white')
        self.btn3.place(x=160, y=20, width=50, height=50)

        self.btn4 = tkinter.Button(self.root, text=list[3], bg='white')
        self.btn4.place(x=230, y=20, width=50, height=50)

        self.btn5 = tkinter.Button(self.root, text=list[4], bg='white')
        self.btn5.place(x=230, y=90, width=50, height=50)

        self.btn6 = tkinter.Button(self.root, text=list[5], bg='white')
        self.btn6.place(x=230, y=160, width=50, height=50)

        self.btn7 = tkinter.Button(self.root, text=list[6], bg='white')
        self.btn7.place(x=230, y=230, width=50, height=50)

        self.btn8 = tkinter.Button(self.root, text=list[7], bg='white')
        self.btn8.place(x=160, y=230, width=50, height=50)

        self.btn9 = tkinter.Button(self.root, text=list[8], bg='white')
        self.btn9.place(x=90, y=230, width=50, height=50)

        self.btn10 = tkinter.Button(self.root, text=list[9], bg='white')
        self.btn10.place(x=20, y=230, width=50, height=50)

        self.btn11 = tkinter.Button(self.root, text=list[10], bg='white')
        self.btn11.place(x=20, y=160, width=50, height=50)

        self.btn12 = tkinter.Button(self.root, text=list[11], bg='white')
        self.btn12.place(x=20, y=90, width=50, height=50)

        self.turns = [self.btn1, self.btn2, self.btn3, self.btn4, self.btn5, self.btn6,
                      self.btn7, self.btn8, self.btn9, self.btn10, self.btn11, self.btn12]
        self.root.mainloop()
    # thefunctiontoUse↑
    # thefunctiontoUse↓
    def setinterval(self, interval):
        global itv
        itv = interval
    # thefunctiontoUse↑
    def rounds(self):
        if self.isloop == True:
            return
        i = 0
        while True:
            if self.newloop == True:
                self.newloop = False
                return
            time.sleep(itv)
            for x in self.turns:
                x['bg'] = 'white'
            self.turns[i]['bg'] = 'red'
            i += 1
            if i >= len(self.turns):
                i = 0

    def newtaskT(self):
        t = threading.Thread(target=self.rounds)
        t.start()
        self.isloop = True
        self.newloop = False

    def newtaskF(self):
        self.isloop = False
        self.newloop = True
