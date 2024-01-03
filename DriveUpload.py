from google.oauth2 import service_account
import os

SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = os.environ.get("SERVICE_ACCOUNT_JSON")
PARENT_FOLDER_ID = os.environ.get("DRIVE_PARENT_FOLDER_ID")

creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

def upload_folder_to_drive(file_path, folder_name):
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    import os
    try:
        drive_service = build('drive', 'v3', credentials=creds)

        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [PARENT_FOLDER_ID]
        }

        drive_folder = drive_service.files().create(body=file_metadata).execute()

        for root, dirs, files in os.walk(file_path):
            for file in files:
                local_file_path = os.path.join(root, file)
                media = MediaFileUpload(local_file_path)
                file_metadata = {
                    'name': file,
                    'parents': [drive_folder.get('id')]
                }
                drive_service.files().create(body=file_metadata, media_body=media).execute()
        return f'Folder "{folder_name}" uploaded to Google Drive as "{folder_name}"'

    except Exception as e:
        return f'error: {e}'
    
def get_file_download_link(videoname):
    from googleapiclient.discovery import build
    try:
        drive_service = build('drive', 'v3', credentials=creds)
        file_id = videoname + '.mp4'

        results = drive_service.files().list().execute()

        download_url = None
        for file in results.get('files', []):
            if file_id == file['name']:
                download_url = 'https://drive.google.com/uc?export=download&id={}'.format(file['id'])
                preview_url = "https://drive.google.com/uc?id={}".format(file['id'])
                break

        return {"downloadUrl": download_url, "previewUrl": preview_url, 'driveId': file['id']}
    except:
        return None
    
def share_file_with_link(file_id):
    from googleapiclient.discovery import build
    service = build('drive', 'v3', credentials=creds)
    permission = {
        'type': 'anyone',
        'role': 'reader',
    }

    request = service.permissions().create(
        fileId=file_id,
        body=permission,
        fields='id',
    )
    response = request.execute()

    print(f'File shared with link. Permission ID: {response["id"]}')