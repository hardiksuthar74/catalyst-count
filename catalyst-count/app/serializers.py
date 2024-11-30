from rest_framework import serializers
from .models import UploadHistory


class IndustrySerializer(serializers.Serializer):
    industry = serializers.CharField()


class CountrySerializer(serializers.Serializer):
    country = serializers.CharField()


class StateSerializer(serializers.Serializer):
    state = serializers.CharField()


class CitySerializer(serializers.Serializer):
    city = serializers.CharField()


class CompanyFilterSerializer(serializers.Serializer):
    keyword = serializers.CharField(required=False, allow_blank=True)
    industry = serializers.CharField(required=False, allow_blank=True)
    year_founded = serializers.IntegerField(required=False)
    country = serializers.CharField(required=False, allow_blank=True)
    state = serializers.CharField(required=False, allow_blank=True)
    city = serializers.CharField(required=False, allow_blank=True)
    employees_from = serializers.IntegerField(required=False)
    employees_to = serializers.IntegerField(required=False)


class UploadHistorySerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = UploadHistory
        fields = ["id", "file_name", "progress", "status", "created_at"]
