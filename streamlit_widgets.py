import streamlit as st
import Streamlit_Utils as su

r = su.script_text_loader('streamlit_script.txt')
r_load = su.parse_loaded_script(r)

#유저 수를 입력받아 반환하는 함수
#이미 유저가 할당되어 있는 경우에는 유저 수를 입력받지 않음 
#max_users: 유저 수 제한
def get_user_count(key, state, user_list = [], is_assigned = False, max_users = None):
    if is_assigned and user_list != []:
        st.write("number of assigned users: ", len(user_list))
        num_candidates = len(user_list)
    else:
        if max_users:
             if num_candidates > max_users:
                st.error(f"후보자 수는 {max_users}명 이하로 입력하세요.")
                st.stop()           
        num_candidates = st.number_input("후보자 수를 입력하세요", value=state, step=1, min_value=0, key=f'{key}_num_candidates', format="%d")        
    return num_candidates

#유저 정보의 리스트를 입력받아 반환하는 함수
#candidate_dict: 유저 명단이 이미 확보되어 있는 경우
#is_assigned: 유저 정보가 이미 할당되어 있는 경우

#state_list를 for문 내에 돌릴 수 있도록 buffer:
def buffer_state_list(state, num_candidates):
    try:
        state_names = list(state.keys())
    except:
        state_names = []
    try:
        state_scores = list(state.values())
    except:
        state_scores = []
    if len(state_names) < num_candidates:
        for i in range(num_candidates - len(state_names)):
            state_names.append("")
            state_scores.append(2147483647)
    return state_names, state_scores

#userinput_widget(키, 참여자 수, 참여자 정보, 토탈 유저 명단, 지정했는지 여부)
def candidate_info_receiver(key, num_candidates, state, candidate_dict = None, is_assigned = False):
    try:
        user_list = list(candidate_dict.keys())
    except:
        user_list = []
    current_user_list = []
    user_info = {}
    state_names, state_scores = buffer_state_list(state, num_candidates)
    for i in range(num_candidates):
        if is_assigned:
            name, score = unit_userinput_widget(key, i, state_names[i], state_scores[i], user_list, current_user_list, user_list[i])
        else:
            name, score = unit_userinput_widget(key, i, state_names[i], state_scores[i], user_list, current_user_list)
        user_info[name] = score
        current_user_list.append(name)
    return user_info


#unit_userinput_widget(키, 인덱스, 현재 이름, 현재 점수, 유저 명단, 현재 유저 명단, 지정된 유저)
def unit_userinput_widget(key, i, current_name, current_score, total_user_list, current_user_list, assigned_user = None):
    # Create a row of 2 columns
    col1, col2 = st.columns(2)

    current_user_list = []

    addme = ""
    if assigned_user:
        addme = "(Assigned)"
    is_assigned = False
    if assigned_user:
        is_assigned = True

    with col1:  # Use the first column for the name input
        name = assign_name_widget(key, i, addme, current_name, assigned_user, is_assigned)
        
    with col2:  # Use the second column for the score input
        score = assign_score_widget(key, i, addme, current_score)

    if is_assigned == False:
        check_user_input(name, total_user_list, current_user_list)

    return [name, score]

def assign_name_widget(key, index, addme, state_name, assigned_user, is_assigned = False):
  # If no name is provided, use the placeholder
    if is_assigned:
        st_key = f'{key}_name_{index}{addme}'
        name = st.text_input(
            "이름/닉네임을 입력하세요",
            value= assigned_user,
            key= st_key  # Unique key for each name input
        )
    else:
        st_key = key=f'{key}_name_{index}{addme}'
        name = st.text_input(
            "이름/닉네임을 입력하세요",
            value = state_name,
            key= st_key  # Unique key for each name input
        )
    return name

def assign_score_widget(key, i, addme, state_score):
    st_key = f'{key}_score_{i}{addme}'
    if state_score == 2147483647:
        score = st.number_input(
            "점수를 입력하세요", 
            value= 1,
            step=1, 
            min_value=0, 
            format="%d",
            key= st_key  # Unique key for each score input
        )
    else:
        score = st.number_input(
            "점수를 입력하세요", 
            value=state_score, 
            step=1, 
            min_value=0, 
            format="%d",
            key= st_key  # Unique key for each score input
        )

    return score

