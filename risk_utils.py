import streamlit as st
from fpdf import FPDF
from datetime import datetime
from typing import Tuple, List


def calculate_risk(
    age: int,
    bmi: float,
    bp: int,
    cholesterol: int,
    glucose: int,
    smoking: str = "Non-smoker"
) -> Tuple[str, str, float, List[str]]:
    """
    Calculate comprehensive health risk based on multiple factors.
    
    Args:
        age: Age in years
        bmi: Body Mass Index
        bp: Systolic blood pressure (mmHg)
        cholesterol: Total cholesterol (mg/dL)
        glucose: Fasting glucose (mg/dL)
        smoking: Smoking status
        
    Returns:
        Tuple of (risk_level, color, risk_score, recommendations)
    """
    risk_score = 0.0
    recommendations = []
    
    # BMI Risk Assessment
    if bmi < 18.5:
        risk_score += 1.0
        recommendations.append("Your BMI is below normal. Consider consulting a nutritionist to reach a healthy weight.")
    elif 18.5 <= bmi < 25:
        recommendations.append("Your BMI is in the healthy range. Maintain your current lifestyle!")
    elif 25 <= bmi < 30:
        risk_score += 1.5
        recommendations.append("Your BMI indicates overweight. Regular exercise and balanced diet can help reduce health risks.")
    elif 30 <= bmi < 35:
        risk_score += 2.5
        recommendations.append("Your BMI indicates obesity (Class I). Consult a healthcare provider for a weight management plan.")
    else:
        risk_score += 3.5
        recommendations.append("Your BMI indicates severe obesity. Medical supervision is strongly recommended for weight management.")
    
    # Blood Pressure Assessment
    if bp < 90:
        risk_score += 1.0
        recommendations.append("Your blood pressure is low. Monitor for symptoms of hypotension and consult a doctor if concerned.")
    elif 90 <= bp < 120:
        recommendations.append("Your blood pressure is optimal. Keep up the good work!")
    elif 120 <= bp < 130:
        risk_score += 0.5
        recommendations.append("Your blood pressure is elevated. Lifestyle modifications may help prevent hypertension.")
    elif 130 <= bp < 140:
        risk_score += 1.5
        recommendations.append("Your blood pressure indicates Stage 1 hypertension. Consult your doctor about management strategies.")
    elif 140 <= bp < 180:
        risk_score += 2.5
        recommendations.append("Your blood pressure indicates Stage 2 hypertension. Medical treatment is likely needed.")
    else:
        risk_score += 4.0
        recommendations.append("Your blood pressure is dangerously high. Seek immediate medical attention!")
    
    # Cholesterol Assessment
    if cholesterol < 200:
        recommendations.append("Your cholesterol level is desirable. Continue heart-healthy habits!")
    elif 200 <= cholesterol < 240:
        risk_score += 1.5
        recommendations.append("Your cholesterol is borderline high. Consider dietary changes to reduce cardiovascular risk.")
    else:
        risk_score += 2.5
        recommendations.append("Your cholesterol is high. Consult your doctor about medication and lifestyle changes.")
    
    # Glucose Assessment
    if glucose < 70:
        risk_score += 1.0
        recommendations.append("Your glucose level is low. Monitor for hypoglycemia symptoms and consult your doctor.")
    elif 70 <= glucose < 100:
        recommendations.append("Your fasting glucose is normal. Maintain a balanced diet!")
    elif 100 <= glucose < 126:
        risk_score += 1.5
        recommendations.append("Your glucose indicates prediabetes. Lifestyle changes can prevent type 2 diabetes.")
    else:
        risk_score += 3.0
        recommendations.append("Your glucose level suggests diabetes. Consult your doctor for proper diagnosis and management.")
    
    # Age Factor
    if age < 30:
        pass  # Low risk
    elif 30 <= age < 45:
        risk_score += 0.3
    elif 45 <= age < 60:
        risk_score += 0.8
        recommendations.append("Age is a risk factor. Regular health screenings become increasingly important.")
    else:
        risk_score += 1.2
        recommendations.append("At your age, regular medical check-ups and monitoring are essential.")
    
    # Smoking Factor
    if smoking == "Current smoker":
        risk_score += 2.0
        recommendations.append("Smoking significantly increases health risks. Consider a smoking cessation program.")
    elif smoking == "Former smoker":
        risk_score += 0.5
        recommendations.append("Great job quitting smoking! Continue to avoid tobacco products.")
    else:
        recommendations.append("Excellent! Staying smoke-free is one of the best health decisions.")
    
    # General recommendations
    recommendations.append("Engage in at least 150 minutes of moderate aerobic activity per week.")
    recommendations.append("Stay hydrated and maintain a balanced diet rich in fruits, vegetables, and whole grains.")
    recommendations.append("Get 7-9 hours of quality sleep each night.")
    recommendations.append("Manage stress through relaxation techniques, meditation, or hobbies.")
    recommendations.append("Schedule regular check-ups with your healthcare provider.")
    
    # Determine risk level and color
    if risk_score >= 7:
        risk_level = "High Risk"
        color = "#E74C3C"
    elif risk_score >= 4:
        risk_level = "Moderate Risk"
        color = "#F39C12"
    elif risk_score >= 2:
        risk_level = "Low-Moderate Risk"
        color = "#F9A825"
    else:
        risk_level = "Low Risk"
        color = "#27AE60"
    
    return risk_level, color, risk_score, recommendations


