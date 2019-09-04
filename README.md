
## How to run
Step 1: Clone/Download the code  
Step 2: Download and install Python 3.0+ (https://www.python.org/downloads/) and MongoDB (https://www.mongodb.com/download-center#community) 
Run the following command to check python version:
python --version
Step 3: Open a terminal and navigate to the folder outside the main code folder ie. code  
Step 4: Run this command

virtualenv env

Step 5: Navigate to env\Scripts and type (Only for Windows users)

activate.bat

You should be able to see (env) added before the working directory 
For example:
(env)C:\code> 
Step 6: Navigate to code folder and type

python -m pip install -r requirements.txt 
Or
 pip install -r requirements.txt

Step 7: Open another terminal and Run MongoDB.

Step 8: Navigate out of the venv folder and into the code folder. Run the app.

python run.py
NOTE: 
To Stop the application press ctrl+c
To get out of env goto env/scripts and type:
deactivate.bat 
