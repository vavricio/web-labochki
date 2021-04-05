from json import loads

from django.http import HttpRequest
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from fibonacci.models import CalculateResponse, CalculateRequest
from fibonacci.serializers import CalculationResponseSerializer, CalculationRequestSerializer
from fibonacci.utils import Calculator


class ExampleView(APIView):

    def post(self, request: HttpRequest):
        parsed_request = loads(request.body)
        print(parsed_request)
        request_data_serializer = CalculationRequestSerializer(data=parsed_request)
        if not request_data_serializer.is_valid():
            # Валідацію не пройдено
            return Response(status=400)

        request_data = CalculateRequest(**request_data_serializer.validated_data)
        calculation_result = Calculator.calculate(request_data.number)

        response_data = CalculateResponse(calculation_result)
        response_data_serializer = CalculationResponseSerializer(response_data)
        response = Response(response_data_serializer.data)

        return response


def index(request):
    return render(request, "fibonacci/index.html")
