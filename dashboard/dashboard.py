import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
# from babel.numbers import format_currency
import plotly.express as px
sns.set(style='dark')


# Load Data 
all_data = pd.read_csv('../data/all_dataset.csv')

st.title("diCommerce Dashboard")

with st.sidebar:
    st.image('img/logo.png', width=280)
    st.write("This code will be printed to the sidebar.")
    

tab1, tab2, tab3 = st.tabs(["Customer", "Product", "Order"])

with tab1:
    # Tab 1 Customer
    # cust by states
    custby_states = all_data.groupby(
                        by=['customer_state']).customer_id.nunique().sort_values(
                            ascending=False).reset_index().rename(
                                columns={'customer_id':'jml_cust'})

    fig_cust_by_states = px.bar(
        custby_states, 
        x='customer_state', 
        y='jml_cust',
        title='States With The Largest Customer' )
    fig_cust_by_states.show()

    st.plotly_chart(fig_cust_by_states, theme="streamlit", use_container_width=True)

    # Cust by cities
    by_city_states = all_data.loc[:,['customer_city','customer_id']].groupby(by=['customer_city']).agg({'customer_id':'count'}).sort_values(
        by='customer_id', 
        ascending=False).reset_index().rename(columns={'customer_id':'jml_cust'})

    fig_cust_by_cities = px.bar(
        by_city_states.head(10), 
        x='jml_cust',
        y='customer_city',
        title='Top 10 Cities With The Largest Customer',
        orientation='h',
        )
    fig_cust_by_cities.update_layout(yaxis={'categoryorder':'total ascending'})
    fig_cust_by_cities.show()

    st.plotly_chart(fig_cust_by_cities, theme="streamlit", use_container_width=True)

with tab2:

    # Tab 2 Product
    # Top 10 product category
    top_product_cat = all_data.groupby(by='product_category_name_english').agg({
        'order_id':'count'
    }).sort_values(by='order_id', ascending=False).reset_index().rename(columns={'order_id':'jumlah'})

    fig_top_product_cat = px.bar(
        top_product_cat.head(10), 
        x='jumlah',
        y='product_category_name_english',
        title='Top 10 Cities With The Largest Customer',
        orientation='h',
        )
    fig_top_product_cat.update_layout(yaxis={'categoryorder':'total ascending'})
    fig_top_product_cat.show()

    col1, col2 = st.columns([2,1], gap='medium')

    with col1:
        st.plotly_chart(fig_top_product_cat, theme="streamlit", use_container_width=True)

    with col2:
        st.dataframe(top_product_cat.iloc[11:,], hide_index=False)
