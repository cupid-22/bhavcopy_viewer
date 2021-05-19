from rest_framework import serializers
from ...models.import_duty import ImportDuty


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportDuty
        fields = ('id', 'text')
