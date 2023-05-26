
from enum import auto
from itertools import count
import tkinter as tk
# import tk
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
from turtle import back, heading
import cv2
import os
import csv
import numpy as np
import pyttsx3
from PIL import Image
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import datetime
import time
import face_recognition
import yagmail
import qrcode



global email
email = "facialcheckin.software@gmail.com"

emailpass = open("AdminDetails/mail_password.txt", "r")
mail_password = emailpass.read()

time_format = 24
new_face_recognised = True

background_color = '#16281A'
frame_color = '#548C4F'
heading_color = '#B8CF69'


def id_card(a_id,b_name,c_mail):
    image = Image.new('RGB', (1000, 700), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('arial.ttf', size=45)


    (x, y) = (480, 75)
    idno = a_id
    message = str('ID: ' + str(idno))
    color = 'rgb(0, 0, 0)'  # black color
    font = ImageFont.truetype('arial.ttf', size=60)
    draw.text((x, y), message, fill=color, font=font)

    (x, y) = (50, 190)
    message = b_name
    name = message
    message = str('Name: ' + str(message))
    color = 'rgb(0, 0, 0)'  # black color
    font = ImageFont.truetype('arial.ttf', size=45)
    draw.text((x, y), message, fill=color, font=font)

    (x, y) = (50, 250)
    message = c_mail
    did = message
    message = str('MailId: ' + str(message))
    color = 'rgb(0, 0, 0)'  # black color
    font = ImageFont.truetype('arial.ttf', size=45)
    draw.text((x, y), message, fill=color, font=font)

    # save the edited image

    image.save("IDcard/"+str(name) + '.jpg')

    img = qrcode.make(str(idno))  # this info. is added in QR code, also add other things
    img.save("IDcard/"+str(idno) + '.bmp')

    til = Image.open("IDcard/" + name + '.jpg')
    im = Image.open("IDcard/" + str(idno) + '.bmp')  # 25x25
    photo_attendee = Image.open("IDcard/recent_attendee" + '.jpg')
    til.paste(im, (50, 300))
    til.paste(photo_attendee, (650, 300))
    til.save("IDcard/" + name + '.png')



def qrcode_mail(a_id,b_name,c_mail):
        receiver = c_mail  # receiver email address
        body = "Your ID card is attached with the mail.\n\n\nRegards,\nFacial Check-IN Software Team"  # email body
        filename = "IDcard"+os.sep+b_name+".png"  # attach the file

        # mail information
        yag = yagmail.SMTP("facialcheckin.software@gmail.com", mail_password)

        # sent the mail
        yag.send(
            to=receiver,
            subject="Attendee's IDcard",  # email subject
            contents=body,  # email body
            attachments=filename,  # file attached
        )





def automail(test):
    #correction
    print(test)

    for i in test:
        if i =='' or i=='facialcheckin.software@gmail.com':
            continue
        else:
            receiver = i  # receiver email address
            body = "Your presence is marked.\n\n\nRegards,\nFacial Check-IN Software Team"  # email body
            # mail information
            yag = yagmail.SMTP("facialcheckin.software@gmail.com", mail_password)
            # sent the mail
            yag.send(
            to=receiver,
            subject="Checked-IN",  # email subject
            contents=body,  # email body
            )



def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()



def admin_face():
    video_capture = cv2.VideoCapture(0)

    # Load a sample picture and learn how to recognize it.
    admin_image = face_recognition.load_image_file("AdminDetails/admin.jpg")
    admin_face_encoding = face_recognition.face_encodings(admin_image)[0]

    # Load a second sample picture and learn how to recognize it.


    # Create arrays of known face encodings and their names
    known_face_encodings = [
        admin_face_encoding,
    ]
    known_face_names = [
        "Admin"
    ]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            if name == 'Admin':
                video_capture.release()
                cv2.destroyAllWindows()
                TrainImages()
                speak("Facial Identification Successful..!!    Your ID card has been sent to the registered Mail ID")
                break

            else:
                speak("Admin's face mismatched.. Unable to save the profile")
                mess._show(title='Wrong Password', message='This is not Admin\'s face. Profile not saved')
                break


    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()


def attendee_photo():
    cam = cv2.VideoCapture(0)
    speak("Please look at the camera,  capturing image for ID card")
    while True:
        ret, img = cam.read()
        cv2.imshow("Attendee's Image", img)

        if not ret:
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            file="IDcard"+os.sep+"recent_attendee"+".jpg"
            cv2.imwrite(file, img)
            cam.release()
            cv2.destroyAllWindows()
            break

    im = Image.open('IDcard/recent_attendee.jpg')
    xcenter = im.width/2
    ycenter = im.height/2

    cropped = im.crop((xcenter-220,ycenter-220,xcenter+220,ycenter+220))
    cropped.save('IDcard/recent_attendee.jpg')
    #cropped.show()    

    cam.release
    cv2.destroyAllWindows    




def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)


