import pandas as pd


def transform(customers, orders, order_items, order_payments, order_reviews, products, product_cat_english, sellers):
    # add colum total price
    order_items['total_price'] = order_items['order_item_id'] * order_items['price']

    # add colum delivery time
    orders['delivery_time'] = (orders['order_delivered_customer_date'] - orders['order_approved_at']).dt.days

    customers['cust_status'] = ['Active' if x == True else 'Inactive' for x in orders.customer_id.isin(customers.customer_id.to_list())]

    # merger order and order item 
    orders_items = pd.merge(left=orders, right=order_items, on='order_id', how='inner')
        
    # merge order item and order payment
    orders_items_payments = pd.merge(left=orders_items, right=order_payments, on='order_id')

    # merge all order data 
    all_orders = pd.merge(left=orders_items_payments, right=order_reviews, on='order_id')

    # merge product and product category english 
    products_cat_name_translation = pd.merge(left=products, right=product_cat_english, on='product_category_name')

    # merge all order and customer 
    order_cust = pd.merge(left=all_orders, right=customers, on='customer_id')
    
    # merge order_cust and seller 
    order_seller = pd.merge(left=order_cust, right=sellers, on='seller_id')
    
    # merge all 
    all_dataset = pd.merge(left=order_seller, right=products_cat_name_translation, on='product_id')

    all_dataset['order_date'] = all_dataset["order_purchase_timestamp"].dt.strftime('%Y-%m-%d').apply(pd.to_datetime).dt.date

    # set Index 
    all_dataset = all_dataset.reset_index().rename(columns={'index':'id'})

    print('Transform finished ...!')

    return all_dataset
