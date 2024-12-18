import configparser
import getpass
import os
import sys
import webbrowser
import keyring
if os.name == 'nt':
    os.system('color')

def create_config(config_path, config = None, write_config = True):
    config_changed = False
    default_config = configparser.ConfigParser()
    default_config['Login information'] = { 'service name': 'Elisa Viihde API',
                                            'username': '',
                                            'auto login': 'false' }
    default_config['General settings'] = { 'print help at start': 'true',
                                           'move prompt min': '1',
                                           'print at start': 'true',
                                           'print all': 'true',
                                           'sorting key': 'startTime',
                                           'sorting dir': 'asc',
                                           'recycle duplicates': 'false' }
    default_config['Download settings'] = { 'player': '\"C:\\Program Files\\MPC-HC\\mpc-hc64.exe\"',
                                            'platform': 'ios',
                                            'download folder': '',
                                            'folder structure': 'false',
                                            'season episode filename': 'false',
                                            'audio languages': 'fin, dut',
                                            'subtitle languages': 'fi, nl',
                                            'default audio': 'fin, dut',
                                            'default subtitle': 'fin, dut',
                                            'visual impaired': 'dut',
                                            'hearing impaired': 'dut',
                                            'maximum bandwidth': '0',
                                            'maximum width': '0',
                                            'maximum height': '0',
                                            'file extension': 'mkv',
                                            'external subtitles': 'true',
                                            'ffmpeg options': '-v error -stats',
                                            'ffmpeg video codec': 'copy',
                                            'ffmpeg audio codec': 'copy',
                                            'save description': 'true',
                                            'prompt overwrite': 'true' }
    defaults = [{'home': '0'}, {'esimerkki': 'C:\\Lataukset'}, {'nelonen': 'c nelonen | hero | liv | jim'}]
    if not config:
        config = default_config
        config_changed = True
    else:
        for s in ['Login information', 'General settings', 'Download settings']:
            if s in config:
                for k in default_config[s]:
                    if k in config[s]:
                        default_config[s][k] = config[s][k]
                    else:
                        config_changed = True
            else:
                config_changed = True
    for i, s in enumerate(['Folder shortcuts', 'Download folders', 'Filter shortcuts']):
        if s in config and not len(config[s]) == 0:
            default_config[s] = config[s]
        else:
            default_config[s] = defaults[i]
            config_changed = True
    if write_config and config_changed:
        if not os.path.exists(config_path):
            os.makedirs(config_path)
        with open(os.path.join(config_path, 'settings.ini'), 'w') as configfile:
            default_config.write(configfile)
    return default_config

