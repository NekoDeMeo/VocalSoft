"""Synthesizes speech from the input string of text or ssml.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""
from google.cloud import texttospeech
import os



def GGT2S(ssmlStr, targetLanguage, languageName, voiceGender, audioOutputPath):

    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(ssml=ssmlStr)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code= targetLanguage, name = languageName, ssml_gender=voiceGender
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(audioOutputPath, "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file' + audioOutputPath)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    directory = 'C:/Users/miph272640/PycharmProjects/VocalSoft/Output/SSML/_out/'

    for filename in os.listdir(directory):
        if filename.endswith(".ssml"):
            #print(os.path.join(directory, filename))
            #print(filename)
            continue
        else:
            continue

    file = "005_Vocal__VocalMasterSheet_Template_JA_LO_M.ssml"
    file_wo_ext = os.path.splitext(file)[0]
    x = file_wo_ext.split("_")
    print(x)
    tarLan = x[len(x) - 1 - 2]
    quality = x[len(x) - 1 - 1]
    voice = x[len(x) - 1 - 0]
    print(tarLan, quality, voice)


    ssmlInput = 'C:/Users/miph272640/PycharmProjects/VocalSoft/Output/SSML/_out/005_Vocal__VocalMasterSheet_Template_JA_LO_M.ssml'
    targetLanguage = 'ja'
    #languageName = 'ja-JP-Wavenet-B'
    languageName = 'ja-JP-Standard-A'
    voiceGender = texttospeech.SsmlVoiceGender.FEMALE
    audioOutput = 'C:/Users/miph272640/PycharmProjects/VocalSoft/Output/SSML/_out/005_Vocal__VocalMasterSheet_Template_JA_LO_M.mp3'

    with open(ssmlInput, 'r', encoding='utf-8') as file:
        data = file.read().replace('\n', '')

    print(data)


    #GGT2S(data, targetLanguage, languageName, voiceGender, audioOutput)