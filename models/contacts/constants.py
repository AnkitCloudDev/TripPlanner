import boto3
import config
CONTACT = "contact"
queue_url = 'https://sqs.eu-west-1.amazonaws.com/447123079606/trip'
sqs = boto3.client('sqs')
def checkAdm(x):
    flag=0
    for v in config.ADMINS:
            if x == v:
                print(x)
                flag=1
            if(flag==1):
                print("Admin Found")
                return 1
                break
            else:
                print("Not an admin")
                return 0