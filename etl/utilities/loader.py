def create_table(db_client):
    query = """ 
        CREATE TABLE IF NOT EXISTS default.dicommerce
        (
            id UInt64,
            order_id String,
            customer_id String NULL,
            order_status String NULL,
            order_purchase_timestamp DateTime64(3) NULL,
            order_approved_at DateTime64(3) NULL,
            order_delivered_carrier_date DateTime64(3) NULL,
            order_delivered_customer_date DateTime64(3) NULL,
            order_estimated_delivery_date DateTime64(3) NULL,
            delivery_time Float64 NULL,
            order_item_id UInt64 NULL,
            product_id String NULL,
            seller_id String NULL,
            shipping_limit_date DateTime64(3) NULL,
            price Float64 NULL,
            freight_value Float64 NULL,
            total_price Float64 NULL,
            payment_sequential UInt64 NULL,
            payment_type String NULL,
            payment_installments UInt64 NULL,
            payment_value Float64 NULL,
            review_id String NULL,
            review_score UInt64 NULL,
            review_comment_title TEXT NULL,
            review_comment_message TEXT NULL,
            review_creation_date DateTime64(3) NULL,
            review_answer_timestamp DateTime64(3) NULL,
            customer_unique_id String NULL,
            customer_zip_code_prefix UInt64 NULL,
            customer_city String NULL,
            customer_state String NULL,
            cust_status String NULL,
            seller_zip_code_prefix UInt64 NULL,
            seller_city String NULL,
            seller_state String NULL,
            product_category_name String NULL,
            product_name_lenght Float64 NULL,
            product_description_lenght Float64 NULL,
            product_photos_qty Float64 NULL,
            product_weight_g Float64 NULL,
            product_length_cm Float64 NULL,
            product_height_cm Float64 NULL,
            product_width_cm Float64 NULL,
            product_category_name_english String NULL,
            order_date Date NULL,
        )
        ENGINE = MergeTree()
        PRIMARY KEY (id)
        """
    try:
        db_client.command(query)
        print('Create table success !!')
    except Exception as err:
        print('Create table failed !!', err)

    return

def load_to_clickhouse(db_client, df, table_name:str):
    try:
        db_client.insert_df(table_name, df)
        print('Success instert to db !!')
    except Exception as err:
        print('Failed instert to db !!', err)

    return