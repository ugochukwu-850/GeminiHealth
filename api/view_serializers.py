from rest_framework import serializers

class PDFFileSerializer(serializers.Serializer):
    file = serializers.FileField()
    

