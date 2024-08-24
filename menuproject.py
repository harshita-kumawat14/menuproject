import pywhatkit
from twilio.rest import Client
import smtplib
from googlesearch import search
import time
from instagrapi import Client as InstaClient
import cv2
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import encoders
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def send_whatsapp_message():
    phone_number = '+91' + input('Enter your phone number: ')
    message = input('Enter your message: ')
    pywhatkit.sendwhatmsg_instantly(phone_number, message)

def send_text_message():
    text_message = input('Enter your message: ')
    account_sid = ''  # Add your Twilio account SID here
    auth_token = ''  # Add your Twilio auth token here
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=text_message,
        from_='',  # Add a Twilio phone number here
        to=''  # Add the recipient phone number here
    )
    print(f'Message SID: {message.sid}')

def phone_call():
    account_sid = ''  # Add your Twilio account SID here
    auth_token = ''  # Add your Twilio auth token here
    client = Client(account_sid, auth_token)
    call = client.calls.create(
        to='',  # Add the recipient phone number here
        from_='',  # Add a Twilio phone number here
        url='(link unavailable)'  # This URL should be a Twilio-hosted voice URL
    )
    print(f"Call SID: {call.sid}")

def google_search():
    query = input('Enter your query: ')
    count = 0
    for i in search(query, num_results=5):
        print(i)
        count += 1
        if count >= 5:
            break

def send_email():
    email_id = input('Enter your email id: ')
    password = input('Enter your password: ')
    server = smtplib.SMTP('smtp.example.com', 587)  # Use a real SMTP server
    server.ehlo()
    server.starttls()
    server.login(email_id, password)
    to_email = input("Enter recipient's email id: ")
    content = input('Enter body: ')
    server.sendmail(email_id, to_email, content)
    server.close()

def schedule_send_email():
    email_id = input('Enter your email id: ')
    password = input('Enter your password: ')
    server = smtplib.SMTP('smtp.example.com', 587)  # Use a real SMTP server
    server.starttls()
    server.login(email_id, password)
    to_email = input('Enter recipient\'s email id: ')
    content = input('Enter body: ')
    schedule_time = int(input('Enter second(s) to schedule the mail: '))
    time.sleep(schedule_time)
    server.sendmail(email_id, to_email, content)
    server.close()

def post_on_instagram():
    client = InstaClient()
    username = input('Enter your username: ')
    password = input('Enter your password: ')
    client.login(username, password)
    photo_path = input('Enter the path of the image: ')
    post_caption = input('Enter your caption: ')
    try:
        client.photo_upload(photo_path, caption=post_caption)
        print("Photo posted successfully!")
    except Exception as e:
        print(f'Error publishing photo: {e}')

def click_image_and_send():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera not accessible.")
        return
    
    status, photo = cap.read()
    if status:
        cv2.imshow("image", photo)
        cv2.waitKey(5000)
        cv2.imwrite("image.png", photo)
        cap.release()
        
        email_id = input('Enter your email id: ')
        password = input('Enter your password: ')
        to_email = input("Enter recipient's email id: ")
    
        msg = MIMEMultipart()
        msg['From'] = email_id
        msg['To'] = to_email
        msg['Subject'] = 'Photo from Python'
        body = input('Enter your body: ')
    
        filename = 'image.png'
        attachment = open(filename, 'rb')
        mime_image = MIMEImage(attachment.read())
        mime_image.add_header('Content-Disposition', f'attachment; filename={filename}')
        msg.attach(mime_image)
        msg.attach(MIMEText(body, 'plain'))
    
        server = smtplib.SMTP('smtp.example.com', 587)  # Use a real SMTP server
        server.ehlo()
        server.starttls()
        server.login(email_id, password)
        server.sendmail(email_id, to_email, msg.as_string())
        server.close()
    else:
        print("Failed to capture image.")
    cap.release()

