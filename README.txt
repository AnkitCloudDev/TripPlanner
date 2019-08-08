STEPS FOR DEPLOYING THE APPLICATION ON HEROKU
*****You need to be logged in gitcli and herokucli before we start********
1.OPEN CMD/POWERSHELL(WINDOWS) OR TERMINAL (linux)
2. NAVIGATE TO CODE FOLDER TYPE the following commands one by one in the command line
git init
heroku create 
git add .
git commit -m "Your command"'
git push heroku master

3. GOTO Heroku Dashboard-> Select your application -> Settings-> Configure Vars 
Add the following parameters for AWS SQS integration for message passing:
1.AWS_ACCESS_KEY_ID
2.AWS_DEFAULT_REGION
3.AWS_SECRET_ACCESS_KEY
4.MONGODB_URI


Once done, open app and run the application 