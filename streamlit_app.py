import streamlit as st
#from Weighted_Lottery_Base import *
import Streamlit_Utils as su
import streamlit_widgets as sw
from Weighted_Lottery_Base import *
from streamlit_option_menu import option_menu
from sympy import symbols, sympify, SympifyError

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
    st.session_state.event_valid = [False]

event_state_pack = {
    "event_name_list": st.session_state.event_name_list,
    "event_data_list": st.session_state.event_data_list,
    "event_prize_list": st.session_state.event_prize_list,
    "event_prize_count_list": st.session_state.event_prize_count_list,
    "event_formula_list": st.session_state.event_formula_list,
    "event_var_list": st.session_state.event_var_list,
    "event_user_count": st.session_state.event_user_count,
    "event_name_selected": st.session_state.event_name_selected,
    "event_pickme_state": st.session_state.event_pickme_state,
    "event_valid": st.session_state.event_valid
}


def buffer_event_state(event_state_pack, num_events):
    len_states = len(event_state_pack["event_name_list"])
    if num_events > len_states:
        buffer = num_events - len_states
    else:
        buffer = 0
    
    if num_events < len_states:
        reduce = len_states - num_events
    else:
        reduce = 0
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
        event_state_pack["event_valid"].append(False)
    
    for _ in range(reduce):
        event_state_pack["event_name_list"].pop()
        event_state_pack["event_data_list"].pop()
        event_state_pack["event_prize_list"].pop()
        event_state_pack["event_prize_count_list"].pop()
        event_state_pack["event_formula_list"].pop()
        event_state_pack["event_var_list"].pop()
        event_state_pack["event_user_count"].pop()
        event_state_pack["event_name_selected"].pop()
        event_state_pack["event_pickme_state"].pop()    
        event_state_pack["event_valid"].pop()
    
    return event_state_pack

def check_event_validity(event_state_pack, i):

    if event_state_pack["event_prize_list"][i] == "":
        st.error(f"이벤트 {i+1}의 상품을 입력해주세요.")
        return False
    elif event_state_pack["event_prize_count_list"][i] > event_state_pack["event_user_count"][i]:
        st.error(f"이벤트 {i+1}의 상품 수량이 참가자 수보다 많습니다.")
        return False
    elif event_state_pack["event_user_count"][i] == 0:
        st.error(f"이벤트 {i+1}의 참가자를 입력해주세요.")
        return False
    else:
        st.success(f"이벤트 {i+1}의 정보가 성공적으로 입력되었습니다.")
        return True

def check_event_formula_validity(event_state_pack, i):
    with st.expander("가중치 추첨을 하시는 경우에 확인해주세요."):
        if st.session_state["candidate_var"] == "":
            st.error("후보자 변수명을 입력해주세요.")
        if event_state_pack["event_var_list"][i] == "":
            st.error(f"이벤트 {i+1}의 변수명을 입력해주세요.")
        if check_polling_formula(event_state_pack["event_formula_list"][i],st.session_state["candidate_var"],\
                                    event_state_pack["event_var_list"][i]) == False:
            st.error(f"이벤트 {i+1}의 가중치 계산식을 확인해주세요.")
        else:
            st.success(f"이벤트 {i+1}의 가중치 계산식이 성공적으로 입력되었습니다.")
            
