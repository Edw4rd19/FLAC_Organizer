import os
import mutagen
import traceback
import shutil
from colorama import Fore, Style, Back

# Set file extensions and IO folders.
ext1 = "flac"
source_folder2 = "D:\Musica\Discografias"
source_folder = "G:\Musica\Discografias"
destination_folder = "D:\\Musica\\Vacio"


def read_audio_file(audio_dir):

    audio = mutagen.File(audio_dir)
    destination = ''

    # Printing all the metadata
    #print(audio.pprint())

    try:
        disc_number = str(audio["discnumber"]).strip("'[]")
    except:
        disc_number = '0'
    try:
        disc_total = str(audio["disctotal"]).strip("'[]")
    except:
        try:
            disc_total = str(audio["totaldiscs"]).strip("'[]")
        except:
            disc_total = '0'
    try:
        srate = audio.info.sample_rate
    except:
        print(Fore.RED + "Error reading SAMPLE RATE " + audio_dir + Style.RESET_ALL)
    try:
        bits = audio.info.bits_per_sample
    except:
        print(Fore.RED + "Error reading BITS PER SAMPLE " + audio_dir + Style.RESET_ALL)

    try:
        artist = str(audio["albumartist"]).strip("'[]")
    except:
        try:
            artist = str(audio["artist"]).strip("'[]")
        except:
            print(Fore.RED + "Error reading ARTIST " + audio_dir + Style.RESET_ALL)
    try:
        album = str(audio["album"]).strip("'[]?")
    except:
        print(Fore.RED + "Error reading ALBUM " + audio_dir + Style.RESET_ALL)
    try:
        year = str(audio["year"]).strip("'[]")
    except:
        try:
            year = str(audio["date"]).strip("'[]")
        except:
            print(Fore.RED + "Error reading YEAR DATE " + audio_dir + Style.RESET_ALL)
    try:
        None
        folder_name = artist + "\\" + year + " - " + album + " [" + str(bits) + "bit-" + str(srate/1000) + "kHz]"

        for ch in ['~', '“', '"', '#', '%', '*', ':', '<', '>', '?', '/',  '{', '|', '}']:
            if ch in folder_name:
                folder_name = folder_name.replace(ch, "")

        if int(disc_number) * int(disc_total) > 1:
            destination = destination_folder + "\\" + folder_name + "\\Disk " + disc_number
        else:
            destination = destination_folder + "\\" + folder_name

        print("Artist: " + artist)
        print("Album: " + album + "   Year: " + year + "   Disc number: " + disc_number + "/" + disc_total)
        print("Bitrate: " + str(bits) + "   Sample rate[Hz]" + str(srate))
        print(Fore.LIGHTCYAN_EX + "SOURCE: " + audio_dir)
        print("DESTINATION: " + destination + Style.RESET_ALL)
        print("---------------------------------------------------------------------------")
    except:
        None
    #if artist.startswith('A') or artist.startswith('3'): destination = ''
    return destination

def copy_files(source, destination):
    try:
        if not os.path.exists(destination):
            print("Creating directory - " + destination)
            os.makedirs(destination)
            print("Directory created")
        # else:
        #     destination = destination + " QZ"
        shutil.copytree(source, destination, dirs_exist_ok=True)
        print(Fore.GREEN + "Files copied from " + source + " to " + destination + Style.RESET_ALL)
        print("---------------------------------------------------------------------------")
    except:
        print(Fore.RED + "Error copying " + source + " to " + destination + Style.RESET_ALL)
        print("---------------------------------------------------------------------------")

def merge_music_library():
    for path, dirlist, files in os.walk(source_folder):
        for file in files:
            file_ext = file[len(file)-(file[::-1].find('.')):]
            if file_ext == ext1:
                destination_path = read_audio_file(path + "\\" + file)
                if destination_path != '':
                    with open("errors.txt", "a") as log:
                        try:
                            copy_files(path, destination_path)
                            # Below line will print any print to log file as well.
                            print("File read to copy: " + file + "\n Fr: " + path + "\n To: " + destination_path, file=log)
                        except Exception:
                            traceback.print_exc(file=log)
                            continue
                break
    with open("errors.txt", "a"):
        print("Copy files finished")


def all_upper(my_list):
    return [x.upper() for x in my_list]

def empty_folders_check():
    files = os.listdir(source_folder)
    for file in files:
        folder = source_folder + "\\" + file
        #print(folder)
        if os.path.isdir(folder):
            if not os.listdir(folder):
                print(folder)

def empty_folders_extract():
    paths = []

    main_library = os.listdir(source_folder)
    second_library = os.listdir(source_folder2)

    for folder in second_library:
        if folder.upper() not in all_upper(main_library):
            paths.append(source_folder2 + '\\' + folder)
    for path in paths:
        if os.path.isdir(path):
            if not os.listdir(path):
                print(path)
                artist = path[len(path)-(path[::-1].find('\\')):]
                destination = destination_folder + "\\" + artist
                if not os.path.exists(destination):
                    print( artist + " does not exist on: " + destination)
                    print("Creating directory: " + path)
                    os.makedirs(destination)


empty_folders_extract()




