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
    st.session_state['is_candidate_info_valid'] = False
    st.session_state.event_name_list = [""]
    st.session_state.event_data_list = [{}]
    st.session_state.event_prize_list = [""]
    st.session_state.event_prize_count_list = [1]
    st.session_state.event_formula_list = [""]
    st.session_state.event_var_list = [""]
    st.session_state.event_user_count = [0]
    st.session_state.event_name_selected = [False]
    st.session_state.event_pickme_state = ["*None*"]

event_state_pack = {
    "event_name_list": st.session_state.event_name_list,
    "event_data_list": st.session_state.event_data_list,
    "event_prize_list": st.session_state.event_prize_list,
    "event_prize_count_list": st.session_state.event_prize_count_list,
    "event_formula_list": st.session_state.event_formula_list,
    "event_var_list": st.session_state.event_var_list,
    "event_user_count": st.session_state.event_user_count,
    "event_name_selected": st.session_state.event_name_selected,
    "event_pickme_state": st.session_state.event_pickme_state

}

#Pending
def update_event_states(event_list_dict):
    st.session_state.event_name_list = event_list_dict["event_name_list"]
    st.session_state.event_data_list = event_list_dict["event_data_list"]
    st.session_state.event_prize_list = event_list_dict["event_prize_list"]
    st.session_state.event_prize_count_list = event_list_dict["event_prize_count_list"]
    st.session_state.event_formula_list = event_list_dict["event_formula_list"]
    st.session_state.event_var_list = event_list_dict["event_var_list"]
    st.session_state.event_user_count = event_list_dict["event_user_count"]
    st.session_state.event_name_selected = event_list_dict["event_name_selected"]
    st.session_state.event_pickme_state = event_list_dict["event_pickme_state"]

def buffer_event_state(event_state_pack, num_events):
    if num_events > len(event_state_pack["event_name_list"]):
        buffer = num_events - len(event_state_pack["event_name_list"])
    else:
        buffer = 0
    for _ in range(buffer):
        event_state_pack["event_name_list"].append("")
        event_state_pack["event_data_list"].append({})
        event_state_pack["event_prize_list"].append("")
        event_state_pack["event_prize_count_list"].append(0)
        event_state_pack["event_formula_list"].append("")
        event_state_pack["event_var_list"].append("")
        event_state_pack["event_user_count"].append(0)
        event_state_pack["event_name_selected"].append(False)
        event_state_pack["event_pickme_state"].append("*None*")
    return event_state_pack





def construct_event_tabs(num_events):
    event_tabs, event_tab_name = [], []
    for i in range(num_events):
        event_tabs.append(f"이벤트 {i+1}")
        event_tab_name.append(f"이벤트 {i+1}")
    return event_tabs, event_tab_name

def get_event_name(i, value):
    st.header(f"이벤트 {i+1}: ")
    event_name = st.checkbox("이벤트 명 입력", value = value, key=f'event_checkbox_{i}')
    if event_name:
        get_event_name = st.text_input("이벤트 명을 입력하세요", value = st.session_state["event_name_list"][i], \
                                        key=f'event_name_{i}')
        value = True
    else:
        get_event_name = ""
    return get_event_name, value

def union_of_lists(*lists):
    # Convert each list to a set, then perform union operation on all sets
    union_set = set().union(*lists)
    return list(union_set)

def find_absent_candidates(total_candidates, event_candidates_list):
    event_candidates = union_of_lists(event_candidates_list)
    absent_candidates = []
    for candidate in event_candidates:
        if candidate not in total_candidates:
            absent_candidates.append(candidate)
    return absent_candidates

#tab1, tab2, tab3, tab4 = st.sidebar(['후보자 정보 입력', '추첨 정보', '추첨 진행', '결과 확인'])
with st.sidebar:
    option_choice = option_menu("가중치/단계적 추첨", \
                                ["페이지 소개", "후보자 정보 입력", "이벤트 정보 입력", "데이터 확인 / 추첨 진행", "결과 확인", "디버깅"])
    st.session_state["current_page"] = option_choice

if option_choice == "페이지 소개":
    with st.expander("이 페이지는.."):
        su.script_text_writer(r_load, 'head') 

