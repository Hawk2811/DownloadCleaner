#
#   DownloadCleaner - Simple script to clean downloads folder
#   main.py
#


import os
import shutil
from pathlib import Path
from datetime import datetime



date = datetime.now()
# JSON para organização das categorias e extensões de arquivos
DEST = {
    "Images": [".jpg",".jpeg",".png",".bmp",".svg",".webp"],
    "Videos": [".mp4", ".mov",".avi",".avi",".mkv",".wmv"],
    "Documents": [".pdf",".docx",".xlsx","pptx",".rtf",".txt"],
    "Compressed": [".zip",".rar",".7z",".tar",".gz"],
    "Audio": [".mp3",".wav",".ogg",".flac"],
    "Executables": [".exe",".msi"]
}


def get_downloads(): # Esta função e para pegar a pasta downloads do sistema seja ele Windows ou Linux
    if os.name == "posix": # Aqui no caso de for um Sistema UNIX-Like(macOS, Linux)
        if os.path.isdir(os.path.join(os.path.expanduser('~'), 'downloads')):
            return os.path.join(os.path.expanduser('~'), 'downloads')
        else:
            return os.path.join(os.path.expanduser('~'), 'Downloads')
        
    else: 
        import winreg # Em caso do sistema executando o Script for Windows ele importa a bibloteca winreg para acessar o Registro do Windows(RegEdit)
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location


def get_folder(ext: str): #Esta função e para pegar a Pasta que ele vai jogar os arquivos de cada extensão
    ext = ext.lower()
    for directory, exts in DEST.items():
        if ext in exts:
            return directory
    return None


def main(): # Função principal aqui é aonde fica toda a logica do programa
    for file in os.listdir(get_downloads()):
        if os.path.isfile(file) == False:
            filename, ext = os.path.splitext(file) # Esta função vai separar a extensão do arquivo do nome do arquivo
            folder_name = get_folder(ext)

            if folder_name:
                target_dir = os.path.join(get_downloads(),folder_name)

                if os.path.isdir(target_dir) == False:
                    os.makedirs(target_dir)

                final_path = os.path.join(target_dir, file)
                shutil.move(os.path.join(get_downloads(),file), final_path)

                print("Moved:",os.path.join(get_downloads(),file))

print("Completed in",date)


main()