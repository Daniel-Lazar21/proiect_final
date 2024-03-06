import os 
import threading 
from project_pack import ABSOLUTE_PATH_PROIECT
offline_path = ABSOLUTE_PATH_PROIECT + '\proiect_final\offline.py'
online_path = ABSOLUTE_PATH_PROIECT + '\proiect_final\web_structure\online.py'

#Imi definesc 2 functii pentru a deschide simultan aplicatia online si cea offline 

def open_offline_app():
    os.system(f"python {offline_path}")
    
def open_online_app():
    os.system(f"python {online_path}")
    
#definesc o functie care imi deschide 2 thread-uri si mai apoi rulez simultan functiile care deschid 
#aplicatia online  cat si cea offline
def create_and_start_threads():
    offline_thread = threading.Thread(target=open_offline_app)
    online_thread  = threading.Thread(target=open_online_app)

    offline_thread.start()
    online_thread.start()

if __name__ == "__main__":
    create_and_start_threads()    
    
