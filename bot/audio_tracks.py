""" 
I want the bot to be able to play youtube videos. 
I will try that using yt_dlp.
This file is pretty much an exploration of how to proceed for the moment.

"""




import yt_dlp

youtube_url = r'https://youtu.be/SEnRWcfgcz4'

YTDLP_OPTIONS = {"format": "bestaudio/best","quiet": True,"noplaylist": True, "cookiesfrombrowser": ("chrome",)}

with yt_dlp.YoutubeDL(YTDLP_OPTIONS) as ydl:
    info = ydl.extract_info(youtube_url, download=False)

print(info)