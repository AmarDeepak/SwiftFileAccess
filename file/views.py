from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
from file.serializers import FileListSerializer
from rest_framework.parsers import MultiPartParser
from file.utils import upload_to_gdrive, get_directory
from file.models import Files
from allauth.socialaccount.models import SocialAccount

def upload(request):
    return render(request, 'file/upload.html')

def download(request, uid):
    return render(request, 'file/download.html', context={'uid':uid})
class HandleFileUpload(APIView):
    parser_classes = [MultiPartParser]
    def post(self, request):
        try:
            user_social_account = SocialAccount.objects.filter(user=request.user)
            if user_social_account:
                import pdb;pdb.set_trace()
                user_social_account = user_social_account[0]
                if user_social_account.provider == 'Google': # Need to remove static text Google and add the djangoChoice for Google
                    directory = get_directory(provider = 'Google')
                    file_ids = upload_to_gdrive(request)
                    for file_id in file_ids:
                        Files.objects.create(
                            directory = directory,
                            user = user_social_account.user,
                            file_id = file_id,
                        )
                    return Response({
                        'status': 200,
                        'message': 'File Uploaded successfully',
                        'data': file_ids,
                    })
                elif user_social_account.provider == 'Apple':
                    pass
                    # TODO: funtionality need to be added.
            else:
                # if user doesn't belong to Apple/Google provider, upload the file to local.
                data = request.data
                serializer = FileListSerializer(data=data)
                # import pdb;pdb.set_trace()
                if serializer.is_valid():
                    serializer.save()
                    print(serializer)
                return Response({
                    'status': 200,
                    'message': 'File Uploaded successfully',
                    'data': serializer.data,
                })
            return Response({
                'status': 400,
                'message': 'File Not Uploaded successfully',
                'data': request
            })
        except Exception as ex:
            """ EXCPETION HANDLING PENDING"""
            print(ex)