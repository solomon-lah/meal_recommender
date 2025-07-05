from django.urls import path, re_path
# from django.urls import reverse_lazy
# from django.contrib.auth import views as auth_views


from .views import meal_recommendation, bmi_recommender
urlpatterns =[
     path('recommender/', meal_recommendation, name= 'recommender'),
     path('bmi/', bmi_recommender, name= 'bmi'),
]