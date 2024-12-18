import configparser
import os
import sys
import re
import json
import webbrowser
import time
from datetime import date, timedelta
from subprocess import Popen
if os.name == 'nt':
    from subprocess import CREATE_NEW_CONSOLE
from . import viihdeapi
from . import command_strings
from . import viihdehelp
from .filter_recordings import filter_recordings
from .print_recordings import print_recordings, show_terminal_width
from .duplicates import list_duplicates

if os.name == 'nt':
    config_folder = os.path.join(os.environ['APPDATA'], 'viihdecli')
elif os.name == 'posix' and sys.platform != 'darwin':
    config_folder = os.path.join(os.path.expanduser('~/.config'), 'viihdecli')
config_path = os.path.join(config_folder, 'settings.ini')
config = configparser.ConfigParser()
config.read(config_path)
platform = config['Download settings']['platform']

columns_path = os.path.join(config_folder, 'columns.ini')
columns = configparser.ConfigParser()
columns.read(columns_path)

def create_number_list(number_string, last_item):
    number_string = number_string.replace(',', ' ')
    raw_number_list = number_string.split()
    number_list = []
    for x in raw_number_list:
        to_add = []
        reverse_list = False
        if x.startswith('!'):
            reverse_list = True
            x = x.strip('!')
        y = x.split(':')
        if len(y) == 1:
            following = 0
            previous = 0
            while x[-1] in ['+', '-']:
                if x[-1] == '+':
                    following += 1
                else:
                    previous += 1
                x = x[:-1]
            x_ = int(x)
            x_ = x_ + last_item + 1 if x_ < 0 else x_
            to_add = list(range(x_ - previous, x_ + following + 1))
        elif len(y) == 2:
            y[0] = 0 if not y[0] else int(y[0])
            y[1] = last_item if not y[1] else int(y[1])
            y = [z + last_item + 1 if z < 0 else z for z in y]
            to_add = list(range(y[0], y[1] + 1)) if y[0] <= y[1] else list(range(y[0], y[1] - 1, -1))
        elif len(y) == 3:
            step = 1 if not y[1] else int(y[1])
            y.pop(1)
            if step < 0:
                y[0] = last_item if not y[0] else int(y[0])
                y[1] = 0 if not y[1] else int(y[1])
                y = [z + last_item + 1 if z < 0 else z for z in y]
                to_add = list(range(y[0], y[1] - 1, step))
            else:
                y[0] = 0 if not y[0] else int(y[0])
                y[1] = last_item if not y[1] else int(y[1])
                y = [z + last_item + 1 if z < 0 else z for z in y]
                to_add = list(range(y[0], y[1] + 1, step)) if y[1] > y[0] else list(range(y[0], y[1] - 1, -step))
        if reverse_list:
            to_add.reverse()
        if to_add: number_list += to_add
    return number_list

def set_filter_shortcut(shortcut, f_list, so):
    for i, x in enumerate(f_list):
        if len(f_list) == 1:
            config['Filter shortcuts'][shortcut] = x
        else:
            config['Filter shortcuts'][f'{shortcut}_{i}'] = x
    if so:
        config['Filter shortcuts'][f'{shortcut}_so_'] = so
    with open(config_path, 'w') as configfile:
        config.write(configfile)
    print('Luotiin pikavalinta \033[92m' + shortcut + '\033[39m suotimille')
    for x in f_list:
        print('   ' + x)
    print(f'   Sääntö: {so}')

def list_filter_shortcuts():
    filter_dict = dict(config['Filter shortcuts'])
    f_items = list(filter_dict.items())
    print('\n\033[92m' + '{:<20}{}'.format('Pikavalinta', 'Komento') + '\033[39m')
    f_group = False
    f_i = 0
    for i, x in enumerate(f_items):
        if x[0].endswith('_0') and f'{x[0][:-1]}1' in filter_dict:
            print(f'\033[32m{x[0][:-2]}\033[39m')
            print('   {:<20}{}'.format(x[0], x[1]))
            f_i = 1
        elif f_i > 0 and x[0].endswith(f'_{f_i}'):
            print('   {:<20}{}'.format(x[0], x[1]))
            f_i += 1
        elif f_i > 0 and x[0].endswith('_so_'):
            print(f'   Sääntö: {x[1]}')
        else:
            f_i = 0
            print('{:<20}{}'.format(x[0].strip('_0'), x[1]))
    print()

def set_folder_shortcut(folder_id, shortcut, folder_name = '', print_msg = True):
    config['Folder shortcuts'][shortcut] = str(folder_id)
    with open(config_path, 'w') as configfile:
        config.write(configfile)
    if print_msg:
        print('Luotiin pikavalinta \033[92m' + shortcut + '\033[39m kansiolle \033[32m' + folder_name + '\033[39m.')

def list_folder_shortcuts(folder_dict):
    shortcut_dict = dict(config['Folder shortcuts'])
    print('\n\033[92m' + '{:<20}{}'.format('Pikavalinta', 'Kansio') + '\033[39m')
    for x in shortcut_dict:
        if not folder_dict.get(int(shortcut_dict[x])):
            config.remove_option('Folder shortcuts', x)
            with open(config_path, 'w') as configfile:
                config.write(configfile)
        else:
            print('{:<20}{}'.format(x, folder_dict.get(int(shortcut_dict[x]))[0]))
    print()

def set_dl_folder(dl_folder):
    config['Download settings']['download folder'] = dl_folder
    print('Latauskansio: \033[32m' + dl_folder + '\033[39m')
    with open(config_path, 'w') as configfile:
        config.write(configfile)

def set_dl_folder_shortcut(dl_folder, shortcut):
    config['Download folders'][shortcut] = dl_folder
    with open(config_path, 'w') as configfile:
        config.write(configfile)
    print('Luotiin pikavalinta \033[92m' + shortcut + '\033[39m latauskansiolle \033[32m' + dl_folder + '\033[39m.')

def list_dl_folders():
    print('\nNykyinen latauskansio: \033[32m' + config['Download settings']['download folder'] + '\033[39m')
    dl_folder_dict = dict(config['Download folders'])
    print('\n\033[92m' + '{:<20}{}'.format('Pikavalinta', 'Latauskansio') + '\033[39m')
    for x in dl_folder_dict:
        print('{:<20}{}'.format(x, dl_folder_dict[x]))
    print()

