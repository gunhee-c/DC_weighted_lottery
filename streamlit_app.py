import streamlit as st
#from Weighted_Lottery_Base import *
import Streamlit_Utils as su
import streamlit_widgets as sw
from streamlit_option_menu import option_menu


r = su.script_text_loader('streamlit_script.txt')
r_load = su.parse_loaded_script(r)

# Title

#tab1, tab2, tab3, tab4 = st.sidebar(['후보자 정보 입력', '추첨 정보', '추첨 진행', '결과 확인'])
with st.sidebar:
    option_choice = option_menu("가중치/단계적 추첨", ["페이지 소개", "후보자 정보 입력", "추첨 정보", "추첨 진행", "결과 확인"])
if option_choice == "페이지 소개":
    with st.expander("이 페이지는.."):
        su.script_text_writer(r_load, 'head') 

if option_choice == "후보자 정보 입력":
    su.script_text_writer(r_load, 'tab1_info')
    candidates_info, var_name = sw.get_user_input(key = "tab1")
    st.write("Candidates and their scores:")

    st.session_state["candidates_info"] = candidates_info
    st.session_state["candidate_var_name"] = var_name
    st.write(st.session_state.candidates_info)   

     
if option_choice == "추첨 정보":
    su.script_text_writer(r_load, 'tab2_info')
    event_name_list,event_data_list, event_prize_list, event_prize_count_list, event_formula_list, event_var_list = \
    sw.get_event_input(key="tab2", check_user_exists=True, check_user_list=st.session_state.candidates_info, var_name=st.session_state.var_name)
    
    st.session_state.event_name_list = event_name_list
    st.session_state.event_data_list = event_data_list
    st.session_state.event_prize_list = event_prize_list
    st.session_state.event_prize_count_list = event_prize_count_list
    st.session_state.event_formula_list = event_formula_list
    st.session_state.event_var_list = event_var_list

    st.write("---")

if option_choice == "추첨 진행":
    su.script_text_writer(r_load, 'tab3_info')
    with st.expander("참가자 정보:"):
        st.write(candidates_info)
    st.write("이벤트 정보: ")
    for i in range(len(event_name_list)):
        with st.expander(f"이벤트 {i+1}:" + " " + event_name_list[i]):
            st.write("상품: " + event_prize_list[i] + " 수량: " + str(event_prize_count_list[i]), "계산식: " + event_formula_list[i])       
            st.write("참가자 정보: ")
            st.write(event_data_list[i])

if option_choice == "결과 확인":
    su.script_text_writer(r_load, 'tab4_info')