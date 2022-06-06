from rest_framework import serializers
from .models import *


class ConsultantSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return Consultant.objects.create(**validated_data)

    class Meta:
        model = Consultant
        fields = '__all__'
