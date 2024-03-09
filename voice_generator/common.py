import json
import requests
import os
from datetime import *
from elevenlabs.client import ElevenLabs
from elevenlabs import Voice, VoiceSettings, generate, save

# set up a local temp channel where we will land all of the files
os.makedirs("temp", exist_ok=True)

# set up eleven labs token and set up VoiceResponse Object as well as HTTP request parameters
elevenlabs_base_url     = "https://api.elevenlabs.io/v1/text-to-speech/"
elevenlabs_client       = ElevenLabs(api_key=os.getenv("ELEVENLABS_TOKEN"))
elevenlabs_voices       = [x for x in elevenlabs_client.voices.get_all().voices if x.name.startswith('discord')]
default_voice_settings  = {"style" : 0.2, "stability" : 0.5, "similarity_boost" : 0.5, "use_speaker_boost" : True}
querystring             = {"output_format":"mp3_44100_128"}

# create initialization string to print out when bot starts up
init_str = f"""
```
Bot initialized with the following:
- Current Working Directory : {os.getcwd()}
- Eleven Labs Voices Loaded : {", ".join([x.name for x in elevenlabs_voices])}
```
"""

# mapping to names in elevan labs
voice_mappings = {
    "spongebob" : {
        "eleven-labs-name"  : "discord-bot-1",
        "full-name"         : "Spongebob Squarepants"
    },

    "patrick" : {
        "eleven-labs-name"  : "discord-bot-2",
        "full-name"         : "Patrick Star"
    },

    "gordon" : {
        "eleven-labs-name"  : "discord-bot-3",
        "full-name"         : "Gordon Ramsay"
    },

    "drphil" : {
        "eleven-labs-name"  : "discord-bot-4",
        "full-name"         : "Doctor Phil"
    },

    "cody" : {
        "eleven-labs-name"  : "discord-bot-5",
        "full-name"         : "Cody Ko"
    },

    "jakey" : {
        "eleven-labs-name"  : "discord-bot-6",
        "full-name"         : "Nakey Jakey"
    },

    "mario" : {
        "eleven-labs-name"  : "discord-bot-7",
        "full-name"         : "Super Mario"
    },

    "dunkey" : {
        "eleven-labs-name"  : "discord-bot-8",
        "full-name"         : "Video Game Dunkey"
    }
}

# fetch the eleven labs ID and description
# the names in eleven labs are generic to avoid voices being blocked
for bot_voice in voice_mappings.keys():
     for el_voice in elevenlabs_voices:
          if voice_mappings[bot_voice]['eleven-labs-name'] == el_voice.name:
            voice_mappings[bot_voice]['description'] = el_voice.description
            voice_mappings[bot_voice]['eleven-labs-id'] = el_voice.voice_id
            voice_mappings[bot_voice]['voice-settings'] = el_voice.settings

def generate_and_save(input_text: str, request_voice: str, requester: str) -> dict:

    # common vars
    response_dict = {}
    request_dt = datetime.now().strftime("%Y%m%d%H%M%S")
    request_voice_id = voice_mappings[request_voice]['eleven-labs-id']
    file_name = str(requester) + "_" + request_voice + "_" + request_dt
    full_path = os.getcwd() + "\\temp\\" + file_name + ".mp3"
    
    # http request vars
    url = elevenlabs_base_url + request_voice_id
    payload = {
        "text" : input_text,
        "model_id" : "eleven_multilingual_v2",
        "voice_settings" : default_voice_settings
    }
    
    headers = {
        "xi-api-key": os.getenv("ELEVENLABS_TOKEN"),
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers, params=querystring)
    response_dict['status'] = str(response.status_code)

    # if the response is good we save, if it is not, we save the code and error message
    if response_dict['status'].startswith("20"):
        save(response.content, full_path)
        response_dict['full-path'] = full_path
        response_dict['debug-string'] = f"Saved audio file under {full_path}, API response was {response_dict['status']}".replace("\\","/")
    else:
        response_dict['error-msg'] = f"API Response status was {response_dict['status']} with description {response.text}"

    return response_dict

def get_usage():
    """Get Eleven Labs API usage thus far"""

    headers = {"xi-api-key": os.getenv("ELEVENLABS_TOKEN")}
    response = requests.request("GET", "https://api.elevenlabs.io/v1/user/subscription", headers=headers)
    response_dict = json.loads(response.text)
    display_dict = {
        "limit"     : response_dict['character_limit'],
        "used"      : response_dict['character_count'],
        "available" : (response_dict['character_limit'] - response_dict['character_count'])
    }

    return display_dict