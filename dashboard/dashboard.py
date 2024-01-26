import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
# from babel.numbers import format_currency
import plotly.express as px
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
all_data = pd.read_csv('/data/all_dataset.csv',
                       sep=',',
                       parse_dates=['order_purchase_timestamp'])

st.title("diCommerce Dashboard")

with st.sidebar:
    st.image('img/logo.png', width=280)
    st.write("This code will be printed to the sidebar.")
    

tab1, tab2, tab3 = st.tabs(["Customer", "Product", "Order"])

with tab1:

    # Figure Product RFM
    df = all_data.groupby(by='customer_id', as_index=False).agg({
        'order_purchase_timestamp':'max',
        'order_id':'count',
        'total_price':'sum'
    })

    df.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]
    df["max_order_timestamp"] = df.max_order_timestamp.dt.date
    rcnt_date = all_data.order_purchase_timestamp.dt.date.max()
    df["recency"] = df["max_order_timestamp"].apply(lambda x: (rcnt_date - x).days)
    df['cust_id_short'] = df.customer_id.str.slice(start=25)

    df.drop("max_order_timestamp", axis=1, inplace=True)

    st.subheader('Best Customer Based on RFM Parameters (customer_id)')

    col1, col2, col3 = st.columns(3, gap='medium')

    with col1:
        
        fig_recency = px.bar(
            df.sort_values(by="recency", ascending=True).head(), 
            y='recency',
            x='cust_id_short',
            title='By Recency (days)'
            )
        fig_recency.show()

        st.plotly_chart(fig_recency, theme="streamlit", use_container_width=True)

    with col2:
        
        fig_frequency = px.bar(
            df.sort_values(by="frequency", ascending=False).head(), 
            y='frequency',
            x='cust_id_short',
            title='By Frequency'
            )
        fig_frequency.show()

        st.plotly_chart(fig_frequency, theme="streamlit", use_container_width=True)

    with col3:
        
        fig_monetary = px.bar(
            df.sort_values(by="monetary", ascending=False).head(), 
            y='monetary',
            x='cust_id_short',
            title='By Monetary'
            )
        fig_monetary.show()

        st.plotly_chart(fig_monetary, theme="streamlit", use_container_width=True)

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
        title='Top 10 Products With The Largest Order',
        orientation='h',
        )
    fig_top_product_cat.update_layout(yaxis={'categoryorder':'total ascending'})
    fig_top_product_cat.show()

    col1, col2 = st.columns([2,1], gap='medium')

    with col1:
        st.plotly_chart(fig_top_product_cat, theme="streamlit", use_container_width=True)

    with col2:
        st.dataframe(top_product_cat.iloc[11:,], hide_index=False)


    # Figure Product Review 
    product = all_data[['review_id',
                        'review_score', 
                        'review_comment_title', 
                        'review_comment_message',
                        'review_creation_date',
                        'product_category_name_english']]

    product_review = product.groupby(by=['review_score','product_category_name_english']).agg({'review_id':'count'}).sort_values(
        by='review_id', 
        ascending=False).rename(columns={'review_id':'jumlah'}).reset_index()
        
    fig_product_review = px.treemap(product_review, 
                                    path=[px.Constant("Product Score Review"), 'review_score', 'product_category_name_english'], 
                                    values='jumlah', 
                                    title='The Best Category Product Review')
    fig_product_review.update_traces(root_color="grey")
    fig_product_review.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    fig_product_review.show()

    st.plotly_chart(fig_product_review, use_container_width=True)

with tab3:
    order = all_data[['order_id', 'customer_id', 'order_status']]
    status_order = order.groupby(by='order_status').agg({'order_id':'count'}).sort_values(
        by='order_id', 
        ascending=False).rename(columns={'order_id':'jml'}).reset_index()
    
    fig_status_order = px.pie(status_order, 
                              values='jml', 
                              names='order_status', 
                              color_discrete_sequence=px.colors.sequential.RdBu,
                              title='Order Status')
    fig_status_order.show()

    st.plotly_chart(fig_status_order, use_container_width=True)