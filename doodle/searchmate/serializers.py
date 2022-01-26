from rest_framework import serializers

from searchmate import models

class mySerializer(serializers.Serializer):
    id = serializers.IntegerField()


class DocsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.webDoc
        fields = ('id', 'title','content','url')