def main():
    from . import version
    version = version.__version__
    print('ViihdeCLI ' + version + ' (c) 2021-2024 Qotscha\n')
    # Load config file.
    if os.name == 'nt':
        config_folder = os.path.join(os.environ['APPDATA'], 'viihdecli')
    elif os.name == 'posix' and sys.platform != 'darwin':
        config_folder = os.path.join(os.path.expanduser('~/.config'), 'viihdecli')
    config_path = os.path.join(config_folder, 'settings.ini')
    if not os.path.exists(config_path):
        config = create_config(config_folder)
    else:
        config = configparser.ConfigParser()
        config.read(config_path)
        config = create_config(config_folder, config)
    # config_path = os.path.join(config_folder, 'settings.ini')
    config_changed = False
    columns_path = os.path.join(config_folder, 'columns.ini')
    if not os.path.isfile(columns_path):
        columns = configparser.ConfigParser()
        columns['Recordings'] = { 'spacing': '3',
                                  'negative': 'true',
                                  'start day': 'true',
                                  'start date': 'true',
                                  'start time': 'true',
                                  'end day': 'false',
                                  'end date': 'false',
                                  'end time': 'true',
                                  'channel': '9',
                                  'duration': 'true',
                                  'name': '41',
                                  'folder': '12',
                                  'show imdb': 'true',
                                  'show live': 'true' }
        columns['Recycle bin'] = { 'spacing': '3',
                                   'negative': 'false',
                                   'removal day': 'false',
                                   'removal date': 'true',
                                   'removal time': 'false',
                                   'start day': 'true',
                                   'start date': 'true',
                                   'start time': 'true',
                                   'end day': 'false',
                                   'end date': 'false',
                                   'end time': 'false',
                                   'channel': '9',
                                   'duration': 'true',
                                   'name': '43',
                                   'folder': '13',
                                   'show imdb': 'true',
                                   'show live': 'true' }
        with open(columns_path, 'w') as configfile:
            columns.write(configfile)

    service_name = config['Login information']['service name']

    client_secret = 'nZhkFGz8Zd8w'
    api_key = 'Fjv8TK75OStLIz7Sc6jw6PvYQiIEgDtk'
    platform = config['Download settings']['platform']

    # Read/write username.
    save_username = ''
    username = config['Login information']['username']
    if username == '':
        username = input('Käyttäjätunnus: ')
        save_username = input('Tallennetaanko käyttäjätunnus (k/e)? ').lower()
        if save_username in ['k', 'y']:
            config['Login information']['username'] = username
            config_changed = True
    else:
        if config['Login information'].getboolean('auto login'):
            print('Kirjaudutaan käyttäjänä ' + username + '.')
        else:
            new_username = input('Kirjaudu käyttäjänä ' + username + ' painamalla ENTER '
                                'tai anna uusi käyttäjätunnus: ')
            if not new_username == '':
                config['Login information']['username'] = ''
                if not keyring.get_password(service_name, username) is None:
                    keyring.delete_password(service_name, username)
                username = new_username
                save_username = input('Tallennetaanko käyttäjätunnus (k/e)? ').lower()
                if save_username in ['k', 'y']:
                    config['Login information']['username'] = username
                config_changed = True

    # Load/save password.
    save_password = ''
    keyring_works = True
    try:
        password = keyring.get_password(service_name, username)
    except Exception as e:
        keyring_works = False
        password = None
        print('Kirjastoa keyring ei voida käyttää.')
        print(e)
    if password is None:
        print()
        password = getpass.getpass(prompt='Salasana: ')
        if keyring_works and (config['Login information'].getboolean('auto login') or save_username in ['k', 'y']):
            save_password = input('Tallennetaanko salasana (k/e)? ').lower()

    from . import viihdeapi

    try:
        headers = viihdeapi.login(client_secret, api_key, username, password)
        print('\nKirjautuminen onnistui.')
        if config_changed:
            with open(config_path, 'w') as configfile:
                config.write(configfile)
        if save_password in ['k', 'y']:
            keyring.set_password(service_name, username, password)
    except:
        print('\nKirjautuminen ei onnistunut. Tarkista käyttäjätunnus ja salasana.')
        config['Login information']['username'] = ''
        with open(config_path, 'w') as configfile:
            config.write(configfile)
        try:
            if not keyring.get_password(service_name, username) is None:
                keyring.delete_password(service_name, username)
        except:
            pass
        return

    from . import viihde

    while True:

        print('\nLatauskansio: \033[32m' + config['Download settings']['download folder'] + '\033[39m')
        # mode = input('\nValitse toimintatila [p] Liitä, [f] Kansiot, [a] Kaikki tallenteet tai [e] Ohjelmaopas: ').lower()
        mode = input('\nValitse toimintatila:\n   [d] Poista kirjautumistiedot\n   [p] Liitä\n   [f] Kansiot\n   [a] Kaikki tallenteet\
                      \n   [r] Roskakori\n   [c] Avaa asetustiedosto Muistiossa\n   [q] Sulje ohjelma\nValinta: ').lower()
        if mode == 'p':
            print()
            viihde.handle_input(headers)
        elif mode == 'i':
            account_info = viihdeapi.get_account_info(headers)
            print(account_info)
            account_quota = viihdeapi.get_quota(headers, platform)
            print(account_quota)
        elif mode == 'f':
            folder_tree = viihdeapi.get_folder_tree(headers, platform)
            viihde.handle_folders(folder_tree, headers)
        elif mode == 'a':
            folder_tree = viihdeapi.get_folder_tree(headers, platform)
            recordings = viihdeapi.get_all_recordings(config['General settings']['sorting key'], config['General settings']['sorting dir'], headers, platform)
            viihde.handle_recordings(folder_tree, recordings['recordings'], headers, config['General settings'].getboolean('print at start'))
        elif mode == 'r':
            folder_tree = viihdeapi.get_folder_tree(headers, platform)
            recordings = viihdeapi.get_recycle(config['General settings']['sorting key'], config['General settings']['sorting dir'], headers, platform)
            viihde.handle_recordings(folder_tree, recordings['recordings'], headers, config['General settings'].getboolean('print at start'), trash = True)
        elif mode == 'c':
            print('\nAvataan ' + config_path + ' Muistiossa.')
            webbrowser.open(config_path)
        elif mode == 'd':
            if not keyring.get_password(service_name, username) is None:
                keyring.delete_password(service_name, username)
                print('\nPoistettiin tallennettu salasana.')
            config['Login information']['username'] = ''
            with open(config_path, 'w') as configfile:
                config.write(configfile)
            print('Poistettiin käyttäjätunnus asetustiedostosta')
        else:
            break

if __name__ == "__main__":
    main()