if option_choice == "후보자 정보 입력":
    su.script_text_writer(r_load, 'tab1_info')
    event_candidate_list = []

    for i in range(len(event_state_pack["event_data_list"])):
        event_candidate_list.append(event_state_pack["event_data_list"][i])

    num_candidates = sw.get_user_count(key="tab1", state = st.session_state['candidate_count'])

    st.session_state["candidate_count"] = num_candidates

    candidates_dict, candidates_var =sw.get_total_candidates_info(key="tab1", num_candidates=num_candidates, \
                                                       current_num_candidate=st.session_state['candidates_dict'], \
                                                        current_var_name = st.session_state['candidate_var'])
    st.write("Candidates and their scores:")
    st.session_state["candidates_dict"] = candidates_dict
    st.session_state["candidate_var"] = candidates_var
    st.write(st.session_state["candidates_dict"])   

    absent_candidates = find_absent_candidates(list(st.session_state['candidates_dict'].keys()), event_candidate_list)
    
    if st.session_state['candidate_dict'] == {}:
        st.error("후보자 정보를 입력해주세요.")      
    elif "" in st.session_state['candidate_dict'].keys():
        st.error("후보자 정보를 입력을 완료하세요.")
    elif "" in st.session_state['candidate_var']:
        st.error("후보자 변수를 입력해주세요.")
    elif len(absent_candidates) > 0:
        st.error(f"이벤트 참가자 중 누락된 사람이 있습니다: {absent_candidates}")
    else:
        st.session_state['is_candidate_info_valid'] = True
        st.success("후보자 정보가 입력되었습니다.")

if option_choice == "이벤트 정보 입력":

    su.script_text_writer(r_load, 'tab2_info')
    num_events = st.number_input("이벤트 수를 입력하세요", value=st.session_state["event_count"], step=1, min_value=1, max_value = 5, key=f'num_events', format="%d") 
    st.session_state["event_count"] = num_events

    event_state_pack = buffer_event_state(event_state_pack, num_events)
    event_tabs, event_tab_name = construct_event_tabs(num_events)

    event_tabs = st.tabs(event_tab_name)

    for i in range(num_events):
        key = "event#_" + str(i)
        with event_tabs[i]:
            event_name, event_name_selected = get_event_name(i, st.session_state["event_name_selected"][i])
            event_state_pack["event_name_list"][i] = event_name

            event_prize, event_prize_count, event_formula, event_var = \
                sw.get_event_info(key, st.session_state["candidate_var"], event_state_pack, i)
            event_state_pack["event_prize_list"][i] = event_prize
            event_state_pack["event_prize_count_list"][i] = event_prize_count
            event_state_pack["event_formula_list"][i] = event_formula
            event_state_pack["event_var_list"][i] = event_var
            event_state_pack["event_name_selected"][i] = event_name_selected
            event_users, pickme_state = sw.get_event_candidate_info(key, event_state_pack["event_user_count"][i],
                                                      event_state_pack["event_data_list"][i], 
                                                      st.session_state["candidates_dict"],
                                                      event_state_pack["event_pickme_state"][i],)
            event_state_pack["event_data_list"][i] = event_users
            event_state_pack["event_pickme_state"][i] = pickme_state

    st.write("---")

if option_choice == "데이터 확인 / 추첨 진행":
    su.script_text_writer(r_load, 'tab3_info')
    with st.expander("참가자 정보:"):
        st.write(st.session_state["candidates_dict"])
    st.write("이벤트 정보: ")
    for i in range(len(st.session_state.event_name_list)):
        with st.expander(f"이벤트 {i+1}:" + " " + st.session_state.event_name_list[i]):
            st.write("상품: " + st.session_state.event_prize_list[i] + " 수량: " + \
                     str(st.session_state.event_prize_count_list[i]),\
                    "계산식: " + st.session_state.event_formula_list[i])       
            st.write("참가자 정보: ")
            st.write(event_state_pack["event_data_list"][i])
if option_choice == "결과 확인":
    su.script_text_writer(r_load, 'tab4_info')

if option_choice == "디버깅":
    st.write(st.session_state)
