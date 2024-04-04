import streamlit as st
#from Weighted_Lottery_Base import *
import Streamlit_Utils as su

r = su.script_text_loader('streamlit_script.txt')
r_load = su.parse_loaded_script(r)

# Title
st.title('가중치/단계적 추첨')
with st.expander("이 페이지는.."):
    su.script_text_writer(r_load, 'head') 


st.write('---')

tab1, tab2, tab3 = st.tabs(['후보자 정보 입력', '추첨 정보', '추첨 진행'])

if tab1:
    
    su.script_text_writer(r_load, 'tab1_info')


if tab2:
    su.script_text_writer(r_load, 'tab2_info')


if tab3:
    su.script_text_writer(r_load, 'tab3_info')