def generate_pdf(
    risk: str,
    score: float,
    age: int,
    bmi: float,
    bp: int,
    cholesterol: int,
    glucose: int,
    recommendations: List[str]
) -> bytes:
    """
    Generate a professional PDF report for risk assessment.
    
    Args:
        risk: Risk level string
        score: Numeric risk score
        age: Patient age
        bmi: Body Mass Index
        bp: Blood pressure
        cholesterol: Cholesterol level
        glucose: Glucose level
        recommendations: List of recommendations
        
    Returns:
        PDF file as bytes
    """
    try:
        pdf = FPDF()
        pdf.add_page()
        
        # Title
        pdf.set_font("Arial", 'B', 20)
        pdf.set_text_color(44, 62, 80)
        pdf.cell(0, 15, "Health Risk Assessment Report", ln=True, align='C')
        
        # Date
        pdf.set_font("Arial", 'I', 10)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 8, f"Generated: {datetime.now().strftime('%B %d, %Y at %H:%M')}", ln=True, align='C')
        
        pdf.ln(10)
        
        # Risk Summary Box
        pdf.set_font("Arial", 'B', 14)
        pdf.set_text_color(44, 62, 80)
        pdf.cell(0, 10, "Risk Assessment Summary", ln=True)
        
        pdf.set_line_width(0.5)
        pdf.set_draw_color(74, 144, 226)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        
        # Risk Level
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(60, 8, "Risk Level:", 0)
        pdf.set_font("Arial", '', 12)
        
        # Color code the risk
        if "High" in risk:
            pdf.set_text_color(231, 76, 60)
        elif "Moderate" in risk:
            pdf.set_text_color(243, 156, 18)
        else:
            pdf.set_text_color(39, 174, 96)
        
        pdf.cell(0, 8, risk, ln=True)
        
        pdf.set_text_color(44, 62, 80)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(60, 8, "Risk Score:", 0)
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 8, f"{score:.2f} / 10", ln=True)
        
        pdf.ln(10)
        
        # Health Metrics
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Your Health Metrics", ln=True)
        
        pdf.set_line_width(0.5)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        
        # Metrics table
        metrics = [
            ("Age", f"{age} years"),
            ("Body Mass Index (BMI)", f"{bmi:.1f} kg/m²"),
            ("Blood Pressure (Systolic)", f"{bp} mmHg"),
            ("Total Cholesterol", f"{cholesterol} mg/dL"),
            ("Fasting Glucose", f"{glucose} mg/dL")
        ]
        
        pdf.set_font("Arial", '', 11)
        for metric, value in metrics:
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(80, 7, metric + ":", 0)
            pdf.set_font("Arial", '', 11)
            pdf.cell(0, 7, value, ln=True)
        
        pdf.ln(10)
        
        # Recommendations
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Personalized Recommendations", ln=True)
        
        pdf.set_line_width(0.5)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        
        pdf.set_font("Arial", '', 10)
        for i, rec in enumerate(recommendations[:10], 1):  # Limit to 10 recommendations for space
            pdf.multi_cell(0, 6, f"{i}. {rec}")
            pdf.ln(2)
        
        # Disclaimer
        pdf.ln(10)
        pdf.set_font("Arial", 'BI', 8)
        pdf.set_text_color(100, 100, 100)
        pdf.multi_cell(0, 4, 
            "DISCLAIMER: This report is generated for educational and informational purposes only. "
            "It is NOT intended to be a substitute for professional medical advice, diagnosis, or treatment. "
            "Always seek the advice of your physician or other qualified health provider with any questions "
            "you may have regarding a medical condition. Never disregard professional medical advice or "
            "delay in seeking it because of something you have read in this report."
        )
        
        # Footer
        pdf.ln(5)
        pdf.set_font("Arial", 'I', 8)
        pdf.set_text_color(150, 150, 150)
        pdf.cell(0, 5, "Designed by smartcare healt care analysis", 0, 0, 'C')
        
        return pdf.output(dest='S').encode('latin-1')
        
    except Exception as e:
        st.error(f"Error generating PDF: {str(e)}")
        return b""


