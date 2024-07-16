import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import json
import numpy as np



conn = st.connection("gsheets", type=GSheetsConnection)
sheet = conn.read(worksheet="Evaluation Submissions")


# Initialize session state
if 'greater_index' not in st.session_state:
    st.session_state["greater_index"] = 0
if 'lesser_index' not in st.session_state:
    st.session_state["lesser_index"] = 0

GLIDE = pd.read_csv("GLIDE_formatted.csv")
EMDAT = pd.read_csv("public_emdat_2004_formatted.csv")
event_dict = json.load(open("GLIDE_eventdict.json", "r"))
country_translation = json.load(open('iso_dict.json', 'r'))


def case_select(df):
    # greater_back = back.button("", use_container_width=True, key="gb")
    glide_list = dataframe["GLIDE_ID"].unique()
    greater_back = back.button("⟵", use_container_width=True, key=1)
    if greater_back:
        st.session_state["greater_index"] -= 1
        st.session_state["lesser_index"] = 0
    # greater_forward = forward.button("", use_container_width=True, key="gf")
    greater_forward = forward.button("⟶", use_container_width=True, key=2)
    if greater_forward:
        st.session_state["greater_index"] += 1
        st.session_state["lesser_index"] = 0
    glide_num = glide_list[st.session_state["greater_index"]]
    count_left.subheader(f"GLIDE Case: {(st.session_state['greater_index'])}/{len(glide_list) - 1}")
    return glide_num

def match_select(df, ID):

    emdat_list = (df["EMDAT_ID"][df["GLIDE_ID"]==ID]).unique()
    #right.dataframe(eligible_emdat)
    if len(emdat_list) != 1:
        subback, subforward = forward.columns(2)
        # greater_back = back.button("", use_container_width=True, key="gb")
        lesser_back = subback.button("⟵", use_container_width=True, key=3)
        if lesser_back:
            st.session_state["lesser_index"] -= 1
        # greater_forward = forward.button("", use_container_width=True, key="gf")
        lesser_forward = subforward.button("⟶", use_container_width=True, key=4)
        if lesser_forward:
            st.session_state["lesser_index"] += 1
        if st.session_state["lesser_index"] < 0 or st.session_state["lesser_index"] > len(emdat_list)-1:
            st.session_state["lesser_index"] = 0
        count_right.subheader(f"EMDAT Case: {(st.session_state['lesser_index'])}/{len(emdat_list) - 1}")
    emdat_num = emdat_list[st.session_state["lesser_index"]]
    return emdat_num

def grab_glide(ID):
    glide_case = GLIDE[GLIDE["GLIDE_ID"] == ID]
    date_left.subheader(f"GLIDE\: {glide_num}")

    time = pd.DataFrame()
    date_left.subheader("Date of Event")
    time["Year"] = glide_case["year"].astype(str)
    time["Month"] = glide_case["month"]
    time['Day'] = glide_case["day"]
    date_left.dataframe(time, use_container_width=True)

    event = event_dict[glide_case["event"].iloc[0]]
    event_left.metric("Event", event)

    magnitude = glide_case["magnitude"].iloc[0]
    event_left.metric("Magnitude", magnitude)

    location_left.subheader("\n Location")
    place = pd.DataFrame()
    place["Country"] = glide_case["geocode"].map(country_translation)
    place["Location"] = glide_case["location"]
    location_left.dataframe(place, use_container_width=True)

    killed_left.subheader("Impact Statistics")
    killed = glide_case["killed"]
    killed_left.dataframe(killed, use_container_width=True)
    injured = glide_case["injured"]
    injured_left.dataframe(injured, use_container_width=True)
    homeless = glide_case["homeless"]
    homeless_left.dataframe(homeless, use_container_width=True)
    affected = glide_case["affected"]
    affected_left.dataframe(affected, use_container_width=True)
    comments = glide_case["comments"].iloc[0]
    left.divider()
    left.write("Comments:")
    left.write(f"\"{GLIDE comments}\"")

def grab_emdat(ID):
    #st.dataframe(sheet)
    emdat_case = EMDAT[EMDAT["EMDAT_ID"] == ID]

    date_right.subheader(f"EMDAT\: {emdat_num}")

    time = pd.DataFrame()
    date_right.subheader("Date of Event")
    time["Year"] = emdat_case["Start Year"].astype(str)
    time["Month"] = emdat_case["Start Month"]
    time['Day'] = emdat_case["Start Day"]
    date_right.dataframe(time, use_container_width=True)

    disaster = emdat_case["Disaster Subtype"].iloc[0]
    event_right.metric("Event", disaster)

    magnitude = emdat_case["Magnitude"].iloc[0]
    event_right.metric("Magnitude", magnitude)

    location_right.subheader("\n Location")
    place = pd.DataFrame()
    place["Country"] = emdat_case["Country"]
    place["Location"] = emdat_case["Location"]
    location_right.dataframe(place, use_container_width=True)

    killed_right.subheader("Impact Statistics")
    killed = emdat_case["Total Deaths"]
    killed_right.dataframe(killed, use_container_width=True)
    injured = emdat_case["No. Injured"]
    injured_right.dataframe(injured, use_container_width=True)
    homeless = emdat_case["No. Homeless"]
    homeless_right.dataframe(homeless, use_container_width=True)
    affected = emdat_case["No. Affected"]
    affected_right.dataframe(affected, use_container_width=True)


st.title("EMDAT-GLIDE Match Validation Portal")
st.header("CRED--Internal use only")
st.divider()
st.markdown("This portal exists as an internal tool for validating the potential matches resulting from the EM-DAT "
            "interoperability machine learning model. Thank you for your effort and contribution.")
st.subheader("Upload Your Potential Match Index")
data = st.file_uploader("Select your file...")
if data is not None:
    dataframe = pd.read_excel(data)

    count_left, count_right = st.columns(2)
    back, forward = st.columns(2)
    glide_num = case_select(dataframe)
    emdat_num = match_select(dataframe, glide_num)
    st.divider()

    date_left, date_right = st.columns(2)
    event_left, event_right = st.columns(2)
    location_left, location_right = st.columns(2)
    killed_left, killed_right = st.columns(2)
    injured_left, injured_right = st.columns(2)
    homeless_left, homeless_right = st.columns(2)
    affected_left, affected_right = st.columns(2)

    left, right = st.columns(2)

    grab_glide(glide_num)
    grab_emdat(emdat_num)

    st.divider()
    name = st.text_input("Reviewer's Name")
    form = st.form(key="eval_form", clear_on_submit=True)
    form.write(f"Evaluating: {glide_num} and {emdat_num}")
    match = form.radio("Do the two selected cases match?", ["False", "True"], captions=["These cases do not refer to the same event", "These cases do refer to the same event"])
    confidence = form.select_slider("How confident are you in your answer?", options=["Not Confident","Confident","Very Confident"])
    comments = form.text_area("Do you have any additional comments or notes?")
    submitted = form.form_submit_button("Submit Evaluation")
    if submitted == True:
        new_line = pd.DataFrame([[name, emdat_num, glide_num, match, confidence, comments]], columns= ["Name", "EMDAT_ID", "GLIDE_ID", "Match", "Confidence", "Comments"])
        sheet = pd.concat([sheet, new_line])
        conn.update(worksheet="Evaluation Submissions", data=sheet)
        st.write("Successfully Submitted!")