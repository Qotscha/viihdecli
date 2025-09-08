import locale
import os
import textwrap
# import time
from datetime import datetime, timedelta
locale.setlocale(locale.LC_ALL, '')

def get_date_format(spacing, wd, sd, st, long, short):
    if sd:
        if st:
            f = 16
            i = (0, 16)
        else:
            f = 10
            i = (0, 10)
    else:
        if st:
            f = 5
            header = short
            i = (11, 16)
        else:
            f = 0
            header = ''
            i = None
    if wd:
        if f > 0:
            f += 1
        f += max([len(datetime.fromisoformat(f'2000-01-0{x}').strftime('%a')) for x in range(1,8)])
    if f:
        f += spacing
    if f > len(long):
        header = long
    elif f > len(short):
        header = short
    elif f:
        header = short[0] + '.'
    return f, header, wd, i

def get_format_list(n, ms, columns, trash):
    c = [[len(str(n)) + ms, '#'], [len(str(n)) + 1 + ms, '-#'] if columns.getboolean('negative') else [0, ''],
         get_date_format(ms, columns.getboolean('start day'), columns.getboolean('start date'),
                         columns.getboolean('start time'), 'Alkoi', 'Alk.'),
         get_date_format(ms, columns.getboolean('end day'), columns.getboolean('end date'),
                         columns.getboolean('end time'), 'Päättyi', 'Lopp.'),
         [int(columns['channel']) + ms, 'Kanava'] if int(columns['channel']) else [0, ''],
         [4 + ms, 'Kesto'] if columns.getboolean('duration') else [0, ''],
         [int(columns['name']) + ms if int(columns['name']) > 20 else 20 + ms, 'Nimi'],
         [4 + ms, 'Kausi'] if columns.getboolean('season') else [0, ''],
         [4 + ms, 'Jakso'] if columns.getboolean('episode') else [0, ''],
         [int(columns['folder']), 'Kansio'] if int(columns['folder']) else [0, '']]
    # if not c[2][0][0]: c[2][1] = ''
    # if not c[3][0][0]: c[3][1] = ''
    if c[4][0] and c[4][0] < 7: c[4][1] = 'Kan.'
    if c[5][0] and c[5][0] < 6: c[5][1] = 'K.'
    if columns.getboolean('show imdb'): c[6][1] += ' [IMDB-arvosana]'
    if trash:
        c.append(get_date_format(ms, columns.getboolean('removal day'), columns.getboolean('removal date'),
                  columns.getboolean('removal time'), 'Poistuu', 'Poist.'))
        # if not c[10][0][0]: c[10][1] = ''
    return c

def show_terminal_width(config, n, trash):
    if trash:
        columns = config['Recycle bin']
    else:
        columns = config['Recordings']
    ms = int(columns['spacing'])
    c = get_format_list(n, ms, columns, trash)
    t_width = os.get_terminal_size()[0]
    n_width = sum([i[0] for i in c])
    print(f'Tämänhetkinen terminaalin leveys: {t_width}')
    print(f'Tarvittava terminaalin leveys:    {n_width}')

