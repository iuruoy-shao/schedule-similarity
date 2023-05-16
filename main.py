import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import json

st.set_page_config(layout="wide",
                   page_title="Schedule Similarity",
                   menu_items={"Get help":"mailto:youruishao115022@gmail.com",
                               "About":"Made by Yourui Shao for BISV students to compare their schedules more effectively."})

st.markdown("""
# Schedule Similarity
""")

with st.sidebar:
    st.write("## Settings")

    abbreviate_class_names = st.checkbox("Use abbreviations",value=True)
    replacement_keys = json.load(open('text_replacement.json'))
    schedule_data = pd.read_csv('schedule_data.csv').set_index('Name').fillna("").sort_index()
    if not abbreviate_class_names:
        schedule_data = schedule_data.replace(replacement_keys)

    add_own = st.checkbox("Add your own schedule")
    st.caption("""For hypothetical schedules or private use. This will not save upon reload. 
    If you are interested in adding yourself to the public database, please contact Yourui. 
    Unfortunately, selecting unique class periods is not an option right now.""")

    if add_own:
        new_name = st.text_input("Your name (ensure this is distinguishable if your data is already on here)")

        schedule_data.loc[new_name] = [st.selectbox(label=f"Period {i}",options=schedule_data[f'{i}'].unique()) for i in range(9)]
        schedule_data = schedule_data.sort_index()

data,matrix,search = st.tabs(['Data','Matrix','Search & Filter'])

with data:
    st.dataframe(schedule_data,use_container_width=True)

    p5 = schedule_data['5'].value_counts()['L' if abbreviate_class_names else 'Lunch']
    p6 = schedule_data['6'].value_counts()['L' if abbreviate_class_names else 'Lunch']

    st.markdown(f"""
    **P5 Lunch:** {p5} ({round(p5/(p5+p6),2)}\%)
    <br> **P6 Lunch:** {p6} ({round(p6/(p5+p6),2)}\%)
    """,unsafe_allow_html=True)

    st.write("## Compare Students")
    selected_list = st.multiselect("Display selected students together:",schedule_data.index)
    
    if selected_list:
        selected_students = schedule_data.loc[selected_list]
        st.dataframe(selected_students,use_container_width=True)

with matrix:
    def color_background(val):
        if isinstance(val,int):
            color = "#0b5394" if val >= 9 else "#e06666" if val >= 7 else "#f6b26b" if val >= 5 else "#ffe599" if val >= 3 else "#f3f3f3" if val >= 1 else "white"
            return f'background-color: {color}'
    def color_text(val):
        if isinstance(val,int):
            return 'color: white' if val >= 9 else ''

    opt1, opt2 = st.columns(2)
    with opt1:
        sorting_by = st.selectbox("Group students by period",["0","1","2","3","4","5","6","7","8"],1)
    with opt2:
        show_full_name = st.checkbox("Show full name")
        view_mode = st.checkbox("View mode (somewhat expanded)",True)

    schedule_data = schedule_data.sort_values(by=sorting_by)

    similarity_array = [[np.where(schedule_data.loc[[name1]].reset_index(drop=True)
                                ==schedule_data.loc[[name2]].reset_index(drop=True),1,0)[0]
                                .tolist().count(1)
                        for name2 in schedule_data.index]
                        for name1 in schedule_data.index]
    
    hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            thead {display:none}
            tbody th {display:none}
            </style>
            """
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    
    similarity_matrix = pd.concat([pd.DataFrame([[name if show_full_name else name[:3] for name in schedule_data.index]],index=[1]),
                                   pd.DataFrame(similarity_array)]).reset_index(drop=True)
    similarity_matrix.insert(0,'',['']+[name if show_full_name else name[:8] for name in schedule_data.index])
    matrix_styler = similarity_matrix.style.applymap(color_background).applymap(color_text)
    
    if view_mode:
        st.table(matrix_styler)
    else:
        st.dataframe(matrix_styler,use_container_width=True)

with search:
    st.write("## Standard Filter")
    subjects = st.multiselect("Filter students who are in the following classes:",
                              list(replacement_keys.keys() if abbreviate_class_names else replacement_keys.values()))
    def highlight_classes(val):
        if val in subjects:
            return 'background-color: #ffe599' 
    if subjects:
        index_list = [
            student
            for student in schedule_data.index
            if pd.Series(subjects).isin(list(schedule_data.loc[student])).all()
        ]
        
        filtered_students = schedule_data.loc[index_list].style.applymap(highlight_classes)
        st.dataframe(filtered_students,use_container_width=True)
    
    st.write("## Filter by Period")
    c0, c1, c2, c3, c4, c5, c6, c7, c8 = st.columns(9)
    columns = [c0,c1,c2,c3,c4,c5,c6,c7,c8]
    p_filters = [] 

    def column_is_empty(val):
        return val in [f'{i}' for i in range(9)]
    
    for i in range(9):
        with columns[i]:
            p_filters.append(st.selectbox(
                label=f"Period {i}",
                label_visibility="hidden",
                options=np.insert(schedule_data[f'{i}'].unique(),0,f"{i}")
                ))
            
    if any(not column_is_empty(p_filters[i]) for i in range(9)):
        p_index_list = [
            student
            for student in schedule_data.index
            if all(schedule_data.loc[student][key] == p_filters[key] or column_is_empty(p_filters[key])
                   for key in range(9))
        ]
        st.dataframe(schedule_data.loc[p_index_list],use_container_width=True)