def play_recording(recording_id, headers, get_url_only = False):
    recording_url = viihdeapi.get_recording_url(recording_id, headers, platform)
    if get_url_only:
        return recording_url
    # cmd = 'wscript.exe \"C:\\Ohjelmat\\Elisa Viihde Media Manager\\run_mpc-hc_hls.vbs\" ' + recording_url
    cmd = config['Download settings']['player'] + ' ' + recording_url
    # print(cmd)
    Popen(cmd)

def download_folder(folder_id, headers):
    folder_info = viihdeapi.get_recordings(folder_id, 'startTime', 'asc', headers, platform)
    cmd = 'viihdedl '
    for x in folder_info['recordings']:
        cmd += str(x['programId']) + ' '
    # print(cmd)
    cmd += str(headers)
    Popen(cmd, creationflags=CREATE_NEW_CONSOLE)

def handle_folders(folder_tree, headers, move_recordings = False, folder_dict = None):
    global platform
    if not folder_dict:
        folder_dict = create_folder_dict(folder_tree)
    folder_numbers = []
    current_folder = list_folders(folder_dict, folder_tree, folder_numbers)
    if config['General settings'].getboolean('print help at start'):
        viihdehelp.print_help('folders')
        print()
    while True:
        try:
            folder_number = input('Mene kansioon X tai anna muu komento: ').strip()
            if folder_number == '':
                break
            if folder_number == command_strings.SHOW_HELP:
                print()
                viihdehelp.print_help('folders')
                print()
                continue
            elif folder_number == command_strings.SHOW_QUOTA:
                account_quota = viihdeapi.get_quota(headers, platform)
                seconds = account_quota['secondsLeft']
                hours_seconds = divmod(seconds, 3600)
                minutes = hours_seconds[1] // 60
                print(f'Tallennustilaa jäljellä {hours_seconds[0]} tuntia, {minutes} minuuttia')
                continue
            elif folder_number == command_strings.ROOT_FOLDER:
                folder_numbers = []
            elif folder_number == command_strings.FOLDER_UP:
                folder_numbers.pop()
            elif folder_number == command_strings.LIST_FOLDERS:
                pass
            elif folder_number == command_strings.REFRESH_RECORDINGS:
                folder_tree = viihdeapi.get_folder_tree(headers, platform)
                folder_dict = create_folder_dict(folder_tree)
            elif folder_number.isnumeric():
                folder_numbers.append(int(folder_number))
            elif folder_number.startswith(command_strings.NEW_FOLDER):
                new_folder_name = folder_number.split(' ', 1)[1]
                new_folder = viihdeapi.create_folder(new_folder_name, str(current_folder['id']), headers, platform)
                folder_tree = viihdeapi.get_folder_tree(headers, platform)
                folder_dict = create_folder_dict(folder_tree)
            elif folder_number == command_strings.LIST_RECORDINGS:
                recordings = viihdeapi.get_recordings(str(current_folder['id']), 'startTime', 'asc', headers, platform)
                if move_recordings:
                    refresh_folders = handle_recordings(folder_tree, recordings['recordings'], headers, True, True, current_folder['id'])
                else:
                    refresh_folders = handle_recordings(folder_tree, recordings['recordings'], headers, True, False, current_folder['id'])
                if refresh_folders:
                    folder_tree = viihdeapi.get_folder_tree(headers, platform)
            elif folder_number == command_strings.DOWNLOAD_FOLDER:
                download_folder(str(current_folder['id']), headers)
                continue
            elif folder_number.startswith(command_strings.SET_SHORTCUT):
                set_folder_shortcut(current_folder['id'], folder_number.split(' ', 1)[1], folder_dict[current_folder['id']][0])
                continue
            elif folder_number == command_strings.LIST_FOLDER_SHORTCUTS:
                list_folder_shortcuts(folder_dict)
                continue
            elif folder_number.startswith(command_strings.DL_FOLDER_SHORTCUT):
                set_dl_folder(config['Download folders'][folder_number.split(' ', 1)[1]])
                continue
            elif folder_number.startswith(command_strings.SET_DL_FOLDER):
                set_dl_folder(folder_number.split(' ', 1)[1])
                continue
            elif folder_number.startswith(command_strings.SET_DL_FOLDER_SHORTCUT):
                f_split = folder_number.split(' ', 1)[1].split('|', 1)
                if len(f_split) == 1:
                    f_split.append(config['Download settings']['download folder'])
                set_dl_folder_shortcut(f_split[1].strip(), f_split[0].strip())
                continue
            elif folder_number == command_strings.LIST_DL_FOLDERS:
                list_dl_folders()
                continue
            elif folder_number.startswith(command_strings.DELETE_FOLDER):
                if folder_number == command_strings.DELETE_FOLDER:
                    del_folder = current_folder
                    folder_numbers.pop()
                else:
                    del_folder = current_folder['folders'][int(folder_number.split()[1])]
                del_confirmation = input('Haluatko varmasti poistaa kansion ' + str(del_folder['name']) + ' tallenteineen (k/e)? ')
                if del_confirmation in ['k', 'y']:
                    if viihdeapi.delete_folder(str(del_folder['id']), headers, platform) == 200:
                        print('Kansio ' + str(del_folder['name']) + ' poistettiin.')
                        folder_tree = viihdeapi.get_folder_tree(headers, platform)
                        folder_dict.pop(del_folder['id'])
            elif folder_number == command_strings.RELOAD_CONFIG:
                config['Folder shortcuts'] = {}
                config['Download folders'] = {}
                config.read(config_path)
                columns.read(columns_path)
                platform = config['Download settings']['platform']
                print('Asetukset päivitetty.')
                continue
            elif folder_number == command_strings.OPEN_CONFIG:
                print('Avataan ' + config_path + ' Muistiossa.')
                print('Muokattuasi asetustiedostoa kirjoita ' + command_strings.RELOAD_CONFIG + ' päivittääksesi asetukset.')
                webbrowser.open(config_path)
            elif folder_number == command_strings.OPEN_COLUMNS:
                print('Avataan ' + columns_path + ' Muistiossa.')
                print('Muokattuasi asetustiedostoa kirjoita ' + command_strings.RELOAD_CONFIG + ' päivittääksesi asetukset.')
                webbrowser.open(columns_path)
            else:
                print('Komentoa ei tunnistettu.')
                continue
            current_folder = list_folders(folder_dict, folder_tree, folder_numbers)
        except:
            print('Virheellinen komento.')
            # raise
        # except Exception as e: print(e)
    return current_folder['id'], folder_tree, folder_dict

