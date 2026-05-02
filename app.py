import gradio as gr
import pandas as pd
import numpy as np
import joblib
import os

from utils.food_warnings import FOOD_WARNINGS, HEALTHY_ALTERNATIVES, ALLERGY_REPLACEMENTS
from utils.meal_planner import generate_meal_plan, get_meal_plan_dataframe
from utils.report_generator import build_report_html

# --- Helper Functions ---
def get_bmi_category(bmi):
    if bmi < 18.5: return 'Underweight'
    elif bmi < 25: return 'Normal'
    elif bmi < 30: return 'Overweight'
    else: return 'Obese'

def get_bp_category(sys_val, dia_val):
    if sys_val < 120 and dia_val < 80: return 'Normal'
    elif sys_val < 130 and dia_val < 80: return 'Elevated'
    elif sys_val < 140 or dia_val < 90: return 'High Stage 1'
    else: return 'High Stage 2'

def get_bmi_color(bmi):
    if bmi < 18.5: return '#FF9800'
    elif bmi < 25: return '#4CAF50'
    elif bmi < 30: return '#FF9800'
    else: return '#F44336'

# --- Load Models ---
print("Loading models...")
clf = joblib.load('models/meal_plan_classifier.pkl')
reg = joblib.load('models/macro_regressor.pkl')
model_data = joblib.load('models/label_encoders.pkl')
encoders = model_data['encoders']
target_encoder = model_data['target_encoder']
feature_cols = model_data['feature_cols']
defaults = model_data['defaults']
print("Models loaded successfully!")

def safe_encode(col, val):
    le = encoders[col]
    val_str = str(val)
    if val_str in le.classes_:
        return int(le.transform([val_str])[0])
    else:
        return 0

