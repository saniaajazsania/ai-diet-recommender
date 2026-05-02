import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score, mean_absolute_error, r2_score
import joblib
import os

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

def main():
    print("=" * 60)
    print("  AI Smart Diet Recommender — Model Training")
    print("=" * 60)

    # Create directories
    os.makedirs('models', exist_ok=True)

    # Load dataset
    print("\n[1/6] Loading dataset...")
    df = pd.read_csv('data/Personalized_Diet_Recommendations.csv')
    print(f"  Loaded {len(df)} records with {len(df.columns)} columns")

    # Drop Patient_ID
    df = df.drop('Patient_ID', axis=1)

    # --- Feature Engineering ---
    print("\n[2/6] Engineering features...")
    df['BMI_Category'] = df['BMI'].apply(get_bmi_category)
    df['BP_Category'] = df.apply(
        lambda r: get_bp_category(r['Blood_Pressure_Systolic'], r['Blood_Pressure_Diastolic']), axis=1
    )
    df['Activity_Score'] = (df['Daily_Steps'] / 1000) + (df['Exercise_Frequency'] * 1.5)
    print("  Derived: BMI_Category, BP_Category, Activity_Score")

    # --- Label Encoding ---
    print("\n[3/6] Encoding categorical variables...")
    CATEGORICAL_COLS = [
        'Gender', 'Chronic_Disease', 'Genetic_Risk_Factor', 'Allergies',
        'Alcohol_Consumption', 'Smoking_Habit', 'Dietary_Habits',
        'Preferred_Cuisine', 'Food_Aversions', 'BMI_Category', 'BP_Category'
    ]

    label_encoders = {}
    for col in CATEGORICAL_COLS:
        le = LabelEncoder()
        df[col + '_enc'] = le.fit_transform(df[col].astype(str))
        label_encoders[col] = le
        print(f"  {col}: {list(le.classes_)}")

    # Target encoding
    target_le = LabelEncoder()
    df['Meal_Plan_enc'] = target_le.fit_transform(df['Recommended_Meal_Plan'])
    print(f"\n  Target classes: {list(target_le.classes_)}")

    # --- Define Features ---
    FEATURE_COLS = [
        'Age', 'Gender_enc', 'Height_cm', 'Weight_kg', 'BMI', 'BMI_Category_enc',
        'Chronic_Disease_enc', 'Blood_Pressure_Systolic', 'Blood_Pressure_Diastolic',
        'BP_Category_enc', 'Cholesterol_Level', 'Blood_Sugar_Level',
        'Genetic_Risk_Factor_enc', 'Allergies_enc', 'Daily_Steps', 'Exercise_Frequency',
        'Sleep_Hours', 'Alcohol_Consumption_enc', 'Smoking_Habit_enc', 'Dietary_Habits_enc',
        'Caloric_Intake', 'Protein_Intake', 'Carbohydrate_Intake', 'Fat_Intake',
        'Preferred_Cuisine_enc', 'Food_Aversions_enc', 'Activity_Score'
    ]

    X = df[FEATURE_COLS].values
    y_clf = df['Meal_Plan_enc'].values
    y_reg = df[['Recommended_Calories', 'Recommended_Protein', 'Recommended_Carbs', 'Recommended_Fats']].values

    # --- Train/Test Split ---
    print("\n[4/6] Splitting data (80/20)...")
    X_train, X_test, y_clf_train, y_clf_test, y_reg_train, y_reg_test = train_test_split(
        X, y_clf, y_reg, test_size=0.2, random_state=42, stratify=y_clf
    )
    print(f"  Train: {len(X_train)} | Test: {len(X_test)}")

    # --- Train Classifier ---
    print("\n[5/6] Training models...")
    print("  Training Meal Plan Classifier (Random Forest)...")
    clf = RandomForestClassifier(
        n_estimators=200, max_depth=20, min_samples_split=5,
        random_state=42, n_jobs=-1
    )
    clf.fit(X_train, y_clf_train)

    y_clf_pred = clf.predict(X_test)
    acc = accuracy_score(y_clf_test, y_clf_pred)
    print(f"\n  === Classification Results ===")
    print(f"  Accuracy: {acc:.4f} ({acc*100:.1f}%)")
    print(classification_report(y_clf_test, y_clf_pred, target_names=target_le.classes_))

    # --- Train Regressor ---
    print("  Training Macronutrient Regressor (MultiOutput Random Forest)...")
    reg = MultiOutputRegressor(
        RandomForestRegressor(n_estimators=200, max_depth=20, min_samples_split=5, random_state=42, n_jobs=-1)
    )
    reg.fit(X_train, y_reg_train)

    y_reg_pred = reg.predict(X_test)
    print(f"\n  === Regression Results ===")
    macro_names = ['Calories', 'Protein', 'Carbs', 'Fats']
    for i, name in enumerate(macro_names):
        mae = mean_absolute_error(y_reg_test[:, i], y_reg_pred[:, i])
        r2 = r2_score(y_reg_test[:, i], y_reg_pred[:, i])
        print(f"  {name}: MAE={mae:.2f}, R²={r2:.4f}")

    # --- Save Models ---
    print("\n[6/6] Saving models...")
    joblib.dump(clf, 'models/meal_plan_classifier.pkl')
    joblib.dump(reg, 'models/macro_regressor.pkl')
    joblib.dump({
        'encoders': label_encoders,
        'target_encoder': target_le,
        'feature_cols': FEATURE_COLS,
        'defaults': {
            'Caloric_Intake': int(df['Caloric_Intake'].median()),
            'Protein_Intake': int(df['Protein_Intake'].median()),
            'Carbohydrate_Intake': int(df['Carbohydrate_Intake'].median()),
            'Fat_Intake': int(df['Fat_Intake'].median()),
        }
    }, 'models/label_encoders.pkl')

    print("\n  ✅ meal_plan_classifier.pkl saved")
    print("  ✅ macro_regressor.pkl saved")
    print("  ✅ label_encoders.pkl saved")
    print("\n" + "=" * 60)
    print("  Training complete! Run 'python app.py' to launch the app.")
    print("=" * 60)

if __name__ == '__main__':
    main()