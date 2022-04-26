def prompt_ok(event = 0):
    global cancel, button, button1, button2
    cancel = True

    button.place_forget()
    button1 = Button(frame_photograph, text="Take", command=saveAndExit)
    button2 = Button(frame_photograph, text="Again", command=resume)
    button1.place(anchor=CENTER, x = 100, y=310)
    button2.place(anchor=CENTER, x = 170, y=310)
    button1.focus()


def saveAndExit(event = 0):
    global link_img
    global prevImg

    if (len(sys.argv) < 2):
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        timestamp = str(timestamp)
        filepath= timestamp.replace('.','_')
        filepath = filepath+".png"
    else:
        filepath = sys.argv[1]

    print ("Output file to: " + filepath)
    link_img = filepath
    prevImg.save(filepath)

    # display
    label_entrance_full = Label(frame_photograph,text='Camera and Image entrance',font=('Courier',15,'bold'),fg='#008B8B')
    label_entrance_full.place(x=140,y=10)
    image_entrance_full = Image.open(link_img)
    image_entrance_full = image_entrance_full.resize((250,250))
    img1 = ImageTk.PhotoImage(image_entrance_full)
    label_image = Label(frame_photograph,image=img1)
    label_image.image = img1
    label_image.place(x=280,y=40)
   
   

def resume(event = 0):
    global button1, button2, button, lmain, cancel

    cancel = False

    button1.place_forget()
    button2.place_forget()

    mainWindow.bind('<Return>', prompt_ok)
    button.place(x = 120,y=300)
    lmain.after(10, show_frame)

def changeCam(event=0, nextCam=-1):
    global camIndex, cap, fileName

    if nextCam == -1:
        camIndex += 1
    else:
        camIndex = nextCam
    del(cap)
    cap = cv2.VideoCapture(camIndex)

    #try to get a frame, if it returns nothing
    success, frame = cap.read()
    if not success:
        camIndex = 0
        del(cap)
        cap = cv2.VideoCapture(camIndex)

    f = open(fileName, 'w')
    f.write(str(camIndex))
    f.close()

try:
    f = open(fileName, 'r')
    camIndex = int(f.readline())
except:
    camIndex = 0

cap = cv2.VideoCapture(camIndex)
capWidth = cap.get(3)
capHeight = cap.get(4)

success, frame = cap.read()
if not success:
    if camIndex == 0:
        print("Error, No webcam found!")
        sys.exit(1)
    else:
        changeCam(nextCam=0)
        success, frame = cap.read()
        if not success:
            print("Error, No webcam found!")
            sys.exit(1)