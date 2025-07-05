import joblib
import os
class Utils:
    def __init__(self):
        pass

    def calculate_bmi_and_needs(self, height_cm, weight_kg, age, gender, activity_level, health_goal):
        """Calculate BMI, BMR, and daily calorie needs based on user profile"""
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)

        if bmi < 18.5:
            bmi_category = 'Underweight'
        elif 18.5 <= bmi < 25:
            bmi_category = 'Normal'
        elif 25 <= bmi < 30:
            bmi_category = 'Overweight'
        else:
            bmi_category = 'Obese'

        # BMR (Basal Metabolic Rate) using Mifflin-St Jeor Equation
        if gender.lower() == 'male':
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
        else:
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

        # Activity level multiplier
        activity_multipliers = {
            'low': 1.2,
            'medium': 1.55,
            'high': 1.9
        }
        activity_multiplier = activity_multipliers.get(activity_level.lower(), 1.2)

        daily_calories = bmr * activity_multiplier

        # Adjust based on health goal
        if health_goal.lower() == 'lose':
            daily_calories -= 300
        elif health_goal.lower() == 'gain':
            daily_calories += 300
        # else maintain as is

        return {
            'bmi': round(bmi, 1),
            'bmi_category': bmi_category,
            'bmr': round(bmr, 1),
            'daily_calories': round(daily_calories, 1)
        }
    
    def create_meal_plan_with_options(self, height_cm, weight_kg, age, gender, activity_level, health_goal, weekly_budget, n_options=1):
        
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        # Load the model
        model_path = os.path.join(BASE_DIR, 'models/meals_df.pkl')
        meals_df = joblib.load(model_path)
        
        needs = self.calculate_bmi_and_needs(height_cm, weight_kg, age, gender, activity_level, health_goal)
        daily_budget = weekly_budget / 7
        daily_calories = needs['daily_calories']

        
        meal_budgets = {
            'breakfast': daily_budget * 0.25,
            'lunch': daily_budget * 0.45,
            'dinner': daily_budget * 0.30
        }
        meal_calories = {
            'breakfast': daily_calories * 0.25,
            'lunch': daily_calories * 0.45,
            'dinner': daily_calories * 0.30
        }

        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekly_plan = {}

        for day in days:
            daily_meals = {}
            for meal_type in ['breakfast', 'lunch', 'dinner']:
                budget = meal_budgets[meal_type]
                max_cal = meal_calories[meal_type] * 1.3  # 30% margin

                # RELAXED FILTER: No meal_type filtering + more forgiving budget/calorie
                filtered_meals = meals_df[
                    (meals_df['price'] <= budget * 1.5) &
                    (meals_df['calories'] <= max_cal * 1.5)
                ]

                if len(filtered_meals) >= n_options:
                    options = filtered_meals.sample(n=n_options, replace=False).to_dict('records')
                elif len(filtered_meals) > 0:
                    options = filtered_meals.to_dict('records')
                else:
                    fallback_meals = meals_df.nsmallest(n_options, 'price')
                    options = fallback_meals.to_dict('records')

                daily_meals[f'{meal_type}_options'] = options

            # Calculate daily cost and calories based on first options safely
            day_cost = 0
            day_calories = 0
            for key, options in daily_meals.items():
                if key.endswith('_options') and options:
                    day_cost += options[0]['price']
                    day_calories += options[0]['calories']

            daily_meals['daily_cost'] = day_cost
            daily_meals['daily_calories'] = day_calories

            weekly_plan[day] = daily_meals

        weekly_cost = sum(day['daily_cost'] for day in weekly_plan.values())
        weekly_calories = sum(day['daily_calories'] for day in weekly_plan.values())
        budget_used_percent = (weekly_cost / weekly_budget) * 100 if weekly_budget else 0

        return {
            'profile': needs,
            'weekly_plan': weekly_plan,
            'weekly_cost': weekly_cost,
            'weekly_calories': weekly_calories,
            'budget_used_percent': budget_used_percent
    }