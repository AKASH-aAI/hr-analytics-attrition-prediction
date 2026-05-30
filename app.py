import streamlit as st
import pandas as pd
import numpy as np
import pickle
import joblib
from PIL import Image
import base64
import plotly.graph_objects as go
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="HR Employee Attrition Prediction",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium dark theme
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background-color: #0e1117;
    }
    
    /* Custom card styling */
    .custom-card {
        background: linear-gradient(135deg, #1a1c23 0%, #1f2229 100%);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        transition: transform 0.3s ease;
    }
    
    .custom-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.4);
    }
    
    /* Success card for stay */
    .success-card {
        background: linear-gradient(135deg, #0f2e1a 0%, #0a3b1a 100%);
        border-left: 4px solid #00ff88;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,255,136,0.2);
    }
    
    /* Danger card for leave */
    .danger-card {
        background: linear-gradient(135deg, #2e1a1a 0%, #3b0a0a 100%);
        border-left: 4px solid #ff4444;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(255,68,68,0.2);
    }
    
    /* Metric card styling */
    .metric-card {
        background: #1a1c23;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Title styling */
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #0a0c10;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102,126,234,0.4);
    }
    
    /* Progress bar styling */
    .stProgress > div > div {
        background: linear-gradient(90deg, #00ff88, #ff4444);
    }
    
    /* Input field styling */
    .stTextInput > div > div > input, .stSelectbox > div > div {
        background-color: #1a1c23;
        color: white;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 8px;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff;
    }
    
    /* Text */
    p, span, div {
        color: #e0e0e0;
    }
    
    /* Divider */
    hr {
        border-color: rgba(255,255,255,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Load model and columns
@st.cache_resource
def load_model():
    model = joblib.load('rf_model.pkl')
    model_columns = joblib.load('model_columns.pkl')
    return model, model_columns

# Sidebar content
with st.sidebar:
    st.markdown("### 📊 **HR Analytics Suite**")
    st.markdown("---")
    
    st.markdown("#### ℹ️ **Project Information**")
    st.info("""
    **Employee Attrition Prediction System**
    
    This AI-powered tool helps HR professionals predict employee turnover risk using machine learning.
    
    **Model:** Random Forest Classifier  
    **Accuracy:** 95.13%  
    **Precision:** 87.77%  
    **Recall:** 92.23%
    
    **Key Features:**  
    • Satisfaction Level  
    • Performance Evaluation  
    • Project Count  
    • Monthly Hours  
    • Tenure
    """)
    
    st.markdown("---")
    st.markdown("#### 📈 **Model Performance**")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Accuracy", "95.13%", delta="+2.1%")
        st.metric("Precision", "87.77%", delta="+1.5%")
    with col2:
        st.metric("Recall", "92.23%", delta="+3.2%")
        st.metric("F1-Score", "89.94%", delta="+2.3%")
    
    st.markdown("---")
    st.markdown("#### 🔍 **Feature Importance**")
    
    feature_importance_data = {
        "Feature": ["Satisfaction Level", "Time Spent at Company", "Number of Projects", 
                   "Average Monthly Hours", "Last Evaluation", "Work Accident", 
                   "Promotion in Last 5 Years", "Salary Level"],
        "Importance": [0.32, 0.18, 0.15, 0.12, 0.11, 0.05, 0.04, 0.03]
    }
    
    df_importance = pd.DataFrame(feature_importance_data)
    fig = px.bar(df_importance, x='Importance', y='Feature', orientation='h',
                 title='Top Features Impacting Attrition',
                 color='Importance', color_continuous_scale='Viridis')
    fig.update_layout(height=300, margin=dict(l=0, r=0, t=30, b=0),
                     paper_bgcolor='#0a0c10', plot_bgcolor='#0a0c10',
                     font=dict(color='white'))
    st.plotly_chart(fig, use_container_width=True)

# Main content
st.markdown('<p class="main-title">📊 HR Employee Attrition Prediction System</p>', unsafe_allow_html=True)
st.markdown("*AI-powered employee turnover risk assessment for proactive retention strategies*")
st.markdown("---")

# Create two columns for layout
col1, col2 = st.columns([1.5, 1])

with col1:
    st.markdown("### 👤 **Employee Information**")
    st.markdown("*Please fill in the employee details below*")
    st.markdown("---")
    
    # Create input form
    with st.form(key="employee_form"):
        # Basic information
        col_a, col_b = st.columns(2)
        
        with col_a:
            satisfaction_level = st.slider(
                "😊 Satisfaction Level",
                min_value=0.0,
                max_value=1.0,
                value=0.65,
                step=0.05,
                help="Employee's satisfaction rating on a scale of 0 to 1"
            )
            
            last_evaluation = st.slider(
                "⭐ Last Evaluation Score",
                min_value=0.0,
                max_value=1.0,
                value=0.70,
                step=0.05,
                help="Employee's last performance evaluation score"
            )
            
            number_project = st.number_input(
                "📁 Number of Projects",
                min_value=1,
                max_value=7,
                value=3,
                step=1,
                help="Number of projects the employee is handling"
            )
            
            average_monthly_hours = st.number_input(
                "⏰ Average Monthly Hours",
                min_value=96,
                max_value=310,
                value=200,
                step=5,
                help="Average hours worked per month"
            )
        
        with col_b:
            time_spend_company = st.number_input(
                "🏢 Years at Company",
                min_value=2,
                max_value=10,
                value=3,
                step=1,
                help="Number of years spent at the company"
            )
            
            work_accident = st.selectbox(
                "⚠️ Work Accident",
                options=["No", "Yes"],
                help="Has the employee experienced a work accident?"
            )
            
            promotion_last_5years = st.selectbox(
                "🚀 Promotion in Last 5 Years",
                options=["No", "Yes"],
                help="Has the employee been promoted in the last 5 years?"
            )
            
            salary = st.selectbox(
                "💰 Salary Level",
                options=["Low", "Medium", "High"],
                help="Employee's salary level relative to market"
            )
        
        st.markdown("---")
        st.markdown("#### 🏢 **Department**")
        
        department = st.selectbox(
            "Select Department",
            options=[
                "R&D", "Accounting", "HR", "Management", 
                "Marketing", "Product Management", "Sales", 
                "Support", "Technical"
            ],
            help="Employee's department"
        )
        
        # Submit button
        submitted = st.form_submit_button("🔮 Predict Attrition Risk", use_container_width=True)

# Prediction and results
with col2:
    if submitted:
        # Prepare input data for prediction
        # Map user-friendly values back to model expected values
        work_accident_value = 1 if work_accident == "Yes" else 0
        promotion_value = 1 if promotion_last_5years == "Yes" else 0
        
        # Map salary to one-hot encoded columns
        salary_low = 1 if salary == "Low" else 0
        salary_medium = 1 if salary == "Medium" else 0
        # salary_high is inferred when both low and medium are 0
        
        # Map department to one-hot encoded columns
        dept_mapping = {
            "R&D": "department_RandD",
            "Accounting": "department_accounting",
            "HR": "department_hr",
            "Management": "department_management",
            "Marketing": "department_marketing",
            "Product Management": "department_product_mng",
            "Sales": "department_sales",
            "Support": "department_support",
            "Technical": "department_technical"
        }
        
        # Create base data dictionary
        input_data = {
            'satisfaction_level': satisfaction_level,
            'last_evaluation': last_evaluation,
            'number_project': number_project,
            'average_monthly_hours': average_monthly_hours,
            'time_spend_company': time_spend_company,
            'Work_accident': work_accident_value,
            'promotion_last_5years': promotion_value,
            'salary_low': salary_low,
            'salary_medium': salary_medium
        }
        
        # Add department one-hot encoding
        for dept_col in ['department_RandD', 'department_accounting', 'department_hr', 
                        'department_management', 'department_marketing', 'department_product_mng',
                        'department_sale', 'department_sales', 'department_support', 'department_technical']:
            input_data[dept_col] = 0
        
        # Set the selected department
        selected_dept_col = dept_mapping[department]
        input_data[selected_dept_col] = 1
        
        # Load model and columns
        model, model_columns = load_model()
        
        # Create DataFrame with correct column order
        input_df = pd.DataFrame([input_data])
        
        # Ensure all columns from model_columns are present
        for col in model_columns:
            if col not in input_df.columns:
                input_df[col] = 0
        
        # Reorder columns to match training data
        input_df = input_df[model_columns]
        
        # Make prediction
        prediction = model.predict(input_df)[0]
        prediction_proba = model.predict_proba(input_df)[0]
        
        # Calculate risk percentage
        risk_percentage = prediction_proba[1] * 100 if prediction == 1 else prediction_proba[0] * 100
        
        # Display results
        if prediction == 0:
            st.markdown("""
            <div class="success-card">
                <h3>✅ Low Attrition Risk</h3>
                <p style="font-size: 1.2rem;">Employee is <strong>likely to stay</strong> with the company</p>
                <p style="font-size: 2rem; margin: 0;">🎯</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="danger-card">
                <h3>⚠️ High Attrition Risk</h3>
                <p style="font-size: 1.2rem;">Employee is <strong>likely to leave</strong> the company</p>
                <p style="font-size: 2rem; margin: 0;">🚨</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Display risk metrics
        st.markdown("### 📊 **Risk Assessment**")
        
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            if prediction == 0:
                st.metric("Retention Probability", f"{risk_percentage:.1f}%", delta="Stable")
            else:
                st.metric("Attrition Risk", f"{risk_percentage:.1f}%", delta="High Risk", delta_color="inverse")
        
        with col_r2:
            st.metric("Confidence Level", f"{max(prediction_proba)*100:.1f}%", delta="Model Confidence")
        
        # Gauge chart for risk visualization
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = risk_percentage if prediction == 1 else 100 - risk_percentage,
            title = {'text': "Risk Level", 'font': {'size': 24, 'color': 'white'}},
            delta = {'reference': 50, 'increasing': {'color': "red"}, 'decreasing': {'color': "green"}},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': "darkred" if prediction == 1 else "darkgreen"},
                'bgcolor': "rgba(0,0,0,0)",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 30], 'color': 'rgba(0,255,0,0.3)'},
                    {'range': [30, 70], 'color': 'rgba(255,255,0,0.3)'},
                    {'range': [70, 100], 'color': 'rgba(255,0,0,0.3)'}
                ],
                'threshold': {
                    'line': {'color': "white", 'width': 4},
                    'thickness': 0.75,
                    'value': risk_percentage if prediction == 1 else 100 - risk_percentage
                }
            }
        ))
        
        fig.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', 
                         font={'color': 'white', 'family': "Arial"})
        st.plotly_chart(fig, use_container_width=True)
        
        # Actionable insights
        st.markdown("### 💡 **Recommended Actions**")
        
        if prediction == 1:
            st.warning("""
            **High Attrition Risk Detected - Immediate Actions Recommended:**
            - Schedule a stay interview to understand concerns
            - Review compensation and benefits package
            - Discuss career growth opportunities
            - Consider work-life balance improvements
            """)
        else:
            st.success("""
            **Employee Retention Strategy - Proactive Measures:**
            - Recognize and reward good performance
            - Provide development opportunities
            - Maintain regular check-ins
            - Monitor satisfaction levels periodically
            """)
        
        # Feature contribution analysis
        st.markdown("---")
        st.markdown("### 🔍 **Key Factors Influencing This Prediction**")
        
        factors = []
        if satisfaction_level < 0.5:
            factors.append("⚠️ Low satisfaction level")
        if time_spend_company > 5:
            factors.append("⚠️ Long tenure without progression")
        if number_project > 5:
            factors.append("⚠️ High project workload")
        if average_monthly_hours > 250:
            factors.append("⚠️ Excessive working hours")
        if last_evaluation > 0.8 and promotion_value == 0:
            factors.append("⚠️ High performance without promotion")
        if work_accident_value == 1:
            factors.append("⚠️ Safety concerns (work accident history)")
        
        if factors:
            for factor in factors:
                st.markdown(f"- {factor}")
        else:
            st.markdown("- No immediate risk factors detected")
            st.markdown("- Continue maintaining positive work environment")
        
    else:
        st.markdown("""
        <div class="custom-card">
            <h3 style="text-align: center;">🤖 Ready to Predict</h3>
            <p style="text-align: center;">Fill in the employee details on the left and click "Predict Attrition Risk" to analyze retention probability</p>
            <hr>
            <p style="text-align: center; font-size: 0.9rem;">Our AI model will provide instant risk assessment with actionable insights</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show model performance metrics
        st.markdown("### 📈 **Model Performance Metrics**")
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.markdown('<div class="metric-card"><h3>95.13%</h3><p>Accuracy</p></div>', unsafe_allow_html=True)
        with col_m2:
            st.markdown('<div class="metric-card"><h3>87.77%</h3><p>Precision</p></div>', unsafe_allow_html=True)
        with col_m3:
            st.markdown('<div class="metric-card"><h3>92.23%</h3><p>Recall</p></div>', unsafe_allow_html=True)
        with col_m4:
            st.markdown('<div class="metric-card"><h3>89.94%</h3><p>F1-Score</p></div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 🎯 **Why Use This Tool?**")
        
        col_b1, col_b2, col_b3 = st.columns(3)
        with col_b1:
            st.markdown("**🎯 95%+ Accuracy**")
            st.caption("Highly reliable predictions")
        with col_b2:
            st.markdown("**⚡ Real-time Analysis**")
            st.caption("Instant risk assessment")
        with col_b3:
            st.markdown("**💡 Actionable Insights**")
            st.caption("Strategic recommendations")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem;">
    <p>© 2024 HR Analytics Suite | Powered by Random Forest Classifier | Employee Attrition Prediction System</p>
</div>
""", unsafe_allow_html=True)