def list_folders(folder_dict, current_folder, folder_numbers):
    for x in folder_numbers:
        current_folder = current_folder['folders'][x]
    print('\nNykyinen kansio: \033[32m' + folder_dict[current_folder['id']][0] + '\033[39m')
    print('\n\033[92m{:<5}{:<35}{:<14}{}\033[39m'.format('#', 'Kansio', 'Tallenteita', 'Tallenteita ml. alikansiot'))
    for i, x in enumerate(current_folder['folders']):
        print('{:<5}{:<35}{:<14}{}'.format(str(i), x['name'], x['recordingsCount'], x['totalRecordingsCount']))
    if current_folder['recordingsCount'] == 1:
        print('Kansiossa 1 tallenne.')
    else:
        print('Kansiossa ' + str(current_folder['recordingsCount']) + ' tallennetta.')
    print()
    return current_folder

def create_folder_dict(folder_tree):
    folder_dict = {}
    folder_dict = folder_loop(folder_dict, folder_tree['folders'], folder_tree['id'], '', tuple())
    folder_dict[0] = ['(Tallennekansio)', None, '(Tallennekansio)']
    if config['Download settings'].getboolean('folder structure'):
        if os.name == 'nt':
            config_folder = os.path.join(os.environ['APPDATA'], 'viihdecli')
        elif os.name == 'posix' and sys.platform != 'darwin':
            config_folder = os.path.join(os.path.expanduser('~/.config'), 'viihdecli')
        with open (os.path.join(config_folder, 'kansiot.json'), 'w') as f:
            json.dump(folder_dict, f)
    return folder_dict

def folder_loop(folder_dict, folder, folder_id, folder_path, parent_folders):
    for x in folder:
        parent_folder_list = list(parent_folders)
        parent_folder_list.append(folder_id)
        folder_dict[x['id']] = [folder_path + x['name'], parent_folder_list, x['name']]
        if len(x['folders']) > 0:
            folder_loop(folder_dict, x['folders'], x['id'], folder_dict[x['id']][0] + ' / ', tuple(folder_dict[x['id']][1]))
    return folder_dict

