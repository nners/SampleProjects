# Accessing Google Trends data on Courseta & Udemy and loading these into a DB


import sqlite3
import pytrends
import pandas as pd
from sqlite3 import Error
from pyspark.sql import SparkSession
from pytrends.request import TrendReq
conn = sqlite3.connect('analytics.db') 
c = conn.cursor()

# Extract Data from Google Trends

kw_list = ['udemy','coursera']
pytrends = TrendReq(hl='en-US', tz=360)
pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y')
ed_tech_interest = 

# Transform 
ed_tech_interest.to_sql(name='company_interest', con=conn)
transform_query = \
"""
WITH staging_ed_data AS (
SELECT 
    date
  , udemy as interest_udemy
  , coursera AS interest_coursera 
FROM company_interest 
WHERE date >= '{datestamp}'
)
SELECT 
    date
  , AVG(interest_udemy) OVER(ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS udemy_running_avg
  , AVG(interest_coursera) OVER(ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS coursera_running_avg
  , (AVG(interest_udemy) OVER(ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) -
    AVG(interest_coursera) OVER(ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)) AS interest_dif
FROM staging_ed_data
""".format(datestamp='2021-01-01')
ed_tech_data_transform = pd.read_sql(transform_query, conn)

# Load
ed_tech_data_transform.to_sql('avg_company_interest', conn, if_exists='replace', index=False)


class PyTrendsETL():
    def __init__(self,keyword_list,raw_data_name=None,conn=None):
        self.keyword_list = keyword_list
        self.conn = conn
        self.raw_data_name = raw_data_name
    def extract(self):
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload(self.keyword_list, cat=0, timeframe='today 5-y')
        df = pytrends.interest_over_time()
        df.to_sql(name=self.raw_data_name, con=self.conn)
        return df
    def transform(self,query):
        return pd.read_sql(self.query, conn)
    def load(self,table_name):
        self.to_sql(table_name, conn, if_exists='replace', index=False)
        
if __name__ == "__main__":
    PyTrendsETL(['udemy','coursera'],conn=sqlite3.connect('analytics.db'))