def print_recordings(config, folder_dict, recording_list, hl_set = set(), print_descriptions = False, trash = False):
    # stime = time.time()
    n = len(recording_list)
    if trash:
        columns = config['Recycle bin']
    else:
        columns = config['Recordings']
    ms = int(columns['spacing'])
    c = get_format_list(n, ms, columns, trash)
    t_width, t_lines = os.get_terminal_size()
    n_width = sum([i[0] for i in c])
    c[9][0] = max(t_width - n_width + c[9][0], 0)
    if not c[9][0]: c[9][1] = ''
    c = tuple(tuple(i) for i in c)
    # for col in c:
        # print(col)
    if trash:
        header_row = f'{c[0][1]:<{c[0][0]}}{c[1][1]:<{c[1][0]}}{c[10][1]:<{c[10][0]}}{c[2][1]:<{c[2][0]}}{c[3][1]:<{c[3][0]}}' \
                     f'{c[4][1]:<{c[4][0]}}{c[5][1]:<{c[5][0]}}{c[6][1]:<{c[6][0]}}{c[7][1]:<{c[7][0]}}{c[8][1]:<{c[8][0]}}{c[9][1]:<{c[9][0]}}'
    else:
        header_row = f'{c[0][1]:<{c[0][0]}}{c[1][1]:<{c[1][0]}}{c[2][1]:<{c[2][0]}}{c[3][1]:<{c[3][0]}}{c[4][1]:<{c[4][0]}}' \
                     f'{c[5][1]:<{c[5][0]}}{c[6][1]:<{c[6][0]}}{c[7][1]:<{c[7][0]}}{c[8][1]:<{c[8][0]}}{c[9][1]:<{c[9][0]}}'
    y = 0
    z = - n if c[1][1] else ''
    print('\n\033[92m' + header_row + '\033[39m')
    total_duration = 0

    for x in recording_list:
        start_day = f"{datetime.fromisoformat(x['startTime']).strftime('%a')} " if c[2][2] else ''
        start_date = f"{start_day}{x['startTime'][c[2][3][0]:c[2][3][1]]}" if c[2][3] else start_day
        end_day = f"{datetime.fromisoformat(x['endTime']).strftime('%a')} " if c[3][2] else ''
        end_date = f"{end_day}{x['endTime'][c[3][3][0]:c[3][3][1]]}" if c[3][3] else end_day
        if trash:
            removal_day = f"{datetime.fromisoformat(x['removalDate']).strftime('%a')} " if c[10][2] else ''
            removal_date = f"\033[31m{removal_day}{x['removalDate'][c[10][3][0]:c[10][3][1]]}" if c[10][3] else f"\033[31m{removal_day}"
        dur = str(timedelta(seconds=x['duration'])).rsplit(':',1)[0] if c[5][0] else ''
        channel = x['channelName'][:c[4][0] - ms] if c[4][0] else ''
        extra = 0
        padding = c[6][0] + 5
        name_length = c[6][0] - ms
        live = ''
        imdb = ''
        hl = ''
        if x['programId'] in hl_set:
            hl = '\033[31m'
            padding += 5
        if x['recordingState'] == 'ongoing' and columns.getboolean('show live'):
            live = ' \033[91m[LIVE]'
            extra += 7
            padding += 5
        if 'imdbRating' in x and columns.getboolean('show imdb'):
            imdb = ' \033[33m[' + str(x['imdbRating']) + ']'
            extra += 6
            padding += 5
        name_length -= extra
        recording_name = f"{hl}{x['name'][:name_length].rstrip()}{imdb}{live}"
        # recording_name = f"{hl}{x['name'][:name_length-3].rstrip()}...{imdb}{live}" if name_length < len(x['name']) else f"{hl}{x['name'].rstrip()}{imdb}{live}"
        # fl = len(folder_dict[x['folderId']][0])
        if c[7][0] and 'series' in x and 'season' in x['series']:
            season = x['series']['season']
        else:
            season = ''
        if c[8][0] and 'series' in x and 'episode' in x['series']:
            episode = x['series']['episode']
        else:
            episode = ''
        if c[9][0]:
            folder_name = folder_dict[x['folderId']][0]
            if c[9][0] < len(folder_name):
                if folder_dict[x['folderId']][1] and len(folder_dict[x['folderId']][1]) > 1:
                    folder_start = '.. /'
                    for i in range(1, len(folder_dict[x['folderId']][1])):
                        folder_name = f"{folder_start}{folder_name.split('/', i)[i]}"
                        if len(folder_name) <= c[9][0]:
                            break
                        folder_start += ' .. /'
                folder_name = folder_name[:c[9][0]]
        else:
            folder_name = ''
        # folder_name = folder_dict[x['folderId']][0][:c[9][0]] if c[9][0] else ''
        if print_descriptions:
            recording_name += '\033[39m'
            if trash:
                removal_date += '\033[39m'
                info_row = f"{y:<{c[0][0]}}{z:<{c[1][0]}}{removal_date:<{c[10][0]+10}}{start_date:<{c[2][0]}}{end_date:<{c[3][0]}}" \
                           f"{channel:<{c[4][0]}}{dur:<{c[5][0]}}{recording_name:<{padding}}{season:<{c[7][0]}}{episode:<{c[8][0]}}{folder_name:<{c[9][0]}}"
            else:
                info_row = f"{y:<{c[0][0]}}{z:<{c[1][0]}}{start_date:<{c[2][0]}}{end_date:<{c[3][0]}}{channel:<{c[4][0]}}" \
                           f"{dur:<{c[5][0]}}{recording_name:<{padding}}{season:<{c[7][0]}}{episode:<{c[8][0]}}{folder_name:<{c[9][0]}}"
            print(info_row)
            if 'description' in x:
                desc_lines = textwrap.wrap(x['description'], width = t_width - 15)
                for line in desc_lines:
                    print(f"\033[36m{'':<{c[0][0] + c[1][0]}}{line}\033[39m")
            else:
                print(f"\033[36m{'':<{c[0][0] + c[1][0]}}{'Ei kuvausta'}\033[39m")
        else:
            if (y % 2) == 1:
                recording_name += '\033[36m'
                if trash:
                    removal_date += '\033[36m'
                    info_row = f"{y:<{c[0][0]}}{z:<{c[1][0]}}{removal_date:<{c[10][0]+10}}{start_date:<{c[2][0]}}" \
                               f"{end_date:<{c[3][0]}}{channel:<{c[4][0]}}{dur:<{c[5][0]}}{recording_name:<{padding}}{season:<{c[7][0]}}{episode:<{c[8][0]}}{folder_name:<{c[9][0]}}"
                else:
                    info_row = f"{y:<{c[0][0]}}{z:<{c[1][0]}}{start_date:<{c[2][0]}}{end_date:<{c[3][0]}}{channel:<{c[4][0]}}" \
                               f"{dur:<{c[5][0]}}{recording_name:<{padding}}{season:<{c[7][0]}}{episode:<{c[8][0]}}{folder_name:<{c[9][0]}}"
                print('\033[36m' + info_row + '\033[39m')
            else:
                recording_name += '\033[39m'
                if trash:
                    removal_date += '\033[39m'
                    info_row = f"{y:<{c[0][0]}}{z:<{c[1][0]}}{removal_date:<{c[10][0]+10}}{start_date:<{c[2][0]}}" \
                               f"{end_date:<{c[3][0]}}{channel:<{c[4][0]}}{dur:<{c[5][0]}}{recording_name:<{padding}}{season:<{c[7][0]}}{episode:<{c[8][0]}}{folder_name:<{c[9][0]}}"
                else:
                    info_row = f"{y:<{c[0][0]}}{z:<{c[1][0]}}{start_date:<{c[2][0]}}{end_date:<{c[3][0]}}{channel:<{c[4][0]}}" \
                               f"{dur:<{c[5][0]}}{recording_name:<{padding}}{season:<{c[7][0]}}{episode:<{c[8][0]}}{folder_name:<{c[9][0]}}"
                print(info_row)
        y += 1
        if c[1][1]: z += 1
        total_duration += x['duration']
    if n > t_lines - 4:
        print('\033[92m' + header_row + '\033[39m')
    hours_seconds = divmod(total_duration, 3600)
    minutes = hours_seconds[1] // 60
    print('Suodatettujen tallenteiden kesto yhteensä ' + str(hours_seconds[0]) + ' tuntia, ' + str(minutes) + ' minuuttia.')
    # print(f'Aikaa kului {time.time() - stime} sekuntia.')
    # print(f'Terminaalin leveys: {t_width}')
    # print(f'Tarvittava terminaalin leveys: {n_width}')
    print()
