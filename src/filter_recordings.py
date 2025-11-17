from datetime import datetime, time
import locale
from . import command_strings
locale.setlocale(locale.LC_ALL, '')

def filter_recordings(recording_list, filtered_recordings, not_in, f, arguments):
    # filtered_recordings = filteredRecordings_
    # print(recording_list)
    f_len = len(filtered_recordings)
    dict_key = ''
    if not_in:
        dict_key = 'EI: '
    # stime = time.time()
    if f == 'folder':
        if not_in:
            dict_key = 'Kansiossa: ' + arguments[1]
        else:
            dict_key = 'Ei kansiossa: ' + arguments[1]
        if not dict_key in filtered_recordings.keys():
            filtered_recordings[dict_key] = [not_in, set(), [f, arguments]]
            for x in recording_list:
                if arguments[0] != x['folderId']:
                    filtered_recordings[dict_key][1].add(x['programId'])
        else:
            return 2, filtered_recordings

    elif f == command_strings.F_ACTOR:
        # stime = time.time()
        names_split = arguments.split('|')
        name_list = []
        for x in names_split:
            name_split = x.split(',')
            name_split = [y.strip() for y in name_split]
            last_name_only = len(name_split) == 1
            first_name_only = name_split[0] == ''
            last_name_starts = not first_name_only and name_split[0].endswith('*')
            first_name_starts = not last_name_only and name_split[1].endswith('*')
            name_split = [y.rstrip('*') for y in name_split]
            name_list.append({'names': name_split, 'last_name_only': last_name_only, 'first_name_only': first_name_only,
                             'last_name_starts': last_name_starts, 'first_name_starts': first_name_starts})
        dict_key += 'Näyttelijä: ' + arguments
        if not dict_key in filtered_recordings.keys():
            filtered_recordings[dict_key] = [not_in, set(), [f, arguments]]
            for x in recording_list:
                if 'actors' in x:
                    for y in x['actors']:
                        for z in name_list:
                            if z['last_name_only']:
                                if z['last_name_starts']:
                                    if y['lastName'].upper().startswith(z['names'][0]):
                                        filtered_recordings[dict_key][1].add(x['programId'])
                                else:
                                    if y['lastName'].upper() == z['names'][0]:
                                        filtered_recordings[dict_key][1].add(x['programId'])
                            elif z['first_name_only']:
                                if z['first_name_starts']:
                                    if y['firstName'].upper().startswith(z['names'][1]):
                                        filtered_recordings[dict_key][1].add(x['programId'])
                                else:
                                    if y['firstName'].upper() == z['names'][1]:
                                        filtered_recordings[dict_key][1].add(x['programId'])
                            else:
                                if z['last_name_starts']:
                                    if z['first_name_starts']:
                                        if y['lastName'].upper().startswith(z['names'][0]) and y['firstName'].upper().startswith(z['names'][1]):
                                            filtered_recordings[dict_key][1].add(x['programId'])
                                    else:
                                        if y['lastName'].upper().startswith(z['names'][0]) and y['firstName'].upper() == z['names'][1]:
                                            filtered_recordings[dict_key][1].add(x['programId'])
                                else:
                                    if z['first_name_starts']:
                                        if y['lastName'].upper() == z['names'][0] and y['firstName'].upper().startswith(z['names'][1]):
                                            filtered_recordings[dict_key][1].add(x['programId'])
                                    else:
                                        if y['lastName'].upper() == z['names'][0] and y['firstName'].upper() == z['names'][1]:
                                            filtered_recordings[dict_key][1].add(x['programId'])
        else:
            return 2, filtered_recordings
        # print(time.time()-stime)

    elif f == command_strings.F_DIRECTOR:
        names_split = arguments.split('|')
        name_list = []
        for x in names_split:
            name_split = x.split(',')
            name_split = [y.strip() for y in name_split]
            last_name_only = len(name_split) == 1
            first_name_only = name_split[0] == ''
            last_name_starts = not first_name_only and name_split[0].endswith('*')
            first_name_starts = not last_name_only and name_split[1].endswith('*')
            name_split = [y.rstrip('*') for y in name_split]
            name_list.append({'names': name_split, 'last_name_only': last_name_only, 'first_name_only': first_name_only,
                             'last_name_starts': last_name_starts, 'first_name_starts': first_name_starts})
        dict_key += 'Ohjaaja: ' + arguments
        if not dict_key in filtered_recordings.keys():
            filtered_recordings[dict_key] = [not_in, set(), [f, arguments]]
            for x in recording_list:
                if 'directors' in x:
                    for y in x['directors']:
                        for z in name_list:
                            if z['last_name_only']:
                                if z['last_name_starts']:
                                    if y['lastName'].upper().startswith(z['names'][0]):
                                        filtered_recordings[dict_key][1].add(x['programId'])
                                else:
                                    if y['lastName'].upper() == z['names'][0]:
                                        filtered_recordings[dict_key][1].add(x['programId'])
                            elif z['first_name_only']:
                                if z['first_name_starts']:
                                    if y['firstName'].upper().startswith(z['names'][1]):
                                        filtered_recordings[dict_key][1].add(x['programId'])
                                else:
                                    if y['firstName'].upper() == z['names'][1]:
                                        filtered_recordings[dict_key][1].add(x['programId'])
                            else:
                                if z['last_name_starts']:
                                    if z['first_name_starts']:
                                        if y['lastName'].upper().startswith(z['names'][0]) and y['firstName'].upper().startswith(z['names'][1]):
                                            filtered_recordings[dict_key][1].add(x['programId'])
                                    else:
                                        if y['lastName'].upper().startswith(z['names'][0]) and y['firstName'].upper() == z['names'][1]:
                                            filtered_recordings[dict_key][1].add(x['programId'])
                                else:
                                    if z['first_name_starts']:
                                        if y['lastName'].upper() == z['names'][0] and y['firstName'].upper().startswith(z['names'][1]):
                                            filtered_recordings[dict_key][1].add(x['programId'])
                                    else:
                                        if y['lastName'].upper() == z['names'][0] and y['firstName'].upper() == z['names'][1]:
                                            filtered_recordings[dict_key][1].add(x['programId'])
        else:
            return 2, filtered_recordings

    elif f == command_strings.F_NAME:
        if not_in:
            dict_key = 'Nimi ei sisällä: ' + arguments
        else:
            dict_key = 'Nimi sisältää: ' + arguments
        if not dict_key in filtered_recordings.keys():
            in_name = arguments.split('|')
            in_name = [x.strip() for x in in_name]
            filtered_recordings[dict_key] = [not_in, set(), [f, arguments]]
            for x in recording_list:
                for y in in_name:
                    if y in x['name'].upper():
                        filtered_recordings[dict_key][1].add(x['programId'])
        else:
            return 2, filtered_recordings

    elif f == command_strings.F_DESCRIPTION:
        if not_in:
            dict_key = 'Kuvaus ei sisällä: ' + arguments
        else:
            dict_key = 'Kuvaus sisältää: ' + arguments
        if not dict_key in filtered_recordings.keys():
            in_description = arguments.split('|')
            in_description = [x.strip() for x in in_description]
            filtered_recordings[dict_key] = [not_in, set(), [f, arguments]]
            for x in recording_list:
                for y in in_description:
                    if 'description' in x and y in x['description'].upper():
                        filtered_recordings[dict_key][1].add(x['programId'])
        else:
            return 2, filtered_recordings

    elif f == command_strings.F_CHANNEL:
        dict_key += 'Kanavat: ' + arguments
        if not dict_key in filtered_recordings.keys():
            channels = arguments.split('|')
            channels = [x.strip() for x in channels]
            filtered_recordings[dict_key] = [not_in, set(), [f, arguments]]
            for x in recording_list:
                for y in channels:
                    if y in x['channelName'].upper():
                        filtered_recordings[dict_key][1].add(x['programId'])
        else:
            return 2, filtered_recordings

    elif f == command_strings.F_SHOWTYPE:
        dict_key += 'Showtype: ' + arguments
        if not dict_key in filtered_recordings.keys():
            showtypes = arguments.split('|')
            showtypes = [x.strip() for x in showtypes]
            filtered_recordings[dict_key] = [not_in, set(), [f, arguments]]
            for x in recording_list:
                for y in showtypes:
                    if 'showType' in x and y in x['showType'].upper():
                        filtered_recordings[dict_key][1].add(x['programId'])
        else:
            return 2, filtered_recordings

    elif f == command_strings.F_GENRE:
        dict_key += 'Genre: ' + arguments
        if not dict_key in filtered_recordings.keys():
            genres = arguments.split('|')
            genres = [x.strip() for x in genres]
            filtered_recordings[dict_key] = [not_in, set(), [f, arguments]]
            for x in recording_list:
                if 'genres' in x:
                    for y in x['genres']:
                        for z in genres:
                            if z in y['name'].upper():
                                filtered_recordings[dict_key][1].add(x['programId'])
        else:
            return 2, filtered_recordings

    elif f == command_strings.F_SERIES:
        dict_key += 'Sarja: ' + arguments
        if not dict_key in filtered_recordings.keys():
            series = arguments.split('|')
            series = [x.strip() for x in series]
            filtered_recordings[dict_key] = [not_in, set(), [f, arguments]]
            for x in recording_list:
                if 'series' in x and 'title' in x['series']:
                    for y in series:
                        if y in x['series']['title'].upper():
                            filtered_recordings[dict_key][1].add(x['programId'])
        else:
            return 2, filtered_recordings

    elif f == command_strings.F_EPISODE_NAME:
        dict_key += 'Episodin nimi: ' + arguments
        if not dict_key in filtered_recordings.keys():
            series = arguments.split('|')
            series = [x.strip() for x in series]
            filtered_recordings[dict_key] = [not_in, set(), [f, arguments]]
            for x in recording_list:
                if 'series' in x and 'episodeName' in x['series']:
                    for y in series:
                        if y in x['series']['episodeName'].upper():
                            filtered_recordings[dict_key][1].add(x['programId'])
        else:
            return 2, filtered_recordings

    elif f == command_strings.F_SEASON:
        dict_key += 'Kausi: ' + arguments
        if not dict_key in filtered_recordings.keys():
            seasons = arguments.replace('|', ' ').split()
            seasons = [int(x.strip()) for x in seasons]
            filtered_recordings[dict_key] = [not_in, set(), [f, arguments]]
            for x in recording_list:
                if 'series' in x and 'season' in x['series'] and int(x['series']['season']) in seasons:
                    filtered_recordings[dict_key][1].add(x['programId'])
        else:
            return 2, filtered_recordings

    elif f == command_strings.F_EPISODE:
        dict_key += 'Jakso: ' + arguments
        if not dict_key in filtered_recordings.keys():
            episodes = arguments.replace('|', ' ').split()
            episodes = [int(x.strip()) for x in episodes]
            filtered_recordings[dict_key] = [not_in, set(), [f, arguments]]
            for x in recording_list:
                if 'series' in x and 'episode' in x['series'] and int(x['series']['episode']) in episodes:
                    filtered_recordings[dict_key][1].add(x['programId'])
        else:
            return 2, filtered_recordings

    elif f == command_strings.F_DURATION:
        if not_in:
            dict_key = 'Kesto alle ' + arguments + ' minuuttia'
        else:
            dict_key = 'Kesto vähintään ' + arguments + ' minuuttia'
        if not dict_key in filtered_recordings.keys():
            filtered_recordings[dict_key] = [not_in, set(), [f, arguments]]
            argument_split = arguments.split(':')
            if len(argument_split) == 1:
                duration = 60 * int(argument_split[0])
            else:
                duration = 3600 * int(argument_split[0]) + 60 * int(argument_split[1])
            for x in recording_list:
                if x['duration'] >= duration:
                    filtered_recordings[dict_key][1].add(x['programId'])
        else:
            return 2, filtered_recordings

    elif f == command_strings.F_START_TIME:
        if not_in:
            dict_key = 'Tallennus alkoi aikaisintaan ' + arguments
        else:
            dict_key = 'Tallennus alkoi ennen ' + arguments
        if not dict_key in filtered_recordings.keys():
            filtered_recordings[dict_key] = [not_in, set(), [f, arguments]]
            if '.' in arguments:
                d = datetime.strptime(arguments, '%x')
            else:
                d = datetime.fromisoformat(arguments)
            d_utc = d.timestamp()*1000
            for x in recording_list:
                if x['startTimeUTC'] < d_utc:
                    filtered_recordings[dict_key][1].add(x['programId'])
        else:
            return 2, filtered_recordings

    elif f == command_strings.F_END_TIME:
        if not_in:
            dict_key = 'Tallennus päättyi aikaisintaan ' + arguments
        else:
            dict_key = 'Tallennus päättyi ennen ' + arguments
        if not dict_key in filtered_recordings.keys():
            filtered_recordings[dict_key] = [not_in, set(), [f, arguments]]
            if '.' in arguments:
                d = datetime.strptime(arguments, '%x')
            else:
                d = datetime.fromisoformat(arguments)
            d_utc = d.timestamp()*1000
            for x in recording_list:
                if x['endTimeUTC'] < d_utc:
                    filtered_recordings[dict_key][1].add(x['programId'])
        else:
            return 2, filtered_recordings

    elif f == command_strings.F_WEEKDAY:
        dict_key += 'Viikonpäivät: ' + arguments
        if not dict_key in filtered_recordings.keys():
            weekdays = arguments.split('|')
            weekdays = [x.strip() for x in weekdays]
            filtered_recordings[dict_key] = [not_in, set(), [f, arguments]]
            for x in recording_list:
                for y in weekdays:
                    if datetime.fromisoformat(x['startTime']).strftime('%a').upper() == y:
                        filtered_recordings[dict_key][1].add(x['programId'])
        else:
            return 2, filtered_recordings

    elif f == command_strings.F_TIME:
        if not_in:
            dict_key = 'Tallennusaika jälkeen ' + arguments
        else:
            dict_key = 'Tallennusaika ennen ' + arguments
        if not dict_key in filtered_recordings.keys():
            filtered_recordings[dict_key] = [not_in, set(), [f, arguments]]
            hours_minutes = [int(x.strip()) for x in arguments.split(':', 1)]
            t = time(hour = hours_minutes[0], minute = hours_minutes[1])
            for x in recording_list:
                if datetime.fromisoformat(x['startTime']).time() < t:
                    filtered_recordings[dict_key][1].add(x['programId'])
        else:
            return 2, filtered_recordings

    elif f == 'tr':
        if not_in:
            dict_key = 'Katseluaikaa jäljellä vähintään ' + arguments + ' vuorokautta'
        else:
            dict_key = 'Katseluaikaa jäljellä alle ' + arguments + ' vuorokautta'
        if not dict_key in filtered_recordings.keys():
            filtered_recordings[dict_key] = [not_in, set(), [f, arguments]]
            for x in recording_list:
                if int(x['remainingTime']['years']) * 365 + int(x['remainingTime']['months']) * 30 + int(x['remainingTime']['days']) < int(arguments):
                    filtered_recordings[dict_key][1].add(x['programId'])
        else:
            return 2, filtered_recordings

    elif f == command_strings.F_IMDB:
        if not_in:
            dict_key = 'IMDB-pisteet alle ' + arguments
        else:
            dict_key = 'IMDB-pisteet vähintään ' + arguments
        if not dict_key in filtered_recordings.keys():
            filtered_recordings[dict_key] = [not_in, set(), [f, arguments]]
            for x in recording_list:
                if 'imdbRating' in x:
                    # if x['imdbRating'] >= float(arguments) and x['showType'] == 'MOVIE':
                    if x['imdbRating'] >= float(arguments):
                        filtered_recordings[dict_key][1].add(x['programId'])
        else:
            return 2, filtered_recordings
    valid_filter = 1 if len(filtered_recordings) > f_len else 0
    return valid_filter, filtered_recordings
    # print(filtered_recordings)
