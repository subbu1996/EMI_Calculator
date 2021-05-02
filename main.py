import streamlit as st
from multiapp import MultiApp
from apps import app1,app2,app3

app = MultiApp()

st.markdown("<div id='linkto_top'></div>", unsafe_allow_html=True)
st.write("""<h1><span style = "color:green">Loan EMI Calculation App</span></h1>""", unsafe_allow_html= True)

app.add_app("EMI Calculation",app1.app)
app.add_app("Tenure Calculation",app2.app)
app.add_app("Loan Comparison",app3.app)


st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
app.run()
st.markdown("<a href='#linkto_top'>Link to top</a>", unsafe_allow_html=True)
