# GOESTOOLS Discord Thread Image Sender
## Welcome!
This bot will detect any new images within the goes-tools "goes" folder, and subsequently send these to a specified discord thread.
Unfortunately, discord has a limitation to 9mb files, so some Full-Disk images can be higher than this, however this code reduces the quality of the image for sending in discord - leaving the original unaltered. (Note: The temp directory DOES NOT auto delete images, so feel free to delete the files within anytime)

This bot WILL NOT delete images from the original send location. I.E Rapberry Pi, Windows Desktop etc.

## Pre-requisites 
The first step is to create a discord application, and then a discord bot. (https://discord.com/developers/applications)
The variables in this such as name, PFP etc can be whatever you would like.
Please enable ALL Privileged Gateway Intents (there are 3 at time of writing) found under "Bot" tab.

I would reccomend installing GIT as this is the easiest way to install libraries. Otherwise these can be installed in any other means that suit.
If you don't have GIT installed already, look here: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

As for required libraries, these are here with the correct git command to paste into your console.
| Library | GIT |
| ------ | ------ |
| discord | git install discord |
| Watchdog | git install watchdog |
| PIL | git install Pillow |

#IMPORTANT
Discord's latest library (discord.py) failed to recognize alot of my code. I believe this is because that version is 1.5.X, however the good news is the beta version of 2.0 has been released for some time, and just requires different steps to download. This can be found here:
```
$ git clone https://github.com/Rapptz/discord.py
$ cd discord.py
$ python3 -m pip install -U .[voice]
```

## Getting-Started
1. Ensure all libraries are installed.
2. Using a text editor (please god not notepad) open bot.py. At the very top, you will see the following code to update. Nothing else needs to be changed, and the included comments should be pretty straight-forward:
```python
#===================================
#Discord Token for your bot
TOKEN = 'DISCORD-BOT-TOKEN-HERE'

#Local variables
GOES_PATH = "PATH-TO-GOES-FOLDER-HERE"
PIL_TEMP_PATH = "CREATE-TEMP-FOLDER-ANY-LOCATION"
#Discord thread location
GOES_18_THREAD_ID = INSERT-DISCORD-THREAD-ID-HERE
GOES_16_THREAD_ID = INSERT-DISCORD-THREAD-ID-HERE
Himawari_8_THREAD_ID = INSERT-DISCORD-THREAD-ID-HERE
NWS_THREAD_ID = INSERT-DISCORD-THREAD-ID-HERE
#quality Percentage, Discord max file size is 8mb so dropping quality to 90% works for me
QUALITY_P = 90

#===================================

```
Create multiple threads in a discord channel. The bot MUST have access to these threads for obvious reasons. This bot requires 4 threads, they can be named whatever. I.e: GOES 18, GOES 16, Himawari 8 (or 9) and NWS.

Create a folder, any location, any name. This will house temp image files if they were greater than 8mb, for discord. I would recommend placing this folder somewhere accessable, as noted before; temp files are not yet automatically deleted. To prevent your storage filling up, these may need to be cleaned out every once in a while. 
```
discord.client logging in using static token
discord.gateway Shard ID None has connected to Gateway (Session ID: #######################)
```
If you share your token anywhere on the internet, you will get an error like this below
```sh
discord.gateway Shard ID None session has been invalidated.
```
If this happens, please learn your lesson of not sharing this token anywhere, and generate a new one via https://discord.com/developers/applications


# To-Do:
Create automatic deletion of temp images. OS worked perfectly fine in windows but debian wasnt too pleased with it, so it's been removed for now.

Feel free to open an issue for anything (even just support) and i'll do my best to help
