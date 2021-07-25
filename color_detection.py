from tkinter import *
import cv2
import numpy as np
import urllib.request
import pandas as pd
from tkinter import filedialog
from PIL import ImageTk,Image
import pyperclip as pc


root = Tk()
root.title("Image Color Detection")
root.geometry("936x536+300+130")
root.configure(bg='#243B53')
image_path = ""
def open():
    global image_path
    root.filename = filedialog.askopenfilename(initialdir=r"C:\Users\7p\Desktop\temp pypro\python-project-color-detection",title="Select an image file", filetypes=(("All files","*.*"),("jpg files","*.jpg"),("png files","*.png")))
    image_path = root.filename
    print(image_path)

    # open select2 btn image
    selectimg2 = Image.open("C:/Users/7p/Desktop/temp pypro/python-project-color-detection/buttons/selectbtn2.png")
    #resize btn image
    resized2 = selectimg2.resize((200,50),Image.ANTIALIAS)

    finalimg2 = ImageTk.PhotoImage(resized2)
    my_btn.configure(image=finalimg2,state=DISABLED)
    my_btn.image=finalimg2

    root.configure(bg='#363062')
    
    return image_path

image_url=StringVar()
def urlimg():
    imgurl = image_url.get()
    url_response = urllib.request.urlopen(imgurl)
    img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)

    urlimg.image = cv2.imdecode(img_array,-1)
    image_url.set("")
    root.destroy()
   
# open urllabel btn image
urllabel = Image.open("C:/Users/7p/Desktop/temp pypro/python-project-color-detection/buttons/urllabel.png")
#resize btn image
resized3 = urllabel.resize((100,50),Image.ANTIALIAS)
finalimg3 = ImageTk.PhotoImage(resized3)

img_label = Label(root, image=finalimg3,borderwidth=0,bg='#243B53').place(x=150,y=260)


# open urlopen btn image
urlopen = Image.open("C:/Users/7p/Desktop/temp pypro/python-project-color-detection/buttons/urlopen.png")
#resize btn image
resized4 = urlopen.resize((200,50),Image.ANTIALIAS)
finalimg4 = ImageTk.PhotoImage(resized4)

url_btn=Button(root,image=finalimg4, command = urlimg,borderwidth=0,bg='#243B53').place(x=590,y=260)

img_entry = Entry(root,textvariable = image_url,width=12,font=('Roboto',26)).place(x=300,y=260)




# open select btn image
selectimg = Image.open("C:/Users/7p/Desktop/temp pypro/python-project-color-detection/buttons/selectbtn.png")
#resize btn image
resized = selectimg.resize((200,50),Image.ANTIALIAS)
finalimg = ImageTk.PhotoImage(resized)

my_btn = Button(root,image=finalimg,command=open,borderwidth=0,bg='#243B53')
my_btn.place(x=100,y=150)

# open start btn image
openimg = Image.open("C:/Users/7p/Desktop/temp pypro/python-project-color-detection/buttons/startbtn1.png")
#resize btn image
resized1 = openimg.resize((118,50),Image.ANTIALIAS)
finalimg1 = ImageTk.PhotoImage(resized1)

strt_btn = Button(root,image=finalimg1,command=root.quit,borderwidth=0,bg='#243B53').place(x=620,y=155)



root.mainloop()


if image_path == "":
    img = urlimg.image
else :    
    #Reading the image with opencv
    img = cv2.imread(image_path)


#declaring global variables (are used later on)
clicked = False
r = g = b = hexcode = xpos = ypos = 0

#Reading csv file with pandas and giving names to each column
index=["color","color_name","hex","R","G","B"]
csv = pd.read_csv('C:/Users/7p/Desktop/temp pypro/python-project-color-detection/colors.csv', names=index, header=None)

#function to calculate minimum distance from all colors and get the most matching color
def getColorName(R,G,B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            getColorName.cname = csv.loc[i,"color_name"]
            getColorName.hexcode = csv.loc[i,"hex"]
   

#function to get x,y coordinates of mouse double click
def draw_function(event, x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b,g,r,xpos,ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)

   
cv2.namedWindow('Image Color Detection')


cv2.setMouseCallback('Image Color Detection',draw_function)

while(1):

    cv2.imshow("Image Color Detection",img)
    if (clicked):

        #scale text according to image size
        imageWidth = img.shape[0]
        imageHeight = img.shape[1]

        fontScale = min(imageWidth,imageHeight)/(800)

        #cv2.rectangle(image, startpoint, endpoint, color, thickness)-1 fills entire rectangle 
        cv2.rectangle(img,(50,10), (max(imageWidth,imageHeight),50), (b,g,r), -1)

        getColorName(r,g,b)
        #Creating text string to display( Color name and RGB values )
        text = getColorName.cname + ' R='+ str(r) +  ' G='+ str(g) +  ' B='+ str(b) +" "+ getColorName.hexcode

        #copying color code to clipboard
        pc.copy(getColorName.hexcode)
        
        #scale text according to image size
        imageWidth = img.shape[0]
        imageHeight = img.shape[1]

        fontScale = min(imageWidth,imageHeight)/(800)

        #cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
        cv2.putText(img, text,(50,40),2,fontScale,(255,255,255),1,cv2.LINE_AA)

        #For very light colours we will display text in black colour
        if(r+g+b>=600):
            cv2.putText(img, text,(50,40),2,fontScale,(0,0,0),1,cv2.LINE_AA)
            
        clicked=False

    #Break the loop when User hits 'enter' key    
    if cv2.waitKey(20) & 0xFF ==13:
        break
  
cv2.destroyAllWindows()




