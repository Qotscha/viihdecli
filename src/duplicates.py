def clean_name(recording_name):
    cleaned_name = recording_name.upper()
    for x in ['ELOKUVA:', 'UUSI KINO:', 'KINO KLASSIKKO:', 'KINO SUOMI:', 'KINO:', 'SUBLEFFA:']:
        if cleaned_name.startswith(x):
            cleaned_name = cleaned_name.replace(x, '')
            break
    if cleaned_name.endswith(')'):
        cleaned_name = cleaned_name.rsplit('(', 1)[0]
    cleaned_name = cleaned_name.strip(':!. ')
    return cleaned_name

def clean_description(description):
    cleaned_description = description.upper()
    for x in ['(U)', 'UUSI SARJA ALKAA', 'UUSI KAUSI ALKAA', 'UUSI KAUSI', '(KAAPELI-TV)', 'SUOMEN-ENSI-ILTA', 'SUOMEN ENSI-ILTA', 'SUOMEN TV-ENSI-ILTA', 'TV-ENSI-ILTA', 'SUORA LÄHETYS']:
        if x in cleaned_description:
            cleaned_description = cleaned_description.replace(x, '')
            break
    if cleaned_description.endswith(')'):
        cleaned_description = cleaned_description.rsplit('(', 1)[0]
    cleaned_description = cleaned_description.strip(':!. ')
    return cleaned_description

