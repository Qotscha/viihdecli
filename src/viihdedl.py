import configparser
import os
import re
import sys
import ast
import time
import json
from subprocess import Popen
from . import viihdeapi
from . import naming_rules
if os.name == 'nt':
    os.system('color')

def main():
    if os.name == 'nt':
        config_folder = os.path.join(os.environ['APPDATA'], 'viihdecli')
    elif os.name == 'posix' and sys.platform != 'darwin':
        config_folder = os.path.join(os.path.expanduser('~/.config'), 'viihdecli')
    config_path = os.path.join(config_folder, 'settings.ini')
    config = configparser.ConfigParser()
    config.read(config_path)
    dl_settings = config['Download settings']
    dl_folder = dl_settings['download folder']
    folder_structure = dl_settings.getboolean('folder structure')

    arguments = sys.argv[1:]
    dl_list = []
    for i, x in enumerate(arguments):
        if x.isnumeric():
            dl_list.append(x)
        else:
            header_string = ' '.join(arguments[i:])
            break

    queue_size = len(dl_list) - 1
    headers = ast.literal_eval(header_string)

    if dl_folder == '':
        # print('Latauskansio: ' + os.getcwd() + '\\')
        print('Latauskansio: ' + os.getcwd())
    elif not dl_folder.endswith('\\'):
        # dl_folder += '\\'
        if not os.path.isdir(dl_folder): os.makedirs(dl_folder)
        print('Latauskansio: ' + dl_folder)
    else:
        if not os.path.isdir(dl_folder): os.makedirs(dl_folder)
        print('Latauskansio: ' + dl_folder)

    if folder_structure:
        with open(os.path.join(config_folder, 'kansiot.json')) as f:
            folders = json.load(f)

    for recording in dl_list:
        filename = dl_folder
        recording_info = viihdeapi.get_recording_info(recording, headers, dl_settings['platform'])
        recording_url = viihdeapi.get_recording_url(recording, headers, dl_settings['platform'])
        if folder_structure and 'folderId' in recording_info:
            if len(folders[str(recording_info['folderId'])][1]) > 1:
                for x in folders[str(recording_info['folderId'])][1][1:]:
                    filename = os.path.join(filename, re.sub(r'[\\/*?:"<>|]', "_", folders[str(x)][2]))
            filename = os.path.join(filename, re.sub(r'[\\/*?:"<>|]', "_", folders[str(recording_info['folderId'])][2]))
            if not os.path.isdir(filename): os.makedirs(filename)
        filename = os.path.join(filename, naming_rules.create_filename(recording_info))
        if dl_settings.getboolean('prompt overwrite') and os.path.isfile(filename + '.' + dl_settings['file extension']):
            overwrite = input('\nTiedosto \033[91m' + filename + '.' + dl_settings['file extension']
                              + '\033[39m on jo olemassa. Ladataanko se silti uudelleen (k/e)? ').lower()
            if not overwrite in ['k', 'y']:
                print('Tallennetta ei ladata uudestaan.')
                queue_size -= 1
                continue
        cmd = 'viihdexdl -c \"' + config_path + '\" -y '
        if dl_settings.getboolean('external subtitles'):
            cmd += '-e '
        cmd += '\"' + recording_url + '\" \"' + filename + '\"'

    # Save description
        if dl_settings.getboolean('save description'):
            file = open(filename + '.txt', 'w', encoding = 'utf-8')
            if 'description' in recording_info:
                file.write(recording_info['description'])
            else:
                file.write('Tallenteella ei ole kuvausta.')
            file.close()

        if queue_size == 1:
            print('\nJonossa \033[36m' + str(queue_size) + '\033[39m tallenne.')
        elif queue_size > 1:
            print('\nJonossa \033[36m' + str(queue_size) + '\033[39m tallennetta.')
        print()
        Popen(cmd, shell=True).wait()
        print()
        time.sleep(2)
        queue_size -= 1
    print()
    a = input('Tallenteet ladattu.')
