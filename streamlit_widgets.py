import streamlit as st
import Streamlit_Utils as su

r = su.script_text_loader('streamlit_script.txt')
r_load = su.parse_loaded_script(r)

def userinput_widget(key, check_user_exists, check_user_list, assign_users = False, max_users = None):
    try:
        user_list = list(check_user_list.keys())
    except:
        user_list = None

    if assign_users:
        st.write("number of assigned users: ", len(check_user_list))
        num_candidates = len(check_user_list)
    else:
        num_candidates = st.number_input("후보자 수를 입력하세요", value=1, step=1, min_value=0, key=f'{key}_num_candidates', format="%d")        
        if max_users:
            if num_candidates > max_users:
                st.error(f"후보자 수는 {max_users}명 이하로 입력하세요.")
                st.stop()
    names = []
    scores = []

    for i in range(num_candidates):
        if assign_users:
            name, score = unit_userinput_widget(key, i,names, check_user_exists, user_list, user_list[i])
        else:
            name, score = unit_userinput_widget(key, i,names, check_user_exists, user_list)
        names.append(name)
        scores.append(score)

    return dict(zip(names, scores))

def unit_userinput_widget(key, i, names, check_user_exists, check_user_list, assigned_user = None):
    # Create a row of 2 columns
    col1, col2 = st.columns(2)
    addme = ""
    if assigned_user:
        placeholder_name = assigned_user
        addme = "(Assigned)"
    else:
        placeholder_name = "This is a placeholder"
    with col1:  # Use the first column for the name input
        if assigned_user:
            name = st.text_input(
                "이름/닉네임을 입력하세요",
                value=placeholder_name,
                key=f'{key}_name_{i}{addme}'  # Unique key for each name input
            )
        else:
            name = st.text_input(
                "이름/닉네임을 입력하세요",
                placeholder=placeholder_name,
                key=f'{key}_name_{i}{addme}'  # Unique key for each name input
            )

    with col2:  # Use the second column for the score input
        score = st.number_input(
            "점수를 입력하세요", 
            value=1, 
            step=1, 
            min_value=0, 
            format="%d",
            key=f'{key}_score_{i}{addme}'  # Unique key for each score input
        )
    if assigned_user == None:
        if name in names:
            if name != "":
               st.error(f"닉네임/이름 {name}: 중복된 데이터가 있습니다.")
            #st.stop()
        if check_user_exists:
            if name not in check_user_list:
                if name != "":
                    st.error(f"닉네임/이름 {name}: 참가자 명단에 없습니다.")
                #st.stop()
    return [name, score]

def get_user_input(key, check_user_exists = False, check_user_list = None, max_users = None):
    user_input_dict = userinput_widget(key, check_user_exists, check_user_list, max_users)
    st.write("마지막으로..")
    var_name = st.text_input("변수명을 입력하세요", key=f'{key}_variable_name')
    return user_input_dict, var_name

def get_event_input(key, check_user_exists, check_user_list, var_name):
    num_events = st.number_input("이벤트 수를 입력하세요", value=1, step=1, min_value=0, key=f'{key}_num_candidates', format="%d")        
    event_data_list = []
    event_prize_list = []
    event_prize_count_list = []
    event_formula_list = []
    event_var_list = []
    st.write("---")

    for i in range(num_events):
        event_data, event_prize, event_prize_count, event_formula, event_var  = get_event_input_radio(key+str(i), check_user_exists, check_user_list, var_name)
        event_data_list.append(event_data)
        event_prize_list.append(event_prize)
        event_prize_count_list.append(event_prize_count)
        event_formula_list.append(event_formula)
        event_var_list.append(event_var)
        st.write("---")
    return event_data_list, event_prize_list, event_prize_count_list, event_formula_list, event_var_list
    
def get_event_input_radio(key, check_user_exists, check_user_list, var_name):
    event_prize = st.text_input("이벤트 상품 명을 입력하세요", key=f'{key}_prize')
    event_prize_count = st.number_input("이벤트 상품 수를 입력하세요", value=1, step=1, min_value=0, key=f'{key}_prize_count', format="%d")
    st.markdown(":gray[참가자 변수명은 ''으로 설정되어 있습니다.]")
    event_var = st.text_input("이벤트 변수명을 입력하세요", key=f'{key}_variable_name')
    event_formula = st.text_input("이벤트 가중치 계산식을 입력하세요", key=f'{key}_formula')
    with st.expander("도움말을 확인하세요"):
        event_formula_info(var_name, event_var)

    pickme = st.radio(
        key = key,
        label= "해당 이벤트 후보자 = 전체 후보자인가요?",
        options = ["Yes", "No"],
        horizontal=True
    )
    if pickme == "Yes":
        event_data = userinput_widget(key+"Yes", check_user_exists, check_user_list, assign_users = True)
    if pickme == "No":  
        st.write("참가자 명단을 확인하세요")
        st.write(check_user_list)  
        event_data = userinput_widget(key+"No", check_user_exists, check_user_list, max_users = len(check_user_list))
    st.write("이벤트 후보자 정보: ")
    st.write(event_data)
    return event_data, event_prize, event_prize_count, event_formula, event_var

def event_formula_info(var1, var2):
    st.write(f"가중치 계산식 예시: {var1} + {var2}")
    st.write(f"기본적 연산 기호: + * / - ^")
    st.write(f"변수명은 영문으로 설정하세요")
    st.write(f"min, max, abs, sqrt 등의 함수를 사용할 수 있습니다.")
    st.write(f"예시: max({var1}, {var2})")
    st.write(f"계산이 되지 않는 식의 경우 0으로 처리됩니다.")
    st.write("반드시 수식이 옳은지 확인하시고 추첨하세요!")
    return None

'''
def get_user_input():    
    pickme = st.radio(
        "후보자를 어떻게 입력할까요?",
        ["Textbox", "GUI"],
        horizontal=True
    )
    if pickme == "Textbox":
        with st.expander("Textbox를 통해 입력하는 방식은 다음과 같습니다"):
            su.script_text_writer(r_load, 'user_input')
        
        txt = st.text_area("write here")
        
    else:
        st.write("GUI로 입력하세요")
    st.write('---')
    st.write("입력한 후보자 정보: ")
    st.write(txt)

    return txt
'''