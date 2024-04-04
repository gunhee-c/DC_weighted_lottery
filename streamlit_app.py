import streamlit as st
#from Weighted_Lottery_Base import *
import Streamlit_Utils as su

r = su.script_text_loader('streamlit_script.txt')
r_load = su.parse_loaded_script(r)

# Title
st.title('가중치/단계적 추첨')

su.script_text_writer(r_load, 'head') 

st.write('---')
st.write('## 1. 후보자 정보 입력')
st.write('후보자의 이름과 가중치를 입력하세요.')