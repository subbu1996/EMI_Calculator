import streamlit as st
import functions as fun
import plotly.graph_objects as go

def app():
    st.title('Loan Comparison') 
    col1, col2 = st.beta_columns(2)

    with col1:
        st.subheader("Loan 1")
        principal1 = st.number_input('Principle Amount',value = 500000, step = 50000, min_value = 0, max_value = 6000000,key = 1)
        interest_rate1 = st.number_input('Annual Interest Rate',value = 10.5, step = 0.5, min_value = 0.0, max_value = 20.0,key = 1)
        m_peroid1 = st.number_input('Moratorium Period in Months',value = 0, step = 1, min_value = 0, max_value = 360,key = 1)
        st1 = st.checkbox("Click for Input in Months", key =1)
        tenure_widget1 = st.empty()
        tenure1 = tenure_widget1.slider('Tenure in Years',value = 8.0, step = 0.5,min_value= 0.5, max_value = 30.0,key =1)
        if st1:
            tenure1 = tenure_widget1.slider('Tenure in Months',value = 96, step = 1,min_value= 1, max_value = 360, key = 1)
            
        m_interest1 = round(fun.Moratorium_Interest(principal1,interest_rate1,m_peroid1,1),2)
        EMI1, EMI2_1 = fun.EMI_Calculator(principal1+m_interest1,interest_rate1,tenure1,st1)

        if st1:
            total_payment1 = EMI1*tenure1
        else:
            total_payment1= EMI1*tenure1*12

        total_interest1 = total_payment1 - principal1

        st.subheader("EMI Details: ")
        st.text("")
        st.success("Loan EMI: "+str(f"{EMI2_1:,}"))
        st.success("Total Interest: "+str(f"{round(total_interest1,2):,}"))
        st.error("Total Payment: "+str(f"{round(total_payment1):,}"))
        st.success("Moratorium Interest: "+str(f"{m_interest1:,}"))

        labels1 = ['Principal Amount','Total Interest']
        values1 = [principal1, total_interest1]
        pie_fig1 = fun.my_plotly_pie_obj("Total Payment Break-up")
        pie_fig1.add_trace(go.Pie(labels = labels1, values = values1,textinfo='label+percent'))

        st.plotly_chart(pie_fig1,use_container_width = True)

    with col2:
        st.subheader("Loan 2")
        principal2 = st.number_input('Principle Amount',value = 500000, step = 50000, min_value = 0, max_value = 6000000,key = 2)
        interest_rate2= st.number_input('Annual Interest Rate',value = 12.0, step = 0.5, min_value = 0.0, max_value = 20.0,key = 2)
        m_peroid2 = st.number_input('Moratorium Period in Months',value = 0, step = 1, min_value = 0, max_value = 360,key = 2)
        st2 = st.checkbox("Click for Input in Months",key = 2)
        tenure_widget2 = st.empty()
        tenure2 = tenure_widget2.slider('Tenure in Years',value = 6.0, step = 0.5,min_value= 0.5, max_value = 30.0,key =2)
        if st1:
            tenure2 = tenure_widget2.slider('Tenure in Months',value = 96, step = 1,min_value= 1, max_value = 360, key = 2)
            
        m_interest2 = round(fun.Moratorium_Interest(principal2,interest_rate2,m_peroid2,1),2)
        EMI2, EMI2_2 = fun.EMI_Calculator(principal2+m_interest2,interest_rate2,tenure2,st2)

        if st1:
            total_payment2 = EMI2*tenure2
        else:
            total_payment2= EMI2*tenure2*12

        total_interest2 = total_payment2 - principal2

        st.subheader("EMI Details: ")
        st.text("")
        st.success("Loan EMI: "+str(f"{EMI2_2:,}"))
        st.success("Total Interest: "+str(f"{round(total_interest2,2):,}"))
        st.error("Total Payment: "+str(f"{round(total_payment2):,}"))
        st.success("Moratorium Interest: "+str(f"{m_interest2:,}"))

        labels2 = ['Principal Amount','Total Interest']
        values2 = [principal2, total_interest2]
        pie_fig2 = fun.my_plotly_pie_obj("Total Payment Break-up")
        pie_fig2.add_trace(go.Pie(labels = labels2, values = values2,textinfo='label+percent'))

        st.plotly_chart(pie_fig2,use_container_width = True)
    
    