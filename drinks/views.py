from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.response import Response

from . models import Drink
from . serializers import DrinkSerializer


@api_view(['GET','POST'])
def drinkList(request):
    if request.method == 'GET':
        drinks = Drink.objects.all()
        serializer = DrinkSerializer(drinks, many=True)
        return Response(serializer.data)


    if request.method == 'POST':
        serializer = DrinkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({'msg':serializer.errors})


@api_view(['GET','PUT', 'DELETE'])
def drinkDeets(request, pk):
    try:
        drink = Drink.objects.get(pk=pk)
    except Drink.DoesNotExist:
        return Response({"Error":f"No drink with id {pk}"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DrinkSerializer(drink)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DrinkSerializer(drink, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.error_messages)

    elif request.method == 'DELETE':
        drink.delete()
        return Response({"msg":"Deleted succesfully"}, status=status.HTTP_200_OK)

