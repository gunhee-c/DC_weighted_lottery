import streamlit as st
# Initialize a current page in session state if not already done

#Initializing st session states
if 'current_page' not in st.session_state:
    st.session_state["current_page"] = "Home"

st.session_state['candidate_count'] = 0
st.session_state['event_count'] = []


# Example navigation
page = st.selectbox("Choose a page", ["Home", "Page 1", "Page 2"])
st.session_state.current_page = page

if st.session_state.current_page == "Home":
    st.write("Welcome to the Home Page")
elif st.session_state.current_page == "Page 1":
    if 'page_1_input' not in st.session_state:
        st.session_state.page_1_input = ""
    st.session_state.page_1_input = st.text_input("Page 1 Input", st.session_state.page_1_input)
    st.write(st.session_state.page_1_input)
elif st.session_state.current_page == "Page 2":
    # Similar handling for Page 2
    pass



'''
if option_choice == "후보자 정보 입력":
    su.script_text_writer(r_load, 'tab1_info')
    
    num_candidates = sw.get_user_count(key="tab1")
    if st.session_state['candidate_count'] == 0 or \
        st.session_state['candidate_count'] != 0 and st.session_state['candidate_count'] != num_candidates:
        st.session_state["candidate_count"] = num_candidates

    candidates_dict, candidates_var =sw.get_user_input(key="tab1", num_candidates=num_candidates)

    st.write("Candidates and their scores:")

    st.session_state["candidates_dict"] = candidates_dict
    st.session_state["candidate_var"] = candidates_var
    st.write(st.session_state["candidates_dict"])   
'''