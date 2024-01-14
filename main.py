from flask import Flask, request
from twilio.rest import Client
import os,requests
import sys
sys.path.append(r"/home/rahulrawatr320/Desktop/project/File_organiser")
from file_organiser import organise_file,print_files
import time
import shutil
import uuid
import filetype
import subprocess
# from server_file import run_localhost_8081
import asyncio
from plyer import notification
import csv
import re
from glob import glob 
import shlex
# from werkzeug.server import shutdown


app = Flask(__name__)

from token_whatsapp import account_sid, auth_token

link=None



# bot_whatsapp_number = 'whatsapp:+14155238886'



def send_response(message_body):
    client.messages.create(
        body=message_body,
        from_='whatsapp:+14155238886',
        to='whatsapp:+919588384760'
        # to="whatsapp:+918295977760"
    )
    send_notification(message_body,"Whatsapp Bot")




def send_file_response(file_path):
    global link
    # link="https://806e-2409-4051-21e-d32b-6d2e-7153-3091-aeab.ngrok-free.app"
    file_path = link+file_path
    print(file_path)
    client.messages.create(
        media_url=[file_path],
        body="media file",
        from_='whatsapp:+14155238886',
        to='whatsapp:+919588384760'
    )



def save_media(media_url,media_directory):
    if not os.path.exists(media_directory):
        os.makedirs(media_directory)
    print(media_url)

    response = requests.get(media_url)
    headers=response.headers
    only_file_name=headers['Content-Disposition'].split('filename=')[-1]
    only_file_name=only_file_name.strip('"')
    only_file_name=only_file_name.replace("+","_")
    
    file_name = os.path.join(media_directory, only_file_name)

    if response.status_code == 200:
        with open(file_name, 'wb') as f:
            f.write(response.content)
            f.close()
        # ext=get_file_type(file_name)

        # unique_identifier = uuid.uuid4()

        # new_filename = f"file_({unique_identifier})_.{ext}"
        # new_filename=os.path.join(media_directory,new_filename)
        # shutil.move(file_name,new_filename)

    else:
        print(f"Failed to download media from {media_url}")



def get_file_type(file_path):
    try:
        with open(file_path, 'rb') as f:
            file_contents = f.read()
            file_type = filetype.guess(file_contents)
            return file_type.extension
    except:
        return None
    
def send_notification(message,title):
    notification.notify(
        title=title,
        message=message,
        app_icon="/home/rahulrawatr320/geeks-bot/img1.png",
        timeout=3
    )


def tree_directory(path):
    result=subprocess.run(["tree",path],capture_output=True)
    if result.returncode==0:
        send_response(result.stdout.decode())
    else:
        send_response(result.stderr.decode())

def history(content):
    history_file=rf"/home/rahulrawatr320/Desktop/project/File_organiser/history.txt"
    with open(history_file,"a") as file:
        file.write(content+"\n")
        file.close()

def show_history():
    history_file=rf"/home/rahulrawatr320/Desktop/project/File_organiser/history.txt"
    with open(history_file,"r") as file:
        content=file.read()
        send_response(content[-1000:])
        




client = Client(account_sid, auth_token)
send_response("I am online.... 🤖")
global last_message
global glo_path




