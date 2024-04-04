import streamlit as st
import Streamlit_Utils as su

r = su.script_text_loader('streamlit_script.txt')
r_load = su.parse_loaded_script(r)

def userinput_widget(key, check_user_exists, check_user_list, assigned_users = None):
    if assigned_users:
        st.write("# of assigned users: ", len(assigned_users))
        num_candidates = len(assigned_users)
    else:
        num_candidates = st.number_input("후보자 수를 입력하세요", value=1, step=1, min_value=0, key=f'{key}_num_candidates', format="%d")        
    names = []
    scores = []
    for i in range(num_candidates):
        if assigned_users:
            name, score = unit_userinput_widget(key, i,names, check_user_exists, check_user_list, assigned_users[i])
        else:
            name, score = unit_userinput_widget(key, i,names, check_user_exists, check_user_list)
        names.append(name)
        scores.append(score)
    st.write("Candidates and their scores:")
    st.write(dict(zip(names, scores)))
    return names, scores

def unit_userinput_widget(key, i, names, check_user_exists, check_user_list, assigned_user = None):
    # Create a row of 2 columns
    col1, col2 = st.columns(2)
    if assigned_user:
        placeholder_name = assigned_user
    else:
        placeholder_name = "This is a placeholder"
    with col1:  # Use the first column for the name input
        name = st.text_input(
            "이름/닉네임을 입력하세요",
            placeholder=placeholder_name,
            key=f'{key}_name_{i}'  # Unique key for each name input
        )

    with col2:  # Use the second column for the score input
        score = st.number_input(
            "점수를 입력하세요", 
            value=1, 
            step=1, 
            min_value=0, 
            format="%d",
            key=f'{key}_score_{i}'  # Unique key for each score input
        )

    if name in names:
        st.error(f"닉네임/이름 {name}: 중복된 데이터가 있습니다.")
        st.stop()
    if check_user_exists:
        if name not in check_user_list:
            st.error(f"닉네임/이름 {name}: 참가자 명단에 없습니다.")
            st.stop()
    return [name, score]

def tokenize_text(text):
    return text.split("\n")

def get_user_input(key, check_user_exists = False, check_user_list = None):
    names, scores = userinput_widget(key, check_user_exists, check_user_list)
    st.write("마지막으로..")
    st.text_input("변수명을 입력하세요", key=f'{key}_variable_name')
    return names, scores

def get_event_input(key, check_user_exists, check_user_list):
    num_events = st.number_input("이벤트 수를 입력하세요", value=1, step=1, min_value=0, key=f'{key}_num_candidates', format="%d")        
    event_names = []
    event_scores = []
    for i in range(num_events):
        event_name, event_score = get_event_input_radio(key+str(i), check_user_exists, check_user_list)
        event_names.append(event_name)
        event_scores.append(event_score)
    return event_names, event_scores

def get_event_input_radio(key, check_user_exists, check_user_list):

    pickme = st.radio(
        "해당 이벤트 후보자 = 전체 후보자인가요?",
        ["Yes", "No"],
        horizontal=True
    )
    if pickme == "Yes":
        event_name, event_score = userinput_widget(key, check_user_exists, check_user_list, assigned_users=check_user_list)
    if pickme == "No":    
        event_name, event_score = userinput_widget(key, check_user_exists, check_user_list)

    return event_name, event_score

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