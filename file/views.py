from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
from file.serializers import FileListSerializer
from rest_framework.parsers import MultiPartParser

def upload(request):
    return render(request, 'upload.html')

def download(request, uid):
    return render(request, 'download.html', context={'uid':uid})
class HandleFileUpload(APIView):
    parser_classes = [MultiPartParser]
    def post(self, request):
        try:
            data = request.data
            serializer = FileListSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                # print(serializer)
                return Response({
                    'status': 200,
                    'message': 'File Uploaded successfully',
                    'data': serializer.data,
                })
            return Response({
                'status': 400,
                'message': 'File Not Uploaded successfully',
                'data': serializer.errors
            })
        except Exception as ex:
            """ EXCPETION HANDLING PENDING"""
            print(ex)