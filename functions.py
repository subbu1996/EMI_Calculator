import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import math

@st.cache(suppress_st_warning=1,allow_output_mutation=True)
def EMI_Calculator(P,R,T,sts):
    r = R/(12*100)
    if sts:
        n = T
    else:
        n = T*12
    
    k = pow(1+r,n)
    EMI = P*r*(k/(k-1))
    EMI2 = math.ceil(EMI)
    return EMI, EMI2

@st.cache(suppress_st_warning=1,allow_output_mutation=True)
def Moratorium_Interest(P,R,T,sts):
    r = R/(12*100)
    if sts:
        n = T
    else:
        n = T*12
    
    m_interest = (P*r*n)

    return m_interest

@st.cache(suppress_st_warning=1,allow_output_mutation=True)
def monthly_info_calculator(P,R,E,T,sts):
    r = R/(12*100)
    if sts:
        n = T
    else:
        n = int(T*12)

    
    df = pd.DataFrame(columns = ['EMI No.', 'Principal', 'Interest','Total Payment','Balance','Loan Paid to Date'])
    c_b = P
    
    for i in range(1,n+1):
        s_i = round(c_b*r,2)
        if i==n:
            E = c_b+s_i
        c_p = E - s_i
        p_pc = c_p/c_b
        c_b = c_b-c_p
        df = df.append({'EMI No.':i, 'Principal':c_p, 'Interest':s_i,'Total Payment':E,'Balance':c_b,'Loan Paid to Date':p_pc},ignore_index = True)
    
    df = df.round({'Principal':2, 'Interest':2,'Total Payment':2,'Balance':2})
    #df_s = df.style.format({'EMI No.':"{:.0f}",'Principal':"{:.2f}", 'Interest':"{:.2f}",'Total Payment':"{:.2f}",'Balance':"{:.2f}",'Loan Paid to Date':"{:.2%}"})
    return df


@st.cache(suppress_st_warning=1,allow_output_mutation=True)
def peroid_grouping(df1,dn):
    df_g = df1.groupby((df1['EMI No.']/dn).apply(lambda x:math.ceil(x)))
    df2 = df_g['Principal','Interest','Total Payment'].sum()
    df2 = df2.join(df_g['Balance'].min())
    df2 = df2.join(df_g['Loan Paid to Date'].max())
    df2_s = df2.style.format({'Principal':"{:.2f}", 'Interest':"{:.2f}",'Total Payment':"{:.2f}",'Balance':"{:.2f}",'Loan Paid to Date':"{:.2%}"})
    return df2,df2_s

@st.cache(suppress_st_warning=1,allow_output_mutation=True)
def tenure_calculator(P,R,D_E):
    r = R/(12*100)
    tenure = math.log((D_E/(D_E-(P*r))),(1+r))
    return math.ceil(tenure)


#@st.cache(suppress_st_warning=1,allow_output_mutation=True)
def my_plotly_bar_obj(in_title,x_title,y_title,y_title2):
    #fig = go.Figure()
    fig = make_subplots(rows=1, cols=2, column_widths=[0.5,1], shared_xaxes = False,
                    shared_yaxes=False, vertical_spacing=0.001)
    fig.update_layout(plot_bgcolor='rgb(255,255,255)',
                       title = dict(text = "<b>"+in_title+"</b>",font_family = 'Arial',x = 0.5,y = 0.9),
                       margin = dict(l=0,r=0,pad=0),
                       legend=dict(orientation="h",yanchor="bottom", y=1.02,xanchor="right",x=1,font_family = 'Arial'))
    fig.update_layout(barmode = 'stack')
    fig.update_layout(hovermode="x")
    fig.update_layout(
        xaxis=dict(showline=False, linewidth=1.25, linecolor='black',mirror =True,gridcolor='LightGrey',
                    ticks='outside',title =dict(text=y_title2,font_family='Arial')),
        yaxis=dict(showline=False, showgrid = False, linewidth=1.25, linecolor='black',mirror =True,gridcolor='LightGrey',
                    ticks='',title =dict(text=x_title,font_family='Arial'),autorange = 'reversed'),
        xaxis2=dict(showline=True, linewidth=1.25, linecolor='black',mirror =True,gridcolor='LightGrey',
                    ticks='outside',title =dict(text=x_title,font_family='Arial')),
        yaxis2=dict(showline=True, linewidth=1.25, linecolor='black',mirror =True,gridcolor='LightGrey',
                   ticks='outside',title =dict(text=y_title,font_family='Arial')),
    )
    return fig

#@st.cache(suppress_st_warning=1,allow_output_mutation=True)
def my_plotly_pie_obj(in_title):
    fig = go.Figure()
    fig.update_layout(plot_bgcolor='rgb(255,255,255)',
                       title = dict(text = in_title,font_family = 'Arial'),
                       margin = dict(l=0,r=0, pad=0), showlegend = False)
    return fig