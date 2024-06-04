from rest_framework import serializers
from keywords.models import Keywords

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keywords
        fields = '__all__'