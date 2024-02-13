# import modul
import os
from utilities import extractor, transformer, loader, connector

def main():
        
    ## read data from csv/gz
    path = 'data/E-Commerce Public Dataset/'
    extracted_customers = extractor.extract_data(os.path.abspath(f'{path}/customers_dataset.csv'))
    extracted_order_items = extractor.extract_data(os.path.abspath(f'{path}/order_items_dataset.csv'), date_col=['shipping_limit_date'])
    extracted_order_payments = extractor.extract_data(os.path.abspath(f'{path}/order_payments_dataset.csv'))
    extracted_order_reviews = extractor.extract_data(os.path.abspath(f'{path}/order_reviews_dataset.csv'), date_col=['review_creation_date',
                                                                                                              'review_answer_timestamp'])
    extracted_orders = extractor.extract_data(os.path.abspath(f'{path}/orders_dataset.csv'), date_col=['order_purchase_timestamp',
                                                                                                'order_approved_at',
                                                                                                'order_delivered_carrier_date',
                                                                                                'order_delivered_customer_date',
                                                                                                'order_estimated_delivery_date'])
    extracted_product_category_name_translation = extractor.extract_data(os.path.abspath(f'{path}/product_category_name_translation.csv'))
    extracted_products = extractor.extract_data(os.path.abspath(f'{path}/products_dataset.csv'))
    extracted_sellers = extractor.extract_data(os.path.abspath(f'{path}/sellers_dataset.csv'))

    ## transform become single file csv
    order_items = transformer.order_items_trans(extracted_order_items)

    orders = transformer.delivery_time_orders(extracted_orders)

    customers = transformer.cust_active_status(extracted_customers, orders)

    all_df = transformer.transform(
        customers=customers,
        orders=orders,
        order_items=order_items,
        order_payments=extracted_order_payments,
        order_reviews=extracted_order_reviews,
        products=extracted_products,
        product_cat_english=extracted_product_category_name_translation,
        sellers=extracted_sellers
    )

    ## load to clickhouse db
    # create connection and client clickhouse
    client = connector.ConnectToDatabase().connect()

    # create table on clickhouse
    loader.create_table(client)

    # load to table on clickhouse
    loader.load_to_clickhouse(db_client=client, df=all_df, table_name='dicommerce')

if __name__ == '__main__':
    main()