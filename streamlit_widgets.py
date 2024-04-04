import streamlit as st
import Streamlit_Utils as su

r = su.script_text_loader('streamlit_script.txt')
r_load = su.parse_loaded_script(r)


def tokenize_text(text):
    return text.split("\n")

def get_user_input():    
    pickme = st.radio(
        "후보자를 어떻게 입력할까요?",
        ["Textbox", "GUI"],
        horizontal=True
    )
    if pickme == "Textbox":
        su.script_text_writer(r_load, 'user_input')
        
        txt = st.text_area()
        
    else:
        st.write("GUI로 입력하세요")
    st.write('---')
    st.write("입력한 후보자 정보: ")
    st.write(txt)
    
    return txt