def list_duplicates(recording_list, mode = 2, use_description = True, use_name = True, use_metadata = False, max_dur_diff = None):
    folder_length = len(recording_list)
    # duplicates = [[None] * 10 for i in range(folder_length)]
    # stime = time.time()
    if mode != 0:
        use_name = False if mode == 5 else True
        use_description = False if mode in (5, 9) else True
        use_metadata = False if mode in (2, 8, 9) else True
        use_episode = True if mode in (8, 9) else False
    if use_name:
        names_cleaned = [clean_name(x['name']) for x in recording_list]
    if use_description:
        descriptions_cleaned = [clean_description(x['description']) if 'description' in x else '' for x in recording_list]
    if use_metadata:
        metadata_ids = [x['metadataId'] if 'metadataId' in x else 0 for x in recording_list]
    if use_episode:
        episodes = [(x['series'].get('season'), x['series'].get('episode')) if 'series' in x else None for x in recording_list]
    if max_dur_diff is not None:
        use_dur_diff = True
        durations = [x['duration'] for x in recording_list]
        max_dur_diff_sec = 60 * max_dur_diff
    else:
        use_dur_diff = False
    duplicates_found = [False] * folder_length
    duplicate_list = [None] * folder_length
    duplicate_set = set()
    i = 0

    if mode == 1:
        # Name AND description AND metadataId
        print('Haetaan duplikaatteja (nimi JA kuvaus JA metadataId).')
        for x in range(folder_length):
            if duplicates_found[x] or not metadata_ids[x] or not descriptions_cleaned[x]:
                continue
            for y in range(x + 1, folder_length):
                if duplicates_found[y] or not metadata_ids[y] or not descriptions_cleaned[y]:
                    continue
                if ( metadata_ids[x] == metadata_ids[y] and names_cleaned[x] == names_cleaned[y] and
                     (descriptions_cleaned[x].startswith(descriptions_cleaned[y]) or descriptions_cleaned[y].startswith(descriptions_cleaned[x])) ):
                    if not duplicates_found[x]:
                        duplicates_found[x] = True
                        duplicate_list[i] = recording_list[x]
                        i += 1
                    duplicates_found[y] = True
                    duplicate_list[i] = recording_list[y]
                    duplicate_set.add(recording_list[y]['programId'])
                    i += 1

    elif mode == 2:
        # Name AND description
        print('Haetaan duplikaatteja (nimi JA kuvaus).')
        for x in range(folder_length):
            if duplicates_found[x] or not descriptions_cleaned[x]:
                continue
            for y in range(x + 1, folder_length):
                if duplicates_found[y] or not descriptions_cleaned[y]:
                    continue
                if names_cleaned[x] == names_cleaned[y] and (descriptions_cleaned[x].startswith(descriptions_cleaned[y]) or descriptions_cleaned[y].startswith(descriptions_cleaned[x])):
                    if not duplicates_found[x]:
                        duplicates_found[x] = True
                        duplicate_list[i] = recording_list[x]
                        i += 1
                    duplicates_found[y] = True
                    duplicate_list[i] = recording_list[y]
                    duplicate_set.add(recording_list[y]['programId'])
                    i += 1

    elif mode == 3:
        # Description AND (name OR metadataId)
        print('Haetaan duplikaatteja (kuvaus JA (nimi TAI metadataId)).')
        for x in range(folder_length):
            if duplicates_found[x] or not descriptions_cleaned[x]:
                continue
            for y in range(x + 1, folder_length):
                if duplicates_found[y] or not descriptions_cleaned[y]:
                    continue
                if ( ((metadata_ids[x] and  metadata_ids[x] == metadata_ids[y]) or names_cleaned[x] == names_cleaned[y]) and
                     (descriptions_cleaned[x].startswith(descriptions_cleaned[y]) or descriptions_cleaned[y].startswith(descriptions_cleaned[x])) ):
                    if not duplicates_found[x]:
                        duplicates_found[x] = True
                        duplicate_list[i] = recording_list[x]
                        i += 1
                    duplicates_found[y] = True
                    duplicate_list[i] = recording_list[y]
                    duplicate_set.add(recording_list[y]['programId'])
                    i += 1
    elif mode == 4:
        # MetadataId AND (name OR description)
        print('Haetaan duplikaatteja (metadataId JA (nimi tai kuvaus)).')
        for x in range(folder_length):
            if duplicates_found[x] or not metadata_ids[x]:
                continue
            for y in range(x + 1, folder_length):
                if duplicates_found[y] or not metadata_ids[y]:
                    continue
                if ( metadata_ids[x] == metadata_ids[y] and (names_cleaned[x] == names_cleaned[y] or
                     (descriptions_cleaned[y] and descriptions_cleaned[x].startswith(descriptions_cleaned[y])) or
                     (descriptions_cleaned[x] and descriptions_cleaned[y].startswith(descriptions_cleaned[x]))) ):
                    if not duplicates_found[x]:
                        duplicates_found[x] = True
                        duplicate_list[i] = recording_list[x]
                        i += 1
                    duplicates_found[y] = True
                    duplicate_list[i] = recording_list[y]
                    duplicate_set.add(recording_list[y]['programId'])
                    i += 1
    elif mode == 5:
        # MetadataId
        print('Haetaan duplikaatteja (metadataId).')
        for x in range(folder_length):
            if duplicates_found[x] or not metadata_ids[x]:
                continue
            for y in range(x + 1, folder_length):
                if duplicates_found[y] or not metadata_ids[y]:
                    continue
                if metadata_ids[x] == metadata_ids[y]:
                    if not duplicates_found[x]:
                        duplicates_found[x] = True
                        duplicate_list[i] = recording_list[x]
                        i += 1
                    duplicates_found[y] = True
                    duplicate_list[i] = recording_list[y]
                    duplicate_set.add(recording_list[y]['programId'])
                    i += 1
    elif mode == 6:
        # Name AND (description OR metadataId)
        print('Haetaan duplikaatteja (nimi JA (kuvaus TAI metadataId)).')
        for x in range(folder_length):
            if duplicates_found[x] or (not metadata_ids[x] and not descriptions_cleaned[x]):
                continue
            for y in range(x + 1, folder_length):
                if duplicates_found[y] or (not metadata_ids[y] and not descriptions_cleaned[y]):
                    continue
                if ( names_cleaned[x] == names_cleaned[y] and ((metadata_ids[x] and  metadata_ids[x] == metadata_ids[y]) or
                     (descriptions_cleaned[y] and descriptions_cleaned[x].startswith(descriptions_cleaned[y])) or
                     (descriptions_cleaned[x] and descriptions_cleaned[y].startswith(descriptions_cleaned[x]))) ):
                    if not duplicates_found[x]:
                        duplicates_found[x] = True
                        duplicate_list[i] = recording_list[x]
                        i += 1
                    duplicates_found[y] = True
                    duplicate_list[i] = recording_list[y]
                    duplicate_set.add(recording_list[y]['programId'])
                    i += 1
    elif mode == 7:
        # (Name AND description) OR metadataId
        print('Haetaan duplikaatteja ((nimi JA kuvaus) TAI metadataId).')
        for x in range(folder_length):
            if duplicates_found[x] or (not metadata_ids[x] and not descriptions_cleaned[x]):
                continue
            for y in range(x + 1, folder_length):
                if duplicates_found[y] or (not metadata_ids[y] and not descriptions_cleaned[y]):
                    continue
                if ( (metadata_ids[x] and metadata_ids[x] == metadata_ids[y]) or (names_cleaned[x] == names_cleaned[y] and
                     ((descriptions_cleaned[y] and descriptions_cleaned[x].startswith(descriptions_cleaned[y])) or
                     (descriptions_cleaned[x] and descriptions_cleaned[y].startswith(descriptions_cleaned[x])))) ):
                    if not duplicates_found[x]:
                        duplicates_found[x] = True
                        duplicate_list[i] = recording_list[x]
                        i += 1
                    duplicates_found[y] = True
                    duplicate_list[i] = recording_list[y]
                    duplicate_set.add(recording_list[y]['programId'])
                    i += 1

    elif mode == 8:
        # Name AND description AND episode number
        print('Haetaan duplikaatteja (nimi JA kuvaus JA jakson numero).')
        for x in range(folder_length):
            if duplicates_found[x] or not descriptions_cleaned[x] or not episodes[x]:
                continue
            for y in range(x + 1, folder_length):
                if duplicates_found[y] or not descriptions_cleaned[y] or not episodes[y]:
                    continue
                if names_cleaned[x] == names_cleaned[y] and (descriptions_cleaned[x].startswith(descriptions_cleaned[y]) or descriptions_cleaned[y].startswith(descriptions_cleaned[x])) and episodes[x] == episodes[y]:
                    if not duplicates_found[x]:
                        duplicates_found[x] = True
                        duplicate_list[i] = recording_list[x]
                        i += 1
                    duplicates_found[y] = True
                    duplicate_list[i] = recording_list[y]
                    duplicate_set.add(recording_list[y]['programId'])
                    i += 1

    elif mode == 9:
        # Name AND episode number
        print('Haetaan duplikaatteja (nimi JA jakson numero).')
        for x in range(folder_length):
            if duplicates_found[x] or not episodes[x]:
                continue
            for y in range(x + 1, folder_length):
                if duplicates_found[y] or not episodes[y]:
                    continue
                if names_cleaned[x] == names_cleaned[y] and episodes[x] == episodes[y]:
                    if not duplicates_found[x]:
                        duplicates_found[x] = True
                        duplicate_list[i] = recording_list[x]
                        i += 1
                    duplicates_found[y] = True
                    duplicate_list[i] = recording_list[y]
                    duplicate_set.add(recording_list[y]['programId'])
                    i += 1

    else:
        if use_name:
            if use_description:
                if use_metadata:
                    if use_dur_diff:
                        # Name, description, metadataId, durations
                        print('Haetaan duplikaatteja (nimi, kuvaus, metadataId, ero kestossa korkeintaan ' + str(max_dur_diff) + ' minuuttia).')
                        for x in range(folder_length):
                            if duplicates_found[x] or not metadata_ids[x] or not descriptions_cleaned[x]:
                                continue
                            for y in range(x + 1, folder_length):
                                if duplicates_found[y] or not metadata_ids[y] or not descriptions_cleaned[y]:
                                    continue
                                if (metadata_ids[x] == metadata_ids[y] and names_cleaned[x] == names_cleaned[y] and (descriptions_cleaned[x].startswith(descriptions_cleaned[y]) or descriptions_cleaned[y].startswith(descriptions_cleaned[x]))
                                    and abs(durations[x] - durations[y]) <= max_dur_diff_sec):
                                    if not duplicates_found[x]:
                                        duplicates_found[x] = True
                                        duplicate_list[i] = recording_list[x]
                                        i += 1
                                    duplicates_found[y] = True
                                    duplicate_list[i] = recording_list[y]
                                    duplicate_set.add(recording_list[y]['programId'])
                                    i += 1
                    else:
                        # Name, description, metadataId
                        print('Haetaan duplikaatteja (nimi, kuvaus, metadataId).')
                        for x in range(folder_length):
                            if duplicates_found[x] or not metadata_ids[x] or not descriptions_cleaned[x]:
                                continue
                            for y in range(x + 1, folder_length):
                                if duplicates_found[y] or not metadata_ids[y] or not descriptions_cleaned[y]:
                                    continue
                                if (metadata_ids[x] == metadata_ids[y] and names_cleaned[x] == names_cleaned[y] and (descriptions_cleaned[x].startswith(descriptions_cleaned[y]) or descriptions_cleaned[y].startswith(descriptions_cleaned[x]))):
                                    if not duplicates_found[x]:
                                        duplicates_found[x] = True
                                        duplicate_list[i] = recording_list[x]
                                        i += 1
                                    duplicates_found[y] = True
                                    duplicate_list[i] = recording_list[y]
                                    duplicate_set.add(recording_list[y]['programId'])
                                    i += 1

                else:
                    if use_dur_diff:
                        # Name, description, durations
                        print('Haetaan duplikaatteja (nimi, kuvaus, ero kestossa korkeintaan ' + str(max_dur_diff) + ' minuuttia).')
                        for x in range(folder_length):
                            if duplicates_found[x] or not descriptions_cleaned[x]:
                                continue
                            for y in range(x + 1, folder_length):
                                if duplicates_found[y] or not descriptions_cleaned[y]:
                                    continue
                                if (names_cleaned[x] == names_cleaned[y] and (descriptions_cleaned[x].startswith(descriptions_cleaned[y]) or descriptions_cleaned[y].startswith(descriptions_cleaned[x]))
                                    and abs(durations[x] - durations[y]) <= max_dur_diff_sec):
                                    if not duplicates_found[x]:
                                        duplicates_found[x] = True
                                        duplicate_list[i] = recording_list[x]
                                        i += 1
                                    duplicates_found[y] = True
                                    duplicate_list[i] = recording_list[y]
                                    duplicate_set.add(recording_list[y]['programId'])
                                    i += 1
                    else:
                        # Name, description
                        print('Haetaan duplikaatteja (nimi, kuvaus).')
                        for x in range(folder_length):
                            if duplicates_found[x] or not descriptions_cleaned[x]:
                                continue
                            for y in range(x + 1, folder_length):
                                if duplicates_found[y] or not descriptions_cleaned[y]:
                                    continue
                                if names_cleaned[x] == names_cleaned[y] and (descriptions_cleaned[x].startswith(descriptions_cleaned[y]) or descriptions_cleaned[y].startswith(descriptions_cleaned[x])):
                                    if not duplicates_found[x]:
                                        duplicates_found[x] = True
                                        duplicate_list[i] = recording_list[x]
                                        i += 1
                                    duplicates_found[y] = True
                                    duplicate_list[i] = recording_list[y]
                                    duplicate_set.add(recording_list[y]['programId'])
                                    i += 1
            else:
                if use_metadata:
                    if use_dur_diff:
                        # Name, metadata, durations
                        print('Haetaan duplikaatteja (nimi, metadataId, ero kestossa korkeintaan ' + str(max_dur_diff) + ' minuuttia).')
                        for x in range(folder_length):
                            if duplicates_found[x] or not metadata_ids[x]:
                                continue
                            for y in range(x + 1, folder_length):
                                if duplicates_found[y] or not metadata_ids[y]:
                                    continue
                                if names_cleaned[x] == names_cleaned[y] and metadata_ids[x] == metadata_ids[y] and abs(durations[x] - durations[y]) <= max_dur_diff_sec:
                                    if not duplicates_found[x]:
                                        duplicates_found[x] = True
                                        duplicate_list[i] = recording_list[x]
                                        i += 1
                                    duplicates_found[y] = True
                                    duplicate_list[i] = recording_list[y]
                                    duplicate_set.add(recording_list[y]['programId'])
                                    i += 1
                    else:
                        # Name, metadata
                        print('Haetaan duplikaatteja (nimi, metadataId).')
                        for x in range(folder_length):
                            if duplicates_found[x] or not metadata_ids[x]:
                                continue
                            for y in range(x + 1, folder_length):
                                if duplicates_found[y] or not metadata_ids[y]:
                                    continue
                                if names_cleaned[x] == names_cleaned[y] and metadata_ids[x] == metadata_ids[y]:
                                    if not duplicates_found[x]:
                                        duplicates_found[x] = True
                                        duplicate_list[i] = recording_list[x]
                                        i += 1
                                    duplicates_found[y] = True
                                    duplicate_list[i] = recording_list[y]
                                    duplicate_set.add(recording_list[y]['programId'])
                                    i += 1
                else:
                    if use_dur_diff:
                        # Name, durations
                        print('Haetaan duplikaatteja (nimi, ero kestossa korkeintaan ' + str(max_dur_diff) + ' minuuttia).')
                        for x in range(folder_length):
                            if duplicates_found[x]:
                                continue
                            for y in range(x + 1, folder_length):
                                if duplicates_found[y]:
                                    continue
                                if names_cleaned[x] == names_cleaned[y] and abs(durations[x] - durations[y]) <= max_dur_diff_sec:
                                    if not duplicates_found[x]:
                                        duplicates_found[x] = True
                                        duplicate_list[i] = recording_list[x]
                                        i += 1
                                    duplicates_found[y] = True
                                    duplicate_list[i] = recording_list[y]
                                    duplicate_set.add(recording_list[y]['programId'])
                                    i += 1
                    else:
                        # Name
                        print('Haetaan duplikaatteja (nimi).')
                        for x in range(folder_length):
                            if duplicates_found[x]:
                                continue
                            for y in range(x + 1, folder_length):
                                if duplicates_found[y]:
                                    continue
                                if names_cleaned[x] == names_cleaned[y]:
                                    if not duplicates_found[x]:
                                        duplicates_found[x] = True
                                        duplicate_list[i] = recording_list[x]
                                        i += 1
                                    duplicates_found[y] = True
                                    duplicate_list[i] = recording_list[y]
                                    duplicate_set.add(recording_list[y]['programId'])
                                    i += 1
        else:
            if use_description:
                if use_metadata:
                    if use_dur_diff:
                        # Description, metadataId, durations
                        print('Haetaan duplikaatteja (kuvaus, metadataId, ero kestossa korkeintaan ' + str(max_dur_diff) + ' minuuttia).')
                        for x in range(folder_length):
                            if duplicates_found[x] or not metadata_ids[x] or not descriptions_cleaned[x]:
                                continue
                            for y in range(x + 1, folder_length):
                                if duplicates_found[y] or not metadata_ids[y] or not descriptions_cleaned[y]:
                                    continue
                                if (metadata_ids[x] == metadata_ids[y] and (descriptions_cleaned[x].startswith(descriptions_cleaned[y]) or descriptions_cleaned[y].startswith(descriptions_cleaned[x]))
                                    and abs(durations[x] - durations[y]) <= max_dur_diff_sec):
                                    if not duplicates_found[x]:
                                        duplicates_found[x] = True
                                        duplicate_list[i] = recording_list[x]
                                        i += 1
                                    duplicates_found[y] = True
                                    duplicate_list[i] = recording_list[y]
                                    duplicate_set.add(recording_list[y]['programId'])
                                    i += 1
                    else:
                        # Description, metadataId
                        print('Haetaan duplikaatteja (kuvaus, metadataId).')
                        for x in range(folder_length):
                            if duplicates_found[x] or not metadata_ids[x] or not descriptions_cleaned[x]:
                                continue
                            for y in range(x + 1, folder_length):
                                if duplicates_found[y] or not metadata_ids[y] or not descriptions_cleaned[y]:
                                    continue
                                if (metadata_ids[x] == metadata_ids[y] and (descriptions_cleaned[x].startswith(descriptions_cleaned[y]) or descriptions_cleaned[y].startswith(descriptions_cleaned[x]))):
                                    if not duplicates_found[x]:
                                        duplicates_found[x] = True
                                        duplicate_list[i] = recording_list[x]
                                        i += 1
                                    duplicates_found[y] = True
                                    duplicate_list[i] = recording_list[y]
                                    duplicate_set.add(recording_list[y]['programId'])
                                    i += 1

                else:
                    if use_dur_diff:
                        # Description, durations
                        print('Haetaan duplikaatteja (kuvaus, ero kestossa korkeintaan ' + str(max_dur_diff) + ' minuuttia).')
                        for x in range(folder_length):
                            if duplicates_found[x] or not descriptions_cleaned[x]:
                                continue
                            for y in range(x + 1, folder_length):
                                if duplicates_found[y] or not descriptions_cleaned[y]:
                                    continue
                                if (abs(durations[x] - durations[y]) <= max_dur_diff_sec and (descriptions_cleaned[x].startswith(descriptions_cleaned[y]) or descriptions_cleaned[y].startswith(descriptions_cleaned[x]))):
                                    if not duplicates_found[x]:
                                        duplicates_found[x] = True
                                        duplicate_list[i] = recording_list[x]
                                        i += 1
                                    duplicates_found[y] = True
                                    duplicate_list[i] = recording_list[y]
                                    duplicate_set.add(recording_list[y]['programId'])
                                    i += 1
                    else:
                        # Description
                        print('Haetaan duplikaatteja (kuvaus).')
                        for x in range(folder_length):
                            if duplicates_found[x] or not descriptions_cleaned[x]:
                                continue
                            for y in range(x + 1, folder_length):
                                if duplicates_found[y] or not descriptions_cleaned[y]:
                                    continue
                                if (descriptions_cleaned[x].startswith(descriptions_cleaned[y]) or descriptions_cleaned[y].startswith(descriptions_cleaned[x])):
                                    if not duplicates_found[x]:
                                        duplicates_found[x] = True
                                        duplicate_list[i] = recording_list[x]
                                        i += 1
                                    duplicates_found[y] = True
                                    duplicate_list[i] = recording_list[y]
                                    duplicate_set.add(recording_list[y]['programId'])
                                    i += 1
            else:
                if use_metadata:
                    if use_dur_diff:
                        # Metadata, durations
                        print('Haetaan duplikaatteja (metadataId, ero kestossa korkeintaan ' + str(max_dur_diff) + ' minuuttia).')
                        for x in range(folder_length):
                            if duplicates_found[x] or not metadata_ids[x]:
                                continue
                            for y in range(x + 1, folder_length):
                                if duplicates_found[y] or not metadata_ids[y]:
                                    continue
                                if metadata_ids[x] == metadata_ids[y] and abs(durations[x] - durations[y]) <= max_dur_diff_sec:
                                    if not duplicates_found[x]:
                                        duplicates_found[x] = True
                                        duplicate_list[i] = recording_list[x]
                                        i += 1
                                    duplicates_found[y] = True
                                    duplicate_list[i] = recording_list[y]
                                    duplicate_set.add(recording_list[y]['programId'])
                                    i += 1
                    else:
                        # Metadata
                        print('Haetaan duplikaatteja (metadataId).')
                        for x in range(folder_length):
                            if duplicates_found[x] or not metadata_ids[x]:
                                continue
                            for y in range(x + 1, folder_length):
                                if duplicates_found[y] or not metadata_ids[y]:
                                    continue
                                if metadata_ids[x] == metadata_ids[y]:
                                    if not duplicates_found[x]:
                                        duplicates_found[x] = True
                                        duplicate_list[i] = recording_list[x]
                                        i += 1
                                    duplicates_found[y] = True
                                    duplicate_list[i] = recording_list[y]
                                    duplicate_set.add(recording_list[y]['programId'])
                                    i += 1
                else:
                    if use_dur_diff:
                        # Durations
                        print('Haetaan duplikaatteja (ero kestossa korkeintaan ' + str(max_dur_diff) + ' minuuttia).')
                        for x in range(folder_length):
                            if duplicates_found[x]:
                                continue
                            for y in range(x + 1, folder_length):
                                if duplicates_found[y]:
                                    continue
                                if abs(durations[x] - durations[y]) <= max_dur_diff_sec:
                                    if not duplicates_found[x]:
                                        duplicates_found[x] = True
                                        duplicate_list[i] = recording_list[x]
                                        i += 1
                                    duplicates_found[y] = True
                                    duplicate_list[i] = recording_list[y]
                                    duplicate_set.add(recording_list[y]['programId'])
                                    i += 1

    return duplicate_set, duplicate_list[:i]
