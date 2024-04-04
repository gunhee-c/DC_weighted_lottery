import streamlit as st

def script_text_loader(file_path):
    with open(file_path, 'r', encoding = "utf-8") as file:
        r = file.readlines()
    return r

def parse_loaded_script(script_text):
    scripts = {}
    flag = False
    script_tokens = []
    variable_name = ""
    for lines in script_text:
        lines = lines.strip()
        #print(lines)
        #print(script_tokens)
        if lines == "%END%":
            #print("ending detected")
            scripts[variable_name] = script_tokens
            flag = False

        if flag == False:
            script_tokens = []
            
        if flag == True:
            script_tokens.append(lines)
        
        if lines.startswith("%Script"):
            variable_name = lines[9:]
            flag = True
    return scripts
r = script_text_loader('streamlit_script.txt')
r_load = parse_loaded_script(r)
print(r_load)

def script_text_writer(script, script_name):
    str_list = script[script_name]
    for item in str_list:
        st.markdown(item)
