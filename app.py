import streamlit as st
from eda_utils import *
from risk_utils import *
import pandas as pd

def main():
    st.set_page_config(
        page_title="Smart Healthcare Analytics",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Link to external CSS file
    st.markdown('<link rel="stylesheet" href="styles.css">', unsafe_allow_html=True)

    # Sidebar navigation with icons
    st.sidebar.markdown("# 🏥 Healthcare Analytics")
    st.sidebar.markdown("---")
    
    menu_options = {
        "🏠 Home": "home",
        "📊 Exploratory Data Analysis": "eda",
        "📈 Advanced Visualization": "visualization",
        "⚠️ Risk Assessment": "risk",
        "ℹ️ About": "about"
    }
    
    menu = st.sidebar.radio("Navigation", list(menu_options.keys()))
    selected_page = menu_options[menu]
    

    st.sidebar.markdown("---")
    st.sidebar.caption("Designed & Developed By Nakul Dhiman")

    # Route to appropriate page
    if selected_page == "home":
        show_home()
    elif selected_page == "eda":
        show_eda()
    elif selected_page == "visualization":
        show_visualization()
    elif selected_page == "risk":
        show_risk_simulation()
    elif selected_page == "about":
        show_about()


def show_home():
    st.markdown("# 🏥 Smart Healthcare Data Analysis Platform")
    st.markdown("### Empowering Healthcare Decisions with Data-Driven Insights")
    
    # Hero section
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
            <div style="background-color: #0000FF; padding: 15px; border-radius: 8px; border-left: 4px solid #0000FF;">
            <div class="custom-card">
                <p style="font-size: 18px; line-height: 1.6;">
                Welcome to the Smart Healthcare Data Analysis Platform - your comprehensive solution 
                for analyzing healthcare data and assessing health risks. This application combines 
                powerful data analytics with user-friendly interfaces to help you make informed 
                healthcare decisions.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.info("🎯 **Quick Start**\n\n1. Upload your dataset\n2. Explore the data\n3. Visualize insights\n4. Assess risk factors")
    
    st.markdown("---")
    
    # Feature cards
    st.markdown("## 🌟 Key Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="feature-card" style="background-color: #DC143C;">
                <h3>📊 Data Analysis</h3>
                <p>Comprehensive exploratory data analysis with summary statistics,
                missing value detection, and correlation analysis.</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="feature-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                <h3>📈 Visualization</h3>
                <p>Interactive charts including histograms, scatter plots, 
                boxplots, and heatmaps for deeper insights.</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="feature-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                <h3>⚠️ Risk Assessment</h3>
                <p>Simulate health risk factors based on key parameters 
                like BMI, blood pressure, and glucose levels.</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Supported analyses
    st.markdown("## 🔬 Supported Analyses")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="custom-card">
                <h3>📋 Data Insights</h3>
                <ul>
                    <li>Summary statistics and distributions</li>
                    <li>Missing value analysis</li>
                    <li>Correlation matrices</li>
                    <li>Outlier detection</li>
                    <li>Data quality reports</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="custom-card">
                <h3>🎯 Risk Factors</h3>
                <ul>
                    <li>Cardiovascular risk assessment</li>
                    <li>Diabetes risk prediction</li>
                    <li>BMI-based health evaluation</li>
                    <li>Blood pressure analysis</li>
                    <li>Cholesterol level monitoring</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Important notice
    st.warning("⚠️ **Medical Disclaimer**: This tool is for educational and informational purposes only. It is not intended to be a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.")

def show_eda():
    st.markdown("# 📊 Exploratory Data Analysis")
    st.markdown("Upload your healthcare dataset to begin comprehensive analysis")
    
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type="csv",
        help="Upload a CSV file with healthcare data"
    )
    
    if uploaded_file is not None:
        try:
            df = load_data(uploaded_file)
            
            if df is not None and not df.empty:
                # Dataset overview
                st.success(f"✅ Dataset loaded successfully! Shape: {df.shape[0]} rows × {df.shape[1]} columns")
                
                # Tabs for organized view
                tab1, tab2, tab3, tab4 = st.tabs(["📋 Preview", "📈 Statistics", "🔍 Quality", "🔗 Correlations"])
                
                with tab1:
                    st.markdown("### Data Preview")
                    st.dataframe(df.head(15), use_container_width=True)
                    
                    # Quick stats
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Rows", df.shape[0])
                    with col2:
                        st.metric("Total Columns", df.shape[1])
                    with col3:
                        st.metric("Numeric Columns", len(df.select_dtypes(include=[np.number]).columns))
                    with col4:
                        st.metric("Missing Values", df.isnull().sum().sum())
                
                with tab2:
                    show_summary_stats(df)
                
                with tab3:
                    col1, col2 = st.columns(2)
                    with col1:
                        show_missing_values(df)
                    with col2:
                        show_data_types(df)
                
                with tab4:
                    show_correlations(df)
                
                st.markdown("---")
                
                # Interactive visualizations
                st.markdown("## 📊 Interactive Visualizations")
                
                chart_type = st.selectbox(
                    "Select Visualization Type",
                    ["Histogram", "Scatter Plot", "Box Plot", "Distribution Plot"],
                    help="Choose the type of chart you want to generate"
                )
                
                if chart_type == "Histogram":
                    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
                    if numeric_columns:
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            column = st.selectbox("Select Column", numeric_columns)
                        with col2:
                            bins = st.slider("Number of Bins", 10, 100, 30)
                        show_histogram(df, column, bins)
                    else:
                        st.warning("No numeric columns available for histogram")
                
                elif chart_type == "Scatter Plot":
                    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
                    if len(numeric_columns) >= 2:
                        col1, col2 = st.columns(2)
                        with col1:
                            x_col = st.selectbox("X-Axis", numeric_columns)
                        with col2:
                            y_col = st.selectbox("Y-Axis", numeric_columns, index=1)
                        show_scatter(df, x_col, y_col)
                    else:
                        st.warning("Need at least 2 numeric columns for scatter plot")
                
                elif chart_type == "Box Plot":
                    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
                    if numeric_columns:
                        col1, col2 = st.columns(2)
                        with col1:
                            x_col = st.selectbox("Category (X-Axis)", df.columns.tolist())
                        with col2:
                            y_col = st.selectbox("Value (Y-Axis)", numeric_columns)
                        show_boxplot(df, x_col, y_col)
                    else:
                        st.warning("No numeric columns available for box plot")
                
                elif chart_type == "Distribution Plot":
                    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
                    if numeric_columns:
                        column = st.selectbox("Select Column", numeric_columns)
                        show_distribution(df, column)
                    else:
                        st.warning("No numeric columns available for distribution plot")
                        
            else:
                st.error("❌ Failed to load data or dataset is empty")
                
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")
            st.info("Please ensure your CSV file is properly formatted")
    else:
        st.info("👆 Please upload a CSV file to begin analysis")
        
        # Show sample format
        with st.expander("📄 View Sample CSV Format"):
            st.markdown("""
                Your CSV should have the following structure:
                ```
                PatientID,Age,Gender,BMI,BloodPressure,Cholesterol,Glucose,HeartDisease
                1,45,Male,28.5,130,220,110,0
                2,52,Female,32.1,145,240,130,1
                ...
                ```
            """)


def show_visualization():
    st.markdown("# 📈 Advanced Data Visualization")
    st.markdown("Create detailed visualizations to understand your healthcare data")
    
    uploaded_file = st.file_uploader(
        "Upload CSV Dataset",
        type="csv",
        key="viz_upload"
    )
    
    if uploaded_file is not None:
        try:
            df = load_data(uploaded_file)
            
            if df is not None and not df.empty:
                st.success("✅ Dataset loaded successfully!")
                
                # Create visualization dashboard
                st.markdown("## 📊 Visualization Dashboard")
                
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                
                if not numeric_cols:
                    st.warning("No numeric columns found in the dataset")
                    return
                
                # Multiple histograms side by side
                st.markdown("### 📊 Distribution Analysis")
                col1, col2 = st.columns(2)
                
                with col1:
                    hist_col1 = st.selectbox("First Distribution", numeric_cols, key="hist1")
                    if hist_col1:
                        show_histogram(df, hist_col1, 30)
                
                with col2:
                    hist_col2 = st.selectbox("Second Distribution", numeric_cols, index=min(1, len(numeric_cols)-1), key="hist2")
                    if hist_col2:
                        show_histogram(df, hist_col2, 30)
                
                st.markdown("---")
                
                # Box plots
                st.markdown("### 📦 Box Plot Analysis")
                col1, col2 = st.columns([1, 1])
                with col1:
                    box_x = st.selectbox("Category Variable", df.columns.tolist(), key="box_x")
                with col2:
                    box_y = st.selectbox("Numeric Variable", numeric_cols, key="box_y")
                
                if box_x and box_y:
                    show_boxplot(df, box_x, box_y)
                
                st.markdown("---")
                
                # Scatter plots
                st.markdown("### 🔵 Scatter Plot Analysis")
                col1, col2 = st.columns(2)
                with col1:
                    scatter_x = st.selectbox("X-Axis Variable", numeric_cols, key="scatter_x")
                with col2:
                    scatter_y = st.selectbox("Y-Axis Variable", numeric_cols, index=min(1, len(numeric_cols)-1), key="scatter_y")
                
                if scatter_x and scatter_y:
                    show_scatter(df, scatter_x, scatter_y)
                
                st.markdown("---")
                
                # Correlation heatmap
                st.markdown("### 🔥 Correlation Heatmap")
                show_correlations(df)
                
            else:
                st.error("❌ Failed to load data or dataset is empty")
                
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    else:
        st.info("👆 Upload a dataset to create visualizations")


def show_risk_simulation():
    st.markdown("# ⚠️ Health Risk Assessment Tool")
    st.markdown("Enter your health parameters to receive a personalized risk assessment")
    
    # Create a nice form layout
    with st.form("risk_form"):
        st.markdown("### 📝 Enter Your Health Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input(
                "Age (years)",
                min_value=1,
                max_value=120,
                value=30,
                help="Your current age in years"
            )
            
            bmi = st.number_input(
                "Body Mass Index (BMI)",
                min_value=10.0,
                max_value=60.0,
                value=25.0,
                step=0.1,
                help="BMI = weight(kg) / height(m)²"
            )
            
            bp = st.number_input(
                "Blood Pressure - Systolic (mmHg)",
                min_value=60,
                max_value=250,
                value=120,
                help="The top number in a blood pressure reading"
            )
        
        with col2:
            cholesterol = st.number_input(
                "Total Cholesterol (mg/dL)",
                min_value=100,
                max_value=400,
                value=200,
                help="Total cholesterol level in blood"
            )
            
            glucose = st.number_input(
                "Fasting Glucose (mg/dL)",
                min_value=50,
                max_value=300,
                value=100,
                help="Blood sugar level after fasting"
            )
            
            smoking = st.selectbox(
                "Smoking Status",
                ["Non-smoker", "Former smoker", "Current smoker"],
                help="Your smoking history"
            )
        
        submitted = st.form_submit_button("🔍 Calculate Risk Assessment", use_container_width=True)
    
    if submitted:
        with st.spinner("Analyzing your health parameters..."):
            risk, color, score, recommendations = calculate_risk(
                age, bmi, bp, cholesterol, glucose, smoking
            )
            
            st.markdown("---")
            st.markdown("## 📋 Your Risk Assessment Results")
            
            # Risk indicator
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, {color}22 0%, {color}44 100%);
                        padding: 30px;
                        border-radius: 15px;
                        text-align: center;
                        border: 3px solid {color};
                        margin: 20px 0;
                    ">
                        <h2 style="color: {color}; margin: 0;">Risk Level: {risk}</h2>
                        <p style="font-size: 18px; color: #555; margin-top: 10px;">
                            Risk Score: {score:.1f}/10
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            
            # Metrics
            st.markdown("### 📊 Your Health Metrics")
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                bmi_status = "Normal" if 18.5 <= bmi <= 24.9 else "Elevated"
                st.metric("BMI", f"{bmi:.1f}", bmi_status, delta_color="inverse")
            
            with col2:
                bp_status = "Normal" if bp < 120 else "Elevated"
                st.metric("Blood Pressure", f"{bp}", bp_status, delta_color="inverse")
            
            with col3:
                chol_status = "Normal" if cholesterol < 200 else "Elevated"
                st.metric("Cholesterol", f"{cholesterol}", chol_status, delta_color="inverse")
            
            with col4:
                gluc_status = "Normal" if glucose < 100 else "Elevated"
                st.metric("Glucose", f"{glucose}", gluc_status, delta_color="inverse")
            
            with col5:
                st.metric("Age", f"{age}", "years")
            
            # Recommendations
            st.markdown("### 💡 Personalized Recommendations")
            for i, rec in enumerate(recommendations, 1):
                st.info(f"{i}. {rec}")
            
            st.markdown("---")
            
            # Download report
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                # Generate PDF bytes immediately on form submit
                try:
                    pdf_bytes = generate_pdf(risk, score, age, bmi, bp, cholesterol, glucose, recommendations)
                    if pdf_bytes and len(pdf_bytes) > 0:
                        st.download_button(
                            label="📄 Download Detailed PDF Report",
                            data=pdf_bytes,
                            file_name=f"health_risk_report_{pd.Timestamp.now().strftime('%Y%m%d')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                    else:
                        st.error("Failed to generate PDF report.")
                except Exception as e:
                    st.error(f"Error generating PDF: {str(e)}")
            
            # Medical disclaimer
            st.warning("⚠️ **Important Medical Disclaimer**: This risk assessment is based on simplified algorithms and is for educational purposes only. It does NOT replace professional medical evaluation. Please consult with a qualified healthcare provider for accurate diagnosis and personalized medical advice.")


def show_about():
    st.markdown("# ℹ️ About This Application")
    
    st.markdown("""
        <div class="custom-card">
            <h2>🎯 Project Overview</h2>
            <p style="font-size: 16px; line-height: 1.8;">
            The Smart Healthcare Data Analysis Platform is a comprehensive tool designed to help 
            healthcare professionals, researchers, and individuals analyze health data and assess 
            various risk factors. Built with Python and Streamlit, this application provides an 
            intuitive interface for exploring healthcare datasets and understanding health metrics.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div style="background-color: #00FF7F; padding: 15px; border-radius: 8px; border-left: 4px solid #00FF7;">
                    
            <div class="custom-card">
                <h3>🛠️ Technologies Used</h3>
                <ul style="line-height: 2;">
                    <li><strong>Streamlit</strong> - Web application framework</li>
                    <li><strong>Pandas</strong> - Data manipulation</li>
                    <li><strong>NumPy</strong> - Numerical computing</li>
                    <li><strong>Matplotlib</strong> - Data visualization</li>
                    <li><strong>Seaborn</strong> - Statistical graphics</li>
                    <li><strong>FPDF</strong> - PDF report generation</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style="background-color: #008080; padding: 15px; border-radius: 8px; border-left: 4px solid #008080;">
                    
            <div class="custom-card">
                <h3>✨ Key Features</h3>
                <ul style="line-height: 2;">
                    <li>Comprehensive EDA capabilities</li>
                    <li>Interactive visualizations</li>
                    <li>Risk assessment algorithms</li>
                    <li>PDF report generation</li>
                    <li>User-friendly interface</li>
                    <li>Real-time data analysis</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
                
        <div class="custom-card">
            <h3>📊 Data Sources</h3>
            <p style="font-size: 16px;">
            This application is designed to work with healthcare datasets from various sources including:
            </p>
            <ul style="line-height: 2;">
                <li><strong>Scikit-learn</strong> - Built-in health datasets</li>
                <li><strong>Kaggle</strong> - Public healthcare datasets</li>
                <li><strong>UCI ML Repository</strong> - Medical databases</li>
                <li><strong>Custom datasets</strong> - User-uploaded CSV files</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="custom-card">
            <h3>⚠️ Important Disclaimers</h3>
            <div style="background-color: #0000FF; padding: 15px; border-radius: 8px; border-left: 4px solid #0000FF;">
                <p style="margin: 0; font-size: 15px;">
                <strong>Medical Disclaimer:</strong> This tool is provided for educational and informational 
                purposes only. It is NOT intended to be a substitute for professional medical advice, diagnosis, 
                or treatment. The risk assessments and recommendations provided are based on simplified algorithms 
                and should not be used as the sole basis for medical decisions.
                </p>
            </div>
            <br>
            <div style="background-color: #00008B; padding: 15px; border-radius: 8px; border-left: 4px solid #00008B;">
                <p style="margin: 0; font-size: 15px;">
                <strong>Data Privacy:</strong> All data processing occurs locally in your browser session. 
                No health data is stored or transmitted to external servers. However, users are responsible 
                for ensuring compliance with applicable data protection regulations (HIPAA, GDPR, etc.) when 
                using this tool with real patient data.
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <p style="font-size: 14px; color: #666;">
                Designed & Developed By Nakul Dhiman
            </p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()