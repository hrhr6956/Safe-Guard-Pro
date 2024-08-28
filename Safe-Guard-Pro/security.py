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
    
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    
    message.attach(MIMEText(body, "plain"))

    
    with open(attachment_path, "rb") as attachment:
        
        
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    
    encoders.encode_base64(part)

    
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {attachment_path}",
    )

    
    message.attach(part)
    text = message.as_string()

    
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, text)

def send_email1(sender_email, receiver_email, subject, body, smtp_server, smtp_port, smtp_username, smtp_password):
    
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    
    message.attach(MIMEText(body, "plain"))

    
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, message.as_string())



sender_email = "hr66510@outlook.com"
receiver_email = "hr665101@gmail.com"
subject = "Email with Attachment"
subject1 = "Camera Status Alert"
body = "This is a test email with an attachment."
body1 = "The Camera is covered or not functioning properly and cannot monitor the device"
attachment_path = "test.jpg"
smtp_server = "smtp-mail.outlook.com"
smtp_port = 587  
smtp_username = "hr66510@outlook.com"
smtp_password = "Thatsfunibruh123!"



print(" [INFO] sampling frames from the dataset for webcam...")
video_capture = cv2.VideoCapture(0)

if not video_capture.isOpened():
    send_email1(sender_email, receiver_email, subject1, body1, smtp_server, smtp_port, smtp_username, smtp_password)
    print("Error: Unable to open webcam.")
    #exit()


sreevishnu_image = face_recognition.load_image_file("dataset_family/sreevishnu.jpg")
sreevishnu_face_encoding = face_recognition.face_encodings(sreevishnu_image)[0]


hari_image = face_recognition.load_image_file("dataset_family/hari.jpg")
hari_face_encoding = face_recognition.face_encodings(hari_image)[0]



noyal_image = face_recognition.load_image_file("dataset_family/noyal.jpg")
noyal_face_encoding = face_recognition.face_encodings(noyal_image)[0]



sreedarsh_image = face_recognition.load_image_file("dataset_family/sreedarsh.jpg")
sreedarsh_face_encoding = face_recognition.face_encodings(sreedarsh_image)[0]



known_encoding_face = [
    sreevishnu_face_encoding,
    hari_face_encoding,
    noyal_face_encoding,
#    sreedarsh_face_encoding,    
]
known_face_names = [
    "Sreevishnu",
    "Hari",
    "Noyal",
#    "Sreedarsh",
]


face_names = [] 
face_encodings = []
face_locations = []
process_this_frame = True


#known_encoding_face = [hari_face_encoding]
#known_face_names = ["Hari"]
last_email_time = 0
prev_frame_sum = None
max_black_frames = 2  
black_frames_count = 0

while True:
    
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    if not ret:
        print("Error: Unable to read frame from webcam.")
        break
    if frame is None:
        print("Webcam not functioning properly. Sending email...")
        send_email1(sender_email, receiver_email, subject1, body1, smtp_server, smtp_port, smtp_username, smtp_password)
        break

     
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    
    frame_sum = numpy.sum(gray_frame)

    
    
    if prev_frame_sum is None or frame_sum < prev_frame_sum * 0.9:
        black_frames_count += 1
    else:
        black_frames_count = 0

    
    prev_frame_sum = frame_sum

    
    if black_frames_count >= max_black_frames:
        print("Camera covered or not functioning properly. Sending email...")
        send_email1(sender_email, receiver_email, subject1, body1, smtp_server, smtp_port, smtp_username, smtp_password)
        
    
    rgb_small_frame = numpy.ascontiguousarray(small_frame[:, :, ::-1])




    
    if process_this_frame:
        
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []

        for face_encoding in face_encodings:
            
            distances = face_recognition.face_distance(known_encoding_face, face_encoding)
            matches = face_recognition.compare_faces(known_encoding_face, face_encoding, 0.55)
           
	    
            name = "Unknown"

            
            if True in matches:
                best_match_index = distances.argmin()
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame


    
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        
        bottom *= 4
        top *= 4
        right *= 4    
        left *= 4

        
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), 5)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
       
    
    
    cv2.imshow('Camera', frame)
    
    
    
    
    
    


    if 'Unknown' in face_names:
        
        if (time.time() - last_email_time) > 20:
            
            if (time.time() - os.path.getctime(r'test.jpg')) > 30:
                img = cv2.imwrite("test.jpg", frame)
                send_email(sender_email, receiver_email, subject, body, attachment_path, smtp_server, smtp_port, smtp_username, smtp_password)
                last_email_time = time.time()  
    
    
    
    
    
    
            
    
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


video_capture.release()
cv2.destroyAllWindows()