import streamlit as st
import pandas as pd
import io

uploaded_files = st.file_uploader(
    "Choose a CSV file", accept_multiple_files=True
)
for uploaded_file in uploaded_files:
    st.write("Filename:", uploaded_file.name)
    try:
        df_file = pd.read_csv(uploaded_file)
        st.write(df_file)

        st.success("Here you can add any code to upload you dataframe to database or to storage(s3,blob cloud storage)")
        if not df_file.empty:
            if st.button("Upload the file", key="file"):
                pass



    except pd.errors.EmptyDataError:
        st.error("The uploaded file is empty or does not contain any columns.")

file_link = st.text_input("Or enter a link to the CSV file")

# Process file link
if file_link:
    import requests
    response = requests.get(file_link)
    if response.status_code == 200:
        st.write("Filename:", file_link.split("/")[-1])
        # Convert response content to dataframe
        df_link = pd.read_csv(io.StringIO(response.text))
        st.write(df_link)
        st.success("Here you can add any code to upload you dataframe to database or to storage(s3,blob cloud storage)")
        if not df_link.empty:
            if st.button("Upload the file", key="link"):
                pass



    else:
        st.error("Failed to fetch the file from the provided link.")


