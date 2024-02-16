import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from handler import rfm_analysis, cust_by_states, cust_by_cities, top_product_cat, product_review, status_order, seller_cities, seller_states, amount_of_order_status
import plotly.express as px
import posixpath
from pathlib import Path

sns.set_theme(style='dark')

st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    # page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load Data 
all_data = pd.read_csv(posixpath.abspath('dashboard/data/all_dataset.csv'),
                       sep=',',
                       parse_dates=['order_purchase_timestamp'])

# all_data = pd.read_csv('data/all_dataset.csv',
#                        sep=',',
#                        parse_dates=['order_purchase_timestamp'])

st.title("diCommerce Dashboard")

min_date = all_data["order_purchase_timestamp"].min()
max_date = all_data["order_purchase_timestamp"].max()

with st.sidebar:

    st.image(posixpath.abspath('dashboard/img/logo.png'), width=280)

    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_data[(all_data["order_purchase_timestamp"] >= str(start_date)) & 
                (all_data["order_purchase_timestamp"] <= str(end_date))]

    
tab_customer, tab_product, tab_order = st.tabs(["Customer", "Product", "Order"])

with tab_customer: # Customers
    # Figure Product RFM
    st.subheader('Best Customer Based on RFM Parameters (customer_id)')

    row1_col1, row1_col2, row1_col3 = st.columns(3, gap='medium')
    with row1_col1:
        fig_recency = px.bar(
            rfm_analysis(main_df).sort_values(by="recency", ascending=True).head(), 
            y='recency',
            x='cust_id_short',
            title='By Recency (days)'
            )
        st.plotly_chart(fig_recency, theme="streamlit", use_container_width=True)


    with row1_col2:
        fig_frequency = px.bar(
            rfm_analysis(main_df).sort_values(by="frequency", ascending=False).head(), 
            y='frequency',
            x='cust_id_short',
            title='By Frequency')
        st.plotly_chart(fig_frequency, theme="streamlit", use_container_width=True)


    with row1_col3:
        fig_monetary = px.bar(
            rfm_analysis(main_df).sort_values(by="monetary", ascending=False).head(), 
            y='monetary',
            x='cust_id_short',
            title='By Monetary')
        st.plotly_chart(fig_monetary, theme="streamlit", use_container_width=True)

            
    row2_col1, row2_col2 = st.columns(2, gap='medium')
    with row2_col1:
        # Cust by states
        fig_cust_by_states = px.bar(
            cust_by_states(main_df).head(20), 
            x='customer_state', 
            y='jumlah',
            title='Top 20 States With The Largest Customers')
        st.plotly_chart(fig_cust_by_states, theme="streamlit", use_container_width=True)


    with row2_col2:
        fig_seller_by_states = px.bar(
            seller_states(main_df).head(20), 
            x='seller_state', 
            y='jumlah',
            title='Top 20 States With The Largest Sellers')
        st.plotly_chart(fig_seller_by_states, theme="streamlit", use_container_width=True)


    row3_col1, row3_col2 = st.columns(2, gap='medium')
    # Cust by cities
    with row3_col1:
        fig_cust_by_cities = px.bar(
            cust_by_cities(main_df).head(10), 
            x='jml_cust',
            y='customer_city',
            title='Top 10 Cities With The Largest Customer',
            orientation='h')
        fig_cust_by_cities.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_cust_by_cities, theme="streamlit", use_container_width=True)
    

    with row3_col2:
        fig_seller_cities = px.bar(
            seller_cities(main_df).head(10), 
            x='jumlah',
            y='seller_city',
            title='Top 10 Cities With The Largest Sellers',
            orientation='h')
        fig_seller_cities.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_seller_cities, theme="streamlit", use_container_width=True)


with tab_product: # Products
    # Top 10 product category
    fig_top_product_cat = px.bar(
        top_product_cat(main_df).head(10), 
        x='jumlah',
        y='product_category_name_english',
        title='Top 10 Products With The Largest Order',
        orientation='h')
    fig_top_product_cat.update_layout(yaxis={'categoryorder':'total ascending'})


    col1, col2 = st.columns([2,1], gap='medium')
    with col1:
        st.plotly_chart(fig_top_product_cat, theme="streamlit", use_container_width=True)


    with col2:
        st.dataframe(top_product_cat(main_df).iloc[11:,], hide_index=False)


    # Figure Product Review 
    fig_product_review = px.treemap(product_review(main_df), 
                                    path=[px.Constant("Product Score Review"), 'review_score', 'product_category_name_english'], 
                                    values='jumlah', 
                                    title='The Best Category Product Review')
    fig_product_review.update_traces(root_color="grey")
    fig_product_review.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    st.plotly_chart(fig_product_review, use_container_width=True)


with tab_order: # Orders    
    fig_status_order = px.pie(status_order(main_df), 
                              values='jml', 
                              names='order_status', 
                              color_discrete_sequence=px.colors.sequential.RdBu,
                              title='Prensentage of Order Status')
    st.plotly_chart(fig_status_order, use_container_width=True)


    col1_filter, col2_filter = st.columns([1,2], gap='medium')
    with col1_filter:
        option_year = st.selectbox('What the year is?', tuple(main_df.order_purchase_timestamp.sort_values().dt.year.unique()))
    
    with col2_filter:
        option_status = st.multiselect('Choose the status!', list(main_df.order_status.unique()), list(main_df.order_status.unique())[0])

        fig_amount_of_order_status = px.line(amount_of_order_status(all_data, option_status, option_year), 
                x="order_purch_month_year", 
                y="jumlah", 
                color="order_status", 
                text="jumlah",
                title="Purchase Order by Status")
        
    st.plotly_chart(fig_amount_of_order_status, use_container_width=True)