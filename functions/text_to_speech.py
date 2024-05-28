import requests

from decouple import config

ELEVEN_LABS_API_KEY = config("ELEVEN_LABS_API_KEY")

#eleven labs
#convert text to speech

def convert_text_to_speech(message):
   
    
#DEFINE DATA(BODY)
    body = {
        "text": message,        
        "voice_settings":{
            "stability":1,
            "similarity_boost": 0.5,
        }
    }
    #DEFINE VOICE
    # ,"accept":"audio/mpeg"
    voice_rachel ="Nt5ij6Ck0IOdFekp0TGZ"
    headers = {"xi-api-key":ELEVEN_LABS_API_KEY,"Content-Type": "application/json"}
    endpoint ="https://api.elevenlabs.io/v1/text-to-speech/"+voice_rachel

    #send request
    try:
        response = requests.post(endpoint,json=body,headers=headers)

    except Exception as e:
        return
    #handle response
    if response.status_code ==200:
       return response.content
    else:
       return

 
