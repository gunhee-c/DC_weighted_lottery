import streamlit as st
#from Weighted_Lottery_Base import *
import Streamlit_Utils as su

r = su.script_text_loader('streamlit_script.txt')
r_load = su.parse_loaded_script(r)

# Title
st.title('가중치/단계적 추첨')
with st.expander("뭐하는 프로그램인가요?"):
    su.script_text_writer(r_load, 'head') 
tab1, tab2, tab3 = st.tabs('tab', ['후보자 정보 입력', '추첨 정보', '추첨 진행'])

if tab1:
    st.write('---')
    su.script_text_writer(r_load, 'tab1_info')
    #st.write('## 1. 후보자 정보 입력')
    #st.write('후보자의 이름과 가중치를 입력하세요.')
    #st.write('가중치는 0 이상의 정수여야 합니다.')
