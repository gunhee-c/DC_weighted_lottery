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
