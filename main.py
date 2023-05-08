import streamlit as st
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

        c0 = st.selectbox(label="Period 0",options=schedule_data['0'].unique())
        c1 = st.selectbox(label="Period 1",options=schedule_data['1'].unique())
        c2 = st.selectbox(label="Period 2",options=schedule_data['2'].unique())
        c3 = st.selectbox(label="Period 3",options=schedule_data['3'].unique())
        c4 = st.selectbox(label="Period 4",options=schedule_data['4'].unique())
        c5 = st.selectbox(label="Period 5",options=schedule_data['5'].unique())
        c6 = st.selectbox(label="Period 6",options=schedule_data['6'].unique())
        c7 = st.selectbox(label="Period 7",options=schedule_data['7'].unique())
        c8 = st.selectbox(label="Period 8",options=schedule_data['8'].unique())
        
        schedule_data.loc[new_name] = [c0,c1,c2,c3,c4,c5,c6,c7,c8]
        schedule_data = schedule_data.sort_index()

data,matrix = st.tabs(['Data','Matrix'])

with data:
    st.dataframe(schedule_data,use_container_width=True)

    p5 = schedule_data['5'].value_counts()['L' if abbreviate_class_names else 'Lunch']
    p6 = schedule_data['6'].value_counts()['L' if abbreviate_class_names else 'Lunch']

    st.markdown(f"""
    **P5 Lunch:** {p5} ({round(p5/(p5+p6),2)}\%)
    <br> **P6 Lunch:** {p6} ({round(p6/(p5+p6),2)}\%)
    """,unsafe_allow_html=True)

    st.write("## Compare Multiple")
    selected_list = st.multiselect("Display selected students together:",schedule_data.index)

    selected_students = schedule_data.loc[selected_list]
    st.dataframe(selected_students,use_container_width=True)

with matrix:
    def color_background(val):
        color = "#0b5394" if val >= 9 else "#e06666" if val >= 7 else "#f6b26b" if val >= 5 else "#ffe599" if val >= 3 else "#f3f3f3" if val >= 1 else "white"
        return f'background-color: {color}'
    def color_text(val):
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
    
    similarity_matrix = pd.DataFrame(
        similarity_array,
        columns=schedule_data.index if show_full_name else [name[0:3] for name in schedule_data.index],
        index=schedule_data.index if show_full_name else [name[0:5] for name in schedule_data.index]
        ).style.applymap(color_background)
    similarity_matrix = similarity_matrix.applymap(color_text)
    if view_mode:
        st.table(similarity_matrix)
    else:
        st.dataframe(similarity_matrix)