#Necessary imports
import discord
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
from PIL import Image

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

#create discord client, intentions all for ease of use
intents = discord.Intents.all()
client = discord.Client(intents=intents)

class ImageHandler(FileSystemEventHandler):
    async def send_image(self, path, thread):
        #split apart .jpg and the file name, for sending and processing later on
        file_name, file_ext = os.path.splitext(os.path.basename(path))
        #This reduces the size if it is greater than 8mb
        if os.path.getsize(path) > 8000000:
            print("Image greater than 8mb. Discord Limit reached. Reducing quality to 90%")
            temp_path = os.path.join(PIL_TEMP_PATH,file_name+file_ext)
            image = Image.open(path)
            print("Temp Path:", temp_path)
            #saves the image in a temp folder
            #TO DO HERE: AUTO DELETE THE TEMP IMAGES
            image.save(temp_path, quality=QUALITY_P, optimize=True)
            path = temp_path
        #This sends the image in discord    
        with open(path, 'rb') as f:
            file = discord.File(f)
            await thread.send(content=file_name, file=file)
    #using watchdog we can use on_created to be called when a new file (image in this case) is created    
    def on_created(self, event):
        if event.is_directory:
            return None
        #Only checks for jpg and png files, you can add another or statement to include gifs as well.
        elif event.src_path.endswith('.jpg') or event.src_path.endswith('.png'):
            print("Event type:", event.event_type)
            print("Path:", event.src_path)
            #if statements, as the default folders are called "goes18, goes16 and himawari8", we can search in the path for that name.
            #This allows us to set the thread to the right discord thread before sending
            if "goes18" in event.src_path:
                thread = client.get_channel(GOES_18_THREAD_ID)
                
            elif "goes16" in event.src_path:
                thread = client.get_channel(GOES_16_THREAD_ID)
                
            elif "himawari8" in event.src_path:
                thread = client.get_channel(Himawari_8_THREAD_ID)
            
            elif "nws" in event.src_path:
                thread = client.get_channel(NWS_THREAD_ID)
            else:
                thread = 0
            #If nothing was found, throw this error.    
            if thread == 0:
                print("Unknown Sattelite. Supported are GOES 18 & 16, and Himawari 8.")
            else:
                print("Calling send_image function")
                client.loop.create_task(self.send_image(event.src_path, thread))
#Calling observer in main                
observer = Observer()
event_handler = ImageHandler()

#When bot is connected to discord, on_ready is called.
#This starts the observer, which will wait for any update in the files.
@client.event
async def on_ready():
    print("Bot is ready.")
    observer.schedule(event_handler, path=GOES_PATH, recursive=True)
    observer.start()

client.run(TOKEN)