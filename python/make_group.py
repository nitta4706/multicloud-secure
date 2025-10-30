#####################
#
# 開発環境で作成されたグループであることを示すため、グループ名に [dev] をつける処理を加えている (31行目)
#
#####################

from google.oauth2 import service_account
from googleapiclient.discovery import build

import json, os

SCOPES = [
    'https://www.googleapis.com/auth/admin.directory.group'
]
DOMAIN = 'mec.co.jp'
CREDENTIAL_FILE = '/opt/credentials/credential.json'

credentials = service_account.Credentials.from_service_account_file(CREDENTIAL_FILE, scopes=SCOPES)
service = build("admin", "directory_v1", credentials=credentials)

def check_exist_email(email):
    groups = service.groups().list(domain=DOMAIN).execute()
    for group in groups.get('groups'):
        if email == group['email']:
            print(f'{email}は既に存在します。')
            return True
    return False

def make_new_group(name, email):
    group_info = {
        'name': "[dev]" + name,
        'email': email
    }
    result = service.groups().insert(body=group_info).execute()
    print(f'{result.get("email")}を作成しました。')

def main():    
    items = os.listdir('./')

    directories = [item for item in items if os.path.isdir(os.path.join('.', item))]
    for directory in directories:
        with open(os.path.join('.', directory, 'data.json'), 'r') as file:
            data = json.load(file)
            if 'group_name' not in data or \
                'group_email' not in data or \
                'user_group_name' not in data or \
                'user_group_email' not in data:
                print(f'data.jsonに必要なキーがありません')
                continue

        if not check_exist_email(data.get('group_email')):
            make_new_group(data.get('group_name'), data.get('group_email'))

        if data.get('group_name') == data.get('user_group_name'):
            print('「Googleグループe-mail(管理者用)」と「Googleグループ e-mail(利用者用)」で同一のメールアドレスが記入されていました。利用者用Googleグループは作成せず処理を終了します。')
            return
    
        if not check_exist_email(data.get('user_group_email')):
            make_new_group(data.get('user_group_name'), data.get('user_group_email'))

if __name__ == '__main__':
    main()