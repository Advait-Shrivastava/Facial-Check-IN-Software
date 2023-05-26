# Facial Check-IN Software

- This GUI based project verifies the identity of attendees through face recognition, in real time. Pictured ID card with
QR code is generated and sent to attendee’s mail ID after successful registration.

- Attendees receive confirmation mail every time their face is recognized.


***

<div align="center">
    <img src="https://github.com/Advait-Shrivastava/Facial-Check-IN-Software/assets/59224726/c2c8e625-95c4-458d-bf82-800e57492dca">
</div>

***

<div align="center">
    <img src="https://github.com/Advait-Shrivastava/Facial-Check-IN-Software/assets/59224726/b24f93e7-0183-455b-bf5e-9bb75ae15b66">
</div>

***


## Description


This software facilitates attendee presence tracking by utilizing facial recognition technology. The initial step involves registering new users, where their details are inputted and a set of images are captured for training purposes. Subsequently, a personalized ID card containing a QR code is generated and delivered to the user's email address. The QR code serves as a means for verification.

Once the registration process is completed, whenever an attendee appears in front of the camera, their face is detected and their entry is displayed on the screen, confirming their attendance. Additionally, an email notification is sent to the attendee to acknowledge that their attendance has been marked. 

The software offers two distinct themes, namely a dark theme and a light theme, providing users with the option to choose their preferred visual interface.Moreover, the registration process is restricted to the admin, who possesses the exclusive authority to register new users. In addition to entering the admini password, the admin has the option to verify their identity through facial recognition during the registration process, eliminating the need to manually enter the password.

***


## Requirements

* python 3.10
* webcame
* Active Internet connection

***

## Execution
 1. `pip install -r requirements.txt`
 2. `python3 Facial_Check.py`
