import locale
import os
import textwrap
from datetime import datetime, timedelta
os.system('color')
locale.setlocale(locale.LC_ALL, '')

def print_recordings(folder_dict, recording_list, hl_set = set(), print_descriptions = False, trash = False):
    y = 0
    z = - len(recording_list)
    if trash:
        header_row = '{:<6}{:<7}{:<23}{:<23}{:<19}{:<17}{:<7}{:<62}{}'.format('#', '-#', 'Poistuu', 'Alkoi', 'Päättyi',
                      'Kanava', 'Kesto', 'Nimi [IMDB-arvosana]', 'Kansio')
    else:
        header_row = '{:<6}{:<7}{:<23}{:<19}{:<17}{:<7}{:<62}{}'.format('#', '-#', 'Alkoi', 'Päättyi', 'Kanava',
                      'Kesto', 'Nimi [IMDB-arvosana]', 'Kansio')
    print('\n\033[92m' + header_row + '\033[39m')
    total_duration = 0
    for x in recording_list:
        start_time = datetime.fromisoformat(x['startTime'])
        weekday = start_time.strftime('%a')
        if trash:
            removal_time = datetime.fromisoformat(x['removalDate'])
            removal_day = '\033[31m' + removal_time.strftime('%a')
            removal_date = x['removalDate'].rsplit(':',1)[0]
        # recording_name = x['name'][:60]
        padding = 67
        name_length = 60
        live = ''
        imdb = ''
        hl = ''
        # if 'description' in x:
            # pituus = len(x['description']) + len(x['name'])
        # else:
            # pituus = len(x['name'])
        if x['programId'] in hl_set:
            # recording_name = '\033[31m' + recording_name
            hl = '\033[31m'
            padding += 5
        if x['recordingState'] == 'ongoing':
            live = ' \033[31m[' + 'LIVE]'
            name_length -= 7
            padding += 5
        if 'imdbRating' in x:
            imdb = ' \033[33m[' + str(x['imdbRating']) + ']'
            name_length -= 6
            padding += 5
        recording_name = hl + x['name'][:name_length] + imdb + live
        if print_descriptions:
            recording_name += '\033[39m'
            if trash:
                removal_date += '\033[39m'
                info_row = ('{:<6}{:<7}{:<9}{:<24}{:<4}{:<19}{:<19}{:<17}{:<7}{:<' + str(padding) + '}{}').format(str(y), str(z),
                            removal_day, removal_date, weekday, x['startTime'].rsplit(':',1)[0], x['endTime'].rsplit(':',1)[0],
                            x['channelName'], str(timedelta(seconds=x['duration'])).rsplit(':',1)[0], recording_name,
                            folder_dict[x['folderId']][0])
            else:
                info_row = ('{:<6}{:<7}{:<4}{:<19}{:<19}{:<17}{:<7}{:<' + str(padding) + '}{}').format(str(y), str(z), weekday,
                            x['startTime'].rsplit(':',1)[0], x['endTime'].rsplit(':',1)[0], x['channelName'],
                            str(timedelta(seconds=x['duration'])).rsplit(':',1)[0], recording_name, folder_dict[x['folderId']][0])
            print(info_row)
            if 'description' in x:
                desc_lines = textwrap.wrap(x['description'], width = 155)
                for line in desc_lines:
                    print('\033[36m' + '{:<13}{}'.format('', line) + '\033[39m')
            else:
                print('\033[36m' + '{:<13}{}'.format('', '(Ei kuvausta)' + '\033[39m'))
        else:
            if (y % 2) == 1:
                recording_name += '\033[36m'
                if trash:
                    removal_date += '\033[36m'
                    info_row = ('{:<6}{:<7}{:<9}{:<24}{:<4}{:<19}{:<19}{:<17}{:<7}{:<' + str(padding) + '}{}').format(str(y), str(z),
                               removal_day, removal_date, weekday, x['startTime'].rsplit(':',1)[0], x['endTime'].rsplit(':',1)[0],
                               x['channelName'], str(timedelta(seconds=x['duration'])).rsplit(':',1)[0], recording_name,
                               folder_dict[x['folderId']][0])
                else:
                    info_row = ('{:<6}{:<7}{:<4}{:<19}{:<19}{:<17}{:<7}{:<' + str(padding) + '}{}').format(str(y), str(z), weekday,
                                x['startTime'].rsplit(':',1)[0], x['endTime'].rsplit(':',1)[0], x['channelName'],
                                str(timedelta(seconds=x['duration'])).rsplit(':',1)[0], recording_name, folder_dict[x['folderId']][0])
                print('\033[36m' + info_row + '\033[39m')
            else:
                recording_name += '\033[39m'
                if trash:
                    removal_date += '\033[39m'
                    info_row = ('{:<6}{:<7}{:<9}{:24}{:<4}{:<19}{:<19}{:<17}{:<7}{:<' + str(padding) + '}{}').format(str(y), str(z),
                               removal_day, removal_date, weekday, x['startTime'].rsplit(':',1)[0], x['endTime'].rsplit(':',1)[0],
                               x['channelName'], str(timedelta(seconds=x['duration'])).rsplit(':',1)[0], recording_name,
                               folder_dict[x['folderId']][0])
                else:
                    info_row = ('{:<6}{:<7}{:<4}{:<19}{:<19}{:<17}{:<7}{:<' + str(padding) + '}{}').format(str(y), str(z), weekday,
                                x['startTime'].rsplit(':',1)[0], x['endTime'].rsplit(':',1)[0], x['channelName'],
                                str(timedelta(seconds=x['duration'])).rsplit(':',1)[0], recording_name, folder_dict[x['folderId']][0])
                print(info_row)
        y += 1
        z += 1
        total_duration += x['duration']
    hours_seconds = divmod(total_duration, 3600)
    minutes = hours_seconds[1] // 60
    print('Suodatettujen tallenteiden kesto yhteensä ' + str(hours_seconds[0]) + ' tuntia, ' + str(minutes) + ' minuuttia.')
    print()