# Route to handle incoming messages
@app.route('/', methods=['POST'])
def handle_incoming_message():
    global last_message
    global glo_path

    media_url=request.form.get("MediaUrl0","")
    media_directory="/home/rahulrawatr320/Desktop/project/File_organiser/Root"

    message = request.form['Body']
    raw_message=message[:]
    message=message.lower()

    if media_url:
        save_media(media_url,media_directory)
        send_response("Media file received")
        send_response("Saved to Root")
    else:
        send_notification(message,"User")

        history(raw_message)

        if "hey" in message or "hello" in message:
            send_response("Hello I am a whatsapp bot.")
            send_response("I can help you to organise files")


        elif "organise file" in message:
            send_response("Initiating task...")
            send_response("Organising ( File_organiser/Root ) directory")
            source_dir="/home/rahulrawatr320/Desktop/project/File_organiser/Root"
            dest_dir="/home/rahulrawatr320/Desktop/project/File_organiser/Root"
            res=organise_file(source_dir,dest_dir)
            send_response(res)

        elif "list file" in message:
            send_response("Initiating task...")
            option=""
            if "recursively" in message:
                option="-R"
            res=print_files(media_directory,option)
            send_response(res)

        elif "send file" in message:
            path=raw_message.split("path=")[-1]
            send_response(path)
            # print(result.stdout.decode())
            # send_response(result.stdout.decode())
            # send_response(result.stderr.decode())
            send_file_response(path)

        # elif "check" in message and "8081" in message:
        #     url = 'http://localhost:8081/'
        #     send_response("Checking")
        #     try:
        #         response = requests.get(url)
        #         if response.status_code == 200:
        #             send_response(f"{url} is active and responsive.")
        #         else:
        #             send_response(f"{url} is active but returned status code {response.status_code}.")
        #     except requests.ConnectionError:
        #         send_response(f"{url} is not active or could not be reached.")
        
        elif "run" in message and "8081" in message:
            result=subprocess.Popen(["python","/home/rahulrawatr320/Desktop/project/File_organiser/server_file.py",media_directory])
            global link
            link=raw_message.split("link=")[-1]
            send_response("Process started")

        elif "show" in message and "commands" in message:
            with open("commands.csv","r") as csv_file:
                csv_reader=csv.reader(csv_file)
                mes=""
                count=1
                for line in csv_reader:
                    command,fun=line[0],line[1]
                    mes+=f"{count}. {command}\n[{fun}]\n\n"
                    count+=1
                send_response(mes)
        
        elif "tree" in message:
            tree_directory(media_directory)
            # result=subprocess.run(["tree",media_directory],capture_output=True)
            # if result.returncode==0:
            #     send_response(result.stdout.decode())
            # else:
            #     send_response(result.stderr.decode())

        elif "status" in message:
            file_path=raw_message.split("path=")[-1]
            file_path=media_directory+file_path
            result=subprocess.run(["stat",file_path],capture_output=True)
            if result.returncode==0:
                send_response(result.stdout.decode())
            else:
                send_response(result.stderr.decode())
            
        elif "turn off" in message or "shutdown" in message:
            send_response("Going offline... 🤖")
            result=subprocess.run(["shutdown","-h","now","System is going to shutdown"],capture_output=True)
            if result.returncode==0:
                send_response(result.stdout.decode())
            else:
                send_response(result.stderr.decode())
        
        elif "organise dir" in message:
            path=raw_message.split("path=")[-1]
            if os.path.isdir(path):
                result=subprocess.run(["ls",path],capture_output=True)
                if result.returncode==0:
                    send_response(f"Data stored at {path} :")
                    if result.stdout.decode()=="":
                        send_response("Empty directory")
                    else:
                        send_response(result.stdout.decode())
                        send_response("Are you sure to organise files in this directory...\nEnter (yes/no)")
                        glo_path=path
                else:
                    send_response("Error while trying to list content:\n\n",result.stderr.decode())
            else:
                send_response("Not a valid directory!")

        
        elif "yes"==message:
            if "organise dir" in last_message:
                send_response("Initiating task...")
                send_response(f"Organising ( {glo_path} ) directory")
                time.sleep(2)
                res=organise_file(glo_path,glo_path)
                send_response(res)
                send_response("Here is final structure of directory: ")
                tree_directory(glo_path)
            else:
                send_response("Not a valid command.... 🤖")


        elif "show" in message and "history" in message:
            show_history()

        elif all(item in message for item in ["convert","to","pdf"]):
            result2=re.search(r"convert ([a-z]+) ",message)
            ty=result2[1].strip()
            # send_response(ty)
            send_response("Converting.....")
            original_cwd=os.getcwd()
            os.chdir(media_directory)
            try:
                file_paths = glob(f"{media_directory}/*.{ty}")
                shlex_path=[shlex.quote(fp) for fp in file_paths]
                conversion_command = ["libreoffice", '--convert-to', 'pdf'] + shlex_path
                result = subprocess.run(" ".join(conversion_command),shell=True,capture_output=True)
                # if result.returncode==0:
                #     send_response(result.stdout.decode())
                #     send_response("Task done")
                # else:
                #     send_response(result.stderr.decode())
                send_response("Task done")
            except Exception as e:
                send_response(f"Conversion failed\ndue to\n{e}")
            os.chdir(original_cwd)

        elif "remove" in message and "file" in message:
            result2=re.search(r"remove ([a-z]+) ",message)
            ty=result2[1].strip()
            send_response("Removing......\n{}".format(ty))

            try:
                file_paths = glob(f"{media_directory}/*.{ty}")
                shlex_path=[shlex.quote(fp) for fp in file_paths]
                conversion_command = ["rm"] + shlex_path
                result = subprocess.run(" ".join(conversion_command),shell=True,capture_output=True)
                # if result.returncode==0:
                #     send_response(result.stdout.decode())
                #     send_response("Task done")
                # else:
                #     send_response(result.stderr.decode())
                send_response("Task done")
            except Exception as e:
                send_response(f"Deletion failed\ndue to\n{e}")

        elif "show calendar" in message:
            month_result=re.search(r"month=([\d]+)",message)
            year_result=re.search(r"year=([\d]+)",message)
            month=month_result[1]
            year=year_result[1]
            result=subprocess.run(f"cal {month} {year} | column -t",shell=True,capture_output=True)
            if result.returncode==0:
                send_response(result.stdout.decode())
            else:
                send_response(result.stderr.decode())



        else:
            send_response("Not a valid command.... 🤖")

    last_message=message


        # sender = 'whatsapp:+919588384760'
        # Process the incoming message as needed
        # You can add your message processing logic here

        # Send a response message
        # response_message = 'This is your bot responding to your message.'
        # # send_response(response_message)
        # file_path="https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
        # # file_path="https://app.blackhole.run/#3e6d563e4419D2dWZxwXVL8NwEaj37WRqDxCNkFBLYuL"

        # send_file_response(file_path)
        # print("file sent")

    return 'OK'

if __name__ == '__main__':
    app.run(debug=True)
    # app.run()
