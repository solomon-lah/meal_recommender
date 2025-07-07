import joblib
import os
class Utils:
    def __init__(self):
        pass

    def calculate_bmi_and_needs(self, height_cm, weight_kg, age, gender, activity_level, health_goal):
        """Calculate BMI, BMR, and daily calorie needs based on user profile"""
        # height_m = height_cm / 100
        # bmi = weight_kg / (height_m ** 2)

        # if bmi < 18.5:
        #     bmi_category = 'Underweight'
        # elif 18.5 <= bmi < 25:
        #     bmi_category = 'Normal'
        # elif 25 <= bmi < 30:
        #     bmi_category = 'Overweight'
        # else:
        #     bmi_category = 'Obese'

        # # BMR (Basal Metabolic Rate) using Mifflin-St Jeor Equation
        # if gender.lower() == 'male':
        #     bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
        # else:
        #     bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

        # # Activity level multiplier
        # activity_multipliers = {
        #     'low': 1.2,
        #     'medium': 1.55,
        #     'high': 1.9
        # }
        # activity_multiplier = activity_multipliers.get(activity_level.lower(), 1.2)

        # daily_calories = bmr * activity_multiplier

        # # Adjust based on health goal
        # if health_goal.lower() == 'lose':
        #     daily_calories -= 300
        # elif health_goal.lower() == 'gain':
        #     daily_calories += 300
        # # else maintain as is

        # return {
        #     'bmi': round(bmi, 1),
        #     'bmi_category': bmi_category,
        #     'bmr': round(bmr, 1),
        #     'daily_calories': round(daily_calories, 1)
        # }
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)

        # Basal Metabolic Rate (BMR)
        if gender.lower() == 'male':
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
        else:
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

        # Activity factor mapping
        activity_factors = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'very active': 1.9
        }

        # Multiply BMR by activity level
        activity_factor = activity_factors.get(activity_level.lower(), 1.2)
        bmr *= activity_factor

        # Adjust BMR based on health goal
        if health_goal.lower() == 'lose':
            bmr *= 0.85
        elif health_goal.lower() == 'gain':
            bmr *= 1.15

        return {
            'bmi': round(bmi, 1),
            'bmi_category': 'Underweight' if bmi < 18.5 else 'Normal' if bmi < 25 else 'Overweight' if bmi < 30 else 'Obese',
            'daily_calories': round(bmr),
            'protein': round((0.15 * bmr) / 4),
            'fat': round((0.25 * bmr) / 9),
            'bmr': round((0.60 * bmr) / 4)
        }
    
    def create_meal_plan_with_options(self, height_cm, weight_kg, age, gender, activity_level, health_goal, weekly_budget, n_options=1):
        
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        # Load the model
        model_path = os.path.join(BASE_DIR, 'models/meals_df.pkl')
        meals_df = joblib.load(model_path)
        

        needs = self.calculate_bmi_and_needs(height_cm, weight_kg, age, gender, activity_level, health_goal)
        total_weekly_calories = needs['daily_calories'] * 7
        total_budget = weekly_budget


        # Smart daily allocation
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        daily_budget = total_budget / 7
        daily_calories = total_weekly_calories / 7

        weekly_plan = {}
        total_cost = 0
        total_calories = 0
        used_meals = set()

        for day in days:
            daily_meals = {}
            day_cost = 0
            day_calories = 0

            for meal_time in ['meal1', 'meal2', 'meal3']:
                # Allow up to 1/3 of daily allocation per meal
                max_price = (daily_budget - day_cost) / (3 - len(daily_meals))
                max_calories = (daily_calories - day_calories) / (3 - len(daily_meals)) * 1.2

                filtered = meals_df[
                    (meals_df['price'] <= max_price) &
                    (meals_df['calories'] <= max_calories) &
                    (~meals_df['name'].isin(used_meals))
                ]

                if not filtered.empty:
                    meal = filtered.sample(1).iloc[0].to_dict()
                    daily_meals[meal_time] = meal
                    day_cost += meal['price']
                    day_calories += meal['calories']
                    used_meals.add(meal['name'])
                else:
                    daily_meals[meal_time] = {"note": "No meal suggestion available"}

            daily_meals['daily_cost'] = round(day_cost, 2)
            daily_meals['daily_calories'] = round(day_calories, 2)
            weekly_plan[day] = daily_meals

            total_cost += day_cost
            total_calories += day_calories

        budget_used_percent = (total_cost / weekly_budget) * 100
        calories_used_percent = (total_calories / total_weekly_calories) * 100


        return {
            'profile': needs,
            'weekly_plan': weekly_plan,
            'weekly_cost': round(total_cost, 2),
            'weekly_calories': round(total_calories, 2),
            'budget_used_percent': round(budget_used_percent, 2),
            'calories_used_percent': round(calories_used_percent, 2)
        }