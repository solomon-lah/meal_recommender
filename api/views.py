from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import Utils
from .serializers import RecommendationSerializer, BmiSerializer
import json
# Create your views here.
@csrf_exempt
def meal_recommendation(request):
    # if(request.method != 'POST'):
    #     raise Exception("Only post method is allowed")
    data = json.loads(request.body)
    serializer = RecommendationSerializer(data= data)
    if not serializer.is_valid():
        raise Exception("Request not valid")
  
    utils = Utils()
    data = utils.create_meal_plan_with_options(weight_kg=serializer.validated_data["weight_kg"], age= serializer.validated_data["age"],gender=serializer.validated_data["gender"], activity_level= serializer.validated_data["activity_level"], health_goal=serializer.validated_data["health_goal"], height_cm = serializer.validated_data["height_cm"], weekly_budget=serializer.validated_data["weekly_budget"])
    return JsonResponse(data)

@csrf_exempt
def bmi_recommender(request):
    # if(request.method != 'POST'):
    #     raise Exception("Only post method is allowed")
    data = json.loads(request.body)
    serializer = BmiSerializer(data= data)
    if not serializer.is_valid():
        raise Exception("Request not valid")
  
    utils = Utils()
    data = utils.calculate_bmi_and_needs(weight_kg=serializer.validated_data["weight_kg"], age= serializer.validated_data["age"],gender=serializer.validated_data["gender"], activity_level= serializer.validated_data["activity_level"], health_goal=serializer.validated_data["health_goal"], height_cm = serializer.validated_data["height_cm"])
    return JsonResponse(data)
