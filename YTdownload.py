#include pytube
from pytube import YouTube
import sys
import os
import regex as re

def validAddress(text):
    # checks if the address is valid

    # starts with http:// or https://
    x = re.match("^(http(s)?:\/\/)?((w){3}.)?youtube\.com\/", text)
    if x:

        croppedText =""
        for character in text:
            if character == "&":
                return croppedText
            croppedText = croppedText+character

        return croppedText
    else:
        return ""


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Put the url as an argument when you use this")
        quit()
    else:
        url = ""

        url = sys.argv[1]
        #blantly don't check the syntax of the url and let the user crash the script
        newURL = validAddress(url)
        if newURL == "":
            print("The url: ", newURL, " input was not recognized as a youtube link")
            quit()

        try:
            yt = YouTube(newURL)
        except:
            print('error connecting to url')

        #d_videos = yt.streams.filter(file_extension='mp4', progressive=True,)
        d_video = yt.streams.get_highest_resolution()


        #for stream in d_videos:
        #    print(stream)

        #print(download)
        try:
            d_video.download(os.getcwd())
        except:
            print('error downloading')
        print("the video has been downloaded")