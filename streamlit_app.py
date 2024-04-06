import streamlit as st
#from Weighted_Lottery_Base import *
import Streamlit_Utils as su
import streamlit_widgets as sw
from streamlit_option_menu import option_menu


r = su.script_text_loader('streamlit_script.txt')
r_load = su.parse_loaded_script(r)

# Title

if 'current_page' not in st.session_state:
    st.session_state["current_page"] = "Home"
    st.session_state['candidate_count'] = 0
    st.session_state['candidates_dict'] = {}
    st.session_state['candidate_var'] = ""
    st.session_state['event_count'] = 1
    st.session_state['event_user_count'] = []
    st.session_state.event_name_list, \
    st.session_state.event_data_list, \
    st.session_state.event_prize_list, \
    st.session_state.event_prize_count_list, \
    st.session_state.event_formula_list, \
    st.session_state.event_var_list, \
    st.session_state.event_user_count = [], [], [], [], [], [], []

event_state_pack = [st.session_state.event_name_list, \
                        st.session_state.event_data_list, \
                            st.session_state.event_prize_list, \
                                st.session_state.event_prize_count_list, \
                                    st.session_state.event_formula_list, \
                                        st.session_state.event_var_list, \
                                            st.session_state.event_user_count]

#tab1, tab2, tab3, tab4 = st.sidebar(['후보자 정보 입력', '추첨 정보', '추첨 진행', '결과 확인'])
with st.sidebar:
    option_choice = option_menu("가중치/단계적 추첨", \
                                ["페이지 소개", "후보자 정보 입력", "추첨 정보", "추첨 진행", "결과 확인", "디버깅"])
    st.session_state["current_page"] = option_choice

if option_choice == "페이지 소개":
    with st.expander("이 페이지는.."):
        su.script_text_writer(r_load, 'head') 

if option_choice == "후보자 정보 입력":
    su.script_text_writer(r_load, 'tab1_info')
    
    num_candidates = sw.get_user_count(key="tab1", state = st.session_state['candidate_count'])

    st.session_state["candidate_count"] = num_candidates

    candidates_dict, candidates_var =sw.get_total_candidates_info(key="tab1", num_candidates=num_candidates, \
                                                       current_num_candidate=st.session_state['candidates_dict'], \
                                                        current_var_name = st.session_state['candidate_var'])
    st.write("Candidates and their scores:")
    st.session_state["candidates_dict"] = candidates_dict
    st.session_state["candidate_var"] = candidates_var
    st.write(st.session_state["candidates_dict"])   

     
if option_choice == "추첨 정보":
    su.script_text_writer(r_load, 'tab2_info')
    num_events = st.number_input("이벤트 수를 입력하세요", value=st.session_state["event_count"], step=1, min_value=1, max_value = 5, key=f'num_events', format="%d") 
    st.session_state["event_count"] = num_events
    
    event_name_list,event_data_list, event_prize_list, event_prize_count_list, event_formula_list, event_var_list, event_participant_count_list = \
    sw.get_event_information(key="tab2", num_events = st.session_state["event_count"], \
                       total_candidate_dict = st.session_state["candidates_dict"], \
                       total_candidate_var_name = st.session_state["candidate_var"],\
                       current_events = event_state_pack)
    #def get_event_input(key, num_events, users_dict, var_name):
    st.session_state.event_name_list = event_name_list
    st.session_state.event_data_list = event_data_list
    st.session_state.event_prize_list = event_prize_list
    st.session_state.event_prize_count_list = event_prize_count_list
    st.session_state.event_formula_list = event_formula_list
    st.session_state.event_var_list = event_var_list
    st.session_state.event_user_count = event_participant_count_list
    st.write("---")

if option_choice == "추첨 진행":
    su.script_text_writer(r_load, 'tab3_info')
    with st.expander("참가자 정보:"):
        st.write(st.session_state["candidates_info"])
    st.write("이벤트 정보: ")
    for i in range(len(st.session_state.event_name_list)):
        with st.expander(f"이벤트 {i+1}:" + " " + st.session_state.event_name_list[i]):
            st.write("상품: " + st.session_state.event_prize_list[i] + " 수량: " + \
                     str(st.session_state.event_prize_count_list[i]),\
                    "계산식: " + st.session_state.event_formula_list[i])       
            st.write("참가자 정보: ")
            st.write(st.session_state.event_data_list[i])

if option_choice == "결과 확인":
    su.script_text_writer(r_load, 'tab4_info')

if option_choice == "디버깅":
    st.write(st.session_state)
