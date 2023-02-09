import azure.cognitiveservices.speech as speechsdk
import json

# Creates an instance of a speech config with specified subscription key and service region.
speech_key = "YOUR_KEY"
service_region = "YOUR_REGION"

speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
# Note: the voice setting will not overwrite the voice element in input SSML.
speech_config.speech_synthesis_voice_name = "en-US-JaneNeural"
text = """
    <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">
        <voice name="en-US-SaraNeural">
            <mstts:viseme type="redlips_front"/>
            <mstts:express-as style="excited">
                <prosody rate="-8%" pitch="23%">
                    Good morning everyone!
                </prosody>
            </mstts:express-as>
            <mstts:express-as style="cheerful">
                <prosody rate="-10%" pitch="23%">
                    Visit EnglishCentral today.
                    Learn about how we're using artificial intelligence and machine learning to improve your language learning experience.
                </prosody>
            </mstts:express-as>
        </voice>
    </speak>""" 

file_name = "outputaudio.wav"
file_config = speechsdk.audio.AudioOutputConfig(filename=file_name)

# use the default speaker as audio output.
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=file_config)

viseme_data = []

def viseme_cb(evt):
    print("Viseme event received: audio offset: {}ms, viseme id: {}.".format(
        evt.audio_offset / 10000, evt.viseme_id))
    
    viseme_data.append({"offset": evt.audio_offset / 10000, "id": evt.viseme_id})

# Subscribes to viseme received event
speech_synthesizer.viseme_received.connect(viseme_cb)

result = speech_synthesizer.speak_ssml_async(ssml=text).get()
# Check result
if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("Speech synthesized for text [{}]".format(text))
    with open("viseme.json", "w") as f:
        json.dump(viseme_data, f, indent = 4)
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print("Speech synthesis canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        print("Error details: {}".format(cancellation_details.error_details))

