from rest_framework import serializers


class QueryRequestSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=500)


class SourceSerializer(serializers.Serializer):
    text = serializers.CharField()
    score = serializers.FloatField()


class QueryResponseSerializer(serializers.Serializer):
    answer = serializers.CharField()
    sources = SourceSerializer(many=True)
    confidence = serializers.FloatField()
    validated = serializers.BooleanField()
