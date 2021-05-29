import tkinter
from tkinter import Canvas
from tkinter import Button, filedialog as fd
from tkinter.constants import ANCHOR
from PIL import ImageTk,Image
import base64
import bs4
import io


filename = fd.askopenfilename()
window = tkinter.Tk()

file = open(filename,'r')
fileDescr = filename.split("/")[-1].replace('.html','')
print(filename)

fileData = file.read()
soup = bs4.BeautifulSoup(fileData)

hList = soup.find_all('h4')
images = soup.find_all('img')


class TkinterWindow():
    def __init__(self,window,images,hList,name):
        self.window = window
        self.images = images
        self.hlist = hList
        self.i = 0
        self.total = len(images)
        self.width = 250
        self.height = 250

        self.btnUp = Button(window,text='up',command= lambda : self.buttonPressed('up'))
        self.btnStop = Button(window,text='stop',command= lambda : self.buttonPressed('stop'))
        self.btnLeft = Button(window,text='left',command= lambda : self.buttonPressed('left'))
        self.btnRight = Button(window,text='right',command= lambda : self.buttonPressed('right'))
        self.btnSkip = Button(window,text='skip',command= lambda : self.buttonPressed('skip'))
        self.btnUp.grid(column=1,row=0)
        self.btnStop.grid(column=2,row=0)
        self.btnLeft.grid(column=1,row=1)
        self.btnRight.grid(column=2,row=1)
        self.btnSkip.grid(column=3,row=0)
        self.name = name

        self.canvas = Canvas(self.window, width = self.width, height = self.height) 
        self.im = self.ParseIm(self.images,1)[0]
        self.tKinterIm = self.canvas.create_image(128,128,image = self.im)
        self.canvas.grid(column=0,row=2)
        self.CreateImageList()
        self.window.mainloop()
    
    def CreateImageList(self):
        v = 0
        self.ParsedIms = []
        for srcIm in self.images:
            result = self.ParseIm(self.images,v)
            tKinterIm = result[0]
            pIm = result[1]
            tupl = (tKinterIm,pIm)
            self.ParsedIms.append(tupl)
            v+=1

    
    def ParseIm(self,images,i):
        global width
        global height
        base64Im = images[i]['src']
        base64Im = base64Im.split(',')[1]
        print(len(base64Im))
        imgBytes = base64.b64decode(str(base64Im) )
        buffer = io.BytesIO(imgBytes)
        img = Image.open(buffer)
        img = img.resize((self.width,self.height))
        imTk = ImageTk.PhotoImage(image=img, master = self.canvas)
        return imTk, img

    def buttonPressed(self,imageType):
        print(self.i)
        if(self.i >= self.total):
            return None
        self.canvas.itemconfig(self.tKinterIm, image=self.ParsedIms[self.i][0])
        self.i +=1
        if(imageType != 'skip'):
            print(imageType)
            self.saveImage(imageType)

    def saveImage(self,imageType):
        pIm = self.ParsedIms[self.i][1]
        fileName = f'{self.name}-{imageType}-{self.i}.png'
        placeToSave = f'./desktop/AllImages/{imageType}/{fileName}'
        print(placeToSave)
        pIm.save(placeToSave)
            

tKinterClass = TkinterWindow(window,images,hList,fileDescr)
