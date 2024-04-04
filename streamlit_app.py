import streamlit as st
#from Weighted_Lottery_Base import *
import Streamlit_Utils as su
import streamlit_widgets as sw

r = su.script_text_loader('streamlit_script.txt')
r_load = su.parse_loaded_script(r)

# Title
st.title('가중치/단계적 추첨')
with st.expander("이 페이지는.."):
    su.script_text_writer(r_load, 'head') 


st.write('---')

tab1, tab2, tab3, tab4 = st.tabs(['후보자 정보 입력', '추첨 정보', '추첨 진행', '결과 확인'])

with tab1:
    su.script_text_writer(r_load, 'tab1_info')
    candidates_info, var_name = sw.get_user_input(key = "tab1")
    st.write("Candidates and their scores:")
    st.write(candidates_info)
with tab2:
    su.script_text_writer(r_load, 'tab2_info')
    sw.get_event_input(key= "tab2", check_user_exists=True, check_user_list = candidates_info, var_name = var_name)

with tab3:
    su.script_text_writer(r_load, 'tab3_info')

with tab4:
    su.script_text_writer(r_load, 'tab4_info')