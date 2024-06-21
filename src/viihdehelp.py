from .command_strings import *

general_help = [['ENTER', '', 'Hyväksy/Palaa/Poistu'],
               [SHOW_HELP, '', 'Näytä tämä listaus'],
               [SHOW_QUOTA, '', 'Näytä jäljellä oleva tallennustila'],
               [LIST_FOLDER_SHORTCUTS, '', 'Listaa kansioiden pikavalinnat'],
               [LIST_DL_FOLDERS, '', 'Näydä nykyinen latauskansio ja pikavalinnat'],
               [SET_DL_FOLDER, 'POLKU', 'Aseta latauskansioksi POLKU'],
               [DL_FOLDER_SHORTCUT, 'NIMI', 'Aseta pikavalinta NIMI latauskansioksi'],
               [SET_DL_FOLDER_SHORTCUT, 'NIMI', 'Lisää nykyinen latauskansio pikavalinnaksi NIMI'],
               [SET_DL_FOLDER_SHORTCUT, 'NIMI | POLKU', 'Lisää latauskansio POLKU pikavalinnaksi NIMI'],
               [RELOAD_CONFIG, '', 'Päivitä asetukset tiedostoista settings.ini ja columns.ini'],
               [OPEN_CONFIG, '', 'Avaa settings.ini Muistiossa'],
               [OPEN_COLUMNS, '', 'Avaa columns.ini Muistiossa']]

folder_help = [general_help[0], general_help[1], general_help[2],
              ['', '#', 'Siirry kansioon # (numero)'],
              [ROOT_FOLDER, '', 'Siirry pääkansioon'],
              [FOLDER_UP, '', 'Siirry yläkansioon'],
              [LIST_FOLDERS, '', 'Listaa kansiot'],
              [NEW_FOLDER, 'NIMI', 'Luo uusi kansio NIMI'],
              [DELETE_FOLDER, '', 'Poista nykyinen kansio'],
              [DELETE_FOLDER, ' #', 'Poista kansio #'],
              [LIST_RECORDINGS, '', 'Listaa nykyisen kansion tallenteet'],
              [REFRESH_RECORDINGS, '', 'Päivitä kansiot'],
              [DOWNLOAD_FOLDER, '', 'Lataa nykyisen kansion tallenteet'], general_help[2],
              [SET_SHORTCUT, 'NIMI', 'Lisää nykyinen kansio pikavalinnaksi NIMI']] + general_help[3:]

recording_help = [general_help[0], general_help[1], general_help[2],
                 [RESTORE_RECORDINGS, '##', 'Palauta tallenteet ## Elisa Viihteen roskakorista'],
                 [LIST_FILTERED, '', 'Listaa suodatetut tallenteet'],
                 [SHOW_WIDTH, '', 'Näytä tallenteiden listaukseen tarvittava terminaalin leveys'],
                 [PRINT_DESCRIPTIONS, '', 'Näytä/piilota tallenteiden kuvaukset'],
                 [SHOW_SORTING_HELP, '', 'Näytä lajitteluavaimet'],
                 [SORT_RECORDINGS, '%', 'Järjestä tallenteet nousevasti avaimen % mukaisesti (ks. LUEMINUT)'],
                 [SORT_RECORDINGS_DESC, '%', 'Järjestä tallenteet laskevasti avaimen % mukaisesti (ks. LUEMINUT)'],
                 [REFRESH_RECORDINGS, '', 'Päivitä tallenteet ja kansiot'],
                 [LIST_FILTERS, '', 'Listaa käytössä olevat suotimet'],
                 [SHOW_FILTER_HELP, '', 'Listaa mahdolliset suotimet'],
                 [CLEAR_FILTERS, '', 'Poista kaikki suotimet'],
                 [CLEAR_LAST_FILTER, '', 'Poista viimeisin suodin'],
                 [CLEAR_FILTER, 'X', 'Poista suodin numero X'],
                 [SET_FILTER_SHORTCUT, 'NIMI', 'Lisää viimeisin suodin pikavalinnaksi NIMI'],
                 [SET_FILTER_SHORTCUT, 'NIMI | X', 'Lisää suodin numero X pikavalinnaksi NIMI'],
                 [SET_FILTER_SHORTCUT, 'NIMI | KOMENTO', 'Lisää KOMENTO pikavalinnaksi NIMI'],
                 [USE_FILTER_SHORTCUT, 'NIMI', 'Käytä pikavalinnan NIMI suodinta'],
                 [LIST_FILTER_SHORTCUTS, '', 'Listaa suodinten pikavalinnat'],
                 [CHANNEL_DAY, '#', 'Näytä tallennetta # edeltävät ja seuraavat tallenteet'],
                 [HIDE_RECORDINGS, '##', 'Suodata pois tallenteet ##'],
                 [EXCLUDE_FOLDER, '', 'Suodata pois valittavassa kansiossa sijaitsevat tallenteet'],
                 [EXCLUDE_FOLDER, ' #', 'Suodata pois tallenteen # kansiossa sijaitsevat tallenteet'],
                 [EXCLUDE_FOLDER, ' > NIMI', 'Suodata pois kansiossa, jonka pikavalinta on NIMI, sijaitsevat tallenteet'],
                 [REMOVE_DUPLICATES, '', 'Etsi duplikaatit (sama nimi ja kuvaus)'],
                 [REMOVE_DUPLICATES, ' X', 'Etsi duplikaatit, hakumoodi X (ks. LUEMINUT)'],
                 [PLAY_RECORDING, '#', 'Toista tallenne # (numero)'],
                 [SHOW_DESCRIPTION, '#', 'Näytä tallenteen # kuvaus'],
                 [SHOW_INFO, '#', 'Näytä tallenteen # tiedot'],
                 [SHOW_URL, '#', 'Näytä tallenteen # URL'],
                 [DOWNLOAD_RECORDINGS, '##', 'Lataa tallenteet ##'],
                 [DELETE_RECORDINGS, '##', 'Siirrä tallenteet ## roskakorikansioon'],
                 [RECYCLE_RECORDINGS, '##', 'Poista tallenteet ## Elisa Viihteen roskakoriin'],
                 [MOVE_RECORDINGS, '##', 'Siirrä tallenteet ## valittavaan kansioon'],
                 [MOVE_RECORDINGS, '## > NIMI', 'Siirrä tallenteet ## kansioon, jonka pikavalinta on NIMI'],
                 [MOVE_RECORDINGS, '## _ #', 'Siirrä tallenteet ## kansioon, jossa tallenne # sijaitsee'], general_help[2],
                 [SET_FOLDER_SHORTCUT, 'NIMI', 'Lisää valittava kansio pikavalinnaksi NIMI'],
                 [SET_FOLDER_SHORTCUT, 'NIMI | #', 'Lisää tallenteen # sisältävä kansio pikavalinnaksi NIMI']] + general_help[3:]

