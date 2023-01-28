#Necessary imports
import discord
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
from PIL import Image

#Token for Discord bot, see developers panel in Discord website
TOKEN = 'INSERT-BOT-TOKEN-HERE'

#Path to goes-tools GOES folder, where the images are kept
GOES_PATH = "PATH-TO-GOES-FOLDER"
#Path to new temp folder, as per github instructions
PIL_TEMP_PATH = "PATH-TO-NEW-TEMP-FOLDER"

#NEW:
#Enable or disable threads in discord, this way you don't have to use them all.
#CUSTOM_LUT is new, for custom FC images
GOES_18_THREAD = True
GOES_18_THREAD_ID = INSERT-DISCORD-THREAD-ID-HERE

GOES_16_THREAD = True
GOES_16_THREAD_ID = INSERT-DISCORD-THREAD-ID-HERE

Himawari_8_THREAD = True
Himawari_8_THREAD_ID = INSERT-DISCORD-THREAD-ID-HERE

NWS_THREAD = True
NWS_THREAD_ID = INSERT-DISCORD-THREAD-ID-HERE

FC_THREAD = True
FC_THREAD_ID = INSERT-DISCORD-THREAD-ID-HERE

CUSTOMLUT_THREAD = True
CUSTOMLUT_THREAD_ID = INSERT-DISCORD-THREAD-ID-HERE

QUALITY_P = 90
#REQUIRED to be global so it can be passed to function
global temp_path
#Discord Intentions - set to all for now
intents = discord.Intents.all()

client = discord.Client(intents=intents)

class ImageHandler(FileSystemEventHandler):
    async def send_image(self, path, thread, temp_path, file_name):
        
        Degrading = 10
        #This reduces the size if it is greater than 8mb, with new degrading counter
        while os.path.getsize(path) > 8000000:
            print("Image greater than 8mb. Discord Limit reached. Reducing quality by", Degrading,"%")
            image = Image.open(path)
            print("Saving to Temp location")
            #saves the image in a temp folder
            image.save(temp_path, quality=QUALITY_P, optimize=True)
            path = temp_path
            Degrading =+10
            
        #sends in discord thread 
        #NEW: deletes the file afterwards
        with open(path, 'rb') as f:
            file = discord.File(f)
            await thread.send(content=file_name, file=file)
            if os.path.exists(temp_path):
                print("Attempting to delete file")
                os.remove(temp_path)
            else:
                print("Sent!")
        
    def on_created(self, event):
        if event.is_directory:
            return None
        elif event.src_path.endswith('.jpg') or event.src_path.endswith('.png') or event.src_path.endswith('.gif'):
            print("Event Caught. Type:", event.event_type, "at:", event.src_path)
            #If statements to parse images into correct threads
            #NEW: CUSTOM_LUT, FC, enable and disable features
            if CUSTOMLUT_THREAD == True and "CUSTOMLUT" in event.src_path:
                thread = client.get_channel(CUSTOMLUT_THREAD_ID)
              
            elif FC_THREAD == True and "FC" in event.src_path:
                thread = client.get_channel(FC_THREAD_ID)
                
            elif GOES_18_THREAD == True and "goes18" in event.src_path:
                thread = client.get_channel(GOES_18_THREAD_ID)
                
            elif GOES_16_THREAD == True and "goes16" in event.src_path:
                thread = client.get_channel(GOES_16_THREAD_ID)
                
            elif HIMAWARI_8_THREAD == True and "himawari8" in event.src_path:
                thread = client.get_channel(Himawari_8_THREAD_ID)
            
            elif NWS_THREAD == True and "nws" in event.src_path:
                thread = client.get_channel(NWS_THREAD_ID)
            else:
                thread = 0
            #NEW: Better errpr messages
            if thread == 0:
                print("Error 1: Thread was equal to null", event.src_path, " is not a valid file.") 
                print ("Custom LUT:", CUSTOMLUT_THREAD, "FC", FC_THREAD, "GOES 18", GOES_18_THREAD, "GOES 16", GOES_16_THREAD, "Himawari 8", HIMAWARI_8_THREAD)
                print("If this is an error, please open a github issue.")
            else:
                #After error checking, splits file name and extension up, THEN sends it to the function.
                print("File Found. Sending to Discord")
                file_name, file_ext = os.path.splitext(os.path.basename(event.src_path))
                temp_path = os.path.join(PIL_TEMP_PATH,file_name+file_ext)
                client.loop.create_task(self.send_image(event.src_path, thread, temp_path, file_name))
#sets observer                
observer = Observer()
event_handler = ImageHandler()

#this loads on startup
@client.event
async def on_ready():
    print("Bot is waiting for file updates.")
    observer.schedule(event_handler, path=GOES_PATH, recursive=True)
    observer.start()
#Run
client.run(TOKEN)
