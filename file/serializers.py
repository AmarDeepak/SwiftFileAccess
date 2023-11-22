import shutil

from rest_framework import serializers
from file.models import Directory, Files

class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Files
        fields = '__all__'

class FileListSerializer(serializers.Serializer):
    files = serializers.ListField(
        child = serializers.FileField(max_length=100000, allow_empty_file= False, use_url=False)
    )
    directory = serializers.CharField(required=False)

    def compress_files(self, directory):
        """ TODO: use own compression algo to reduce the file size without compromising the quatlity or data.
            TODO: store the files to any place without storing/saving it on server or inside the project directory."""
        shutil.make_archive(f'static/zip/{directory}', 'zip', f'file/static/{directory}')


    def create(self, validated_data):
        directory = Directory.objects.create()
        files = validated_data.pop("files")
        files_objs =[]
        for file in files:
            files_obj = Files.objects.create(directory=directory, file=file)
            files_objs.append(files_obj)

        self.compress_files(directory.uid)
        return {'files':[], 'directory':str(directory.uid)}