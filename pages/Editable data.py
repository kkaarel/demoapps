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
        df_file["Select"] = False
        cols = ["Select"] + [col for col in df_file if col != "Select"]
        df_file = df_file[cols]
        edited_df = st.data_editor(df_file)

        filtered_df = edited_df[edited_df['Select']]

        st.success("Here you can add any code to upload you dataframe to database or to storage(s3,blob cloud storage)")
        if filtered_df.empty:
            pass
        else:
            st.write("Validate selected rows and update")

            st.dataframe(filtered_df)
            update_button = st.button('Update Rows')
            if update_button:
                with st.spinner('Updating rows...'):
                    st.success("Data updated")
                    ## here you can add what ever end point you want to write you data in
                    



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
        df_link["Select"] = False
        cols = ["Select"] + [col for col in df_link if col != "Select"]
        df_link = df_link[cols]
        edited_df = st.data_editor(df_link)

        filtered_df = edited_df[edited_df['Select']]

        st.success("Here you can add any code to upload you dataframe to database or to storage(s3,blob cloud storage)")
        if filtered_df.empty:
            pass
        else:
            st.write("Validate selected rows and update")

            st.dataframe(filtered_df)
            update_button = st.button('Update Rows')
            if update_button:
                with st.spinner('Updating rows...'):
                    st.success("Data updated")
                    ## here you can add what ever end point you want to write you data in


    else:
        st.error("Failed to fetch the file from the provided link.")


