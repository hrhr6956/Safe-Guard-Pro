import cv2
import face_recognition
import os
import sys, time
import numpy
import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_email(sender_email, receiver_email, subject, body, attachment_path, smtp_server, smtp_port, smtp_username, smtp_password):
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    # Open the file in binary mode
    with open(attachment_path, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {attachment_path}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to SMTP server and send email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Secure the connection
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, text)

def send_email1(sender_email, receiver_email, subject, body, smtp_server, smtp_port, smtp_username, smtp_password):
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    # Log in to SMTP server and send email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Secure the connection
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, message.as_string())


# Example usage:
sender_email = "hr66510@outlook.com"
receiver_email = "hr665101@gmail.com"
subject = "Email with Attachment"
subject1 = "Camera Status Alert"
body = "This is a test email with an attachment."
body1 = "The Camera is covered or not functioning properly and cannot monitor the device"
attachment_path = "test.jpg"
smtp_server = "smtp-mail.outlook.com"
smtp_port = 587  # For SSL use 465
smtp_username = "hr66510@outlook.com"
smtp_password = "Thatsfunibruh123!"


# Get a sampling frame from webcam for reference
print(" [INFO] sampling frames from the dataset for webcam...")
video_capture = cv2.VideoCapture(0)

if not video_capture.isOpened():
    print("Error: Unable to open webcam.")
    exit()

# sample picture is loaded and working on to recognize 
sreevishnu_image = face_recognition.load_image_file("dataset_family/sreevishnu.jpg")
sreevishnu_face_encoding = face_recognition.face_encodings(sreevishnu_image)[0]

# # sample picture is loaded 
hari_image = face_recognition.load_image_file("dataset_family/hari.jpg")
hari_face_encoding = face_recognition.face_encodings(hari_image)[0]


# Load a second sample picture and learn how to recognize it.
noyal_image = face_recognition.load_image_file("dataset_family/noyal.jpg")
noyal_face_encoding = face_recognition.face_encodings(noyal_image)[0]


# Load a sample picture and learn how to recognize it.
sreedarsh_image = face_recognition.load_image_file("dataset_family/sreedarsh.jpg")
sreedarsh_face_encoding = face_recognition.face_encodings(sreedarsh_image)[0]


# create encoded arrays of known faces and names
known_encoding_face = [
    sreevishnu_face_encoding,
    hari_face_encoding,
    noyal_face_encoding,
    sreedarsh_face_encoding,    
]
known_face_names = [
    "Sreevishnu",
    "Hari",
    "Noyal",
    "Sreedarsh",
]

#some varibles  are initialize
face_names = []
face_encodings = []
face_locations = []
process_this_frame = True


known_encoding_face = [hari_face_encoding]
known_face_names = ["Hari"]
last_email_time = 0
prev_frame_sum = None
max_black_frames = 2  # Adjust as needed
black_frames_count = 0

while True:
    # for a single frame video
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    if not ret:
        print("Error: Unable to read frame from webcam.")
        break
    if frame is None:
        print("Webcam not functioning properly. Sending email...")
        send_email1(sender_email, receiver_email, subject1, body1, smtp_server, smtp_port, smtp_username, smtp_password)
        break

     # Convert frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Calculate sum of pixel values in the frame
    frame_sum = numpy.sum(gray_frame)

    # If previous frame sum is None or current frame sum is significantly lower than the previous frame sum,
    # increment the black frames count
    if prev_frame_sum is None or frame_sum < prev_frame_sum * 0.9:
        black_frames_count += 1
    else:
        black_frames_count = 0

    # Update previous frame sum
    prev_frame_sum = frame_sum

    # If consecutive black frames exceed the threshold, send an email
    if black_frames_count >= max_black_frames:
        print("Camera covered or not functioning properly. Sending email...")
        send_email1(sender_email, receiver_email, subject1, body1, smtp_server, smtp_port, smtp_username, smtp_password)
        
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = numpy.ascontiguousarray(small_frame[:, :, ::-1])




    # Process to save time of every other frame of video
    if process_this_frame:
        # In current frame of video find all the face encodings and faces
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []

        for face_encoding in face_encodings:
            # check if face is match with face save in dataset
            distances = face_recognition.face_distance(known_encoding_face, face_encoding)
            matches = face_recognition.compare_faces(known_encoding_face, face_encoding, 0.55)
           
	    
            name = "Unknown"

            # If a match was found in known_encoding_face, use the one which had minimum face distance i.e. the closest match
            if True in matches:
                best_match_index = distances.argmin()
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame


    # Result will display as
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        #Scaled to 1/4 size to the frame we detected, Scale back up face locations 
        bottom *= 4
        top *= 4
        right *= 4    
        left *= 4

        # A box is draw around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        #A label draw with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), 5)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
       
    # Resulting image will display
    
    cv2.imshow('Camera', frame)
    # if 'Unknown' in face_names:
    #     # To prevent sending multiple emails when the face is in the frame for a long time       
    #     if (time.time() - os.path.getctime(r'C:\Users\USER\Desktop\SECURITY SYSTEM\Home-security-system\test.jpg')) > 30:
    #         img = cv2.imwrite("test.jpg",frame)
    #         send_email(sender_email, receiver_email, subject, body, attachment_path, smtp_server, smtp_port, smtp_username, smtp_password)
    #         #os.system('powershell -ExecutionPolicy Bypass -File mailme1.ps1')


    if 'Unknown' in face_names:
        # Check if 20 seconds have passed since the last email
        if (time.time() - last_email_time) > 20:
            # To prevent sending multiple emails when the fac\Desktop\Face-Recognition-Security-Systee is in the frame for a long time       
            if (time.time() - os.path.getctime(r'C:\Users\USER\Desktop\SECURITY SYSTEM\Home-security-system\test.jpg')) > 30:
                img = cv2.imwrite("test.jpg", frame)
                send_email(sender_email, receiver_email, subject, body, attachment_path, smtp_server, smtp_port, smtp_username, smtp_password)
                last_email_time = time.time()  # Update the last email time
    # if 'Unknown' in face_names:
    #     a += 1
    #     if a >= 3:
    #         a = 0
    #         img = cv2.imwrite("test.jpg",frame)
    #        send_email(sender_email, receiver_email, subject, body, attachment_path, smtp_server, smtp_port, smtp_username, smtp_password)
            #os.system('sh mailme.sh')
    #         print("blah blah")
    #For quit hit 'q' on the keyboard
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()