def check_user_input(name, total_user_list, current_user_list):
    if name in current_user_list:
        if name != "":
            st.error(f"닉네임/이름 {name}: 중복된 데이터가 있습니다.")
        #st.stop()
    if total_user_list != []:
        if name not in total_user_list:
            if name != "":
                st.error(f"닉네임/이름 {name}: 참가자 명단에 없습니다.")
                #st.stop()


#유저 정보를 입력받아 반환하는 함수 - 
def get_total_candidates_info(key, num_candidates, current_num_candidate, current_var_name, candidate_dict = None, is_assigned = False):
    candidate_info_dict = candidate_info_receiver(key, num_candidates, current_num_candidate, candidate_dict, is_assigned)
    st.write("마지막으로..")
    candidate_var_name = st.text_input("변수명을 입력하세요", value = current_var_name, key=f'{key}_variable_name')
    return candidate_info_dict, candidate_var_name

#이벤트 정보를 for문으로 돌릴 수 있도록 동적으로 initialize


def get_event_info(key, var_name, event_state, i):
    #event_state = 
    #[event_name_list, event_data_list, event_prize_list, 
    #event_prize_count_list, event_formula_list, event_var_list]
    col1, col2, col3 = st.columns(3)
    with col1:
        event_prize = st.text_input("상품 명:", value = event_state["event_prize_list"][i], key=f'{key}_prize')
    with col2:
        event_prize_count = st.number_input("상품 수:", value= event_state["event_prize_count_list"][i], step=1, min_value=0, key=f'{key}_prize_count', format="%d")
    with col3:
        event_var = st.text_input("이벤트 변수명:", value = event_state["event_var_list"][i], key=f'{key}_variable_name')
    event_formula = st.text_input("이벤트 가중치 계산식을 입력하세요", value = event_state["event_formula_list"][i], key=f'{key}_formula')
    with st.expander("수식을 입력하는 방법:"):
        event_formula_info(var_name, event_var)
    return event_prize, event_prize_count, event_formula, event_var

def get_event_candidate_info(key, num_participants, states, user_dict):
    #userinput_widget(키, 참여자 수, 참여자 정보, 토탈 유저 명단, 지정했는지 여부)
        #user_input_dict = userinput_widget(key, num_candidates, num_state, candidate_dict, max_users)
    pickme = st.radio(
        key = key,
        label= "해당 이벤트 후보자 = 전체 후보자인가요?",
        options = ["Yes", "No"],
        horizontal=True
    )
    if pickme == "Yes":
        num_candidates = len(user_dict)
        event_data = candidate_info_receiver(key+"Yes", num_candidates, states, user_dict, is_assigned = True)
    if pickme == "No":
        num_candidates = st.number_input("이벤트 후보자 수를 입력하세요", value=num_participants, step=1, min_value=1, key=f'{key}_num_candidates', format="%d")
        if num_candidates > len(user_dict):
            st.error("전체 후보자 수보다 많은 수를 입력할 수 없습니다.")
            st.stop()
        
        st.markdown(":gray[주의: No를 누른 뒤 Yes를 누르면 데이터가 초기화됩니다.]")
        st.write("참가자 명단을 확인하세요")
        st.write(user_dict)  
        event_data = candidate_info_receiver(key+"No", num_candidates, states, user_dict)
    st.write("이벤트 후보자 정보: ")
    st.write(event_data)
    return event_data, num_candidates

def event_formula_info(var1, var2):
    st.write(f"가중치 계산식 예시: {var1} + {var2}")
    st.write(f"기본적 연산 기호: + * / - ^")
    st.write(f"변수명은 영문으로 설정하세요")
    st.write(f"min, max, abs, sqrt 등의 함수를 사용할 수 있습니다.")
    st.write(f"예시: max({var1}, {var2})")
    st.write(f"계산이 되지 않는 식의 경우 0으로 처리됩니다.")
    st.write("반드시 수식이 옳은지 확인하시고 추첨하세요!")
    return None

