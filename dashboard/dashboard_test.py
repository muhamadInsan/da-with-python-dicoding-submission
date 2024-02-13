import unittest
import pandas as pd
import handler
import os
from unittest.mock import MagicMock, patch, Mock


def data_source():
    df = pd.read_csv(os.path.abspath('dashboard/data/all_dataset.csv'), 
                            sep=',', 
                            parse_dates=['order_purchase_timestamp',
                                        'order_approved_at',
                                        'order_delivered_carrier_date',
                                        'order_delivered_customer_date',
                                        'order_estimated_delivery_date',
                                        'review_creation_date',
                                        'review_answer_timestamp',
                                        'shipping_limit_date'],
                            nrows=10)
    
    return df


class TestDashboard(unittest.TestCase):

    @patch('clickhouse_connect.get_client')
    def test_connector(self, mock_connect):

        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        conn = handler.connect_db()

        self.assertEqual(conn, mock_conn)
        mock_connect.assert_called_once_with(
            host='localhost',
            port='8123',
            username='admin',
            password='123qwe'
        )

    def test_rfm_analysis(self):
        input_df = data_source()
        df = handler.rfm_analysis(input_df)
        current_recency = df['recency'].sum()
        current_frequency = df['frequency'].sum()
        current_monetary = df['monetary'].sum()

        self.assertGreater(current_recency, 0, msg="Invalid!")
        self.assertGreater(current_frequency, 0, msg="Invalid!")
        self.assertGreater(current_monetary, 0, msg="Invalid!")

    def test_cust_by_states(self):
        input_df = data_source()

        df = handler.cust_by_states(input_df)
        current_dim = df['jumlah'].sum()

        self.assertGreater(current_dim, 0, msg="Invalid!")


    def test_cust_by_cities(self):
        input_df = data_source()

        df = handler.cust_by_cities(input_df)
        current_dim = df['jml_cust'].sum()

        self.assertGreater(current_dim, 0, msg="Invalid!")

    def test_top_product_cat(self):
        input_df = data_source()

        df = handler.top_product_cat(input_df)
        current_dim = df['jumlah'].sum()

        self.assertGreater(current_dim, 0, msg="Invalid!")
    
    def test_product_review(self):
        input_df = data_source()

        df = handler.product_review(input_df)
        current_review = df['jumlah'].sum()
        min_score = df['review_score'].min()
        max_score = df['review_score'].max()

        self.assertGreater(current_review, 0, msg="Invalid!")
        self.assertLess(min_score, 5, msg="Invalid!")
        self.assertEqual(max_score, 5, msg="Invalid!")

    def test_status_order(self):
        input_df = data_source()

        df = handler.status_order(input_df)
        current_status = df['jml'].sum()

        self.assertGreater(current_status, 0, msg="Invalid!")

    def test_seller_cities(self):
        input_df = data_source()

        df = handler.seller_cities(input_df)
        current_seller = df['jumlah'].sum()

        self.assertGreater(current_seller, 0, msg="Invalid!")

    def test_seller_states(self):
        input_df = data_source()

        df = handler.seller_states(input_df)
        current_seller = df['jumlah'].sum()

        self.assertGreater(current_seller, 0, msg="Invalid!")

    def test_amount_of_order_status(self):
        input_df = data_source()

        df = handler.amount_of_order_status(input_df, status=['delivered','shipped'], year=2017)
        current = df['jumlah'].sum()

        self.assertGreater(current, 0, msg='Invalid!')
        self.assertEqual(df['order_purch_year'].dtypes.name, 'int32', msg='Invalid!')    

if __name__ == "__main__":
    unittest.main()