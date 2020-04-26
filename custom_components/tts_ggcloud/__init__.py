

# Declare variables
DOMAIN = 'tts_ggcloud'
SERVICE_GGCLOUD_TTS = 'say'
# config
CONF_API = 'api'
CONF_SPEED = 'speed'
CONF_PITCH = 'pitch'
CONF_URL_HASS = 'url'
CONF_LANGUAGE_CODE ='language'
# data service
CONF_PLAYER_ID = 'entity_id'
CONF_MESSAGE = 'message'
CONF_VOICE_NAME = 'voice_name'

# audio file path


CONF_FILE_PATH = '/config/www/tts/'
CON_AUDIO_PATH = '/local/tts/'


import requests, json, os, time, urllib, datetime, base64

def setup(hass, config):

    def tts_handler(data_call):


        # Get config
        
        url_hass = str(config[DOMAIN][CONF_URL_HASS])
        api = str(config[DOMAIN][CONF_API])
        # Get data service
        media_id = data_call.data.get(CONF_PLAYER_ID)
        text_message = str(data_call.data.get(CONF_MESSAGE)[0:2000])
        voice_name = data_call.data.get(CONF_VOICE_NAME)
        speed = data_call.data.get(CONF_SPEED)
        pitch = data_call.data.get(CONF_PITCH)
        languageCode = data_call.data.get(CONF_LANGUAGE_CODE)
        # List voice of Google Speech Synthesis
        voice_list = {'ggcloud_voice_1': 'vi-VN-Wavenet-A', 'ggcloud_voice_2': 'vi-VN-Wavenet-B', 'ggcloud_voice_3': 'vi-VN-Wavenet-C', 'ggcloud_voice_4': 'vi-VN-Wavenet-D', 'ggcloud_voice_5': 'vi-VN-Standard-A', 'ggcloud_voice_6': 'vi-VN-Standard-B', 'ggcloud_voice_7':'vi-VN-Standard-C' , 'ggcloud_voice_8':'vi-VN-Standard-D'}
        voice_name = voice_list.get(voice_name)
        #HTTP Request
        url = 'https://texttospeech.googleapis.com/v1beta1/text:synthesize?key='+ api
        #Header Parameters
        headers = {'Content-type': 'application/json'}
        #data = {'text': text_message, "voice": voice_type, "id": "2", "without_filter": False, "speed": speed, "tts_return_option": 3}
        data = { "audioConfig": { "audioEncoding": "MP3", "pitch": pitch, "speakingRate": speed },  "input": { "text": text_message }, "voice": { "languageCode": languageCode, "name": voice_name  }}
        #Get respounse from Server	
        response = requests.post(url, data = json.dumps(data), headers = headers)
        # Cut audio string from response
        audio_string = response.text.split('"')
        # Convert audio string to audio byte
        audio_byte = base64.b64decode(audio_string[3])
        # Create unique audio file name
        uniq_filename = 'tts_ggcloud' + str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '.') + '.mp3'
        # Open audio file
        audio_file = open(CONF_FILE_PATH + uniq_filename, 'wb')
        # Write audio byte to file
        audio_file.write(audio_byte)
        audio_file.close()
	
			# The response's audio_content is binary.
		# with open(uniq_filename, 'wb') as out:
			# Write the response to the output file.
			# out.write(response.audio_content)
			# print('Audio content written to file "output.mp3"')
		
        ## Play audio file on media player ##	
        # media_content_id
        url_audio = url_hass + CON_AUDIO_PATH + uniq_filename
        # service data for 'CALL SERVICE' in Home Assistant
        service_data = {'entity_id': media_id, 'media_content_id': url_audio, 'media_content_type': 'audio/mp3'}
        # Call service from Home Assistant
        hass.services.call('media_player', 'play_media', service_data)
        
    hass.services.register(DOMAIN, SERVICE_GGCLOUD_TTS, tts_handler)
    return True