# --- Main Prediction Function ---
def predict_diet(name, age, gender, height, weight, disease, bp_sys, bp_dia,
                 chol, sugar, genetic, allergies, steps, exercise,
                 sleep, alcohol, smoking, diet_habit, cuisine, aversions):

    # Compute derived features
    bmi = weight / ((height / 100) ** 2)
    bmi_cat = get_bmi_category(bmi)
    bp_cat = get_bp_category(bp_sys, bp_dia)
    activity_score = (steps / 1000) + (exercise * 1.5)

    # Handle allergies from CheckboxGroup
    if not allergies or 'None' in allergies:
        allergy_val = 'None'
    else:
        allergy_val = allergies[0]

    # Handle aversions from CheckboxGroup
    if not aversions or 'None' in aversions:
        aversion_val = 'None'
    else:
        aversion_val = aversions[0]

    # Build feature array
    feature_values = {
        'Age': age,
        'Gender_enc': safe_encode('Gender', gender),
        'Height_cm': height,
        'Weight_kg': weight,
        'BMI': bmi,
        'BMI_Category_enc': safe_encode('BMI_Category', bmi_cat),
        'Chronic_Disease_enc': safe_encode('Chronic_Disease', disease),
        'Blood_Pressure_Systolic': bp_sys,
        'Blood_Pressure_Diastolic': bp_dia,
        'BP_Category_enc': safe_encode('BP_Category', bp_cat),
        'Cholesterol_Level': chol,
        'Blood_Sugar_Level': sugar,
        'Genetic_Risk_Factor_enc': safe_encode('Genetic_Risk_Factor', genetic),
        'Allergies_enc': safe_encode('Allergies', allergy_val),
        'Daily_Steps': steps,
        'Exercise_Frequency': exercise,
        'Sleep_Hours': sleep,
        'Alcohol_Consumption_enc': safe_encode('Alcohol_Consumption', alcohol),
        'Smoking_Habit_enc': safe_encode('Smoking_Habit', smoking),
        'Dietary_Habits_enc': safe_encode('Dietary_Habits', diet_habit),
        'Caloric_Intake': defaults['Caloric_Intake'],
        'Protein_Intake': defaults['Protein_Intake'],
        'Carbohydrate_Intake': defaults['Carbohydrate_Intake'],
        'Fat_Intake': defaults['Fat_Intake'],
        'Preferred_Cuisine_enc': safe_encode('Preferred_Cuisine', cuisine),
        'Food_Aversions_enc': safe_encode('Food_Aversions', aversion_val),
        'Activity_Score': activity_score,
    }

    X = np.array([[feature_values[col] for col in feature_cols]], dtype=np.float64)

    # Predict
    meal_plan_enc = clf.predict(X)[0]
    meal_plan = target_encoder.inverse_transform([meal_plan_enc])[0]
    macros = reg.predict(X)[0]

    # Caloric intake: Calories, Protein (g), Carbs (g), Fats (g)
    cal = int(round(macros[0]))
    prot = int(round(macros[1]))
    carb = int(round(macros[2]))
    fat = int(round(macros[3]))

    # Build macros DataFrame
    macros_df = pd.DataFrame({
        'Nutrient': ['Calories (kcal)', 'Protein (g)', 'Carbohydrates (g)', 'Fats (g)'],
        'Daily Target': [cal, prot, carb, fat]
    })

    # BMI output
    bmi_color = get_bmi_color(bmi)
    bmi_md = f"""
    <div style="background:{bmi_color}15;border:2px solid {bmi_color};border-radius:12px;padding:18px;text-align:center;">
        <div style="font-size:36px;font-weight:800;color:{bmi_color};">{bmi:.1f}</div>
        <div style="font-size:16px;font-weight:600;color:{bmi_color};margin-top:4px;">{bmi_cat}</div>
        <div style="font-size:12px;color:#666;margin-top:6px;">BMI = Weight(kg) / Height(m)²</div>
    </div>"""

    # Food Warnings
    warnings_list = FOOD_WARNINGS.get(disease, [])
    # Apply allergy filtering to warnings
    filtered_warnings = []
    allergy_set = set(allergies) if allergies else set()
    for food, reason in warnings_list:
        skip = False
        if 'Nut Allergy' in allergy_set and 'nuts' in food.lower():
            skip = True
        if not skip:
            filtered_warnings.append((food, reason))

    # Build allergy-specific warnings
    if allergies and 'None' not in allergies:
        for allergy in allergies:
            if allergy in ALLERGY_REPLACEMENTS:
                for bad_food, note in ALLERGY_REPLACEMENTS[allergy].items():
                    filtered_warnings.append((f"{bad_food} ({allergy})", f"Allergy alert: {note}"))

    warnings_md = ""
    if filtered_warnings:
        items = ""
        for food, reason in filtered_warnings:
            items += f'<div style="background:#fff3f3;border-left:4px solid #d32f2f;padding:8px 12px;margin:5px 0;border-radius:0 6px 6px 0;"><strong style="color:#d32f2f;">❌ {food}</strong><br><span style="color:#666;font-size:13px;">{reason}</span></div>'
        warnings_md = f"### ⚠️ Foods to Avoid ({disease if disease != 'None' else 'General'})\n{items}"
    else:
        warnings_md = "### ✅ No Specific Warnings\nNo food warnings for your current health profile. Keep eating healthy!"

    # Healthy Alternatives
    alternatives = {}
    for food, reason in warnings_list:
        if food in HEALTHY_ALTERNATIVES:
            alternatives[food] = HEALTHY_ALTERNATIVES[food]

    alts_md = ""
    if alternatives:
        items = ""
        for bad, good in alternatives.items():
            items += f'<div style="background:#e8f5e9;border-left:4px solid #2e7d32;padding:8px 12px;margin:5px 0;border-radius:0 6px 6px 0;"><span style="color:#d32f2f;text-decoration:line-through;">{bad}</span> → <strong style="color:#2e7d32;">✅ {good}</strong></div>'
        alts_md = f"### 💡 Healthy Alternatives\n{items}"
    else:
        alts_md = "### ✅ Great Choices!\nNo substitutions needed. Your diet looks healthy!"

    # Meal Plan badge
    meal_colors = {
        'Balanced Diet': '#1a73e8',
        'High-Protein Diet': '#2e7d32',
        'Low-Carb Diet': '#e65100',
        'Low-Fat Diet': '#c62828',
    }
    plan_color = meal_colors.get(meal_plan, '#1a73e8')
    meal_plan_md = f"""
    <div style="text-align:center;padding:20px;">
        <div style="font-size:13px;color:#888;margin-bottom:8px;">AI RECOMMENDED MEAL PLAN</div>
        <div style="display:inline-block;background:{plan_color};color:white;padding:15px 40px;border-radius:12px;font-size:24px;font-weight:700;box-shadow:0 4px 15px {plan_color}40;">
            {meal_plan}
        </div>
    </div>"""

    # Generate 7-day meal plan
    patient_allergies = [a for a in allergies if a != 'None'] if allergies else []
    meal_schedule = generate_meal_plan(meal_plan, cuisine, patient_allergies)

    # Build Medical Report HTML
    report_html = build_report_html(
        name=name, age=age, gender=gender, bmi=bmi, disease=disease,
        bp_sys=bp_sys, bp_dia=bp_dia, chol=chol, sugar=sugar,
        genetic=genetic, allergies=patient_allergies, steps=steps,
        exercise=exercise, sleep=sleep, alcohol=alcohol, smoking=smoking,
        diet_habit=diet_habit, cuisine=cuisine, meal_plan=meal_plan,
        macros=macros, meal_schedule=meal_schedule,
        warnings=filtered_warnings, alternatives=alternatives,
        activity_score=activity_score
    )

    # Status message
    status_md = """
    ### ✅ Diet Plan Generated Successfully!
    Your personalized diet recommendation is ready.
    👉 Check the **🍽️ My Diet Plan** tab for quick results.
    👉 Check the **📊 Medical Report** tab for the full medical nutrition report.
    """

    return status_md, meal_plan_md, macros_df, bmi_md, warnings_md, alts_md, report_html


