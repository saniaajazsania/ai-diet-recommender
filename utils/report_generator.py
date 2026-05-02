def get_bmi_category(bmi):
    if bmi < 18.5:
        return 'Underweight', '#FF9800', '⚠️'
    elif bmi < 25:
        return 'Normal', '#4CAF50', '✅'
    elif bmi < 30:
        return 'Overweight', '#FF9800', '⚠️'
    else:
        return 'Obese', '#F44336', '🔴'


def get_bp_status(sys_val, dia_val):
    if sys_val < 120 and dia_val < 80:
        return 'Normal', '#4CAF50'
    elif sys_val < 130 and dia_val < 80:
        return 'Elevated', '#FF9800'
    elif sys_val < 140 or dia_val < 90:
        return 'High Stage 1', '#FF9800'
    else:
        return 'High Stage 2', '#F44336'


def get_sugar_status(sugar):
    if sugar < 100:
        return 'Normal', '#4CAF50'
    elif sugar < 126:
        return 'Pre-Diabetic', '#FF9800'
    else:
        return 'Diabetic Range', '#F44336'


def get_cholesterol_status(chol):
    if chol < 200:
        return 'Desirable', '#4CAF50'
    elif chol < 240:
        return 'Borderline High', '#FF9800'
    else:
        return 'High', '#F44336'


