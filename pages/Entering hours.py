import streamlit as st
import pandas as pd
import io
from datetime import datetime, date
import time

current_datetime = time.time()

current_time = time.time()

# Convert the current time to a struct_time object
current_struct_time = time.localtime(current_time)

# Extract the milliseconds as an integer
milliseconds = int((current_datetime - int(current_datetime)) * 1000)

# Create a key using the date and milliseconds
current_time_str = time.strftime('%Y%m%d%S', time.localtime(current_datetime))

key = current_time_str + str(milliseconds)


# Get the current date
current_date = date.today()


customervalue = ["Customer A", "Customer B", "Customer C"]
role_value = ["Developer", "Manager", "Analyst"]
project_value = ["Project X", "Project Y", "Project Z"]




st.title("Entering hours")

with st.form("Data_entry_form"):
    customer = st.selectbox('Customer', customervalue)
    date = st.date_input("Date", current_date, format="YYYY-MM-DD")
    project = st.selectbox("Project", project_value)
    role = st.selectbox("Role", role_value)
    hours = st.number_input("Hours", format="%.2f", value=7.5)
    comments = st.text_input("What did I do")

    preview_data = {
        'KEY': key,
        'CUSTOMER': customer,
        'DATE': date,
        'PROJECT': project,
        'ROLE': role,
        'HOURS': hours,
        'COMMENTS': comments

    }

    preview_submitted = st.form_submit_button("Preview")

    preview_df = pd.DataFrame(preview_data, index=[0])

if preview_submitted:
    preview_df = pd.DataFrame(preview_data, index=[0])
    st.dataframe(preview_df, hide_index=True)

if st.button("Confirm and Submit"):
    try:
        st.success("Success", icon="✅")
    except Exception as e:
        st.error(f"Error submitting data: {str(e)}")
