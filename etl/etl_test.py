import unittest
import pandas as pd
import os
import datetime
from unittest.mock import MagicMock, patch
from utilities import connector, extractor, transformer



class TestETL(unittest.TestCase):
    
    @patch('clickhouse_connect.get_client')
    def test_connector(self, mock_connect):

        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        conn = connector.ConnectToDatabase().connect()

        self.assertEqual(conn, mock_conn)
        mock_connect.assert_called_once_with(
            host='localhost',
            port='8123',
            username='admin',
            password='123qwe'
        )

    
    def test_is_csv(self):
        pd.DataFrame(data={'nomor':[1,2,3,4,5], 
                           'data':['a','b','c','d','e']}).to_csv(os.path.abspath('etl/temp_file.csv'), index=False)
        
        path_input = extractor.csv_file_path('etl/temp_file.csv')
        path_expected = os.path.abspath('etl/temp_file.csv')
        self.assertEqual(path_input, path_expected)

        os.remove(os.path.abspath('etl/temp_file.csv'))

    
    def test_is_not_csv(self):
        pd.DataFrame(data={'nomor':[1,2,3,4,5], 
                           'data':['a','b','c','d','e']}).to_csv(os.path.abspath('etl/temp_file.csv'), index=False)
        
        path_input = extractor.csv_file_path('etl/temp_file.html')
        path_expected = os.path.abspath('etl/temp_file.csv')
        self.assertNotEqual(path_input, path_expected, 'File format is equal')

        os.remove(os.path.abspath('etl/temp_file.csv'))

    
    def test_extractor(self):
        pd.DataFrame(data={'nomor':[1,2,3,4,5], 
                           'data':['a','b','c','d','e']}).to_csv(os.path.abspath('etl/temp_file.csv'), index=False)
        
        csv_file_df = extractor.extract_data(os.path.abspath('etl/temp_file.csv'))
        
        try:
            pd.testing.assert_frame_equal(csv_file_df, pd.DataFrame(data={'nomor':[1,2,3,4,5], 'data':['a','b','c','d','e']}))
        except AssertionError as err:
            print('Assert error!', err)

        os.remove(os.path.abspath('etl/temp_file.csv'))

    
    def test_order_items_trans(self):
        df = pd.DataFrame(data={'order_item_id':[1,2,3], 'price':[100,200,300]})

        current_df = transformer.order_items_trans(df)
        expected_df = 'int64'

        self.assertEqual(current_df['total_price'].dtype.name, expected_df, 'datatype of total_price is not same!')


    def test_delivery_time_orders(self):
        data = {
            'order_delivered_customer_date':[
                datetime.datetime(2021,1,5).__format__(''),
                datetime.datetime(2021,2,10).__format__(''),
                datetime.datetime(2021,3,3).__format__('')], 
            'order_approved_at':[
                datetime.datetime(2021,1,1).__format__(''),
                datetime.datetime(2021,2,1).__format__(''),
                datetime.datetime(2021,3,1).__format__('')]
                }
        df = pd.DataFrame(data=data, dtype='datetime64[ns]')

        current_df = transformer.delivery_time_orders(df)
        expected_df = 'int64'

        self.assertEqual(current_df['delivery_time'].dtype.name, expected_df, 'datatype of delivery_time is not same!')

if __name__ == "__main__":
    unittest.main()