def build_report_html(name, age, gender, bmi, disease, bp_sys, bp_dia,
                      chol, sugar, genetic, allergies, steps, exercise,
                      sleep, alcohol, smoking, diet_habit, cuisine,
                      meal_plan, macros, meal_schedule, warnings, alternatives,
                      activity_score):
    """Build a complete medical nutrition report as HTML."""

    cal, prot, carbs, fats = int(macros[0]), int(macros[1]), int(macros[2]), int(macros[3])
    bmi_cat, bmi_color, bmi_icon = get_bmi_category(bmi)
    bp_status, bp_color = get_bp_status(bp_sys, bp_dia)
    sugar_status, sugar_color = get_sugar_status(sugar)
    chol_status, chol_color = get_cholesterol_status(chol)

    # Risk score calculation (0-100)
    risk = 0
    if bmi >= 30: risk += 20
    elif bmi >= 25: risk += 10
    if bp_sys >= 140 or bp_dia >= 90: risk += 20
    elif bp_sys >= 130 or bp_dia >= 80: risk += 10
    if sugar >= 126: risk += 20
    elif sugar >= 100: risk += 10
    if chol >= 240: risk += 15
    elif chol >= 200: risk += 8
    if smoking == 'Yes': risk += 15
    if alcohol == 'Yes': risk += 5
    if genetic == 'Yes': risk += 10
    risk = min(risk, 100)
    if risk <= 25:
        risk_label, risk_color = 'Low Risk', '#4CAF50'
    elif risk <= 50:
        risk_label, risk_color = 'Moderate Risk', '#FF9800'
    elif risk <= 75:
        risk_label, risk_color = 'High Risk', '#F44336'
    else:
        risk_label, risk_color = 'Very High Risk', '#B71C1C'

    # Macro progress bars
    cal_pct = min((cal / 3000) * 100, 100)
    prot_pct = min((prot / 200) * 100, 100)
    carb_pct = min((carbs / 400) * 100, 100)
    fat_pct = min((fats / 150) * 100, 100)

    # Meal schedule table rows
    meal_rows = ''
    for day in meal_schedule:
        meal_rows += f'''
        <tr>
            <td style="font-weight:600;color:#1a73e8;">{day['Day']}</td>
            <td>{day['Breakfast']}</td>
            <td>{day['Lunch']}</td>
            <td>{day['Dinner']}</td>
            <td>{day['Snack']}</td>
        </tr>'''

    # Warnings rows
    warn_rows = ''
    if warnings:
        for food, reason in warnings:
            warn_rows += f'''
            <div style="background:#fff3f3;border-left:4px solid #d32f2f;padding:10px 15px;margin:6px 0;border-radius:0 6px 6px 0;">
                <strong style="color:#d32f2f;">❌ {food}</strong>
                <p style="margin:4px 0 0 0;color:#666;font-size:13px;">{reason}</p>
            </div>'''
    else:
        warn_rows = '<p style="color:#4CAF50;font-weight:500;">✅ No specific food warnings for your profile.</p>'

    # Alternatives rows
    alt_rows = ''
    if alternatives:
        for bad, good in alternatives.items():
            alt_rows += f'''
            <div style="background:#e8f5e9;border-left:4px solid #2e7d32;padding:10px 15px;margin:6px 0;border-radius:0 6px 6px 0;">
                <span style="color:#d32f2f;text-decoration:line-through;font-weight:500;">{bad}</span>
                <span style="margin:0 8px;">→</span>
                <span style="color:#2e7d32;font-weight:600;">✅ {good}</span>
            </div>'''
    else:
        alt_rows = '<p style="color:#4CAF50;font-weight:500;">✅ Keep up your current healthy food choices!</p>'

    # Lifestyle recommendations
    lifestyle = []
    if exercise < 3:
        lifestyle.append('Increase exercise frequency to at least 3-5 days per week')
    if steps < 5000:
        lifestyle.append('Aim for 7,000-10,000 daily steps for better cardiovascular health')
    elif steps < 7500:
        lifestyle.append('Try to increase daily steps to 10,000 for optimal health')
    if sleep < 6:
        lifestyle.append('Sleep is critically low. Aim for 7-9 hours per night')
    elif sleep < 7:
        lifestyle.append('Slightly increase sleep to 7-8 hours for better recovery')
    if alcohol == 'Yes':
        lifestyle.append('Consider reducing or eliminating alcohol consumption')
    if smoking == 'Yes':
        lifestyle.append('Quit smoking — it significantly increases all health risks')
    if bmi >= 30:
        lifestyle.append('Focus on gradual weight loss (0.5-1 kg per week) through diet and exercise')
    if disease == 'Diabetes':
        lifestyle.append('Monitor blood sugar regularly. Eat at consistent times daily')
    if disease == 'Hypertension':
        lifestyle.append('Reduce sodium intake to under 2,300mg per day. Practice stress management')
    if disease == 'Heart Disease':
        lifestyle.append('Include omega-3 fatty acids (fish, walnuts). Avoid saturated and trans fats')
    if not lifestyle:
        lifestyle.append('Maintain your current healthy lifestyle habits')
        lifestyle.append('Continue regular health check-ups every 6 months')
        lifestyle.append('Stay hydrated with 8-10 glasses of water daily')

    lifestyle_html = ''
    for i, rec in enumerate(lifestyle, 1):
        lifestyle_html += f'<li style="margin:8px 0;padding-left:8px;color:#444;">{rec}</li>'

    # Allergy info
    allergy_str = ', '.join(allergies) if allergies and 'None' not in allergies else 'No known allergies'

    html = f'''
    <div style="font-family:'Segoe UI',Arial,sans-serif;max-width:900px;margin:0 auto;color:#333;">
        <!-- Header -->
        <div style="background:linear-gradient(135deg,#1a73e8,#0d47a1);color:white;padding:25px 30px;border-radius:12px 12px 0 0;">
            <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;">
                <div>
                    <h1 style="margin:0;font-size:24px;">🍎 AI Smart Diet Recommender</h1>
                    <p style="margin:5px 0 0 0;opacity:0.9;font-size:14px;">Medical Nutrition Report</p>
                </div>
                <div style="text-align:right;font-size:12px;opacity:0.85;">
                    <div>Report Date: _____________</div>
                    <div>Report ID: AIDR-{age}{bp_sys}{int(bmi)}</div>
                </div>
            </div>
        </div>

        <!-- Patient Summary Card -->
        <div style="background:white;padding:20px 25px;border:1px solid #e0e0e0;border-top:none;">
            <h2 style="margin:0 0 15px 0;font-size:17px;color:#1a73e8;border-bottom:2px solid #e8f0fe;padding-bottom:8px;">
                🩺 Patient Summary
            </h2>
            <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px;">
                <div style="background:#f8f9fa;padding:12px;border-radius:8px;">
                    <div style="font-size:11px;color:#888;text-transform:uppercase;letter-spacing:0.5px;">Patient Name</div>
                    <div style="font-weight:600;font-size:15px;margin-top:4px;">{name if name else 'Patient'}</div>
                </div>
                <div style="background:#f8f9fa;padding:12px;border-radius:8px;">
                    <div style="font-size:11px;color:#888;text-transform:uppercase;letter-spacing:0.5px;">Age / Gender</div>
                    <div style="font-weight:600;font-size:15px;margin-top:4px;">{age} years / {gender}</div>
                </div>
                <div style="background:#f8f9fa;padding:12px;border-radius:8px;">
                    <div style="font-size:11px;color:#888;text-transform:uppercase;letter-spacing:0.5px;">BMI</div>
                    <div style="font-weight:600;font-size:15px;margin-top:4px;color:{bmi_color};">{bmi_icon} {bmi:.1f} ({bmi_cat})</div>
                </div>
                <div style="background:#f8f9fa;padding:12px;border-radius:8px;">
                    <div style="font-size:11px;color:#888;text-transform:uppercase;letter-spacing:0.5px;">Chronic Disease</div>
                    <div style="font-weight:600;font-size:15px;margin-top:4px;">{disease if disease != 'None' else 'None Detected'}</div>
                </div>
                <div style="background:#f8f9fa;padding:12px;border-radius:8px;">
                    <div style="font-size:11px;color:#888;text-transform:uppercase;letter-spacing:0.5px;">Allergies</div>
                    <div style="font-weight:600;font-size:15px;margin-top:4px;">{allergy_str}</div>
                </div>
                <div style="background:#f8f9fa;padding:12px;border-radius:8px;">
                    <div style="font-size:11px;color:#888;text-transform:uppercase;letter-spacing:0.5px;">Dietary Habit</div>
                    <div style="font-weight:600;font-size:15px;margin-top:4px;">{diet_habit}</div>
                </div>
            </div>
        </div>

        <!-- Vitals Summary -->
        <div style="background:white;padding:20px 25px;border:1px solid #e0e0e0;border-top:none;">
            <h2 style="margin:0 0 15px 0;font-size:17px;color:#1a73e8;border-bottom:2px solid #e8f0fe;padding-bottom:8px;">
                💓 Vital Signs Summary
            </h2>
            <table style="width:100%;border-collapse:collapse;">
                <thead>
                    <tr style="background:#f8f9fa;">
                        <th style="padding:10px 15px;text-align:left;border-bottom:2px solid #e0e0e0;font-size:13px;">Vital</th>
                        <th style="padding:10px 15px;text-align:center;border-bottom:2px solid #e0e0e0;font-size:13px;">Your Value</th>
                        <th style="padding:10px 15px;text-align:center;border-bottom:2px solid #e0e0e0;font-size:13px;">Normal Range</th>
                        <th style="padding:10px 15px;text-align:center;border-bottom:2px solid #e0e0e0;font-size:13px;">Status</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="padding:10px 15px;border-bottom:1px solid #f0f0f0;font-weight:500;">Blood Pressure</td>
                        <td style="padding:10px 15px;text-align:center;border-bottom:1px solid #f0f0f0;">{bp_sys}/{bp_dia} mmHg</td>
                        <td style="padding:10px 15px;text-align:center;border-bottom:1px solid #f0f0f0;color:#888;">&lt;120/80</td>
                        <td style="padding:10px 15px;text-align:center;border-bottom:1px solid #f0f0f0;"><span style="background:{bp_color}15;color:{bp_color};padding:3px 12px;border-radius:12px;font-size:12px;font-weight:600;">{bp_status}</span></td>
                    </tr>
                    <tr>
                        <td style="padding:10px 15px;border-bottom:1px solid #f0f0f0;font-weight:500;">Blood Sugar (Fasting)</td>
                        <td style="padding:10px 15px;text-align:center;border-bottom:1px solid #f0f0f0;">{sugar} mg/dL</td>
                        <td style="padding:10px 15px;text-align:center;border-bottom:1px solid #f0f0f0;color:#888;">70-100</td>
                        <td style="padding:10px 15px;text-align:center;border-bottom:1px solid #f0f0f0;"><span style="background:{sugar_color}15;color:{sugar_color};padding:3px 12px;border-radius:12px;font-size:12px;font-weight:600;">{sugar_status}</span></td>
                    </tr>
                    <tr>
                        <td style="padding:10px 15px;border-bottom:1px solid #f0f0f0;font-weight:500;">Cholesterol Level</td>
                        <td style="padding:10px 15px;text-align:center;border-bottom:1px solid #f0f0f0;">{chol} mg/dL</td>
                        <td style="padding:10px 15px;text-align:center;border-bottom:1px solid #f0f0f0;color:#888;">&lt;200</td>
                        <td style="padding:10px 15px;text-align:center;border-bottom:1px solid #f0f0f0;"><span style="background:{chol_color}15;color:{chol_color};padding:3px 12px;border-radius:12px;font-size:12px;font-weight:600;">{chol_status}</span></td>
                    </tr>
                    <tr>
                        <td style="padding:10px 15px;font-weight:500;">Activity Score</td>
                        <td style="padding:10px 15px;text-align:center;">{activity_score:.1f}</td>
                        <td style="padding:10px 15px;text-align:center;color:#888;">&gt;10.0</td>
                        <td style="padding:10px 15px;text-align:center;"><span style="background:{'#4CAF50' if activity_score >= 10 else '#FF9800'}15;color:{'#4CAF50' if activity_score >= 10 else '#FF9800'};padding:3px 12px;border-radius:12px;font-size:12px;font-weight:600;">{'Active' if activity_score >= 10 else 'Needs Improvement'}</span></td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Meal Plan Recommendation -->
        <div style="background:white;padding:20px 25px;border:1px solid #e0e0e0;border-top:none;">
            <h2 style="margin:0 0 15px 0;font-size:17px;color:#1a73e8;border-bottom:2px solid #e8f0fe;padding-bottom:8px;">
                🍽️ Recommended Meal Plan
            </h2>
            <div style="background:linear-gradient(135deg,#e8f0fe,#f3e8fd);padding:18px;border-radius:10px;margin-bottom:12px;">
                <span style="font-size:28px;font-weight:700;color:#1a73e8;">{meal_plan}</span>
            </div>
            <div style="color:#555;font-size:14px;line-height:1.6;" id="justification">
                {get_meal_plan_justification(meal_plan, disease, bmi, diet_habit)}
            </div>
        </div>

        <!-- Macronutrient Targets -->
        <div style="background:white;padding:20px 25px;border:1px solid #e0e0e0;border-top:none;">
            <h2 style="margin:0 0 15px 0;font-size:17px;color:#1a73e8;border-bottom:2px solid #e8f0fe;padding-bottom:8px;">
                📊 Daily Macronutrient Targets
            </h2>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:15px;">
                <div>
                    <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
                        <span style="font-weight:600;font-size:14px;">Calories</span>
                        <span style="font-weight:700;color:#1a73e8;">{cal} kcal</span>
                    </div>
                    <div style="background:#e0e0e0;border-radius:10px;height:18px;overflow:hidden;">
                        <div style="height:100%;width:{cal_pct}%;background:linear-gradient(90deg,#1a73e8,#42a5f5);border-radius:10px;transition:width 0.5s;"></div>
                    </div>
                </div>
                <div>
                    <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
                        <span style="font-weight:600;font-size:14px;">Protein</span>
                        <span style="font-weight:700;color:#2e7d32;">{prot}g</span>
                    </div>
                    <div style="background:#e0e0e0;border-radius:10px;height:18px;overflow:hidden;">
                        <div style="height:100%;width:{prot_pct}%;background:linear-gradient(90deg,#2e7d32,#66bb6a);border-radius:10px;transition:width 0.5s;"></div>
                    </div>
                </div>
                <div>
                    <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
                        <span style="font-weight:600;font-size:14px;">Carbohydrates</span>
                        <span style="font-weight:700;color:#e65100;">{carbs}g</span>
                    </div>
                    <div style="background:#e0e0e0;border-radius:10px;height:18px;overflow:hidden;">
                        <div style="height:100%;width:{carb_pct}%;background:linear-gradient(90deg,#e65100,#ff9800);border-radius:10px;transition:width 0.5s;"></div>
                    </div>
                </div>
                <div>
                    <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
                        <span style="font-weight:600;font-size:14px;">Fats</span>
                        <span style="font-weight:700;color:#c62828;">{fats}g</span>
                    </div>
                    <div style="background:#e0e0e0;border-radius:10px;height:18px;overflow:hidden;">
                        <div style="height:100%;width:{fat_pct}%;background:linear-gradient(90deg,#c62828,#ef5350);border-radius:10px;transition:width 0.5s;"></div>
                    </div>
                </div>
            </div>
        </div>

        <!-- 7-Day Meal Schedule -->
        <div style="background:white;padding:20px 25px;border:1px solid #e0e0e0;border-top:none;">
            <h2 style="margin:0 0 15px 0;font-size:17px;color:#1a73e8;border-bottom:2px solid #e8f0fe;padding-bottom:8px;">
                📅 7-Day Meal Schedule ({cuisine} Cuisine)
            </h2>
            <div style="overflow-x:auto;">
                <table style="width:100%;border-collapse:collapse;font-size:13px;">
                    <thead>
                        <tr style="background:#1a73e8;color:white;">
                            <th style="padding:10px;text-align:left;">Day</th>
                            <th style="padding:10px;text-align:left;">Breakfast</th>
                            <th style="padding:10px;text-align:left;">Lunch</th>
                            <th style="padding:10px;text-align:left;">Dinner</th>
                            <th style="padding:10px;text-align:left;">Snack</th>
                        </tr>
                    </thead>
                    <tbody>
                        {meal_rows}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Foods to Avoid -->
        <div style="background:white;padding:20px 25px;border:1px solid #e0e0e0;border-top:none;">
            <h2 style="margin:0 0 15px 0;font-size:17px;color:#d32f2f;border-bottom:2px solid #ffcdd2;padding-bottom:8px;">
                ⚠️ Foods to Avoid
            </h2>
            {warn_rows}
        </div>

        <!-- Healthy Alternatives -->
        <div style="background:white;padding:20px 25px;border:1px solid #e0e0e0;border-top:none;">
            <h2 style="margin:0 0 15px 0;font-size:17px;color:#2e7d32;border-bottom:2px solid #c8e6c9;padding-bottom:8px;">
                💡 Healthy Food Alternatives
            </h2>
            {alt_rows}
        </div>

        <!-- Lifestyle Recommendations -->
        <div style="background:white;padding:20px 25px;border:1px solid #e0e0e0;border-top:none;">
            <h2 style="margin:0 0 15px 0;font-size:17px;color:#1a73e8;border-bottom:2px solid #e8f0fe;padding-bottom:8px;">
                🏃 Lifestyle Recommendations
            </h2>
            <ul style="padding-left:20px;margin:0;">
                {lifestyle_html}
            </ul>
        </div>

        <!-- Risk Score -->
        <div style="background:white;padding:20px 25px;border:1px solid #e0e0e0;border-top:none;">
            <h2 style="margin:0 0 15px 0;font-size:17px;color:#1a73e8;border-bottom:2px solid #e8f0fe;padding-bottom:8px;">
                🎯 Overall Health Risk Score
            </h2>
            <div style="text-align:center;padding:20px;">
                <div style="position:relative;width:150px;height:150px;margin:0 auto;">
                    <svg width="150" height="150" viewBox="0 0 150 150">
                        <circle cx="75" cy="75" r="65" fill="none" stroke="#e0e0e0" stroke-width="12"/>
                        <circle cx="75" cy="75" r="65" fill="none" stroke="{risk_color}" stroke-width="12"
                            stroke-dasharray="{risk * 4.08} 408" stroke-linecap="round"
                            transform="rotate(-90 75 75)" style="transition:stroke-dasharray 1s;"/>
                    </svg>
                    <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);text-align:center;">
                        <div style="font-size:32px;font-weight:700;color:{risk_color};">{risk}</div>
                        <div style="font-size:10px;color:#888;">/100</div>
                    </div>
                </div>
                <div style="margin-top:12px;">
                    <span style="background:{risk_color}15;color:{risk_color};padding:6px 20px;border-radius:20px;font-size:15px;font-weight:700;">
                        {risk_label}
                    </span>
                </div>
            </div>
        </div>

        <!-- Disclaimer -->
        <div style="background:#fff8e1;padding:15px 20px;border:1px solid #ffe082;border-top:none;border-radius:0 0 12px 12px;">
            <p style="margin:0;font-size:12px;color:#f57f17;font-weight:600;">⚠️ DISCLAIMER</p>
            <p style="margin:5px 0 0 0;font-size:11px;color:#666;">
                This report is AI-generated and is intended for educational and academic purposes only.
                It does not constitute professional medical advice, diagnosis, or treatment.
                Always consult a licensed nutritionist, dietitian, or physician before making any changes to your diet or health regimen.
                Individual results may vary. The AI model has limitations and may not account for all medical factors.
            </p>
        </div>
    </div>'''

    return html


