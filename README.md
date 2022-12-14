# nightowls-dev

#Step 1 - Install requirements
pip3 install -r requirements.txt

#Step 2 - Modify .flaskenv and include your SQL instance IP address, username and root password
FLASK_APP=main.py
FLASK_DEBUG=1
FLASK_RUN_PORT=8080
FLASK_RUN_HOST=0.0.0.0
MYSQL_IP='****' <<-- Add your SQL IP address
MYSQL_USER='root'
MYSQL_PASS='****' <<-- Add your root password 
MYSQL_DB='nightowls-dev'

#Step 3 - Run the project
flask run

#admin and user login credentials 
username: admin
password: csc330 

username: user
password: csc330