def handle_recordings(folders, recording_list, headers, list_recordings = False, list_only = False, folder = None,
                     hl_set = set(), prompt = 'Käsittele tallenteita: ', trash = False):
    recordings_moved = False
    folder_dict = create_folder_dict(folders)
    sorting_key = config['General settings']['sorting key']
    sorting_dir = config['General settings']['sorting dir']
    imdb_sort = False
    all_recordings = set()
    for x in recording_list:
        all_recordings.add(x['programId'])
    all_filtered = all_recordings
    all_filtered_list = update_all_filtered_list(recording_list, all_recordings)
    print_descriptions = False
    if list_recordings:
        print_recordings(columns, folder_dict, all_filtered_list, hl_set, print_descriptions, trash)
    if list_only:
        return
    filtered_recordings = {}
    set_operations = ''
    global platform
    if config['General settings'].getboolean('print help at start') and not hl_set:
        viihdehelp.print_help('recordings', trash)
        print()
    while True:
        try:
            f_string = input(prompt).strip()
            if f_string == '':
                return recordings_moved
            if f_string.startswith(command_strings.USE_FILTER_SHORTCUT):
                shortcut = f_string[1:].strip()
                lf = len(filtered_recordings)
                dup_filters = []
                if shortcut in config['Filter shortcuts']:
                    f_list = [config['Filter shortcuts'][shortcut]]
                elif f'{shortcut}_0' in config['Filter shortcuts']:
                    i = 0
                    f_list = []
                    while f'{shortcut}_{i}' in config['Filter shortcuts']:
                        f_list.append(config['Filter shortcuts'][f'{shortcut}_{i}'])
                        i += 1
                for i, x in enumerate(f_list):
                    f_string = x
                    if f_string[0] == '!':
                        not_in = True
                        f_string = f_string[1:]
                    else:
                        not_in = False
                    f_split = f_string.split(' ', 1)
                    valid_filter, filtered_recordings = filter_recordings(recording_list, filtered_recordings, not_in, f_split[0], f_split[1].upper())
                    if valid_filter == 2:
                        dup_filters.append(i)
                if not dup_filters and f'{shortcut}_so_' in config['Filter shortcuts']:
                    so = config['Filter shortcuts'][f'{shortcut}_so_']
                    if lf == 0:
                        set_operations = so
                    else:
                        so = re.sub(r'\d+', lambda x: str(int(x.group(0)) + lf), so)
                        if not set_operations and lf > 0:
                            set_operations = '0'
                            for i in range(1, lf):
                                set_operations += f' & {i}'
                        set_operations = f'({set_operations}) & ({so})'
                elif set_operations:
                    so = str(lf)
                    # print(f'Dups: {len(dup_filters)}')
                    dups = 0
                    for i in range(lf + 1, lf + len(f_list)):
                        if i - lf - 1 not in dup_filters:
                            so += f' & {i - dups}'
                        else:
                            dups += 1
                    set_operations = f'({set_operations}) & ({so})'
                if set_operations:
                    # print(set_operations)
                    all_filtered = custom_filter(all_recordings, filtered_recordings, set_operations)
                else:
                    all_filtered = update_all_filtered(all_recordings, filtered_recordings)
                all_filtered_list = update_all_filtered_list(recording_list, all_filtered)
                print_recordings(columns, folder_dict, all_filtered_list, hl_set, print_descriptions, trash)
                continue
            if f_string[0] == '!':
                not_in = True
                f_string = f_string[1:]
            else:
                not_in = False

            if f_string == command_strings.SHOW_HELP:
                print()
                viihdehelp.print_help('recordings', trash)
                print()

            elif f_string == command_strings.SHOW_FILTER_HELP:
                print()
                viihdehelp.print_help('filters')
                print()

            elif f_string == command_strings.SHOW_SORTING_HELP:
                print()
                viihdehelp.print_help('sorting', trash)
                print()

            elif f_string == command_strings.SHOW_WIDTH:
                print()
                show_terminal_width(columns, len(all_filtered_list), trash)
                print()

            elif f_string == command_strings.SHOW_QUOTA:
                account_quota = viihdeapi.get_quota(headers, platform)
                seconds = account_quota['secondsLeft']
                hours_seconds = divmod(seconds, 3600)
                minutes = hours_seconds[1] // 60
                print(f'Tallennustilaa jäljellä {hours_seconds[0]} tuntia, {minutes} minuuttia')

            elif f_string == command_strings.CLEAR_FILTERS:
                filtered_recordings = {}
                set_operations = ''
                print('Suotimet tyhjennetty.')
                all_filtered = all_recordings
                all_filtered_list = update_all_filtered_list(recording_list, all_filtered)

            elif f_string == command_strings.CLEAR_LAST_FILTER:
                print('Suodin poistettu: ' + str(filtered_recordings.popitem()[0]))
                set_operations = ''
                all_filtered = update_all_filtered(all_recordings, filtered_recordings)
                all_filtered_list = update_all_filtered_list(recording_list, all_filtered)
                if len(filtered_recordings) > 0:
                    print_recordings(columns, folder_dict, all_filtered_list, hl_set, print_descriptions, trash)

            elif f_string.startswith(command_strings.CLEAR_FILTER):
                f_split = int(f_string.split(' ', 1)[1])
                remove_filter = list(filtered_recordings)[f_split]
                filtered_recordings.pop(remove_filter)
                set_operations = ''
                print('Suodin poistettu: ' + str(remove_filter))
                all_filtered = update_all_filtered(all_recordings, filtered_recordings)
                all_filtered_list = update_all_filtered_list(recording_list, all_filtered)
                if len(filtered_recordings) > 0:
                    print_recordings(columns, folder_dict, all_filtered_list, hl_set, print_descriptions, trash)

            elif f_string == command_strings.LIST_FILTERED:
                if len(filtered_recordings) == 0:
                    all_filtered = all_recordings
                    all_filtered_list = update_all_filtered_list(recording_list, all_filtered)
                print_recordings(columns, folder_dict, all_filtered_list, hl_set, print_descriptions, trash)

            elif f_string == command_strings.LIST_FILTERS:
                print('\nAktiiviset suotimet:')
                for i, x in enumerate(list(filtered_recordings)):
                    if set_operations and str(i) not in set_operations:
                        print(f'\033[31m{str(i):<5}{x}\033[39m')
                    else:
                        print(f'{str(i):<5}{x}')
                if set_operations:
                    print('Sääntö: ' + set_operations)
                print()

            elif f_string == command_strings.REFRESH_RECORDINGS:
                if not hl_set:
                    folders = viihdeapi.get_folder_tree(headers, platform)
                    folder_dict = create_folder_dict(folders)
                    if trash:
                        recording_list = viihdeapi.get_recycle(sorting_key, sorting_dir, headers, platform)['recordings']
                    elif folder is None:
                        recording_list = viihdeapi.get_all_recordings(sorting_key, sorting_dir, headers, platform)['recordings']
                    else:
                        recording_list = viihdeapi.get_recordings(str(folder), sorting_key, sorting_dir, headers, platform)['recordings']
                    if imdb_sort:
                        recording_list = sort_recordings(recording_list, 'imdbRating', False if sorting_dir == 'asc' else True)
                    all_recordings = set()
                    for x in recording_list:
                        all_recordings.add(x['programId'])
                        # if 'folderId' in x and not x['folderId'] in folder_dict:
                            # folders = viihdeapi.get_folder_tree(headers, platform)
                            # folder_dict = create_folder_dict(folders)
                            # break
                    if not filtered_recordings:
                        all_filtered = all_recordings
                    else:
                        filtered_recordings_ = {}
                        for y in filtered_recordings.values():
                            if not y[2]:
                                rem_set = y[1] & all_recordings
                                if rem_set:
                                    dict_key = 'Piilotettu listauksesta'
                                    filtered_recordings_[dict_key] = [True, rem_set, None]
                            else:
                                filtered_recordings_ = filter_recordings(recording_list, filtered_recordings_, y[0], y[2][0], y[2][1])[1]
                        filtered_recordings = filtered_recordings_
                        if set_operations:
                            all_filtered = custom_filter(all_recordings, filtered_recordings, set_operations)
                        else:
                            all_filtered = update_all_filtered(all_recordings, filtered_recordings)
                    all_filtered_list = update_all_filtered_list(recording_list, all_filtered)
                    if filtered_recordings or config['General settings'].getboolean('print all'):
                        print_recordings(columns, folder_dict, all_filtered_list, hl_set, print_descriptions, trash)
                else:
                    print('Tallenteita ei voi päivittää duplikaatteja käsitellessä.')

            elif f_string.startswith(command_strings.REMOVE_DUPLICATES):
                if not hl_set:
                    stime = time.time()
                    f_split = f_string.split(' ', 1)
                    if len(f_split) > 1:
                        if f_split[1] in ['1', '2', '3', '4', '5', '6', '7']:
                            mode = int(f_split[1])
                            duplicate_set, duplicate_list = list_duplicates(all_filtered_list.copy(), mode)
                        else:
                            mode = 0
                            use_description = 'd' in f_split[1]
                            use_name = 'n' in f_split[1]
                            use_metadata = 'm' in f_split[1]
                            dot_index = f_split[1].find('.') + 1
                            max_dur_diff = None
                            if not dot_index == -1:
                                digits = ''
                                for i in f_split[1][dot_index:]:
                                    if i.isdigit():
                                        digits += i
                                    else:
                                        break
                                if digits: max_dur_diff = int(digits)
                            duplicate_set, duplicate_list = list_duplicates(all_filtered_list.copy(), mode, use_description, use_name, use_metadata, max_dur_diff)
                    else:
                        duplicate_set, duplicate_list = list_duplicates(all_filtered_list.copy())

                    print(f'Duplikaattien hakuun kului {time.time() - stime} sekuntia.')
                    # print(duplicate_set)
                    if duplicate_set:
                        handle_recordings(folders, duplicate_list, headers, True, True, None, duplicate_set)
                        del_prompt = input('Haluatko poistaa kaikki duplikaatit (k/e)? ')
                        if del_prompt in ['k', 'y']:
                            del_list = []
                            for x in duplicate_list:
                                if x['programId'] in duplicate_set:
                                    del_list.append(x)
                            del_list_str = ','.join(map(str,[x['programId'] for x in del_list]))
                            if config['General settings'].getboolean('recycle duplicates'):
                                if viihdeapi.delete_recordings(del_list_str, headers, platform) == 200:
                                    recordings_moved = True
                                    print('Duplikaatit siirrettiin Viihteen roskakoriin.')
                                    not_in_folder = [x['programId'] for x in del_list]
                                    recording_list = [x for x in recording_list if not x['programId'] in not_in_folder]
                                    for x in not_in_folder:
                                        all_recordings.remove(x)
                                    all_filtered = update_all_filtered(all_recordings, filtered_recordings)
                                    all_filtered_list = update_all_filtered_list(recording_list, all_filtered)
                                    folders = viihdeapi.get_folder_tree(headers, platform)
                            else:
                                if not config.has_option('Folder shortcuts','trash'):
                                    print('Valitse kansio, jota käytetään roskakorina.')
                                    trash_id, folders, folder_dict = handle_folders(folders, headers, True, folder_dict)
                                    set_folder_shortcut(trash_id, 'trash', print_msg = False)
                                else:
                                    trash_id = config['Folder shortcuts']['trash']
                                if viihdeapi.move_recordings(del_list_str, trash_id, headers, platform) == 200:
                                    recordings_moved = True
                                    print('Duplikaatit siirrettiin roskakorikansioon.')
                                    if folder is None:
                                        for x in del_list:
                                            x['folderId'] = int(trash_id)
                                    elif folder != trash_id:
                                        not_in_folder = [x['programId'] for x in del_list]
                                        recording_list = [x for x in recording_list if not x['programId'] in not_in_folder]
                                        for x in not_in_folder:
                                            all_recordings.remove(x)
                                        all_filtered = update_all_filtered(all_recordings, filtered_recordings)
                                        all_filtered_list = update_all_filtered_list(recording_list, all_filtered)
                                    folders = viihdeapi.get_folder_tree(headers, platform)
                        else:
                            handle_recordings(folders, duplicate_list, headers, False, False, None, duplicate_set, 'Käsittele duplikaatteja: ')
                    else:
                        print('Duplikaatteja ei löydetty.')
                else:
                    print('Duplikaatteja ollaan jo käsittelemässä.')

            elif f_string.startswith(command_strings.CHANNEL_DAY):
                f_split = f_string.split(' ', 1)
                recording_info = all_filtered_list[int(f_split[1])]
                start_date = date.fromisoformat(recording_info['startTime'].split()[0])
                days_between = [start_date - timedelta(days=1), start_date + timedelta(days=2)]
                channel = recording_info['channelName']
                filter_list = [[False, 'c', channel], [True, 'b', days_between[0].isoformat()], [False, 'b', days_between[1].isoformat()]]
                filtered_recordings_ = {}
                for x in filter_list:
                    filtered_recordings_ = filter_recordings(recording_list, filtered_recordings_, x[0], x[1], x[2].upper())[1]
                all_filtered_ = update_all_filtered(all_recordings, filtered_recordings_)
                all_filtered_list_ = update_all_filtered_list(recording_list, all_filtered_)
                handle_recordings(folders, all_filtered_list_, headers, True, False, None, {recording_info['programId']}, 'Käsittele tallenteita: ')

            elif f_string.startswith(command_strings.HIDE_RECORDINGS):
                to_remove = create_number_list(f_string.split(' ', 1)[1], len(all_filtered) - 1)
                dict_key = 'Piilotettu listauksesta'
                if dict_key not in filtered_recordings:
                    filtered_recordings[dict_key] = [True, set(), None]
                for x in to_remove:
                    filtered_recordings[dict_key][1].add(all_filtered_list[x]['programId'])
                all_filtered = update_all_filtered(all_recordings, filtered_recordings)
                all_filtered_list = update_all_filtered_list(recording_list, all_filtered)
                print_recordings(columns, folder_dict, all_filtered_list, hl_set, print_descriptions, trash)

            elif f_string.startswith(command_strings.PLAY_RECORDING):
                if trash:
                    print('Viihteen roskakorissa olevia tallenteita ei voida toistaa.')
                    print('Jos haluat katsoa tallenteen, palauta se roskakorista.')
                else:
                    f_split = f_string.split(' ', 1)
                    play_recording(str(all_filtered_list[int(f_split[1])]['programId']), headers)
                    print('Toistetaan tallenne ' + all_filtered_list[int(f_split[1])]['name'] + '.')

            elif f_string.startswith(command_strings.SHOW_DESCRIPTION):
                f_split = f_string.split(' ', 1)
                print()
                print(all_filtered_list[int(f_split[1])]['name'])
                print(all_filtered_list[int(f_split[1])].get('description'))

            elif f_string == command_strings.PRINT_DESCRIPTIONS:
                print_descriptions = not print_descriptions
                print_recordings(columns, folder_dict, all_filtered_list, hl_set, print_descriptions, trash)

            elif f_string.startswith(command_strings.SHOW_INFO):
                f_split = f_string.split(' ', 1)
                recording_info = all_filtered_list[int(f_split[1])]
                print()
                for x in recording_info:
                    print(x,':',recording_info[x])
                print()

            elif f_string.startswith(command_strings.SHOW_URL):
                f_split = f_string.split(' ', 1)
                recording_url = play_recording(str(all_filtered_list[int(f_split[1])]['programId']), headers, True)
                print('Tallenteen ' + all_filtered_list[int(f_split[1])]['name'] + ' URL: ' + recording_url)

            elif f_string.startswith(command_strings.DOWNLOAD_RECORDINGS):
                if trash:
                    print('Viihteen roskakorissa olevia tallenteita ei voida ladata.')
                    print('Jos haluat ladata tallenteita, palauta ne roskakorista.')
                else:
                    f_split = f_string.split(' ', 1)
                    cmd = 'viihdedl '
                    if f_split[1] == 'a':
                        if len(all_filtered) > 0:
                            print('Ladataan suodatetut tallenteet.')
                            cmd += ' '.join([str(x['programId']) for x in all_filtered_list]) + ' '
                    else:
                        dl_list = create_number_list(f_split[1], len(all_filtered) - 1)
                        for x in dl_list:
                            cmd += str(all_filtered_list[x]['programId']) + ' '
                    cmd += f'"{str(headers)}"'
                    # print(cmd)
                    if os.name == 'nt':
                        Popen(cmd, creationflags=CREATE_NEW_CONSOLE)
                    else:
                        Popen(cmd, shell=True).wait()

            elif f_string.startswith(command_strings.RESTORE_RECORDINGS):
                f_split = f_string.split(' ', 1)
                if f_split[1] == 'a':
                    if len(all_filtered) > 0:
                        res_list = all_filtered_list
                        res_list_str = ','.join(map(str,all_filtered))
                else:
                    res_list = []
                    for x in create_number_list(f_split[1], len(all_filtered) - 1):
                        res_list.append(all_filtered_list[x])
                    res_list_str = ','.join(map(str,[x['programId'] for x in res_list]))
                if viihdeapi.restore_recordings(res_list_str, headers, platform) == 200:
                    recordings_moved = True
                    print('Valitut tallenteet palautettiin Viihteen roskakorista.')
                    # for x in res_list:
                        # x['folderId'] = int(trash_id)
                    # folders = folder_tree = viihdeapi.get_folder_tree(headers, platform)

            elif f_string.startswith(command_strings.RECYCLE_RECORDINGS):
                f_split = f_string.split(' ', 1)
                if f_split[1] == 'a':
                    if len(all_filtered) > 0:
                        del_list = all_filtered_list
                        del_list_str = ','.join(map(str,all_filtered))
                else:
                    del_list = []
                    for x in create_number_list(f_split[1], len(all_filtered) - 1):
                        del_list.append(all_filtered_list[x])
                    del_list_str = ','.join(map(str,[x['programId'] for x in del_list]))
                if int(config['General settings']['move prompt min']) and len(del_list) >= int(config['General settings']['move prompt min']):
                    del_confirmation = input('Haluatko varmasti siirtää ' + str(len(del_list)) + ' tallennetta Viihteen roskakoriin (k/e)? ')
                    if del_confirmation not in ('k', 'y'):
                        print('Tallenteita ei siirretty Viihteen roskakoriin.')
                        continue
                if viihdeapi.delete_recordings(del_list_str, headers, platform) == 200:
                    recordings_moved = True
                    print('Valitut tallenteet siirrettiin Viihteen roskakoriin.')
                    not_in_folder = [x['programId'] for x in del_list]
                    recording_list = [x for x in recording_list if not x['programId'] in not_in_folder]
                    for x in not_in_folder:
                        all_recordings.remove(x)
                    all_filtered = update_all_filtered(all_recordings, filtered_recordings)
                    all_filtered_list = update_all_filtered_list(recording_list, all_filtered)
                    folders = viihdeapi.get_folder_tree(headers, platform)

            elif f_string.startswith(command_strings.DELETE_RECORDINGS):
                f_split = f_string.split(' ', 1)
                if f_split[1] == 'a':
                    if len(all_filtered) > 0:
                        del_list = all_filtered_list
                        del_list_str = ','.join(map(str,all_filtered))
                elif f_split[1] == 'd':
                    del_list = []
                    for x in all_filtered_list:
                        if x['programId'] in hl_set:
                            del_list.append(x)
                    del_list_str = ','.join(map(str,[x['programId'] for x in del_list]))
                else:
                    del_list = []
                    for x in create_number_list(f_split[1], len(all_filtered) - 1):
                        del_list.append(all_filtered_list[x])
                    del_list_str = ','.join(map(str,[x['programId'] for x in del_list]))
                if not config.has_option('Folder shortcuts','trash'):
                    print('\nValitse kansio, jota käytetään roskakorina.')
                    trash_id, folders, folder_dict = handle_folders(folders, headers, True, folder_dict)
                    set_folder_shortcut(trash_id, 'trash', print_msg = False)
                else:
                    trash_id = config['Folder shortcuts']['trash']
                if int(config['General settings']['move prompt min']) and len(del_list) >= int(config['General settings']['move prompt min']):
                    del_confirmation = input('Haluatko varmasti siirtää ' + str(len(del_list)) + ' tallennetta roskakoriin (k/e)? ')
                    if del_confirmation not in ('k', 'y'):
                        print('Tallenteita ei siirretty roskakorikansioon.')
                        continue
                if viihdeapi.move_recordings(del_list_str, trash_id, headers, platform) == 200:
                    recordings_moved = True
                    print('Valitut tallenteet siirrettiin roskakorikansioon.')
                    if folder is None:
                        for x in del_list:
                            x['folderId'] = int(trash_id)
                    elif folder != trash_id:
                        not_in_folder = [x['programId'] for x in del_list]
                        recording_list = [x for x in recording_list if not x['programId'] in not_in_folder]
                        for x in not_in_folder:
                            all_recordings.remove(x)
                        all_filtered = update_all_filtered(all_recordings, filtered_recordings)
                        all_filtered_list = update_all_filtered_list(recording_list, all_filtered)
                    folders = viihdeapi.get_folder_tree(headers, platform)

            elif f_string.startswith(command_strings.MOVE_RECORDINGS):
                f_string = f_string.split(' ', 1)[1]
                target_split = f_string.split('_', 1)
                shortcut_split = f_string.split('>', 1)
                if len(target_split) == 2:
                    folder_id = all_filtered_list[int(target_split[1].strip())]['folderId']
                    f_string = target_split[0].strip()
                elif len(shortcut_split) == 2:
                    folder_id = int(config['Folder shortcuts'][shortcut_split[1].strip()])
                    f_string = shortcut_split[0].strip()
                else:
                    print('Valitse kansio, johon tallenteet siirretään.')
                    folder_id, folders, folder_dict = handle_folders(folders, headers, True, folder_dict)
                if f_string == 'a':
                    mov_list = all_filtered_list
                else:
                    mov_list = []
                    for x in create_number_list(f_string, len(all_filtered) - 1):
                        mov_list.append(all_filtered_list[x])
                mov_list_str = ','.join(map(str,[x['programId'] for x in mov_list]))
                if int(config['General settings']['move prompt min']) and len(mov_list) >= int(config['General settings']['move prompt min']):
                    mov_confirmation = input('Haluatko varmasti siirtää ' + str(len(mov_list)) + ' tallennetta kansioon '
                                            + folder_dict[folder_id][0] + ' (k/e)? ')
                    if mov_confirmation not in ('k', 'y'):
                        print('Tallenteita ei siirretty.')
                        continue
                if viihdeapi.move_recordings(mov_list_str, folder_id, headers, platform) == 200:
                    recordings_moved = True
                    print('Valitut tallenteet siirrettiin kansioon ' + folder_dict[folder_id][0] + '.')
                    if folder is None:
                        for x in mov_list:
                            x['folderId'] = int(folder_id)
                    elif folder != folder_id:
                        not_in_folder = [x['programId'] for x in mov_list]
                        recording_list = [x for x in recording_list if not x['programId'] in not_in_folder]
                        for x in not_in_folder:
                            all_recordings.remove(x)
                        all_filtered = update_all_filtered(all_recordings, filtered_recordings)
                        all_filtered_list = update_all_filtered_list(recording_list, all_filtered)
                    folders = viihdeapi.get_folder_tree(headers, platform)

            elif f_string.startswith(command_strings.EXCLUDE_FOLDER):
                if f_string == command_strings.EXCLUDE_FOLDER:
                    if not_in:
                        print('Valitse kansio, jossa tallenteiden tulee sijaita.')
                    else:
                        print('Valitse kansio, jossa sijaitsevat tallenteet suodatetaan pois.')
                    folder_id, folders, folder_dict = handle_folders(folders, headers, True, folder_dict)
                else:
                    shortcut_split = f_string.split('>', 1)
                    f_split = f_string.split(' ', 1)[1].strip()
                    if len(shortcut_split) == 2:
                        folder_id = int(config['Folder shortcuts'][shortcut_split[1].strip()])
                    elif f_split.lstrip('-').isnumeric:
                        folder_id = all_filtered_list[int(f_split.strip())]['folderId']
                valid_filter, filtered_recordings = filter_recordings(recording_list, filtered_recordings, not_in, 'folder', [folder_id, folder_dict[folder_id][0]])
                if valid_filter == 1:
                    if set_operations:
                        set_operations += f' & {len(filtered_recordings) - 1}'
                        all_filtered = custom_filter(all_recordings, filtered_recordings, set_operations)
                    else:
                        all_filtered = update_all_filtered(all_recordings, filtered_recordings)
                    all_filtered_list = update_all_filtered_list(recording_list, all_filtered)
                    print_recordings(columns, folder_dict, all_filtered_list, hl_set, print_descriptions, trash)
                elif valid_filter == 2:
                    print('Suodin on jo käytössä.')
                else:
                    print('Virheellinen komento.')

            elif f_string.startswith(command_strings.SORT_RECORDINGS) or f_string.startswith(command_strings.SORT_RECORDINGS_DESC):
                f_split = f_string.split(' ', 1)
                sort_orders = {'s': 'startTimeUTC', 'e': 'endTimeUTC', 'n': 'name', 'd': 'duration', 'c': 'channelName', 'i': 'imdbRating'}
                if trash: sort_orders['r'] = 'removalDateUTC'
                if f_split[1] in sort_orders:
                    sorting_dir, rev_order = ('asc', False) if f_string.startswith(command_strings.SORT_RECORDINGS) else ('desc', True)
                    imdb_sort = False
                    if f_split[1] in ['s', 'e', 'r']:
                        sorting_key = sort_orders[f_split[1]][:-3]
                    elif f_split[1] == 'i':
                        imdb_sort = True
                    else:
                        sorting_key = sort_orders[f_split[1]]
                    recording_list = sort_recordings(recording_list, sort_orders[f_split[1]], rev_order)
                    all_filtered_list = update_all_filtered_list(recording_list, all_filtered)
                    if config['General settings'].getboolean('print all') or len(filtered_recordings) > 0:
                        print_recordings(columns, folder_dict, all_filtered_list, hl_set, print_descriptions, trash)

            elif f_string == command_strings.RELOAD_CONFIG:
                config['Folder shortcuts'] = {}
                config['Download folders'] = {}
                config.read(config_path)
                columns.read(columns_path)
                platform = config['Download settings']['platform']
                print('Asetukset päivitetty.')

            elif f_string == command_strings.OPEN_CONFIG:
                print('Avataan ' + config_path + ' Muistiossa.')
                print('Muokattuasi asetustiedostoa kirjoita ' + command_strings.RELOAD_CONFIG + ' päivittääksesi asetukset.')
                webbrowser.open(config_path)

            elif f_string == command_strings.OPEN_COLUMNS:
                print('Avataan ' + columns_path + ' Muistiossa.')
                print('Muokattuasi asetustiedostoa kirjoita ' + command_strings.RELOAD_CONFIG + ' päivittääksesi asetukset.')
                webbrowser.open(columns_path)

            # elif f_string.startswith(command_strings.SET_FOLDER_SHORTCUT_NUMBER):
                # f_split = f_string.split(' ', 1)[1].split(':', 1)
                # print(f_split)
                # folder_id = all_filtered_list[int(f_split[1].strip())]['folderId']
                # set_folder_shortcut(folder_id, f_split[0].strip())
                # print('Luotiin pikavalinta ' + f_split[0].strip() + ' kansiolle ' + str(folder_dict[int(folder_id)][0]) + '.')

            elif f_string.startswith(command_strings.SET_FILTER_SHORTCUT):
                f_split = f_string.split(' ', 1)[1].split('|', 1)
                f_split = [x.strip() for x in f_split]
                f_list = [f'{"!" if x[0] else ""}{x[2][0]} {x[2][1]}'.lower() for x in list(filtered_recordings.values())]
                s_o = ''
                if len(f_split) == 1:
                    f_list = [f_list[-1]]
                elif f_split[1] == 'a':
                    s_o = set_operations
                else:
                    f_list_ = []
                    for x in create_number_list(f_split[1], len(f_list) - 1):
                        f_list_.append(f_list[x])
                    f_list = f_list_
                set_filter_shortcut(f_split[0], f_list, s_o)

            elif f_string == command_strings.LIST_FILTER_SHORTCUTS:
                list_filter_shortcuts()

            elif f_string.startswith(command_strings.SET_FOLDER_SHORTCUT):
                f_split = f_string.split(' ', 1)
                shortcut_split = f_split[1].split('|', 1)
                if len(shortcut_split) == 2:
                    f_split[1] = shortcut_split[0].strip()
                    folder_id = all_filtered_list[int(shortcut_split[1].strip())]['folderId']
                else:
                    folder_id, folders, folder_dict = handle_folders(folders, headers, True, folder_dict)
                set_folder_shortcut(folder_id, f_split[1], folder_dict[int(folder_id)][0])

            elif f_string.startswith(command_strings.DL_FOLDER_SHORTCUT):
                set_dl_folder(config['Download folders'][f_string.split(' ', 1)[1]])

            elif f_string.startswith(command_strings.SET_DL_FOLDER):
                set_dl_folder(f_string.split(' ', 1)[1])

            elif f_string.startswith(command_strings.SET_DL_FOLDER_SHORTCUT):
                f_split = f_string.split(' ', 1)[1].split('|', 1)
                if len(f_split) == 1:
                    f_split.append(config['Download settings']['download folder'])
                set_dl_folder_shortcut(f_split[1].strip(), f_split[0].strip())

            elif f_string == command_strings.LIST_DL_FOLDERS:
                list_dl_folders()

            elif f_string == command_strings.LIST_FOLDER_SHORTCUTS:
                list_folder_shortcuts(folder_dict)

            elif f_string == 'd_filtered':
                print(filtered_recordings)

            elif f_string.startswith(command_strings.CUSTOM_FILTER):
                allowed_char = '0123456789a()|&-^ '
                f_o = f_string.split(' ', 1)[1].strip()
                # f_o = re.sub(' +', ' ', f_o)
                if all(c in allowed_char for c in f_o):
                    all_filtered = custom_filter(all_recordings, filtered_recordings, f_o)
                    all_filtered_list = update_all_filtered_list(recording_list, all_filtered)
                    print_recordings(columns, folder_dict, all_filtered_list, hl_set, print_descriptions, trash)
                    set_operations = f_o
                else:
                    print('Komento saa sisältää alun cf:n lisäksi ainostaan numeroita, kirjaimen a ja merkit (, ), |, &, - ja ^.')
            else:
                f_split = f_string.split(' ', 1)
                valid_filter, filtered_recordings = filter_recordings(recording_list, filtered_recordings, not_in, f_split[0], f_split[1].upper())
                if valid_filter == 1:
                    if set_operations:
                        set_operations += f' & {len(filtered_recordings) - 1}'
                        all_filtered = custom_filter(all_recordings, filtered_recordings, set_operations)
                    else:
                        all_filtered = update_all_filtered(all_recordings, filtered_recordings)
                    all_filtered_list = update_all_filtered_list(recording_list, all_filtered)
                    print_recordings(columns, folder_dict, all_filtered_list, hl_set, print_descriptions, trash)
                elif valid_filter == 2:
                    print('Suodin on jo käytössä.')
                else:
                    print('Virheellinen komento.')
        except:
            print('Virheellinen komento.')
            # raise
        # except Exception as e: print(e)

