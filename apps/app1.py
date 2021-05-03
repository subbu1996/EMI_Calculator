import streamlit as st
import pandas as pd
import plotly.graph_objects as go

import functions as fun

def app():
    st.title("EMI Calculation") 

    col1, col2 = st.beta_columns(2)
    principal = col1.number_input('Principle Amount',value = 500000, step = 50000, min_value = 0, max_value = 6000000)
    interest_rate = col2.number_input('Annual Interest Rate',value = 10.5, step = 0.5, min_value = 0.0, max_value = 20.0) 

    col3, col4 = st.beta_columns(2)
    t_st = col3.checkbox('Click for Tenure Input in Months')
    m_st = col4.checkbox('Click for Moratorium Input in Months',value = True)

    tenure_widget = st.empty()
    m_widget = st.empty()
    tenure = tenure_widget.slider('Tenure in Years',value = 8.0, step = 0.5,min_value= 0.5, max_value = 30.0)
    m_peroid = m_widget.slider('Moratorium in Years (simple interest during this peroid)',value = 0.0, step = 0.5,min_value= 0.0, max_value = 5.0)
    if t_st:
        tenure = tenure_widget.slider('Tenure in Months',value = 96, step = 1,min_value= 1, max_value = 360)
    if m_st:
        m_peroid = m_widget.slider('Moratorium in Months (simple interest during this peroid)',value = 0, step = 1,min_value= 0, max_value = 60)

    m_interest = round(fun.Moratorium_Interest(principal,interest_rate,m_peroid,m_st),2)
    EMI, EMI2 = fun.EMI_Calculator(principal+m_interest,interest_rate,tenure,t_st)

    if t_st:
        total_payment = EMI*tenure
    else:
        total_payment = EMI*tenure*12

    total_interest = total_payment - principal

    b_st = st.checkbox("Click here for installment wise summary & more info")

    if not b_st:
        col5, col6 = st.beta_columns([1.5,2])
        with col5:
            st.text("")
            st.subheader("EMI Details: ")
            st.text("")
            st.success("Loan EMI: "+str(f"{EMI2:,}"))
            st.success("Total Interest: "+str(f"{round(total_interest,2):,}"))
            st.error("Total Payment: "+str(f"{round(total_payment):,}"))
            st.success("Moratorium Interest: "+str(f"{m_interest:,}"))

        labels = ['Principal Amount','Total Interest']
        values = [principal, total_interest]
        pie_fig1 = fun.my_plotly_pie_obj("Total Payment Break-up")
        pie_fig1.add_trace(go.Pie(labels = labels, values = values,textinfo='label+percent'))

        col6.plotly_chart(pie_fig1,use_container_width = True)
    else:
        df1 = fun.monthly_info_calculator(principal+m_interest,interest_rate,EMI2,tenure,t_st)
        
        c_interest = round(df1['Interest'].sum(),2)
        df_info = pd.DataFrame([{"Monthly EMI":f"{EMI2:,}","Last Month's EMI":f"{df1['Total Payment'].iloc[-1]:,}", \
                    "Moratorium Interest (A)":f"{m_interest:,}", "Compound Interest (B)":f"{c_interest:,}",\
                    "Total Interest (A+B)":f"{c_interest+m_interest:,}", "Total Payment":f"{c_interest+m_interest+principal:,}"\
                    }])
        st.table(df_info)

        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        g_st = st.radio("Choose on option", ["Monthly Summary","Quaterly Summary","Half-Yearly Summary","Yearly Summary"],index = 3)

        if g_st == "Monthly Summary": df2,df2_s = fun.peroid_grouping(df1,1); x_title = "Month"
        elif g_st == "Quaterly Summary": df2,df2_s = fun.peroid_grouping(df1,4); x_title = "Quarter"
        elif g_st == "Half-Yearly Summary": df2,df2_s = fun.peroid_grouping(df1,6); x_title = "Half-Year"
        elif g_st == "Yearly Summary": df2,df2_s = fun.peroid_grouping(df1,12); x_title = "Year"
        
        bar_fig1 = fun.my_plotly_bar_obj(x_title+" wise Summary",x_title,"EMI Payment","Balance")
        bar_fig1.add_trace(go.Bar(y=df2.index,x=df2['Balance'],name = "Balance",orientation='h',marker_color = 'lightgreen',text=df1['Balance'],textposition='auto',),1,1)
        bar_fig1.add_trace(go.Bar(x=df2.index,y=df2['Principal'],name = "Principal",marker_color = "orange"),1,2)
        bar_fig1.add_trace(go.Bar(x=df2.index, y=df2['Interest'],name = "Interest",marker_color="blue"),1,2)
        st.plotly_chart(bar_fig1,use_container_width = True)
        st.write(df2_s)