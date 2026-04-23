import streamlit as st
import pickle as pkl
import numpy as np

# Load model and metadata
try:
    model = pkl.load(open('model.pkl', 'rb'))
    scaler = pkl.load(open('scaler.pkl', 'rb'))
    model_info = pkl.load(open('model_info.pkl', 'rb'))
except FileNotFoundError:
    st.error(" Model files not found.")
    st.stop()

# Encoding dictionaries
d1 = {'Comprehensive':0, 'Third Party insurance':1, 'Third Party':1, 'Zero Dep':2, 'Not Available':3}
d2 = {'Petrol':0, 'Diesel':1, 'CNG':2}
d3 = {'First Owner':1, 'Second Owner':2, 'Third Owner':3, 'Fourth Owner':4, 'Fifth Owner':5}
d4 = {'Manual':0, 'Automatic':1}

st.title('🚗 Car Price Prediction')

# Create two columns for inputs
col1, col2 = st.columns(2)

with col1:
    val1 = st.selectbox('Insurance Validity', options=list(d1.keys()))
    val2 = st.radio('Fuel Type', options=list(d2.keys()), horizontal=True)
    val3 = st.slider('KMs Driven', min_value=0, max_value=300000, value=50000, step=1000)
    val4 = st.selectbox('Ownership', options=list(d3.keys()))
    val5 = st.radio('Transmission', options=list(d4.keys()), horizontal=True)

with col2:
    val6 = st.number_input('Mileage (km/l)', min_value=5.0, max_value=30.0, value=15.0, step=0.5)
    val7 = st.number_input('Engine (cc)', min_value=500, max_value=5000, value=1500, step=50)
    val8 = st.number_input('Max Power (bhp)', min_value=50, max_value=500, value=120, step=5)
    val9 = st.number_input('Torque (Nm)', min_value=100, max_value=500, value=180, step=10)
    val10 = st.number_input('Manufacturing Year', min_value=2000, max_value=2024, value=2020, step=1)

val11 = st.number_input('Seats', min_value=2, max_value=8, value=5, step=1)

# Calculate car age
car_age = 2024 - val10

# Predict button
if st.button('🎯 Predict Price', use_container_width=True, type='primary'):
    try:
        # Prepare input data
        test_data = np.array([[
            d1[val1],
            d2[val2],
            val3,
            d3[val4],
            d4[val5],
            val6,
            val7,
            val8,
            val9,
            car_age,
            val11
        ]])
        
        # Make prediction
        predicted_price = max(model.predict(test_data)[0], 1.0)
        
        # Display results
        st.markdown("---")
        
        col_res1, col_res2, col_res3 = st.columns(3)
        with col_res1:
            st.metric("Estimated Price", f"₹{predicted_price*100000:,.0f}", f"{predicted_price:.2f} lakhs")
        with col_res2:
            lower = predicted_price * 0.90
            upper = predicted_price * 1.10
            st.metric("Price Range", f"₹{lower*100000:,.0f} - ₹{upper*100000:,.0f}")
        with col_res3:
            st.metric("Car Age", f"{car_age} years", f"Year: {val10}")
        
        
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")