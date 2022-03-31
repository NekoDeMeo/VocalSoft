import os
import sys, getopt
import glob
import moviepy.editor as mpy

WRITE_SINGLE_VIDEO_FILE = False

def parseAgrvs(argv):
   inputPicturePath = ''
   inputAudioPath = ''
   outputPath = ''

   try:
      opts, args = getopt.getopt(argv, "p:a:o:")
   except getopt.GetoptError:
      print('Video_Generator.py -p <inputPicturePath> -a <inputAudioPath> -o <outputPath>')
      sys.exit(2)

   #print(opts, args)

   for opt, arg in opts:
      if opt == "-p":
         inputPicturePath = arg
      if opt == "-a":
         inputAudioPath = arg
      elif opt == "-o":
          outputPath = arg

   return inputPicturePath, inputAudioPath, outputPath

def VideoGen_ProcessFolder(inPictrureFolderPath, inAudioFolderPath, outFolderPath):

    clips = []

    for filename in os.listdir(inPictrureFolderPath):
        if filename.endswith(".jpeg"):

            # Get input file path
            inputPictureFilePath = os.path.join(inPictrureFolderPath, filename)

            fName_wo_extension = os.path.splitext(filename)[0]

            # Check if audio file with partial name exists
            partialAudioFileName = fName_wo_extension + "*.mp3"

            partialAudioFilePath = os.path.join(inAudioFolderPath, partialAudioFileName)

            audioFileList = glob.glob(partialAudioFilePath)

            if not audioFileList:
                print("error: no audio file for this image")
            else:
                if (len(audioFileList) > 1):
                    print("error: many audio file for this image")
                else:

                    audioFilePath = audioFileList[0]

                    # Create output file name and file path
                    outputVideoFileName = fName_wo_extension + ".mp4"
                    outputVideoFilePath = os.path.join(outFolderPath, outputVideoFileName)

                    # Generate single video
                    audio = mpy.AudioFileClip(audioFilePath)

                    clip = mpy.ImageClip(inputPictureFilePath).set_duration(audio.duration)

                    clip = clip.set_audio(audio)

                    if WRITE_SINGLE_VIDEO_FILE:
                        clip.write_videofile(outputVideoFilePath, fps=10)

                    clips.append(clip)

            continue
        else:
            #//TODO: show error if there is dummy file here
            continue

    # Merge mp4 files

    finalVideoFileName = "FinalVideo" + ".mp4"
    finalVideoFilePath = os.path.join(outFolderPath, finalVideoFileName)

    # concatenating all the clips
    final = mpy.concatenate_videoclips(clips, method="compose")
    # writing the video into a file / saving the combined video
    final.write_videofile(finalVideoFilePath, fps=30)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    iPictureFilesPath, iAudioFilePath, oFilesPath = parseAgrvs(sys.argv[1:])


    #iPictureFilesPath = 'C:/Users/miph272640/PycharmProjects/VocalSoft/Output/Image/_out'
    #iAudioFilePath = 'C:/Users/miph272640/PycharmProjects/VocalSoft/Output/Audio/_out'
    #oFilesPath = 'C:/Users/miph272640/PycharmProjects/VocalSoft/Output/Video/_out'

    VideoGen_ProcessFolder(iPictureFilesPath, iAudioFilePath, oFilesPath)