def apply_filter():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera not accessible.")
        return
    
    status, photo = cap.read()
    if status:
        b, g, r = cv2.split(photo)
        blue_only = cv2.merge([b, g * 0, r * 0])
        green_only = cv2.merge([b * 0, g, r * 0])
        red_only = cv2.merge([b * 0, g * 0, r])
        
        cv2.imshow('Python Image', photo)
        cv2.waitKey(1000)
        cv2.destroyAllWindows()
        
        cv2.imshow('Python Image - Blue Filter', blue_only)
        cv2.waitKey(1000)
        cv2.destroyAllWindows()
        
        cv2.imshow('Python Image - Green Filter', green_only)
        cv2.waitKey(1000)
        cv2.destroyAllWindows()
        
        cv2.imshow('Python Image - Red Filter', red_only)
        cv2.waitKey(1000)
        cv2.destroyAllWindows()
    else:
        print("Failed to capture image.")
    
    cap.release()

def speak():
    text = input('Enter the phrase you want to speak: ')
    os.system(f'espeak-ng "{text}"')

def collect_data():
    name = input("Enter Name: ")
    city = input("Enter City: ")
    college = input("Enter College: ")
    whatsapp_number = input("Enter WhatsApp Number: ")
    life_purpose = input("Enter Life Purpose (in max 5 words): ")
    return [name, city, college, whatsapp_number, life_purpose]

def send_whatsapp_messages(data_array):
    whatsapp_numbers = data_array[:, 3]
    message = "Hi, LW Welcomes you"
    current_hour = time.localtime().tm_hour
    current_minute = time.localtime().tm_min + 2
    for number in whatsapp_numbers:
        try:
            pywhatkit.sendwhatmsg(f"+{number}", message, current_hour, current_minute)
            print(f"Message sent to {number}")
        except Exception as e:
            print(f"Failed to send message to {number}. Error: {e}")
        time.sleep(60)
    print("All messages sent!")

def search_and_display_life_purposes(data_array):
    def search_by_college(data, college_name):
        mask = data[:, 2] == college_name
        results = data[mask][:, 4]
        return results
    
    college_name = input("\nEnter college name to search: ")
    life_purposes = search_by_college(data_array, college_name)

def main_menu():
    while True:
        print("\nMenu:")
        print("1. Send WhatsApp message")
        print("2. Send text message")
        print("3. Voice call")
        print("4. Send mail")
        print("5. Google searches")
        print("6. Schedule and email")
        print("7. Post on Instagram")
        print("8. Click photo and send mail")
        print("9. Apply filter")
        print("10. Speak")
        print("11. Collect Data from Team Members")
        print("12. Send WhatsApp Messages to Team Members")
        print("13. Search Life Purposes by College Name")
        print("14. Live Video Streaming from Mobile Camera")
        print("15. Capture, Process and Save Image")
        print("16. Send SMS to Non-Jaipur Residents")
        print("0. Exit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            send_whatsapp_message()
        elif choice == '2':
            send_text_message()
        elif choice == '3':
            phone_call()
        elif choice == '4':
            send_email()
        elif choice == '5':
            google_search()
        elif choice == '6':
            schedule_send_email()
        elif choice == '7':
            post_on_instagram()
        elif choice == '8':
            click_image_and_send()
        elif choice == '9':
            apply_filter()
        elif choice == '10':
            speak()
        elif choice == '11':
            collect_data()
        elif choice == '12':
            send_whatsapp_messages(data_array)  # Ensure data_array is provided
        elif choice == '13':
            search_and_display_life_purposes(data_array)  # Ensure data_array is provided
        elif choice == '14':
            live_video_streaming()
        elif choice == '15':
            capture_process_and_save_image()
        elif choice == '16':
            send_sms_to_non_jaipur(data_array)  # Ensure data_array is provided
        elif choice == '0':
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    # Assuming data_array is defined or imported before calling main_menu()
    main_menu()