from rest_framework import serializers

class mySerializer(serializers.Serializer):
    title = serializers.CharField(max_length=20)
    #id = serializers.IntegerField()
