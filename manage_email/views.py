from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import sendgrid
import os
import requests
SENDGRID_API_KEY='' 
MALIGUN_API_KEY=''

#Service_Maligun

def sendEmail_maliGun(information):
	return requests.post(
		"https://api.mailgun.net/v3/sandbox8f4c7b0a164044ae8b86e47d28e33b32.mailgun.org/messages",
		auth=("api", MALIGUN_API_KEY),
		data=information
            
#Service_SendGrid
def sendEmail_sendGrid(sender_email,information):
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    data = {
        "personalizations": [
            {
                "to": [
                      {
                        "email": information.to
                         }
                      ],
                "subject": "Sending with SendGrid is Fun"
            }
         ],
       "from": {
              "email": sender_email
              },
        "subject": [
             {
              "type": "text/plain",
              "value": information.subject
             }
             ] ,    
        "content": [
             {
              "type": "text/plain",
              "value": information.text
             }
             ]
           }
    return sg.client.mail.send.post(request_body=data)




# Create your views here.
@csrf_exempt
def index(request):
    if request.method == 'GET':
        return render(request,'index.html')
    else:
        context={
            'status':200,
            'message':'Congrats,Mail Sent'
        }

        information={
            "from":request.POST['sender_email'],
			"to":request.POST['receiver_email'],
			"subject":request.POST['subject'],
			"text":request.POST['paragraph_text']
           }
        print(information)
        res=sendEmail_maliGun(information)
        try:
            res.raise_for_status()
        except res.exceptions.HTTPError as err:
             print("EROOOR Maligun :" + err)
             response=sendEmail_sendGrid(request.POST['sender_email'],information)
             try:
                 response.raise_for_status()
             except response.exception.HTTPError as err:
                 print("Error SendGrid :"+err)
                 context.message="Failed! Please try again"

        return render(request,'conformation.html',context)
