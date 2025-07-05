from rest_framework import serializers

class RecommendationSerializer(serializers.Serializer):
    
    weight_kg = serializers.IntegerField()
    height_cm = serializers.IntegerField()
    weekly_budget = serializers.IntegerField()
    activity_level = serializers.CharField(max_length = 20)
    health_goal = serializers.CharField()
    age = serializers.IntegerField()
    gender = serializers.CharField()

class BmiSerializer(serializers.Serializer):
    weight_kg = serializers.IntegerField()
    height_cm = serializers.IntegerField()
    activity_level = serializers.CharField(max_length = 20)
    health_goal = serializers.CharField()
    age = serializers.IntegerField()
    gender = serializers.CharField()    