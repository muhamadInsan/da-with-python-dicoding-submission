def rfm_analysis(df):
    df1 = df.groupby(by='customer_id', as_index=False).agg({
            'order_purchase_timestamp':'max',
            'order_id':'count',
            'total_price':'sum'
        })
        
    df1.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]
    # - df1.max_order_timestamp.dt.date
    df1["max_order_timestamp"] = df1.max_order_timestamp.dt.date
    rcnt_date = df.order_purchase_timestamp.dt.date.max()
    df1["recency"] = df1["max_order_timestamp"].apply(lambda x: (rcnt_date - x).days)
    df1['cust_id_short'] = df1.customer_id.str.slice(start=25)

    df1.drop("max_order_timestamp", axis=1, inplace=True)

    return df1

def cust_by_states(df):
    return df.groupby(by=['customer_state']).customer_id.nunique().sort_values(
                ascending=False).reset_index().rename(
                    columns={'customer_id':'jumlah'})

def cust_by_cities(df):
    return df.loc[:,['customer_city','customer_id']].groupby(by=['customer_city']).agg({'customer_id':'count'}).sort_values(
            by='customer_id', 
            ascending=False).reset_index().rename(columns={'customer_id':'jml_cust'})

def top_product_cat(df):
    return df.groupby(by='product_category_name_english').agg({'order_id':'count'}).sort_values(
        by='order_id',
        ascending=False).reset_index().rename(columns={'order_id':'jumlah'})

def product_review(df):
    return df.groupby(by=['review_score',
                          'product_category_name_english']).agg({'review_id':'count'}).sort_values(
                              by='review_id',
                              ascending=False).rename(columns={'review_id':'jumlah'}).reset_index()

def status_order(df):
    return df.groupby(by='order_status').agg({'order_id':'count'}).sort_values(
        by='order_id', 
        ascending=False).rename(columns={'order_id':'jml'}).reset_index()

def seller_cities(df):
    return df.seller_city.value_counts().to_frame().reset_index().rename(columns={'count':'jumlah'})

def seller_states(df):
    return df.seller_state.value_counts().to_frame().reset_index().rename(columns={'count':'jumlah'})

def amount_of_order_status(df, status:list, year:int):
    df['order_purch_month_year'] = df['order_purchase_timestamp'].dt.strftime('%m-%Y')
    df['order_purch_year'] = df.loc[:,'order_purchase_timestamp'].dt.year

    df2 = df.groupby(by=['order_status',
                    'order_purch_month_year',
                    'order_purch_year']).agg({'order_id':'count'}).reset_index().rename(columns={'order_id':'jumlah'})
    
    return df2[(df2.order_status.isin(status)) & (df2.order_purch_year == year)].sort_values(by='order_purch_month_year')