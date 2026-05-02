import random

MEAL_OPTIONS = {
    'Indian': {
        'Breakfast': [
            ('Moong dal chilla with green chutney', ['Balanced Diet', 'Low-Carb Diet', 'Low-Fat Diet', 'High-Protein Diet'], []),
            ('Oats porridge with fruits', ['Balanced Diet', 'High-Protein Diet'], ['gluten']),
            ('Idli with sambar (2 pcs)', ['Balanced Diet', 'Low-Fat Diet'], ['gluten']),
            ('Egg bhurji with whole wheat roti', ['Balanced Diet', 'High-Protein Diet'], ['gluten']),
            ('Poha with peanuts', ['Balanced Diet', 'High-Protein Diet'], ['nuts', 'gluten']),
            ('Vegetable upma', ['Balanced Diet', 'Low-Fat Diet'], ['gluten']),
            ('Paneer paratha with curd', ['Balanced Diet', 'High-Protein Diet'], ['gluten', 'lactose']),
            ('Smoothie bowl (banana + spinach)', ['Low-Carb Diet', 'Low-Fat Diet'], []),
            ('Egg white omelette with veggies', ['High-Protein Diet', 'Low-Carb Diet', 'Low-Fat Diet'], []),
            ('Sprouts salad with lemon', ['Low-Carb Diet', 'Low-Fat Diet', 'High-Protein Diet'], []),
        ],
        'Lunch': [
            ('Dal with brown rice', ['Balanced Diet', 'High-Protein Diet', 'Low-Fat Diet'], ['gluten']),
            ('Rajma with steamed rice', ['Balanced Diet', 'High-Protein Diet'], ['gluten']),
            ('Grilled chicken with salad', ['High-Protein Diet', 'Low-Carb Diet', 'Low-Fat Diet'], []),
            ('Paneer tikka with mint chutney', ['High-Protein Diet', 'Low-Carb Diet'], ['lactose']),
            ('Fish curry with brown rice', ['Balanced Diet', 'High-Protein Diet'], ['gluten']),
            ('Mixed veg sabzi with roti', ['Balanced Diet', 'Low-Fat Diet'], ['gluten']),
            ('Chole with brown rice', ['Balanced Diet', 'High-Protein Diet'], ['gluten']),
            ('Quinoa pulao with raita', ['Balanced Diet', 'High-Protein Diet', 'Low-Fat Diet'], ['lactose']),
            ('Grilled fish with sauteed veggies', ['Low-Carb Diet', 'High-Protein Diet', 'Low-Fat Diet'], []),
            ('Chicken salad with olive oil dressing', ['Low-Carb Diet', 'High-Protein Diet', 'Low-Fat Diet'], []),
        ],
        'Dinner': [
            ('Vegetable soup with garlic bread', ['Balanced Diet', 'Low-Fat Diet'], ['gluten', 'lactose']),
            ('Dal with jeera rice', ['Balanced Diet', 'Low-Fat Diet'], ['gluten']),
            ('Grilled fish with steamed veggies', ['Low-Carb Diet', 'High-Protein Diet', 'Low-Fat Diet'], []),
            ('Chicken tikka with salad', ['High-Protein Diet', 'Low-Carb Diet', 'Low-Fat Diet'], []),
            ('Palak paneer with roti', ['Balanced Diet', 'High-Protein Diet'], ['gluten', 'lactose']),
            ('Moong dal khichdi', ['Balanced Diet', 'Low-Fat Diet'], ['gluten']),
            ('Mixed salad bowl with grilled tofu', ['Low-Carb Diet', 'High-Protein Diet', 'Low-Fat Diet'], []),
            ('Baked vegetables with herbs', ['Low-Carb Diet', 'Low-Fat Diet'], []),
            ('Egg curry with brown rice', ['Balanced Diet', 'High-Protein Diet'], ['gluten']),
            ('Clear chicken soup with veggies', ['Low-Fat Diet', 'Low-Carb Diet'], []),
        ],
        'Snack': [
            ('Roasted chickpeas (chana)', ['Balanced Diet', 'High-Protein Diet', 'Low-Fat Diet'], []),
            ('Green tea with almonds', ['Low-Carb Diet', 'Low-Fat Diet'], ['nuts']),
            ('Seasonal fruit bowl', ['Balanced Diet', 'Low-Fat Diet'], []),
            ('Low-fat yogurt with honey', ['Balanced Diet', 'High-Protein Diet'], ['lactose']),
            ('Makhana (fox nuts) roasted', ['Low-Carb Diet', 'Low-Fat Diet'], []),
            ('Sprouts salad', ['High-Protein Diet', 'Low-Fat Diet', 'Low-Carb Diet'], []),
            ('Cucumber sticks with hummus', ['Low-Carb Diet', 'Low-Fat Diet'], []),
            ('Lemon water with chia seeds', ['Low-Carb Diet', 'Low-Fat Diet'], []),
        ],
    },
    'Asian': {
        'Breakfast': [
            ('Miso soup with tofu', ['Balanced Diet', 'Low-Fat Diet', 'Low-Carb Diet'], []),
            ('Brown rice congee', ['Balanced Diet', 'Low-Fat Diet'], ['gluten']),
            ('Steamed vegetable dumplings', ['Balanced Diet', 'Low-Fat Diet'], ['gluten']),
            ('Egg fried brown rice', ['Balanced Diet', 'High-Protein Diet'], ['gluten']),
            ('Smoothie bowl (mango + spinach)', ['Low-Carb Diet', 'Low-Fat Diet'], []),
            ('Tamagoyaki (Japanese omelette)', ['High-Protein Diet', 'Low-Carb Diet'], []),
            ('Rice cakes with avocado', ['Balanced Diet', 'Low-Fat Diet'], ['gluten']),
            ('Steamed fish with ginger', ['High-Protein Diet', 'Low-Carb Diet', 'Low-Fat Diet'], []),
        ],
        'Lunch': [
            ('Brown rice with vegetable stir-fry', ['Balanced Diet', 'Low-Fat Diet'], ['gluten']),
            ('Sushi rolls (salmon + veg)', ['Balanced Diet', 'High-Protein Diet'], ['gluten']),
            ('Pad thai with tofu', ['Balanced Diet', 'High-Protein Diet'], ['gluten']),
            ('Teriyaki chicken with brown rice', ['Balanced Diet', 'High-Protein Diet'], ['gluten']),
            ('Pho soup (chicken)', ['Balanced Diet', 'Low-Fat Diet'], ['gluten']),
            ('Bok choy with garlic sauce', ['Low-Carb Diet', 'Low-Fat Diet'], []),
            ('Grilled fish with steamed rice', ['Balanced Diet', 'High-Protein Diet'], ['gluten']),
            ('Chicken salad with sesame dressing', ['High-Protein Diet', 'Low-Carb Diet', 'Low-Fat Diet'], []),
            ('Tofu and vegetable curry', ['Balanced Diet', 'High-Protein Diet', 'Low-Fat Diet'], []),
            ('Zucchini noodles with prawns', ['Low-Carb Diet', 'High-Protein Diet', 'Low-Fat Diet'], []),
        ],
        'Dinner': [
            ('Steamed fish with vegetables', ['Low-Carb Diet', 'High-Protein Diet', 'Low-Fat Diet'], []),
            ('Tofu stir-fry with broccoli', ['Low-Carb Diet', 'High-Protein Diet', 'Low-Fat Diet'], []),
            ('Chicken teriyaki with veggies', ['High-Protein Diet', 'Balanced Diet'], []),
            ('Miso ramen (light broth)', ['Balanced Diet', 'Low-Fat Diet'], ['gluten']),
            ('Fresh spring rolls', ['Low-Fat Diet', 'Low-Carb Diet'], ['gluten']),
            ('Grilled salmon with asparagus', ['High-Protein Diet', 'Low-Carb Diet', 'Low-Fat Diet'], []),
            ('Vegetable dim sum', ['Balanced Diet', 'Low-Fat Diet'], ['gluten']),
            ('Clear soup with mushrooms', ['Low-Carb Diet', 'Low-Fat Diet'], []),
            ('Prawn stir-fry with snow peas', ['High-Protein Diet', 'Low-Carb Diet', 'Low-Fat Diet'], []),
            ('Chicken and vegetable soup', ['Balanced Diet', 'Low-Fat Diet', 'High-Protein Diet'], []),
        ],
        'Snack': [
            ('Edamame beans', ['High-Protein Diet', 'Low-Fat Diet', 'Low-Carb Diet'], []),
            ('Seaweed snacks', ['Low-Carb Diet', 'Low-Fat Diet'], []),
            ('Green tea', ['Low-Carb Diet', 'Low-Fat Diet'], []),
            ('Fresh fruit slices', ['Balanced Diet', 'Low-Fat Diet'], []),
            ('Rice crackers', ['Balanced Diet'], ['gluten']),
            ('Miso soup (small)', ['Low-Fat Diet', 'Low-Carb Diet'], []),
            ('Steamed dumplings (veg)', ['Balanced Diet', 'Low-Fat Diet'], ['gluten']),
            ('Coconut water', ['Low-Carb Diet', 'Low-Fat Diet'], []),
        ],
    },
    'Western': {
        'Breakfast': [
            ('Scrambled eggs with whole wheat toast', ['Balanced Diet', 'High-Protein Diet'], ['gluten']),
            ('Oatmeal with berries and nuts', ['Balanced Diet', 'High-Protein Diet'], ['gluten', 'nuts']),
            ('Greek yogurt parfait', ['High-Protein Diet', 'Low-Fat Diet'], ['lactose']),
            ('Avocado toast on whole grain', ['Balanced Diet', 'Low-Fat Diet'], ['gluten']),
            ('Green smoothie (spinach + banana)', ['Low-Carb Diet', 'Low-Fat Diet'], []),
            ('Whole wheat pancakes', ['Balanced Diet'], ['gluten', 'lactose']),
            ('Egg white omelette with veggies', ['High-Protein Diet', 'Low-Carb Diet', 'Low-Fat Diet'], []),
            ('Protein oat bowl with seeds', ['High-Protein Diet', 'Balanced Diet'], ['gluten', 'nuts']),
        ],
        'Lunch': [
            ('Grilled chicken Caesar salad', ['High-Protein Diet', 'Low-Carb Diet'], ['gluten', 'lactose']),
            ('Quinoa bowl with roasted veggies', ['Balanced Diet', 'High-Protein Diet', 'Low-Fat Diet'], []),
            ('Whole wheat turkey sandwich', ['Balanced Diet', 'High-Protein Diet'], ['gluten']),
            ('Grilled fish with sweet potato', ['Balanced Diet', 'High-Protein Diet'], []),
            ('Pasta salad with olive oil dressing', ['Balanced Diet'], ['gluten']),
            ('Lentil soup with bread', ['Balanced Diet', 'High-Protein Diet', 'Low-Fat Diet'], ['gluten']),
            ('Grilled chicken wrap', ['Balanced Diet', 'High-Protein Diet'], ['gluten']),
            ('Mixed bean salad', ['High-Protein Diet', 'Low-Fat Diet', 'Low-Carb Diet'], []),
            ('Tuna salad with greens', ['High-Protein Diet', 'Low-Carb Diet', 'Low-Fat Diet'], []),
            ('Stuffed bell peppers', ['Low-Carb Diet', 'High-Protein Diet', 'Low-Fat Diet'], []),
        ],
        'Dinner': [
            ('Grilled salmon with steamed broccoli', ['High-Protein Diet', 'Low-Carb Diet', 'Low-Fat Diet'], []),
            ('Chicken breast with mashed potato', ['Balanced Diet', 'High-Protein Diet'], []),
            ('Grilled steak with garden salad', ['High-Protein Diet', 'Low-Carb Diet'], []),
            ('Baked cod with roasted vegetables', ['Low-Fat Diet', 'High-Protein Diet', 'Low-Carb Diet'], []),
            ('Whole wheat pasta with marinara', ['Balanced Diet', 'Low-Fat Diet'], ['gluten']),
            ('Grilled vegetable medley', ['Low-Carb Diet', 'Low-Fat Diet'], []),
            ('Chicken stew with root vegetables', ['Balanced Diet', 'High-Protein Diet'], []),
            ('Herb-roasted chicken breast', ['High-Protein Diet', 'Low-Carb Diet', 'Low-Fat Diet'], []),
            ('Baked trout with lemon', ['High-Protein Diet', 'Low-Fat Diet', 'Low-Carb Diet'], []),
            ('Vegetable and bean chili', ['Balanced Diet', 'High-Protein Diet', 'Low-Fat Diet'], []),
        ],
        'Snack': [
            ('Mixed nuts (unsalted)', ['High-Protein Diet', 'Low-Carb Diet'], ['nuts']),
            ('Apple slices with peanut butter', ['Balanced Diet', 'High-Protein Diet'], ['nuts']),
            ('Carrot sticks with hummus', ['Low-Carb Diet', 'Low-Fat Diet'], []),
            ('Protein bar (low sugar)', ['High-Protein Diet', 'Low-Carb Diet'], []),
            ('Greek yogurt with berries', ['High-Protein Diet', 'Low-Fat Diet'], ['lactose']),
            ('Rice cakes with avocado', ['Balanced Diet', 'Low-Fat Diet'], ['gluten']),
            ('Dark chocolate (2 squares)', ['Low-Carb Diet'], []),
            ('Hard-boiled eggs', ['High-Protein Diet', 'Low-Carb Diet', 'Low-Fat Diet'], []),
        ],
    },
    'Mediterranean': {
        'Breakfast': [
            ('Shakshuka with whole grain bread', ['Balanced Diet', 'High-Protein Diet'], ['gluten']),
            ('Greek yogurt with honey and walnuts', ['Balanced Diet', 'High-Protein Diet'], ['lactose', 'nuts']),
            ('Hummus with whole wheat pita', ['Balanced Diet', 'High-Protein Diet'], ['gluten']),
            ('Avocado toast with olive oil', ['Balanced Diet', 'Low-Fat Diet'], ['gluten']),
            ('Feta cheese salad with olives', ['Balanced Diet', 'Low-Carb Diet'], ['lactose']),
            ('Fresh fruit with mixed nuts', ['Balanced Diet', 'High-Protein Diet'], ['nuts']),
            ('Vegetable omelette with feta', ['High-Protein Diet', 'Low-Carb Diet'], ['lactose']),
            ('Overnight oats with chia seeds', ['Balanced Diet', 'High-Protein Diet'], ['gluten']),
        ],
        'Lunch': [
            ('Falafel wrap with tahini', ['Balanced Diet', 'High-Protein Diet'], ['gluten']),
            ('Greek salad with grilled chicken', ['High-Protein Diet', 'Low-Carb Diet', 'Low-Fat Diet'], []),
            ('Hummus bowl with veggies', ['Balanced Diet', 'Low-Fat Diet', 'Low-Carb Diet'], []),
            ('Grilled fish with couscous', ['Balanced Diet', 'High-Protein Diet'], ['gluten']),
            ('Lentil soup with olive oil', ['Balanced Diet', 'High-Protein Diet', 'Low-Fat Diet'], []),
            ('Tabouleh with grilled chicken', ['Balanced Diet', 'High-Protein Diet'], ['gluten']),
            ('Grilled vegetable wrap', ['Balanced Diet', 'Low-Fat Diet'], ['gluten']),
            ('Tuna salad with olive oil dressing', ['High-Protein Diet', 'Low-Carb Diet', 'Low-Fat Diet'], []),
            ('Chickpea and vegetable stew', ['Balanced Diet', 'High-Protein Diet', 'Low-Fat Diet'], []),
            ('Quinoa salad with roasted veggies', ['Low-Carb Diet', 'High-Protein Diet', 'Low-Fat Diet'], []),
        ],
        'Dinner': [
            ('Grilled lamb with roasted vegetables', ['High-Protein Diet', 'Low-Carb Diet'], []),
            ('Baked fish with olive oil and herbs', ['Low-Fat Diet', 'High-Protein Diet', 'Low-Carb Diet'], []),
            ('Chicken souvlaki with Greek salad', ['High-Protein Diet', 'Low-Carb Diet', 'Low-Fat Diet'], []),
            ('Vegetable moussaka (light)', ['Balanced Diet'], ['lactose']),
            ('Stuffed bell peppers with rice', ['Balanced Diet', 'High-Protein Diet'], ['gluten']),
            ('Seafood risotto', ['Balanced Diet', 'High-Protein Diet'], ['gluten']),
            ('Grilled halloumi with salad', ['High-Protein Diet', 'Low-Carb Diet'], ['lactose']),
            ('Herb-crusted salmon', ['High-Protein Diet', 'Low-Carb Diet', 'Low-Fat Diet'], []),
            ('White bean and vegetable stew', ['Balanced Diet', 'High-Protein Diet', 'Low-Fat Diet'], []),
            ('Grilled prawns with garlic veggies', ['High-Protein Diet', 'Low-Carb Diet', 'Low-Fat Diet'], []),
        ],
        'Snack': [
            ('Hummus with carrot sticks', ['Balanced Diet', 'Low-Fat Diet', 'Low-Carb Diet'], []),
            ('Mixed olives', ['Low-Carb Diet', 'Low-Fat Diet'], []),
            ('Feta cheese with tomatoes', ['High-Protein Diet', 'Low-Carb Diet'], ['lactose']),
            ('Mixed nuts (unsalted)', ['High-Protein Diet', 'Low-Carb Diet'], ['nuts']),
            ('Dried figs and apricots', ['Balanced Diet'], []),
            ('Whole wheat pita with zaatar', ['Balanced Diet'], ['gluten']),
            ('Yogurt with honey', ['Balanced Diet', 'High-Protein Diet'], ['lactose']),
            ('Fresh seasonal fruit', ['Balanced Diet', 'Low-Fat Diet'], []),
        ],
    },
}

DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
MEAL_TYPES = ['Breakfast', 'Lunch', 'Dinner', 'Snack']


def generate_meal_plan(meal_plan_type, cuisine, allergies):
    cuisine = cuisine if cuisine in MEAL_OPTIONS else 'Indian'
    meal_plan_type = meal_plan_type if meal_plan_type else 'Balanced Diet'

    allergy_tags = set()
    if allergies:
        for a in allergies:
            if a == 'Nut Allergy':
                allergy_tags.add('nuts')
            elif a == 'Gluten Intolerance':
                allergy_tags.add('gluten')
            elif a == 'Lactose Intolerance':
                allergy_tags.add('lactose')

    plan = []
    for day in DAYS:
        day_plan = {'Day': day}
        for meal_type in MEAL_TYPES:
            options = MEAL_OPTIONS[cuisine].get(meal_type, [])
            compatible = [m for m in options if meal_plan_type in m[1]]
            safe = [m for m in compatible if not (allergy_tags & set(m[2]))]
            if not safe:
                safe = compatible
            if not safe:
                safe = options

            idx = (DAYS.index(day) * 7 + MEAL_TYPES.index(meal_type) * 3) % len(safe)
            day_plan[meal_type] = safe[idx][0]
        plan.append(day_plan)

    return plan

def get_meal_plan_dataframe(meal_plan_list):
    import pandas as pd
    df = pd.DataFrame(meal_plan_list)
    df = df[['Day', 'Breakfast', 'Lunch', 'Dinner', 'Snack']]
    return df

