import shutil

from rest_framework import serializers
from file.models import Directory, Files
from django.contrib.auth.models import User
class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Files
        fields = '__all__'

class FileListSerializer(serializers.Serializer):
    files = serializers.ListField(
        child = serializers.FileField(max_length=100000, allow_empty_file= False, use_url=False)
    )
    directory = serializers.CharField(required=False)

    user = serializers.CharField(source='User.username', required=False)

    def compress_files(self, directory):
        """ TODO: use own compression algo to reduce the file size without compromising the quatlity or data.
            TODO: store the files to any place without storing/saving it on server or inside the project directory."""
        shutil.make_archive(f'uploaded_files/zip/{directory}', 'zip', f'uploaded_files/{directory}')


    def create(self, validated_data):
        directory = Directory.objects.create()
        files = validated_data.pop("files")
        user = validated_data.pop("User")
        user_obj = User.objects.get(username=user.get('username',''))
        files_objs =[]
        for file in files:
            files_obj = Files.objects.create(directory=directory, user=user_obj, file=file)
            files_objs.append(files_obj)
        self.compress_files(directory.uid)
        return {'files':[], 'directory':str(directory.uid)}