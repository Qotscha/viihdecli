# Folder view
ROOT_FOLDER = '/'
FOLDER_UP = '..'
LIST_FOLDERS = '.'
NEW_FOLDER = 'n '
LIST_RECORDINGS = 'l'
DOWNLOAD_FOLDER = 'dl'
SET_SHORTCUT = 'fs '                # command shortcutName
DELETE_FOLDER = 'del'

# Recordings view
CLEAR_FILTERS = '.'
CLEAR_LAST_FILTER = '..'
CLEAR_FILTER = '. '
LIST_FILTERED = 'l'
LIST_FILTERS = 'f'
REFRESH_RECORDINGS = 'r'
REMOVE_DUPLICATES = 'rd'            # n for checking names only
CHANNEL_DAY = 'cd '
HIDE_RECORDINGS = 'rem '
PLAY_RECORDING = 'p '
SHOW_DESCRIPTION = 'd '
PRINT_DESCRIPTIONS = 'pd'
SHOW_INFO = 'i '
SHOW_URL = 'u '
DOWNLOAD_RECORDINGS = 'dl '         # a for all
DELETE_RECORDINGS = 'del '          # a for all, d for duplicates
MOVE_RECORDINGS = 'm '              # command recordings _ recordingNumber OR command recordings > shortcutName OR command recordings, a for all
EXCLUDE_FOLDER = 'ex'               # command recordingNumber OR command > shortcutName OR command
SORT_RECORDINGS = 's '              # s for starttime, e for endtime, n for name, d for duration, c for channel, i for IMDB rating
SORT_RECORDINGS_DESC = 'sd '
SET_FOLDER_SHORTCUT = 'fs '         # command shortcutName
# SET_FOLDER_SHORTCUT_NUMBER = 'fn '  # command shortcutName : recordingNumber
RECYCLE_RECORDINGS = 'rm '
RESTORE_RECORDINGS = 're '
SHOW_FILTER_HELP = 'fh'
SHOW_SORTING_HELP = 'sh'
SHOW_WIDTH = 'sw'

# Both views
SHOW_HELP = 'h'
SHOW_QUOTA = 'q'
DL_FOLDER_SHORTCUT = 'ds '          # command dlShortcutName
SET_DL_FOLDER_SHORTCUT = 'dp '      # command dlShortcutName : dlFolderPath
SET_DL_FOLDER = 'df '               # command dlFolderPath
LIST_DL_FOLDERS = 'ld'
LIST_FOLDER_SHORTCUTS = 'lf'
RELOAD_CONFIG = 'rc'
OPEN_CONFIG = 'o'
OPEN_COLUMNS = 'oc'

# Filters
F_ACTOR = 'a'                       # lastName, firstName (wildcard * at end possible)
F_DIRECTOR = 'di'                   # lastName, firstName (wildcard * at end possible)
F_NAME = 'n'
F_DESCRIPTION = 'de'
F_CHANNEL = 'c'                     # channelName1 | channelName2 | channelName3 ...
F_SHOWTYPE = 'st'
F_GENRE = 'g'
F_SERIES = 'ser'
F_EPISODE_NAME = 'en'
F_DURATION = 'dur'                  # minutes or hh:mm
F_START_TIME = 'b'                  # start date before
F_END_TIME = 'be'                   # start date before
F_WEEKDAY = 'w'                     # weekday1 | weekday2 ...
F_TIME = 't'                        # start time before
F_IMDB = 'im'                       # includes (st movie)
F_SEASON = 'se'                     # season
F_EPISODE = 'ep'                    # episode
