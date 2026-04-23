import streamlit as st
import pickle as pkl

final_model = pkl.load(open('model.pkl', 'rb'))

d1={'Comprehensive':0,'Third Party insurance':1,'Third Party':1,'Zero Dep':2,'Not Available':3}
d2={'Petrol':0,'Diesel':1,'CNG':2}
d3={'First Owner':1,'Second Owner':2,'Third Owner':3,'Forth Owner':4,'Fifth Owner':5}
d4={'Manual':0,'Automatic':1}

st.title('Car Price Prediction App')
st.markdown("Enter the car details below to estimate the price.")
val1 = st.selectbox('Insurance Validity', options=list(d1.keys()))
val2 = st.radio('Fuel Type', options=list(d2.keys()), horizontal=True)
# val3 = st.number_input('KMs Driven', min_value=0, step=100)
val3 = st.slider('KMs Driven', min_value=0, max_value=200000, value=15000, step=500)
val4 = st.selectbox('Ownership', options=list(d3.keys()))
val5 = st.radio('Transmission', options=list(d4.keys()), horizontal=True)

if st.button('Predict'):
    test = [[d1[val1], d2[val2], val3, d3[val4], d4[val5]]]
    yp = int(final_model.predict(test)[0])
    st.success('Predicted Car price is {} Rs.'.format(yp))
    