# --- Build Gradio Interface ---
with gr.Blocks(title='AI Smart Diet Recommender', theme=gr.themes.Soft(), css="""
    .gradio-container { max-width: 1100px !important; }
    footer { display: none !important; }
""") as demo:

    # Custom Header
    gr.HTML("""
    <div style="background:linear-gradient(135deg,#1a73e8 0%,#0d47a1 50%,#4a148c 100%);
                padding:30px 20px;text-align:center;border-radius:0 0 20px 20px;margin-bottom:25px;">
        <h1 style="color:white;margin:0;font-size:32px;font-weight:800;">🍎 AI Smart Diet Recommender</h1>
        <p style="color:rgba(255,255,255,0.85);margin:8px 0 0 0;font-size:15px;">
            Medical-Based Personalized Food Suggestion System
        </p>
        <p style="color:rgba(255,255,255,0.6);margin:5px 0 0 0;font-size:12px;">
            Powered by Random Forest ML Model | Trained on 5,000 Patient Records
        </p>
    </div>
    """)

    with gr.Tabs():
        # ==================== TAB 1: Patient Profile ====================
        with gr.Tab('🩺 Patient Profile'):
            gr.Markdown("### Enter Patient Medical & Lifestyle Information")
            gr.Markdown("Fill in all the details below to get your personalized diet recommendation.")

            with gr.Row():
                with gr.Column(scale=1):
                    name_input = gr.Textbox(label='Patient Name (Optional)', placeholder='Enter name for report...')
                    age_input = gr.Slider(label='Age', minimum=18, maximum=90, step=1, value=35)
                    gender_input = gr.Radio(label='Gender', choices=['Male', 'Female', 'Other'], value='Male')
                    height_input = gr.Slider(label='Height (cm)', minimum=140, maximum=210, step=1, value=170)
                    weight_input = gr.Slider(label='Weight (kg)', minimum=40, maximum=150, step=1, value=70)

                with gr.Column(scale=1):
                    disease_input = gr.Dropdown(
                        label='Chronic Disease',
                        choices=['None', 'Diabetes', 'Hypertension', 'Obesity', 'Heart Disease'],
                        value='None'
                    )
                    bp_sys_input = gr.Slider(label='Systolic BP (mmHg)', minimum=80, maximum=200, step=1, value=120)
                    bp_dia_input = gr.Slider(label='Diastolic BP (mmHg)', minimum=60, maximum=130, step=1, value=80)
                    chol_input = gr.Slider(label='Cholesterol (mg/dL)', minimum=100, maximum=350, step=1, value=200)
                    sugar_input = gr.Slider(label='Blood Sugar (mg/dL)', minimum=60, maximum=300, step=1, value=100)

            with gr.Row():
                with gr.Column(scale=1):
                    genetic_input = gr.Radio(label='Genetic Risk Factor', choices=['Yes', 'No'], value='No')
                    allergies_input = gr.CheckboxGroup(
                        label='Allergies',
                        choices=['None', 'Nut Allergy', 'Gluten Intolerance', 'Lactose Intolerance'],
                        value=['None']
                    )
                    steps_input = gr.Slider(label='Daily Steps', minimum=1000, maximum=20000, step=500, value=5000)
                    exercise_input = gr.Slider(label='Exercise (days/week)', minimum=0, maximum=7, step=1, value=3)

                with gr.Column(scale=1):
                    sleep_input = gr.Slider(label='Sleep Hours', minimum=3, maximum=12, step=0.5, value=7)
                    alcohol_input = gr.Radio(label='Alcohol Consumption', choices=['Yes', 'No'], value='No')
                    smoking_input = gr.Radio(label='Smoking Habit', choices=['Yes', 'No'], value='No')
                    diet_input = gr.Dropdown(
                        label='Dietary Habits',
                        choices=['Regular', 'Vegetarian', 'Vegan', 'Keto'],
                        value='Regular'
                    )
                    cuisine_input = gr.Dropdown(
                        label='Preferred Cuisine',
                        choices=['Indian', 'Asian', 'Western', 'Mediterranean'],
                        value='Indian'
                    )
                    aversions_input = gr.CheckboxGroup(
                        label='Food Aversions',
                        choices=['None', 'Sweet', 'Salty', 'Spicy'],
                        value=['None']
                    )

            status_output = gr.Markdown(visible=True)
            submit_btn = gr.Button('🚀 Get My Diet Plan', variant='primary', size='lg')

        # ==================== TAB 2: My Diet Plan ====================
        with gr.Tab('🍽️ My Diet Plan'):
            meal_plan_output = gr.Markdown("👆 Submit your profile first to see results here.")
            with gr.Row():
                with gr.Column(scale=2):
                    macros_output = gr.DataFrame(
                        label='📊 Daily Macronutrient Targets',
                        headers=['Nutrient', 'Daily Target'],
                        datatype=['str', 'number'],
                        interactive=False
                    )
                with gr.Column(scale=1):
                    bmi_output = gr.Markdown()
            with gr.Row():
                with gr.Column(scale=1):
                    warnings_output = gr.Markdown()
                with gr.Column(scale=1):
                    alts_output = gr.Markdown()

        # ==================== TAB 3: Medical Report ====================
        with gr.Tab('📊 Medical Report'):
            gr.Markdown("**Full Medical Nutrition Report** — Scroll down to view the complete report with vitals, meal schedule, warnings, and lifestyle recommendations.")
            report_output = gr.HTML()

    # Connect button to prediction function
    submit_btn.click(
        fn=predict_diet,
        inputs=[
            name_input, age_input, gender_input, height_input, weight_input,
            disease_input, bp_sys_input, bp_dia_input, chol_input, sugar_input,
            genetic_input, allergies_input, steps_input, exercise_input,
            sleep_input, alcohol_input, smoking_input, diet_input,
            cuisine_input, aversions_input
        ],
        outputs=[
            status_output, meal_plan_output, macros_output,
            bmi_output, warnings_output, alts_output, report_output
        ]
    )

if __name__ == '__main__':
    demo.launch()