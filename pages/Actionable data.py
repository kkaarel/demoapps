import pandas as pd
import streamlit as st
import os
from pandas.api.types import (

    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)



st.set_page_config(
    layout="wide",
    page_title="Actionable data",
    page_icon="👋"
)

st.header("Create your segment and create a marketing campagin")

st.caption("File used in this demo can be found from here: https://github.com/kkaarel/streamlit_clv/blob/main/data/online_retail_II.csv")

@st.cache_data()
def getdata():
    df_online = pd.read_csv('https://raw.githubusercontent.com/kkaarel/streamlit_clv/refs/heads/main/data/online_retail_II.csv')

    return df_online


df_online = getdata()

df_online['InvoiceDate'] = pd.to_datetime(df_online['InvoiceDate'])


start_date = df_online['InvoiceDate'].min()
end_date = df_online['InvoiceDate'].max()
date_range = pd.date_range(start=start_date, end=end_date, freq='ME')


def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Start filtering values")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col], format='%Y-%m-%d')
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            left.write("↳")
            # Treat columns with < 10 unique values as categorical
            if isinstance(df[column].dtype, pd.CategoricalDtype) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Value: {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Value: {column}",
                    _min,
                    _max,
                    (_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Value: {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]


            else:
                user_text_input = right.text_input(
                    f"Text search {column}",
                )
                if user_text_input:
                    df = df[df[column].fillna('').str.contains(user_text_input)]

    return df



filtered_df = filter_dataframe(df_online)
col1, col2, col3, col4 = st.columns(4)
col1.write(f"Rows: {filtered_df.shape[0]}")
col2.write(f"Invoices: {filtered_df['Invoice'].nunique()}")
col3.write(f"Products: {filtered_df['StockCode'].nunique()}")
col4.write(f"Customers: {filtered_df['Customer ID'].nunique()}")

with st.spinner('Ladataan dataa...'):
    st.dataframe(filtered_df)
    if filtered_df.empty:
        pass
    else:
        st.write("Validate selected rows and update")

        st.dataframe(filtered_df)
        update_button = st.button('Update Rows')
        if update_button:
            with st.spinner('Updating rows...'):

                st.success("Data updated")










