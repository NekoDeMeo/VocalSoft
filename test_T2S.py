"""Synthesizes speech from the input string of text or ssml.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""
from google.cloud import texttospeech
import os
import sys, getopt

credential_path = "C:/Users/miph272640/PycharmProjects/VocalSoft/woven-bonbon-325609-21984ad9f107.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

# SSML file name syntax = 000_Cover_<ExcelFile>_TL_VQ_G.ssml
# TL = Target Langugage (VI/EN/JA)
# VQ = Voice Quality (HI/LO)
# G  = Voice Gender (F/M)

AUDIOSETTING_START_OFFSET = -7
#AUDIOSETTING_STRING_LENGTH = 7
#AUDIOSETTING_END_OFFSET = AUDIOSETTING_START_OFFSET + AUDIOSETTING_STRING_LENGTH - Unused, Assume last characters

# Hash audio settings
AudioSetting_Dict = {   'JA_HI_F':  {   'targetLanguage':'ja-JP',
                                        'languageName':'ja-JP-Wavenet-B',
                                        'voiceGender':texttospeech.SsmlVoiceGender.FEMALE},
                        'JA_LO_F': {    'targetLanguage':'ja-JP',
                                        'languageName':'ja-JP-Standard-B',
                                        'voiceGender':texttospeech.SsmlVoiceGender.FEMALE},
                        'JA_HI_M':  {   'targetLanguage':'ja-JP',
                                        'languageName':'ja-JP-Wavenet-C',
                                        'voiceGender':texttospeech.SsmlVoiceGender.MALE},
                        'JA_LO_M': {    'targetLanguage':'ja-JP',
                                        'languageName':'ja-JP-Standard-C',
                                        'voiceGender':texttospeech.SsmlVoiceGender.MALE},
                     }


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
        print('Audio content written to file: ' + audioOutputPath)

def parseAgrvs(argv):
   inputPath = ''
   outputPath = ''
   try:
      opts, args = getopt.getopt(argv,"i:o:")
   except getopt.GetoptError:
      print('test_T2S.py -i <inputPath> -o <outputPath>')
      sys.exit(2)

   #print(opts, args)

   for opt, arg in opts:
      if opt == "-i":
         inputPath = arg
      elif opt == "-o":
          outputPath = arg

   #print('Input file is ', inputPath)
   #print('Output file is ', outputPath)


   return inputPath, outputPath

def getAudioSettingFromFileName(fName_wo_extension):

    # SSML file name syntax = 000_Cover_<ExcelFile>_TL_VQ_G.ssml
        audiosetting = fName_wo_extension[AUDIOSETTING_START_OFFSET:]

    # Get data using dict
        targetLanguage = AudioSetting_Dict[audiosetting]['targetLanguage']
        languageName = AudioSetting_Dict[audiosetting]['languageName']
        voiceGender = AudioSetting_Dict[audiosetting]['voiceGender']

        return targetLanguage, languageName, voiceGender

def GGT2S_ProcessFolder(inFolderPath, outFolderPath):

    for filename in os.listdir(inFolderPath):
        if filename.endswith(".ssml"):

            # Get input file path
            inputFilePath = os.path.join(inFolderPath, filename)

            # Create output file path
            fName_wo_extension = os.path.splitext(filename)[0]
            outputFileName = fName_wo_extension + '.mp3'
            outputFilePath = os.path.join(inFolderPath, outputFileName)

            # Get audio setting
            targetLanguage, languageName, voiceGender = getAudioSettingFromFileName(fName_wo_extension)

            # Trigger T2S lib
            with open(inputFilePath, 'r', encoding='utf-8') as file:
                data = file.read().replace('\n', '')

            GGT2S(data, targetLanguage, languageName, voiceGender, outputFilePath)

            continue
        else:
            #//TODO: show error if there is dummy file here
            continue

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    iFilesPath, oFilesPath = parseAgrvs(sys.argv[1:])
    #iFilesPath = 'C:/Users/miph272640/PycharmProjects/VocalSoft/Test'
    #oFilesPath = 'C:/Users/miph272640/PycharmProjects/VocalSoft/Test'
    GGT2S_ProcessFolder(iFilesPath, oFilesPath)