filter_help = [[F_NAME, 'TEKSTI', 'Tallenteen nimi sisältää tekstin'],
              [F_DESCRIPTION, 'TEKSTI', 'Tallenteen kuvaus sisältää tekstin'],
              [F_CHANNEL, 'TEKSTI', 'Tallenteen kanavanimi sisältää tekstin'],
              [F_DURATION, 'X tai HH:MM', 'Tallenteen pituus vähintään X min tai HH tuntia, MM minuuttia'],
              [F_START_TIME, 'YYYY-MM-DD tai DD.MM.YYYY', 'Tallennus alkoi ennen päivämäärää'],
              [F_END_TIME, 'YYYY-MM-DD tai DD.MM.YYYY', 'Tallennus päättyi ennen päivämäärää'],
              [F_WEEKDAY, 'VIIKONPÄIVÄN LYHENNE', 'Tallennus alkoi viikonpäivänä'],
              [F_TIME, 'HH:MM', 'Tallennus alkoi ennen kellonaikaa'],
              [F_ACTOR, 'SUKUNIMI, ETUNIMI', 'Näyttelijä esintyy tallenteella'],
              [F_DIRECTOR, 'SUKUNIMI, ETUNIMI', 'Tallenne on ohjaajan ohjaama'],
              [F_IMDB, 'X.Y', 'Tallenteen IMDB-pisteet vähintään X.Y'],
              [F_SHOWTYPE, 'TEKSTI', 'Tallenteen showtype (metadatassa) sisältää tekstin'],
              [F_GENRE, 'TEKSTI', 'Jokin tallenteen genreistä (metadatassa) sisältää tekstin'],
              [F_SERIES, 'TEKSTI', 'Sarjan nimi sisältää tekstin'],
              [F_EPISODE_NAME, 'TEKSTI', 'Sarjan jakson nimi sisältää tekstin'],
              [F_SEASON, 'XX', 'Sarjan kausi XX'],
              [F_EPISODE, 'XX', 'Sarjan jakso XX']]

sorting_help = [['s', 'alkamisaika'],
               ['e', 'päättymisaika'],
               ['n', 'nimi'],
               ['d', 'kesto'],
               ['c', 'kanava'],
               ['i', 'IMDB-arvosana'],
               ['r', 'poistuu lopullisesti']]

def print_help(position, trash = False):
    if position == 'folders':
        print('\033[92m{:<20}{}\033[39m'.format('Komento', 'Selite'))
        for x in folder_help:
            help_line = '{:<20}{}'.format(x[0] + x[1], x[2])
            print(help_line)
    elif position == 'recordings':
        print('\033[92m{:<20}{}\033[39m'.format('Komento', 'Selite'))
        if trash:
            for x in recording_help:
                if not x[0] in [PLAY_RECORDING, SHOW_URL, DOWNLOAD_RECORDINGS, RECYCLE_RECORDINGS]:
                    help_line = '{:<20}{}'.format(x[0] + x[1], x[2])
                    print(help_line)
        else:
            for x in recording_help:
                if not x[0] in [RESTORE_RECORDINGS]:
                    help_line = '{:<20}{}'.format(x[0] + x[1], x[2])
                    print(help_line)
    elif position == 'filters':
        print('\033[92m{:<30}{}\033[39m'.format('Komento', 'Selite'))
        for x in filter_help:
            help_line = '{:<30}{}'.format(x[0] + ' ' + x[1], x[2])
            print(help_line)
    elif position == 'sorting':
        l = len(sorting_help)
        print('\033[92m{:<12}{}\033[39m'.format('Avain', 'Selite'))
        for i, x in enumerate(sorting_help):
            if not trash and i == l - 1:
                break
            help_line = '{:<12}{}'.format(x[0], x[1])
            print(help_line)