def tick_24():
    global time_format
    #print("24 Format")
    if time_format == 12:
        return
    else:
        time_string = time.strftime('%H:%M:%S')
        clock.config(text=time_string)
        clock.after(1000,tick_24)

def tick_12():
    global time_format
    #print("12 Format")
    if time_format == 24:
        return
    else:    
        time_string = time.strftime('%I:%M:%S %p')
        clock.config(text=time_string)
        clock.after(1000,tick_12)


def time_format_change():
    global time_format
    if time_format == 12:
        time_format = 24
        tick_24()

    else:
        time_format = 12
        tick_12()                    



def contact():
    mess._show(title='Contact us', message="Please contact us on : facialcheckin.software@gmail.com ")


def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='Some file missing', message='Please contact us for help')
        window.destroy()

def save_pass():
    assure_path_exists("AdminDetails/")
    exists1 = os.path.isfile("AdminDetails\entry_password.txt")
    if exists1:
        tf = open("AdminDetails\entry_password.txt", "r")
        key = tf.read()
    else:
        master.destroy()
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("AdminDetails\entry_password.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    op = (old.get())
    newp= (new.get())
    nnewp = (nnew.get())
    if (op == key):
        if(newp == nnewp):
            txf = open("AdminDetails\entry_password.txt", "w")
            txf.write(newp)
        else:
            mess._show(title='Error', message='Confirm new password again!!!')
            return
    else:
        mess._show(title='Wrong Password', message='Please enter correct old password.')
        return
    mess._show(title='Password Changed', message='Password changed successfully!!')
    master.destroy()


def change_pass():
    global master
    master = tk.Tk()
    master.geometry("400x160")
    master.resizable(False,False)
    master.title("Change Password")
    master.configure(background="white")
    lbl4 = tk.Label(master,text='    Enter Old Password',bg='white',font=('times', 12, ' bold '))
    lbl4.place(x=10,y=10)
    global old
    old=tk.Entry(master,width=25 ,fg="black",relief='solid',font=('times', 12, ' bold '),show='*')
    old.place(x=180,y=10)
    lbl5 = tk.Label(master, text='   Enter New Password', bg='white', font=('times', 12, ' bold '))
    lbl5.place(x=10, y=45)
    global new
    new = tk.Entry(master, width=25, fg="black",relief='solid', font=('times', 12, ' bold '),show='*')
    new.place(x=180, y=45)
    lbl6 = tk.Label(master, text='Confirm New Password', bg='white', font=('times', 12, ' bold '))
    lbl6.place(x=10, y=80)
    global nnew
    nnew = tk.Entry(master, width=25, fg="black", relief='solid',font=('times', 12, ' bold '),show='*')
    nnew.place(x=180, y=80)
    cancel=tk.Button(master,text="Cancel", command=master.destroy ,fg="white"  ,bg="blue" ,height=1,width=25 , activebackground = "white" ,font=('times', 10, ' bold '))
    cancel.place(x=200, y=120)
    save1 = tk.Button(master, text="Save", command=save_pass, fg="white", bg="purple", height = 1,width=25, activebackground="white", font=('times', 10, ' bold '))
    save1.place(x=10, y=120)
    master.mainloop()


def psw():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("AdminDetails\entry_password.txt")
    if exists1:
        tf = open("AdminDetails\entry_password.txt", "r")
        key = tf.read()
    else:
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("AdminDetails\entry_password.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    password = tsd.askstring('Password', 'Enter Password', show='*')
    if (password == key):
        TrainImages()
        speak("Facial Identification Successful..!!    Your ID card has been sent to the registered Mail ID")
    elif (password == None):
        pass
    else:
        speak("Entered password mismatched...!!    Unable to save the profile")
        mess._show(title='Wrong Password', message='You have entered wrong password')


def change_theme():
    global background_color
    global frame_color
    global heading_color
    global time_format
    global new_face_recognised

    if(new_face_recognised):
        new_face_recognised = False

    elif(frame_color == '#FFF9BA'):
        background_color = '#16281A'
        frame_color = '#548C4F'
        heading_color = '#B8CF69'

    else:    
        background_color = '#441507'
        frame_color = '#FFF9BA'
        heading_color = '#EFD033'
    
    window.configure(background=background_color)
    frame1 = tk.Frame(window, bg=frame_color)
    frame1.place(relx=0.0, rely=0.17, relwidth=0.50, relheight=0.80)

    frame2 = tk.Frame(window, bg=frame_color)
    frame2.place(relx=0.51, rely=0.17, relwidth=0.50, relheight=0.80)

    message3 = tk.Label(window, text="Facial Check-IN Software" ,fg="white",bg=background_color,width=100 ,height=1,font=('times', 29, ' bold '))
    message3.place(x=0, y=5)

    #frame3 = tk.Frame(window, bg="White")
    #frame3.place(relx=0.52, rely=0.09, relwidth=0.001, relheight=0.07)

    frame4 = tk.Frame(window, bg=background_color)
    frame4.place(relx=0.38, rely=0.09, relwidth=0.15, relheight=0.07)

    datef = tk.Label(frame4, text = day+"-"+mont[month]+"-"+year, fg="orange",bg=background_color ,width=55 ,height=1,font=('times', 23, ' bold '))
    datef.pack(fill='both',expand=1)

    #clock = tk.Label(frame3,fg="orange",bg=background_color ,width=55 ,height=1,font=('times', 22, ' bold '))
    #clock.pack(fill='both',expand=1)
    #tick()
    #clock = tk.Button(window, command=time_format_change,fg="white"  ,bg="green"  ,width=11 ,activebackground = "white" ,font=('times', 15, ' bold '))
    #clock.place(x=830, y=80)
    #clock.pack(fill='both',expand=1)
    #tick_24()



    head2 = tk.Label(frame2, text="                       FOR NEW REGISTRATION                       ", fg="black",bg=heading_color,width='54' ,font=('times', 17, ' bold ') )
    head2.grid(row=0,column=0)

    head1 = tk.Label(frame1, text="                       CHECK-IN FOR REGISTERED ATTENDEES                     ", fg="black",bg=heading_color,width='55' ,font=('times', 17, ' bold ') )
    head1.place(x=0,y=0)

    lbl = tk.Label(frame2, text="Attendee's ID",width=11  ,height=1  ,fg="black"  ,bg=frame_color ,font=('times', 17, ' bold ') )
    lbl.place(x=200, y=55)

    txt = tk.Entry(frame2,width=32 ,fg="black",font=('times', 15, ' bold '))
    txt.place(x=200, y=88)

    lbl2 = tk.Label(frame2, text="Attendee's Name",width=14  ,fg="black"  ,bg=frame_color ,font=('times', 17, ' bold '))
    lbl2.place(x=200, y=140)

    txt2 = tk.Entry(frame2,width=32 ,fg="black",font=('times', 15, ' bold ')  )
    txt2.place(x=200, y=173)

    lbl4 = tk.Label(frame2, text="Attendee's Mail ID",width=15  ,fg="black"  ,bg=frame_color ,font=('times', 17, ' bold '))
    lbl4.place(x=200, y=225)

    txte = tk.Entry(frame2,width=32 ,fg="black",font=('times', 15, ' bold ')  )
    txte.place(x=200, y=258)

    message = tk.Label(frame2, text="" ,bg=frame_color ,fg="black"  ,width=39,height=1, activebackground = "yellow" ,font=('times', 16, ' bold '))
    message.place(x=150, y=500)

    lbl3 = tk.Label(frame1, text="LIST OF ATTENDEES",width=20  ,fg="black"  ,bg=frame_color  ,height=1 ,font=('times', 17, ' bold '))
    lbl3.place(x=240, y=125)

    res=0
    exists = os.path.isfile("UserDetails/UserDetails.csv")
    if exists:
        with open("UserDetails/UserDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                res = res + 1
        res = (res // 2) - 1
        csvFile1.close()
    else:
        res = 0
    message.configure(text='Total Registrations till now  : '+str(res))


    menubar = tk.Menu(window,relief='ridge')
    filemenu = tk.Menu(menubar,tearoff=0)
    filemenu.add_command(label='Change Password', command = change_pass)
    filemenu.add_command(label='Contact Us', command = contact)
    filemenu.add_command(label='Exit',command = window.destroy)
    menubar.add_cascade(label='Help',font=('times', 29, ' bold '),menu=filemenu)


    tv= ttk.Treeview(frame1,height =13,columns = ('name','mail','date','time'))
    tv.column('#0',width=70)
    tv.column('name',width=90)
    tv.column('mail',width=140)
    tv.column('date',width=65)
    tv.column('time',width=60)
    tv.grid(row=2,column=0,padx=(0,0),pady=(150,0),columnspan=4)
    tv.heading('#0',text ='ID')
    tv.heading('name',text ='NAME')
    tv.heading('mail',text ='MailId')
    tv.heading('date',text ='DATE')
    tv.heading('time',text ='TIME')


    scroll=ttk.Scrollbar(frame1,orient='vertical',command=tv.yview)
    scroll.grid(row=2,column=4,padx=(0,100),pady=(150,0),sticky='ns')
    tv.configure(yscrollcommand=scroll.set)



    #clock = tk.Button(window, command=time_format_change,fg="white"  ,bg="green"  ,width=11 ,activebackground = "white" ,font=('times', 15, ' bold '))
    #clock.place(x=830, y=80)
    #clock.pack(fill='both',expand=1)
    #tick_24()

    themeButton = tk.Button(window, text="Change Theme", command=change_theme  ,fg="white"  ,bg="green"  ,width=11 ,activebackground = "white" ,font=('times', 15, ' bold '))
    themeButton.place(x=1110, y=80)


    clearButton = tk.Button(frame2, text="Clear", command=clear  ,fg="white"  ,bg="black"  ,width=11 ,activebackground = "white" ,font=('times', 11, ' bold '))
    clearButton.place(x=525, y=86)
    clearButton2 = tk.Button(frame2, text="Clear", command=clear2  ,fg="white"  ,bg="black"  ,width=11 , activebackground = "white" ,font=('times', 11, ' bold '))
    clearButton2.place(x=525, y=172)    
    clearButton3 = tk.Button(frame2, text="Clear", command=clear3  ,fg="white"  ,bg="black"  ,width=11 , activebackground = "white" ,font=('times', 11, ' bold '))
    clearButton3.place(x=525, y=258)
    Idcard_photo = tk.Button(frame2, text="ID Card Photo", command=attendee_photo  ,fg="white"  ,bg="#1C3D52"  ,width=20,height=1 , activebackground = "white" ,font=('times', 15, ' bold '))
    Idcard_photo.place(x=270, y=320)
    takeImg = tk.Button(frame2, text="START  FACIAL  IDENTIFICATION", command=TakeImages  ,fg="white"  ,bg="#51ACC5"  ,width=35  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
    takeImg.place(x=175, y=380)
    trainImg = tk.Button(frame2, text="Confirm Password", command=psw ,fg="white"  ,bg="purple"  ,width=17  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
    trainImg.place(x=170, y=440)

    adminface = tk.Button(frame2, text="Confirm Face", command=admin_face ,fg="white"  ,bg="purple"  ,width=17  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
    adminface.place(x=400, y=440)




    trackImg = tk.Button(frame1, text="START FACIAL RECOGNITION", command=TrackImages  ,fg="black"  ,bg="yellow"  ,width=35  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
    trackImg.place(x=210,y=50)

    quitWindow = tk.Button(frame1, text="Quit", command=window.destroy  ,fg="black"  ,bg="#F42B29"  ,width=20 ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
    quitWindow.place(x=280, y=450)


    clockbutton = tk.Button(window,text="Clock format", command=time_format_change,fg="white"  ,bg="green"  ,width=11 ,activebackground = "white" ,font=('times', 15, ' bold '))
    clockbutton.place(x=1310, y=80)
    tick_24()

    i = 0
    with open("Detect_file/Detect_file_" + date + ".csv", 'r') as csvFile1:
        reader99 = csv.reader(csvFile1)
        for lines in reader99:
            i = i + 1
            if (i > 1):
                if (i % 2 != 0):
                    iidd = str(lines[0]) + '   '
                    tv.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6])))
    csvFile1.close()



def clear():
    txt.delete(0, 'end')

def clear2():
    txt2.delete(0, 'end')

def clear3():
    txte.delete(0, 'end')
    #res = "1)Take Images  >>>  2)Save Profile"
    #message1.configure(text=res)


def TakeImages():
    check_haarcascadefile()
    columns = ['SERIAL NO.', '', 'ID', '', 'NAME','','Mailid']
    assure_path_exists("UserDetails/")
    assure_path_exists("TrainingImage/")
    serial = 0
    exists = os.path.isfile("UserDetails/UserDetails.csv")
    if exists:
        with open("UserDetails/UserDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                serial = serial + 1
        serial = (serial // 2)
        csvFile1.close()
    else:
        with open("UserDetails/UserDetails.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1
        csvFile1.close()
    Id = (txt.get())
    name = (txt2.get())
    email = (txte.get())

    id_card(Id,name,email)
    qrcode_mail(Id,name,email)

    if ((name.isalpha()) or (' ' in name)):
        cam = cv2.VideoCapture(0)
        speak("Please look at the camera...   Taking your images for facial identification.")
        
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        while (True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # incrementing sample number
                sampleNum = sampleNum + 1
                # saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage\ " + name + "." + str(serial) + "." + Id + '.' + str(sampleNum) + ".jpg",
                            gray[y:y + h, x:x + w])
                # display the frame
                cv2.imshow('Taking Images', img)
            # wait for 100 miliseconds
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100

            elif sampleNum == 50:
                speak("Please   wait   this   may   take   a   while.")

            elif sampleNum > 100:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = "Images Taken for ID : " + Id
        row = [serial, '', Id, '', name, '',email]
        with open('UserDetails/UserDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message1.configure(text=res)
    else:
        if (name.isalpha() == False):
            res = "Enter Correct name"
            message.configure(text=res)


def TrainImages():
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels("TrainingImage")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='No Registrations', message='Please Register someone first!!!')
        return
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Profile Saved Successfully"
    message1.configure(text=res)
    message.configure(text='Total Registrations till now  : ' + str(ID[0]))


def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empth face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids


def TrackImages():
    global new_face_recognised
    new_face_recognised = True
    check_haarcascadefile()
    assure_path_exists("Detect_file/")
    assure_path_exists("UserDetails/")
    for k in tv.get_children():
        tv.delete(k)
    msg = ''
    i = 0
    j = 0

    recognizer = cv2.face_LBPHFaceRecognizer.create()
    #cv2.createLBPHFaceRecognizer()
    exists3 = os.path.isfile("TrainingImageLabel\Trainner.yml")
    if exists3:
        recognizer.read("TrainingImageLabel\Trainner.yml")
    else:
        mess._show(title='Data Missing', message='Please click on Save Profile to reset data!!')
        return
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', '', 'Name', '', 'MailId', '', 'Date', '', 'Time']
    exists1 = os.path.isfile("UserDetails/UserDetails.csv")
    if exists1:
        df = pd.read_csv("UserDetails/UserDetails.csv")
    else:
        mess._show(title='Details Missing', message='Students details are missing, please check!')
        cam.release()
        cv2.destroyAllWindows()
        window.destroy()

    mail_list = set()
    ee = 'facialcheckin.software@gmail.com'    
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if (conf < 50):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                mm = df.loc[df['SERIAL NO.'] == serial]['Mailid'].values
                ID = str(ID)
                ID = ID[1:-1]
                bb = str(aa)
                bb = bb[2:-2]
                mm = str(mm)
                test = mm
                ee = mm[2:-2]
                attendance = [str(ID), '', bb, '',ee,'', str(date), '', str(timeStamp)]
                mail_list.add(ee)

            else:
                Id = 'Unknown'
                bb = str(Id)
                ee = 'facialcheckin.software@gmail.com'
                mail_list.add(ee)

            cv2.putText(im, str(bb), (x, y + h), font, 1, (255, 255, 255), 2)
        cv2.imshow('Detect Faces', im)
        if (cv2.waitKey(1) == ord('q')):
            break
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    exists = os.path.isfile("Detect_file/Detect_file_" + date + ".csv")
    if exists:
        with open("Detect_file/Detect_file_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(attendance)
            automail(mail_list)
        csvFile1.close()
    else:
        with open("Detect_file/Detect_file_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(col_names)
            writer.writerow(attendance)
            automail(mail_list)
        csvFile1.close()
    with open("Detect_file/Detect_file_" + date + ".csv", 'r') as csvFile1:
        j=0
        reader1 = csv.reader(csvFile1)
        for lines in reader1:
            j = j + 1
            if (i > 1):
                if (j % 2 != 0):
                    iidd = str(lines[0]) + '   '
                    tv.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6])))


    csvFile1.close()
    cam.release()
    change_theme()
    cv2.destroyAllWindows()


global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day,month,year=date.split("-")

mont={'01':'Jan',
      '02':'Feb',
      '03':'Mar',
      '04':'Apr',
      '05':'May',
      '06':'Jun',
      '07':'Jul',
      '08':'Aug',
      '09':'Sep',
      '10':'Oct',
      '11':'Nov',
      '12':'Dec'
      }


#speak("Initializing Facial Check-IN Software")



window = tk.Tk()
window.geometry("1920x1080")
window.resizable(True,False)
window.title("Facial Check-IN Software")
window.configure(background=background_color)
window.iconphoto(False, tk.PhotoImage(file = 'facial-recognition.png'))
window.attributes('-fullscreen', True)

frame1 = tk.Frame(window, bg=frame_color)
frame1.place(relx=0.0, rely=0.17, relwidth=0.50, relheight=0.80)

frame2 = tk.Frame(window, bg=frame_color)
frame2.place(relx=0.51, rely=0.17, relwidth=0.50, relheight=0.80)

message3 = tk.Label(window, text="Facial Check-IN Software" ,fg="white",bg=background_color,width=100 ,height=1,font=('times', 29, ' bold '))
message3.place(x=0, y=5)

#frame3 = tk.Frame(window, bg="White")
#frame3.place(relx=0.52, rely=0.09, relwidth=0.001, relheight=0.07)

frame4 = tk.Frame(window, bg=background_color)
frame4.place(relx=0.38, rely=0.09, relwidth=0.15, relheight=0.07)

datef = tk.Label(frame4, text = day+"-"+mont[month]+"-"+year, fg="orange",bg=background_color ,width=70 ,height=1,font=('times', 23, ' bold '))
datef.pack(fill='both',expand=1)

#clock = tk.Label(frame3,fg="orange",bg=background_color ,width=55 ,height=1,font=('times', 22, ' bold '))
#clock.pack(fill='both',expand=1)
#tick()


head2 = tk.Label(frame2, text="                       FOR NEW REGISTRATION                                                                                      ", fg="black",bg=heading_color,width='120' ,font=('times', 17, ' bold ') )
head2.grid(row=0,column=0)

head1 = tk.Label(frame1, text="                       CHECK-IN FOR REGISTERED ATTENDEES                      ", fg="black",bg=heading_color,width='90' ,font=('times', 17, ' bold ') )
head1.place(x=0,y=0)

lbl = tk.Label(frame2, text="Attendee's ID",width=16  ,height=1  ,fg="black"  ,bg=frame_color ,font=('times', 17, ' bold ') )
lbl.place(x=200, y=55)

txt = tk.Entry(frame2,width=32 ,fg="black",font=('times', 15, ' bold '))
txt.place(x=200, y=88)

lbl2 = tk.Label(frame2, text="Attendee's Name",width=16  ,fg="black"  ,bg=frame_color ,font=('times', 17, ' bold '))
lbl2.place(x=200, y=140)

txt2 = tk.Entry(frame2,width=32 ,fg="black",font=('times', 15, ' bold ')  )
txt2.place(x=200, y=173)

lbl4 = tk.Label(frame2, text="Attendee's Mail ID",width=17  ,fg="black"  ,bg=frame_color ,font=('times', 17, ' bold '))
lbl4.place(x=200, y=225)

txte = tk.Entry(frame2,width=32 ,fg="black",font=('times', 15, ' bold ')  )
txte.place(x=200, y=258)

message = tk.Label(frame2, text="" ,bg=frame_color ,fg="black"  ,width=39,height=1, activebackground = "yellow" ,font=('times', 16, ' bold '))
message.place(x=150, y=500)

lbl3 = tk.Label(frame1, text="LIST OF ATTENDEES",width=25  ,fg="black"  ,bg=frame_color  ,height=1 ,font=('times', 17, ' bold '))
lbl3.place(x=240, y=125)

res=0
exists = os.path.isfile("UserDetails/UserDetails.csv")
if exists:
    with open("UserDetails/UserDetails.csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for l in reader1:
            res = res + 1
    res = (res // 2) - 1
    csvFile1.close()
else:
    res = 0
message.configure(text='Total Registrations till now  : '+str(res))


menubar = tk.Menu(window,relief='ridge')
filemenu = tk.Menu(menubar,tearoff=0)
filemenu.add_command(label='Change Password', command = change_pass)
filemenu.add_command(label='Contact Us', command = contact)
filemenu.add_command(label='Exit',command = window.destroy)
menubar.add_cascade(label='Help',font=('times', 29, ' bold '),menu=filemenu)


tv= ttk.Treeview(frame1,height =13,columns = ('name','mail','date','time'))
tv.column('#0',width=70)
tv.column('name',width=90)
tv.column('mail',width=140)
tv.column('date',width=65)
tv.column('time',width=60)
tv.grid(row=2,column=0,padx=(0,0),pady=(150,0),columnspan=4)
tv.heading('#0',text ='ID')
tv.heading('name',text ='NAME')
tv.heading('mail',text ='MailId')
tv.heading('date',text ='DATE')
tv.heading('time',text ='TIME')


scroll=ttk.Scrollbar(frame1,orient='vertical',command=tv.yview)
scroll.grid(row=2,column=4,padx=(0,100),pady=(150,0),sticky='ns')
tv.configure(yscrollcommand=scroll.set)



clock = tk.Button(window, command=time_format_change,fg="white"  ,bg="green"  ,width=11 ,activebackground = "white" ,font=('times', 15, ' bold '))
clock.place(x=830, y=80)
#clock.pack(fill='both',expand=1)
tick_24()

themeButton = tk.Button(window, text="Change Theme", command=change_theme  ,fg="white"  ,bg="green"  ,width=11 ,activebackground = "white" ,font=('times', 15, ' bold '))
themeButton.place(x=1110, y=80)

clockbutton = tk.Button(window,text="Clock format", command=time_format_change,fg="white"  ,bg="green"  ,width=11 ,activebackground = "white" ,font=('times', 15, ' bold '))
clockbutton.place(x=1310, y=80)



clearButton = tk.Button(frame2, text="Clear", command=clear  ,fg="white"  ,bg="black"  ,width=11 ,activebackground = "white" ,font=('times', 11, ' bold '))
clearButton.place(x=525, y=86)
clearButton2 = tk.Button(frame2, text="Clear", command=clear2  ,fg="white"  ,bg="black"  ,width=11 , activebackground = "white" ,font=('times', 11, ' bold '))
clearButton2.place(x=525, y=172)    
clearButton3 = tk.Button(frame2, text="Clear", command=clear3  ,fg="white"  ,bg="black"  ,width=11 , activebackground = "white" ,font=('times', 11, ' bold '))
clearButton3.place(x=525, y=258)
Idcard_photo = tk.Button(frame2, text="ID Card Photo", command=attendee_photo  ,fg="white"  ,bg="#1C3D52"  ,width=20,height=1 , activebackground = "white" ,font=('times', 15, ' bold '))
Idcard_photo.place(x=270, y=320)
takeImg = tk.Button(frame2, text="START  FACIAL  IDENTIFICATION", command=TakeImages  ,fg="white"  ,bg="#51ACC5"  ,width=35  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
takeImg.place(x=175, y=380)

trainImg = tk.Button(frame2, text="Confirm Password", command=psw ,fg="white"  ,bg="purple"  ,width=17  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
trainImg.place(x=170, y=440)

adminface = tk.Button(frame2, text="Confirm Face", command=admin_face ,fg="white"  ,bg="purple"  ,width=17  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
adminface.place(x=400, y=440)




trackImg = tk.Button(frame1, text="START FACIAL RECOGNITION", command=TrackImages  ,fg="black"  ,bg="yellow"  ,width=35  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
trackImg.place(x=210,y=50)
quitWindow = tk.Button(frame1, text="Quit", command=window.destroy  ,fg="black"  ,bg="#F42B29"  ,width=20 ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
quitWindow.place(x=280, y=450)


window.configure(menu=menubar)
window.mainloop()


# End of Project