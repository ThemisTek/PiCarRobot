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

def ParseIm(images,i):
    global width
    global height
    base64Im = images[i]['src']
    base64Im = base64Im.split(',')[1]
    imgBytes = base64.b64decode(str(base64Im) )
    buffer = io.BytesIO(imgBytes)
    img = Image.open(buffer)
    img = img.resize((width,height))
    imTk = ImageTk.PhotoImage(image=img, master = canvas)
    return imTk

def CreateImage(images,i):
    global canvas
    global globalImage
    imageTk = ParseIm(images,i)
    canvas.itemconfigure(globalImage, image=imageTk,anchor=tkinter.CENTER)


def buttonPressed():
    global i 
    global images
    print(i)
    CreateImage(images,i)
    i +=1



btnUp = Button(window,text='up',command=buttonPressed)
btnStop = Button(window,text='stop')
btnLeft = Button(window,text='left')
btnRight = Button(window,text='right')
btnSkip = Button(window,text='skip')



btnUp.grid(column=1,row=0)
btnStop.grid(column=2,row=0)
btnLeft.grid(column=1,row=1)
btnRight.grid(column=2,row=1)
btnSkip.grid(column=3,row=0)

file = open(filename,'r')
print(filename)

fileData = file.read()
soup = bs4.BeautifulSoup(fileData)


list = soup.find_all('h4')
images = soup.find_all('img')

print(len(list))
print(len(images))


width = 128
height = 128

canvas = Canvas(window, width = width, height = height) 
canvas.grid(column=0,row=2)

im = ParseIm(images,1)
globalImage = canvas.create_image(128,128,image = im, anchor=tkinter.CENTER)

i = 0

window.mainloop()
