import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from handler import rfm_analysis, cust_by_states, cust_by_cities, top_product_cat, product_review, status_order
import plotly.express as px
import posixpath
from pathlib import Path
sns.set(style='dark')

st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    # page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

# Load Data 
all_data = pd.read_csv(posixpath.abspath('dashboard/data/all_dataset.csv'),
                       sep=',',
                       parse_dates=['order_purchase_timestamp'])
# all_data = pd.read_csv('data/all_dataset.csv',
#                        sep=',',
#                        parse_dates=['order_purchase_timestamp'])

st.title("diCommerce Dashboard")

with st.sidebar:

    # st.image(posixpath.abspath('dashboard/img/logo.png'), width=280)

    min_date = all_data["order_purchase_timestamp"].min()
    max_date = all_data["order_purchase_timestamp"].max()
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_data[(all_data["order_purchase_timestamp"] >= str(start_date)) & 
                (all_data["order_purchase_timestamp"] <= str(end_date))]
    
tab1, tab2, tab3 = st.tabs(["Customer", "Product", "Order"])

with tab1:

    # Figure Product RFM

    st.subheader('Best Customer Based on RFM Parameters (customer_id)')

    col1, col2, col3 = st.columns(3, gap='medium')

    with col1:
        
        fig_recency = px.bar(
            rfm_analysis(main_df).sort_values(by="recency", ascending=True).head(), 
            y='recency',
            x='cust_id_short',
            title='By Recency (days)'
            )
        fig_recency.show()

        st.plotly_chart(fig_recency, theme="streamlit", use_container_width=True)

    with col2:
        
        fig_frequency = px.bar(
            rfm_analysis(main_df).sort_values(by="frequency", ascending=False).head(), 
            y='frequency',
            x='cust_id_short',
            title='By Frequency'
            )
        fig_frequency.show()

        st.plotly_chart(fig_frequency, theme="streamlit", use_container_width=True)

    with col3:
        
        fig_monetary = px.bar(
            rfm_analysis(main_df).sort_values(by="monetary", ascending=False).head(), 
            y='monetary',
            x='cust_id_short',
            title='By Monetary'
            )
        fig_monetary.show()

        st.plotly_chart(fig_monetary, theme="streamlit", use_container_width=True)

    # Cust by states
    fig_cust_by_states = px.bar(
        cust_by_states(main_df), 
        x='customer_state', 
        y='jml_cust',
        title='States With The Largest Customer' )
    fig_cust_by_states.show()

    st.plotly_chart(fig_cust_by_states, theme="streamlit", use_container_width=True)

    # Cust by cities
    fig_cust_by_cities = px.bar(
        cust_by_cities(main_df).head(10), 
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
    fig_top_product_cat = px.bar(
        top_product_cat(main_df).head(10), 
        x='jumlah',
        y='product_category_name_english',
        title='Top 10 Products With The Largest Order',
        orientation='h',
        )
    fig_top_product_cat.update_layout(yaxis={'categoryorder':'total ascending'})
    fig_top_product_cat.show()

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
    fig_product_review.show()

    st.plotly_chart(fig_product_review, use_container_width=True)

with tab3:
        
    fig_status_order = px.pie(status_order(main_df), 
                              values='jml', 
                              names='order_status', 
                              color_discrete_sequence=px.colors.sequential.RdBu,
                              title='Order Status')
    fig_status_order.show()

    st.plotly_chart(fig_status_order, use_container_width=True)