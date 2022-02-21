# UpOnYourLuck
### A service that provides a person who is homeless (the User) with a QR code sticker on it which can be scanned by a passerby. Once scanned,this passerby will be taken to this Users' profile page where they can read about the human behind the sign.

## Installation
### Fork this repo
### Open the terminal and Clone your forked repo (make sure you have Git installed in your machine)
## git clone https://github.com/YOUR-USERNAME/UpOnYourLuck
### Open terminal and change to the newly cloned directory
## cd UpOnYourLuck
### Create a python virtual environment and activate it
## python3 -m venv venv
## source venv/bin/activate
### enter the command 'pip install -r requirements.txt' (this will auto install Django, and several other dependencies, like bootstrap, cristpy forms, qrcode, etc)
### enter the command 'python manage.py makemigrations' 
### enter the command 'python manage.py migrate' (this will create a new sqlite database, so feel free to create and delete users as you please)
### enter the command 'python manage.py runserver' to test if everything is working.  You should see the welcome page.
