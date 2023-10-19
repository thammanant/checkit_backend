from mailjet_rest import Client

api_key = '3d5512c5ee85b009fd25825eba103772'
api_secret = 'd71d4a0ef30dfa4a2d5ba005a127bed0'
mailjet = Client(auth=(api_key, api_secret), version='v3.1')


def sendEmail(username):
    data = {
        'Messages': [
            {
                "From": {
                    "Email": "brightacs74@gmail.com",
                    "Name": "Checkit"
                },
                "To": [
                    {
                        "Email": username,
                        "Name": "Dear customer"
                    }
                ],
                "Subject": "Exploring New Opportunities with Checkit!",
                "TextPart": "Hello from Checkit!",
                "HTMLPart": "<h3>Dear partner, let's dive into exciting collaborations with <a href=\"https://www.mailjet.com/\">Checkit</a>!</h3><br />Wishing you success in all your endeavors!"
            }
        ]
    }
    result = mailjet.send.create(data=data)
    # print(result.status_code)
    # print(result.json())
