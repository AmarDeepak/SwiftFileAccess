from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from allauth.socialaccount.models import SocialToken, SocialApp
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseUpload
from file.models import Directory

def upload_to_gdrive(request):

    # request is the HttpRequest object
    token = SocialToken.objects.get(account__user=request.user, account__provider='Google')

    credentials = Credentials(
        token=token.token,
        refresh_token=token.token_secret,
        token_uri='https://oauth2.googleapis.com/token',
        client_id='client-id', # replace with yours
        client_secret='client-secret') # replace with yours

    service = build('drive', 'v3', credentials=credentials)
    validated_data = request.data
    files = validated_data.pop("files")
    file_ids = []
    # files = []
    for file in files:
        file_metadata = {"name": file.name,
                         "mimeType": "application/vnd.google-apps.drive-sdk"}
        file_obj = file.open()
        media = MediaIoBaseUpload(file_obj, mimetype=file.content_type)
        file = (
            service.files()
            .create(body=file_metadata, media_body=media, fields="id", uploadType=get_optimum_uploadtype(file.size))
            .execute()
        )
        file_ids.append(file.get("id"))
        # files.append(file)
        print(f'File ID: {file.get("id")}')
    return file_ids
def download_from_gdrive():
    pass

def get_optimum_uploadtype(file_size):
    if 0 < file_size < 5000:
        return "multipart"
    elif 5000 < file_size < 10000:
        return "resumable"
    else:
        return "media"


def get_directory(provider=None):
    # if provider == 'Google':
    #     directory = Directory.objects.get_or_create(uid='fileuploadedtogdriveuid_usigq0c_5nmwr_rlhuscp8')
    #     return directory
    # elif provider == 'Apple':
    #     directory = Directory.objects.get_or_create(uid='fileuploadedtoappledriveuid_usigq0c_5nmwr_rlhuscp8')
    return Directory.objects.create()