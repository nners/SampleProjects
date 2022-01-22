# Request a URL
# Using a yml file to get redshift connection values
import requests
from sqlalchemy import create_engine
import pandas as pd
import yaml
import psycopg2

with open("config.yml", "r") as ymlfile:
    utils = yaml.load(ymlfile)


class StockETL():
    def __init__(self, url, engine):
        self.url = url
        self.engine = engine

    def get(self):
        return requests.get(self.url)

    def transform(self):
        df = pd.read_html(self.get().content)
        return df[0].rename(columns={'(USD)': 'Metric', \
                                     'Jun 2021infoFiscal Q2 2021 ended 6/30/21.': 'Value', \
                                     'Year/year change': 'YoY Change'})

    def load(self, df, table_name, schema_name):
        self.table_name = table_name
        self.schema_name = schema_name
        df.to_sql(table_name, self.engine, \
                  schema=schema_name, \
                  if_exists='replace', \
                  index=False)

    def drop_table(self, table, schema):
        conn = self.engine.connect()
        conn.execute('DROP TABLE {schema}.{table}'.format(schema, table))


main_engine = create_engine("""postgresql://{username}:{password}@{host}:{port}/{db}""".format( \
    username=utils['redshift_username'], \
    password=utils['redshift_password'], \
    db=utils['redshift_db'], \
    port=utils['redshift_port'], \
    host=utils['redshift_host']))

# stock_price = StockETL(urls['destination']['url'],engine=main_engine)

# stock_price.load(table_name='narek_test',schema_name='adhoc',df=stock_price.transform())
# Request a URL
# Using a yml file to get redshift connection values

with open("config.yml", "r") as ymlfile:
    utils = yaml.load(ymlfile)


class StockETL:
  """ Loading Stock data into a local database """
  
  
    def __init__(self, url, engine):
        self.url = url
        self.engine = engine

    def get(self):
        return requests.get(self.url)

    def transform(self):
        df = pd.read_html(self.get().content)
        return df[0].rename(columns={'(USD)': 'Metric', \
                                     'Jun 2021infoFiscal Q2 2021 ended 6/30/21.': 'Value', \
                                     'Year/year change': 'YoY Change'})

    def load(self, df, table_name, schema_name):
        self.table_name = table_name
        self.schema_name = schema_name
        df.to_sql(table_name, self.engine, \
                  schema=schema_name, \
                  if_exists='replace', \
                  index=False)

    def drop_table(self, table, schema):
        conn = self.engine.connect()
        conn.execute('DROP TABLE {schema}.{table}'.format(schema, table))

# Using example Redshift instance
main_engine = create_engine("""postgresql://{username}:{password}@{host}:{port}/{db}""".format( \
    username=utils['redshift_username'], \
    password=utils['redshift_password'], \
    db=utils['redshift_db'], \
    port=utils['redshift_port'], \
    host=utils['redshift_host']))


stock_price.load(table_name='stock_prices',schema_name=utils['redshift_schema'],df=stock_price.transform())