def sort_recordings(recording_list, sort_by, reverse_order):
    if sort_by == 'imdbRating':
        imdb_list = []
        no_imdb_list = []
        for x in recording_list:
            if 'imdbRating' in x:
                imdb_list.append(x)
            else:
                no_imdb_list.append(x)
        imdb_list = sorted(imdb_list, key = lambda recording: recording['name'], reverse = False)
        no_imdb_list = sorted(no_imdb_list, key = lambda recording: recording['name'], reverse = False)
        imdb_list = sorted(imdb_list, key = lambda recording: recording[sort_by], reverse = reverse_order)
        new_recording_list = no_imdb_list + imdb_list
    else:
        new_recording_list = sorted(recording_list, key = lambda recording: recording[sort_by], reverse = reverse_order)
    return new_recording_list

def update_all_filtered(all_recordings, filtered_recordings):
    y = 0
    all_filtered = set()
    for x in list(filtered_recordings):
        if y == 0:
            if filtered_recordings[x][0] is False:
                all_filtered = filtered_recordings[x][1]
            else:
                all_filtered = all_recordings - filtered_recordings[x][1]
        elif filtered_recordings[x][0] is True:
            all_filtered = all_filtered - filtered_recordings[x][1]
        else:
            all_filtered = all_filtered & filtered_recordings[x][1]
        y += 1
    all_filtered = all_filtered & all_recordings
    return all_filtered

