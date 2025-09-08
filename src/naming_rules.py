import configparser
import os
import sys
import re

if os.name == 'nt':
    config_folder = os.path.join(os.environ['APPDATA'], 'viihdecli')
elif os.name == 'posix' and sys.platform != 'darwin':
    config_folder = os.path.join(os.path.expanduser('~/.config'), 'viihdecli')
config_path = os.path.join(config_folder, 'settings.ini')
config = configparser.ConfigParser()
config.read(config_path)
dl_settings = config['Download settings']
dl_folder = dl_settings['download folder']

def create_filename(recording_info):
    filename = re.sub(r'[\\/*?:"<>|]',"_",recording_info['name'])

    # Add series and episode information to the filename if available (e.g. S02E14)
    if dl_settings.getboolean('season episode filename'):
        if ('series' in recording_info and 'season' in recording_info['series']
            and 'episode' in recording_info['series']):
            filename = filename.strip()
            if filename.endswith(')'):
                filename = filename.rsplit('(', 1)[0].strip()
            season = recording_info['series']['season']
            episode = recording_info['series']['episode']
            filename += ' S' + str(season).zfill(2) + 'E' + str(episode).zfill(2)
            return filename

    recording_time = recording_info['startTime'].split()
    filename += ' ' + (recording_time[0].replace('-', '.') + ' '
                + recording_time[1].rsplit(':',1)[0].replace(':', '.'))
    return filename

def create_text_file(recording_info):
    return recording_info['description']