def check_polling_formula(formula, var1, var2):

    if var1 == "" or var2 == "":
        return False
    if var1 == var2:
        return False
    
    allowed_vars = symbols(f'{var1} {var2}')
    
    try:
        # Attempt to create an expression from the formula
        expression = sympify(formula)
        # Get all symbols in the expression
        expression_symbols = expression.free_symbols
        
        # Check if there are any symbols in the expression that are not in the allowed list
        is_valid = all(symbol in allowed_vars for symbol in expression_symbols)
        

    except SympifyError:
        is_valid = False
    
    return is_valid

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
    event_candidates = union_of_lists(*event_candidates_list)
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


    num_candidates = sw.get_user_count(key="tab1", state = st.session_state['candidate_count'])

    st.session_state["candidate_count"] = num_candidates

    candidates_dict, candidates_var =sw.get_total_candidates_info(key="tab1", num_candidates=num_candidates, \
                                                       current_num_candidate=st.session_state['candidates_dict'], \
                                                        current_var_name = st.session_state['candidate_var'])

    st.session_state["candidates_dict"] = candidates_dict
    st.session_state["candidate_var"] = candidates_var

    event_candidate_list = []
    for i in range(len(event_state_pack["event_data_list"])):
        event_candidate_list.append(list(event_state_pack["event_data_list"][i].keys()))
    absent_candidates = find_absent_candidates(list(st.session_state['candidates_dict'].keys()), event_candidate_list)
    
    st.write("---")
    st.session_state['is_candidate_info_valid'] = False
    if st.session_state['candidates_dict'] == {}:
        st.error("후보자 정보를 입력해주세요.")      
    elif "" in st.session_state['candidates_dict'].keys():
        st.error("후보자 정보를 입력을 완료하세요.")
    elif len(absent_candidates) > 0:
        st.error(f"이벤트 참가자 중 누락된 사람이 있습니다: {absent_candidates}")
    else:
        st.session_state['is_candidate_info_valid'] = True
        st.success("후보자 정보가 입력되었습니다.")

    with st.expander("참가자 정보 확인"):
        st.write(st.session_state['candidates_dict'])

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
            if event_state_pack["event_name_list"][i] == "":
                event_state_pack["event_name_list"][i] = f"{event_prize} 이벤트"

            event_users, pickme_state, event_user_count = sw.get_event_candidate_info(key, event_state_pack["event_user_count"][i],
                                                      event_state_pack["event_data_list"][i], 
                                                      st.session_state["candidates_dict"],
                                                      event_state_pack["event_pickme_state"][i],)
            event_state_pack["event_data_list"][i] = event_users
            event_state_pack["event_pickme_state"][i] = pickme_state
            event_state_pack["event_user_count"][i] = event_user_count

            st.write("---")            
            
            event_state_pack["event_valid"][i] = check_event_validity(event_state_pack, i)

            check_event_formula_validity(event_state_pack, i)

    st.write("---")

if option_choice == "데이터 확인 / 추첨 진행":
    if st.session_state['is_candidate_info_valid'] == False:
        st.error("먼저 후보자 정보를 수정하세요.")
        st.stop()
    if event_state_pack["event_valid"].count(True) < st.session_state["event_count"]:
        st.error("먼저 이벤트 정보를 수정하세요.")
        st.stop()

    su.script_text_writer(r_load, 'tab3_info')
    with st.expander("참가자 정보:"):
        st.write(st.session_state["candidates_dict"])
    st.write("이벤트 정보: ")
    for i in range(len(st.session_state.event_name_list)):
        with st.expander(f"이벤트 {i+1}:" + " " + st.session_state.event_name_list[i]):
            st.write("상품: " + st.session_state.event_prize_list[i])
            st.write("수량: " + str(st.session_state.event_prize_count_list[i]))
            st.write("계산식: " + st.session_state.event_formula_list[i])       
            st.write("참가자 정보: ")
            st.write(event_state_pack["event_data_list"][i])
    if sum(event_state_pack["event_prize_count_list"]) > len(st.session_state["candidates_dict"]):
        st.error("이벤트 간 중복 없는 추첨이 불가능합니다 (총 상품 수량> 참가자 수)")
    st.write("---")

    #가중치 확인
    on = st.toggle('가중치 계산을 진행합니다.')
    if on:
        st.write('가중치 계산 결과는 다음과 같습니다.')
        polling_base = Candidate(st.session_state["candidates_dict"])
        for i in range(st.session_state["event_count"]):
            polling_base.add_polling_event(st.session_state.event_data_list[i], \
                              st.session_state.event_prize_list[i], \
                              st.session_state.event_prize_count_list[i], \
                              st.session_state.event_formula_list[i], \
                              st.session_state["candidate_var"], \
                              st.session_state.event_var_list[i])
        polling_base.write_streamlit()
        st.write("---")
        polling_simulation = WeightedVote(polling_base)
        polling_simulation.verify_probability()
        
#, event_dict, prize_name, prize_count, formula, var1, var2):
if option_choice == "결과 확인":
    su.script_text_writer(r_load, 'tab4_info')

if option_choice == "디버깅":
    st.write(st.session_state)