def custom_filter(all_recordings, filtered_recordings, operations):
    # fv = [x[1] for x in list(filtered_recordings.values())]
    fv = list(filtered_recordings.values())
    # print(fv)
    all_filtered = set()
    operations = re.sub(r'\d+', r'fv[\g<0>]', operations)
    for i, x in enumerate(fv):
        # operations = operations.replace(str(i), f'fv[{i}]')
        if x[0]:
            operations = operations.replace(f'fv[{i}]', f'(a - fv[{i}])')
        # print(operations)
    operations = operations.replace('a', 'all_recordings')
    operations = operations.replace(']', '][1]')
    # print(operations)
    # print(len(fv))
    all_filtered = eval(operations)
    return all_filtered

def update_all_filtered_list(recording_list, recording_set):
    all_filtered_list = [None] * len(recording_set)
    i = 0
    for x in recording_list:
        if x['programId'] in recording_set:
            if not 'folderId' in x:
                x['folderId'] = 0
            all_filtered_list[i] = x
            i += 1
    return all_filtered_list

def handle_input(headers):
    download = True
    while download:
        recording = input('Tallenteen tai kansion osoite: ').rstrip(' /')
        if recording in ['https://elisaviihde.fi/tallenteet',
                         'https://elisaviihde.fi/tallenteet/sivu/1', '0']:
            download_folder('0', headers)
        elif recording.isnumeric():
            cmd = 'viihdedl ' + recording + ' ' + str(headers)
            Popen(cmd, creationflags=CREATE_NEW_CONSOLE)
        else:
            folder_split = recording.rsplit('/', 3)
            if folder_split[0] == 'https://elisaviihde.fi/tallenteet/kansio':
                download_folder(folder_split[1], headers)
            else:
                recording_split = recording.rsplit('/', 1)
                if ( recording_split[0] == 'https://elisaviihde.fi/ohjelmaopas/ohjelma' or
                     recording_split[0] == 'https://elisaviihde.fi/tallenteet/katso' or
                     recording_split[0] == 'https://elisaviihde.fi/tallenne/katso' ):
                    cmd = 'viihdedl ' + recording_split[1] + ' ' + str(headers)
                    Popen(cmd, creationflags=CREATE_NEW_CONSOLE)
                else:
                    break
