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

def make_state_list(state, num_candidates):
    state_names = list(state.keys())
    state_scores = list(state.values())
    if len(state_names) < num_candidates:
        for i in range(num_candidates - len(state_names)):
            state_names.append("")
            state_scores.append(-1)
    return state_names, state_scores

def userinput_widget(key, num_candidates, state, candidate_dict = None, is_assigned = False):
    try:
        user_list = list(candidate_dict.keys())
    except:
        user_list = []
    current_user_list = []
    user_info = {}
    state_names, state_scores = make_state_list(state, num_candidates)
    for i in range(num_candidates):
        if is_assigned:
            name, score = unit_userinput_widget(key, i, state_names[i], state_scores[i], user_list, current_user_list, user_list[i])
        else:
            name, score = unit_userinput_widget(key, i, state_names[i], state_scores[i], user_list, current_user_list)
        user_info[name] = score
        current_user_list.append(name)
    return user_info



def unit_userinput_widget(key, i, state_name, state_score, user_list, current_user_list, assigned_user = None):
    # Create a row of 2 columns
    col1, col2 = st.columns(2)
    addme = ""
    current_user_list = []
    if assigned_user:
        placeholder_name = assigned_user
        addme = "(Assigned)"
    else:
        placeholder_name = "This is a placeholder"
    is_assigned = False
    if assigned_user:
        is_assigned = True

    with col1:  # Use the first column for the name input
        name = create_widget_name(key, i, addme, state_name, placeholder_name, is_assigned)
        
    with col2:  # Use the second column for the score input
        score = create_widget_score(key, i, addme, state_score)

    check_user_input(name, user_list, current_user_list, assigned_user)

    return [name, score]

def create_widget_name(key, index, addme, state_name, placeholder_name, is_assigned = False):
  # If no name is provided, use the placeholder
    if is_assigned:
        st_key = f'{key}_name_{index}{addme}'
        name = st.text_input(
            "이름/닉네임을 입력하세요",
            value=placeholder_name,
            key= st_key  # Unique key for each name input
        )
    else:
        if state_name == "":
            st_key = key=f'{key}_name_{index}{addme}'
            name = st.text_input(
                "이름/닉네임을 입력하세요",
                value=state_name,
                placeholder=placeholder_name,
                key= st_key  # Unique key for each name input
            )
        else:
            st_key = key=f'{key}_name_{index}{addme}'
            name = st.text_input(
                "이름/닉네임을 입력하세요",
                value=state_name,
                placeholder=placeholder_name,
                key= st_key  # Unique key for each name input
            )
    return name

def create_widget_score(key, i, addme, state_score):
    st_key = f'{key}_score_{i}{addme}'
    score = st.number_input(
        "점수를 입력하세요", 
        value=state_score, 
        step=1, 
        min_value=0, 
        format="%d",
        key= st_key  # Unique key for each score input
    )

    return score

def check_user_input(name, user_list, current_user_list, assigned_user):
    if assigned_user == None: #이름이 할당되어 있지 않은 경우
        if name in current_user_list:
            if name != "":
               st.error(f"닉네임/이름 {name}: 중복된 데이터가 있습니다.")
            #st.stop()
        if user_list != []:
            if name not in user_list:
                if name != "":
                    st.error(f"닉네임/이름 {name}: 참가자 명단에 없습니다.")
                    #st.stop()

def get_user_input(key, num_candidates, state, candidate_dict = None, max_users = None):
    user_input_dict = userinput_widget(key, num_candidates, state, candidate_dict, max_users)
    st.write("마지막으로..")
    var_name = st.text_input("변수명을 입력하세요", key=f'{key}_variable_name')
    return user_input_dict, var_name

def get_event_input(key, num_events, users_dict, var_name):
        
    event_name_list, event_data_list, event_prize_list, event_prize_count_list, \
    event_formula_list, event_var_list, event_tabs, event_divisions = ([] for _ in range(8))
    
    st.write("---")

    for i in range(num_events):
        event_tabs.append(f"이벤트 {i+1}")
        event_divisions.append(f"event{i+1}")
    event_division = st.tabs(event_tabs)

    for i in range(num_events):
        with event_division[i]:
            st.header(f"이벤트 {i+1}: ")
            event_name = st.checkbox("이벤트 명 입력", key=f'{key}_event_check_{i}')
            if event_name:
                get_event_name = st.text_input("이벤트 명을 입력하세요", key=f'{key}_event_name_{i}')
            
            event_prize, event_prize_count, event_formula, event_var\
                    = get_event_info(key+str(i), var_name)
            event_data = get_event_input_radio(key+str(i), users_dict)

            event_prize_list.append(event_prize)
            event_prize_count_list.append(event_prize_count)
            event_formula_list.append(event_formula)
            event_var_list.append(event_var)

            if event_name:
                event_name_list.append(get_event_name)
            else: 
                event_name_list.append(event_prize)

            event_data_list.append(event_data)

            st.write("---")
    return event_name_list, event_data_list, event_prize_list, event_prize_count_list, event_formula_list, event_var_list

def get_event_info(key, var_name):
    col1, col2, col3 = st.columns(3)
    with col1:
        event_prize = st.text_input("상품 명:", key=f'{key}_prize')
    with col2:
        event_prize_count = st.number_input("상품 수:", value=1, step=1, min_value=0, key=f'{key}_prize_count', format="%d")
    with col3:
        event_var = st.text_input("이벤트 변수명:", key=f'{key}_variable_name')
    event_formula = st.text_input("이벤트 가중치 계산식을 입력하세요", key=f'{key}_formula')
    with st.expander("도움말을 확인하세요"):
        event_formula_info(var_name, event_var)
    return event_prize, event_prize_count, event_formula, event_var

def get_event_input_radio(key, user_dict):
    pickme = st.radio(
        key = key,
        label= "해당 이벤트 후보자 = 전체 후보자인가요?",
        options = ["Yes", "No"],
        horizontal=True
    )
    if pickme == "Yes":
        event_data = userinput_widget(key+"Yes", user_dict, is_assigned = True)
    if pickme == "No":  
        st.markdown(":gray[주의: No를 누른 뒤 Yes를 누르면 데이터가 초기화됩니다.]")
        st.write("참가자 명단을 확인하세요")
        st.write(user_dict)  
        event_data = userinput_widget(key+"No", user_dict, max_users = len(user_dict))
    st.write("이벤트 후보자 정보: ")
    st.write(event_data)
    return event_data

def event_formula_info(var1, var2):
    st.write(f"가중치 계산식 예시: {var1} + {var2}")
    st.write(f"기본적 연산 기호: + * / - ^")
    st.write(f"변수명은 영문으로 설정하세요")
    st.write(f"min, max, abs, sqrt 등의 함수를 사용할 수 있습니다.")
    st.write(f"예시: max({var1}, {var2})")
    st.write(f"계산이 되지 않는 식의 경우 0으로 처리됩니다.")
    st.write("반드시 수식이 옳은지 확인하시고 추첨하세요!")
    return None

