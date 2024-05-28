#uvicorn main:app
#uvicorn main:app --reload


from fastapi import FastAPI,File,UploadFile,HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import openai
import sys
sys.path.insert(0, 'C://Users//Lenovo//Desktop//Rachel//backend//Functions')


#Custom Function Imports
from database import store_messages,reset_messages
from openai_requests import convert_audio_to_text ,get_chat_response
from text_to_speech import convert_text_to_speech




#Initiate App
app = FastAPI()


#cors-origins
origins =[
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://localhost:4174",
    "http://localhost:3000",
]

#cors-Middleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



#check health
@app.get("/")
async def check_health():
    return {"message": "Healthy"}

#reset messages
@app.get("/reset")
async def reset_conversation():
    return {"message": "conversation reset"}



@app.post("/post-audio")
async def post_audio(file:UploadFile = File(...)):
    #get saved audio
   # audio_input = open("backend/voice.mp3", "rb")

    #Save File from frontend
    with open(file.filename,"wb")as buffer:
        buffer.write(file.file.read())
    audio_input = open(file.filename,"rb")

    #decode audio
    message_decoded = convert_audio_to_text(audio_input)

    # Guard: Ensure message decoded
    if not message_decoded:
        raise HTTPException(status_code=400, detail="Failed to get decode audio")
    
    # Get chatGPT response
    chat_response = get_chat_response(message_decoded)

    # Guard: Ensure output
    if not chat_response:
        raise HTTPException(status_code=400, detail="Failed to get chat response")


    #store messages
    store_messages(message_decoded,chat_response)

    #convert chat response to audio
    audio_output =convert_text_to_speech(chat_response)

    # Guard: Ensure message decoded
    if not audio_output:
        raise HTTPException(status_code=400, detail="Failed to get Eleven Labs audio response")
    
    # Create a generator that yields chunks of data
    def iterfile():
    #    print("@#@#@#@#@#@#@#")
    #    print(audio_output)
       yield audio_output

    #return audio file
    return StreamingResponse(iterfile(),media_type="application/octet-stream")
    #return StreamingResponse(audio_output,media_type="audio/mpeg")

    
    return "Done"

