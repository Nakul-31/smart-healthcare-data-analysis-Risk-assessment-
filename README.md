# smart-healthcare-data-analysis-Risk-assessment-
A powerful and interactive healthcare data analysis and risk assessment platform built using Python, Streamlit, Pandas, NumPy, and advanced data visualization libraries.
This application helps users analyze healthcare datasets, explore patterns, visualize insights, and compute personalized health risk assessments.

🚀 Features
🔹 1. Home Dashboard

Beautiful UI with feature cards and guided instructions.
(Implemented in app.py 

app

)

🔹 2. Exploratory Data Analysis (EDA)

Data preview & inspection

Summary statistics

Missing value detection

Data type summary

Correlation heatmaps
(Functions from eda_utils.py 

eda_utils

)

🔹 3. Advanced Visualizations

Histogram

Boxplot

Scatter plot

KDE distributions

Multiple side-by-side analysis blocks
(Defined in eda_utils.py)

🔹 4. Health Risk Assessment

Calculates risk based on:

BMI

Blood Pressure

Cholesterol

Glucose

Smoking status

Age
Includes:

Personalized suggestions

Risk color coding

PDF report generation
(From risk_utils.py 

risk_utils

)

🔹 5. PDF Report Generator

Exports:

Risk score

Health metrics

Personalized recommendations

Timestamp
(Implemented with FPDF)

🔹 6. Modern UI/UX

Custom styling through:

styles.css 

styles

Gradient backgrounds

Styled buttons

Metrics cards








📦 Smart-Healthcare-Analytics
│
├── app.py                 # Main Streamlit application  :contentReference[oaicite:4]{index=4}
├── eda_utils.py           # EDA helper functions        :contentReference[oaicite:5]{index=5}
├── risk_utils.py          # Risk calculation + PDF      :contentReference[oaicite:6]{index=6}
├── styles.css             # Custom UI styling           :contentReference[oaicite:7]{index=7}
├── requirements.txt       # Dependencies                :contentReference[oaicite:8]{index=8}
└── sample_healthcare_data.csv   # Example dataset





2️⃣ Install Dependencies
pip install -r requirements.txt





#Run the Application-
streamlit run app.py