def get_risk_interpretation(risk_level: str) -> str:
    """
    Get detailed interpretation of risk level.
    
    Args:
        risk_level: The calculated risk level
        
    Returns:
        Detailed interpretation string
    """
    interpretations = {
        "Low Risk": "Your current health metrics indicate a low risk profile. Continue maintaining healthy lifestyle habits and regular check-ups.",
        "Low-Moderate Risk": "Your health metrics show some areas that could benefit from attention. Minor lifestyle modifications may help reduce your risk further.",
        "Moderate Risk": "Your health metrics indicate moderate risk factors. It's important to address these through lifestyle changes and possibly medical consultation.",
        "High Risk": "Your health metrics indicate significant risk factors. We strongly recommend consulting with a healthcare professional for a comprehensive evaluation and treatment plan."
    }
    
    return interpretations.get(risk_level, "Please consult a healthcare professional for interpretation.")


def calculate_bmi_category(bmi: float) -> str:
    """
    Categorize BMI into standard categories.
    
    Args:
        bmi: Body Mass Index value
        
    Returns:
        BMI category string
    """
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal Weight"
    elif 25 <= bmi < 30:
        return "Overweight"
    elif 30 <= bmi < 35:
        return "Obese (Class I)"
    elif 35 <= bmi < 40:
        return "Obese (Class II)"
    else:
        return "Obese (Class III)"


def calculate_bp_category(bp: int) -> str:
    """
    Categorize blood pressure into standard categories.
    
    Args:
        bp: Systolic blood pressure
        
    Returns:
        BP category string
    """
    if bp < 90:
        return "Low"
    elif bp < 120:
        return "Normal"
    elif bp < 130:
        return "Elevated"
    elif bp < 140:
        return "High (Stage 1)"
    elif bp < 180:
        return "High (Stage 2)"
    else:
        return "Hypertensive Crisis"


def calculate_cholesterol_category(cholesterol: int) -> str:
    """
    Categorize cholesterol into standard categories.
    
    Args:
        cholesterol: Total cholesterol level
        
    Returns:
        Cholesterol category string
    """
    if cholesterol < 200:
        return "Desirable"
    elif cholesterol < 240:
        return "Borderline High"
    else:
        return "High"


def calculate_glucose_category(glucose: int) -> str:
    """
    Categorize glucose into standard categories.
    
    Args:
        glucose: Fasting glucose level
        
    Returns:
        Glucose category string
    """
    if glucose < 70:
        return "Low"
    elif glucose < 100:
        return "Normal"
    elif glucose < 126:
        return "Prediabetes"
    else:
        return "Diabetes Range"