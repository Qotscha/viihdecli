import json
import requests

BASE_URL = 'https://api-viihde-gateway.dc1.elisa.fi/'

def login(client_secret, api_key, username, password):
    # Get access code.
    payload = {'client_id': 'external', 'client_secret': client_secret,
               'response_type': 'code', 'scopes': []}
    headers_ = {'content-type': 'application/json', 'apikey': api_key}
    access_code_json = requests.post(BASE_URL + 'auth/authorize/access-code',
                                  json=payload, headers=headers_)
    access_code = json.loads(access_code_json.text)['code']

    # Get access token.
    payload = {'grant_type': 'authorization_code', 'username': username,
               'password': password, 'client_id': 'external', "code": access_code}
    headers_ = {'content-type': 'application/x-www-form-urlencoded', 'apikey': api_key}
    access_token_json = requests.post(BASE_URL + 'auth/authorize/access-token',
                                   data=payload, headers=headers_)
    access_token = json.loads(access_token_json.text)['access_token']
    headers = {'Authorization': 'Bearer '+ access_token,  'apikey': api_key}
    return headers

def get_folder_tree(headers, platform):
    folders = requests.get(BASE_URL + 'rest/npvr/folders?v=2'
                           + '&platform=' + platform + '&appVersion=1.0', headers=headers)
    return json.loads(folders.text)

def get_folders(folder_id, headers, platform):
    folders = requests.get(BASE_URL + 'rest/npvr/folders/' + folder_id
                           + '?platform=' + platform + '&appVersion=1.0', headers=headers)
    # time.sleep(0.05)
    # print(folders.status_code)
    return json.loads(folders.text)

def get_recordings(folder_id, sort_by, sort_order, headers, platform):
    recordings = requests.get(BASE_URL + 'rest/npvr/recordings/folder/' + folder_id +
                              '?v=2.1&page=0&sortBy=' + sort_by + '&sortOrder=' + sort_order
                              + '&pageSize=10000&platform=' + platform + '&appVersion=1.0'
                              '&includeMetadata=true', headers=headers)
    return json.loads(recordings.text)

def get_recycle(sort_by, sort_order, headers, platform):
    recordings = requests.get(BASE_URL + 'rest/npvr/recordings/recycle'
                                  '?v=1&page=0&sortBy=' + sort_by + '&sortOrder=' + sort_order
                                  + '&pageSize=10000&platform=' + platform + '&appVersion=1.0'
                                  '&includeMetadata=true', headers=headers)
    return json.loads(recordings.text)

def delete_recordings(recording_list, headers, platform):
    payload = {'programId': recording_list}
    del_request = requests.put(BASE_URL + 'rest/npvr/recordings/delete?v=2&platform=' + platform
                               + '&appVersion=1.0', data=payload, headers=headers)
    return del_request.status_code

def restore_recordings(recording_list, headers, platform):
    payload = {'programId': recording_list}
    restore_request = requests.put(BASE_URL + 'rest/npvr/recordings/recycle?v=1&platform=' + platform
                               + '&appVersion=1.0', data=payload, headers=headers)
    return restore_request.status_code

def get_all_recordings(sort_by, sort_order, headers, platform):
    recordings = requests.get(BASE_URL + 'rest/npvr/recordings'
                                  '?v=2.1&page=0&sortBy=' + sort_by + '&sortOrder=' + sort_order
                                  + '&pageSize=10000&platform=' + platform + '&appVersion=1.0'
                                  '&includeMetadata=true', headers=headers)
    return json.loads(recordings.text)

def get_recording_info(recording_id, headers, platform):
    recording_info = requests.get(BASE_URL + 'rest/npvr/recordings/info/' + recording_id
                                 + '?v=2.1&platform=online&appVersion=1.0&includeMetadata=true',
                                 headers=headers)
    return json.loads(recording_info.text)

def get_recording_url(recording_id, headers, platform):
    payload = '{"cdnServiceOptions":["s_ttml"],"protocol":"hls","applicationVersion":"1","deviceId":"123","drmPlatform":"ios"}'
    headers_ = {'content-type': 'application/json; charset=UTF-8', 'Authorization': headers['Authorization']}
    recording_url = requests.post('https://watchable-api.dc.elisa.fi/V3/recordings/play-options/'
                                + recording_id + '/' + platform, data=payload, headers=headers_)
    # return json.loads(recording_url.text)['url']
    temp_url = json.loads(recording_url.text)['requestRouterUrl']
    perm_url = requests.get(temp_url).url
    return perm_url

def get_recording_url_(recording_id, headers, platform):
    recording_url = requests.get('https://rest-api.elisaviihde.fi/rest/npvr/recordings/url/'
                                + recording_id + '?v=2&platform=' + platform
                                + '&appVersion=1.0', headers=headers)
    # return json.loads(recording_url.text)['url']
    temp_url = json.loads(recording_url.text)['url']
    perm_url = requests.get(temp_url).url
    return perm_url

def move_recordings(recording_list, folder_id, headers, platform):
    payload = {'programId': recording_list, 'folderId': folder_id}
    move_request = requests.put(BASE_URL + 'rest/npvr/recordings/move?v=2&platform=' + platform
                               + '&appVersion=1.0', data=payload, headers=headers)
    return move_request.status_code

def create_folder(name, parent_folder_id, headers, platform):
    if parent_folder_id == '0':
        payload = {'name': name}
    else:
        payload = {'name': name, 'parentFolderId': parent_folder_id}
    create_request = requests.put(BASE_URL + 'rest/npvr/folders?v=0.1&platform=' + platform
                                 + '&appVersion=1.0', data=payload, headers=headers)
    return json.loads(create_request.text)['folderId']

def delete_folder(folder_id, headers, platform):
    payload = {'folderId': folder_id}
    del_request = requests.delete(BASE_URL + 'rest/npvr/folders/' + folder_id + '?v=2&platform='
                                   + platform + '&appVersion=1.0', data=payload, headers=headers)
    return del_request.status_code

def get_quota(headers, platform):
    quota_info = requests.get(BASE_URL + 'rest/npvr/recordings/quota?v=2&platform='
                              + platform, headers=headers)
    return json.loads(quota_info.text)

def get_account_info(headers):
    account_info = requests.get(BASE_URL + 'rest/myaccount/devices,services,netpvr,authentication?v=2',
                                 headers=headers)
    return json.loads(account_info.text)

# def mark_as_watched(recording_id, headers, platform):
    # a=1

# def set_play_position(recording_id, play_position, headers, platform):
    # a=1

# def search_recording(search_string, headers, platform):
    # a=1