def get_meal_plan_justification(meal_plan, disease, bmi, diet_habit):
    justifications = {
        'Balanced Diet': (
            'A Balanced Diet provides a well-rounded mix of macronutrients — proteins, carbohydrates, and fats — '
            'in proportions that support overall health. This plan is recommended as it ensures adequate energy, '
            'vitamin, and mineral intake while maintaining a healthy weight.'
        ),
        'High-Protein Diet': (
            'A High-Protein Diet emphasizes increased protein intake to support muscle preservation, metabolic health, '
            'and satiety. This approach helps maintain lean body mass while managing weight. '
            'Protein sources include lean meats, fish, legumes, eggs, and dairy alternatives.'
        ),
        'Low-Carb Diet': (
            'A Low-Carb Diet reduces carbohydrate intake to help manage blood sugar levels and promote fat metabolism. '
            'By limiting refined carbs and sugars, this plan stabilizes glucose levels and reduces insulin spikes. '
            'Focus is on protein-rich foods, healthy fats, and fiber-rich vegetables.'
        ),
        'Low-Fat Diet': (
            'A Low-Fat Diet limits total and saturated fat intake to support cardiovascular health and cholesterol management. '
            'This plan emphasizes lean proteins, whole grains, fruits, and vegetables while minimizing fried foods, '
            'full-fat dairy, and processed meats.'
        ),
    }
    base = justifications.get(meal_plan, justifications['Balanced Diet'])

    disease_note = ''
    if disease == 'Diabetes':
        disease_note = ' This is particularly important for managing blood glucose levels in Diabetes.'
    elif disease == 'Hypertension':
        disease_note = ' This supports blood pressure management by reducing sodium and unhealthy fat intake.'
    elif disease == 'Heart Disease':
        disease_note = ' This helps reduce cardiovascular risk by limiting saturated fats and cholesterol.'
    elif disease == 'Obesity':
        disease_note = ' This approach supports healthy, sustainable weight management.'

    habit_note = ''
    if diet_habit == 'Vegetarian':
        habit_note = ' Plant-based protein sources have been prioritized to align with your vegetarian dietary preference.'
    elif diet_habit == 'Vegan':
        habit_note = ' All meal suggestions are fully plant-based to align with your vegan dietary preference.'
    elif diet_habit == 'Keto':
        habit_note = ' Note: Your current Keto preference has been considered alongside the medical recommendation.'

    return base + disease_note + habit_note