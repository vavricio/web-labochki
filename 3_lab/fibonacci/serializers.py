from rest_framework import serializers


class CalculationRequestSerializer(serializers.Serializer):
    number = serializers.IntegerField()


class CalculationResponseSerializer(serializers.Serializer):
    output_value = serializers.IntegerField()
