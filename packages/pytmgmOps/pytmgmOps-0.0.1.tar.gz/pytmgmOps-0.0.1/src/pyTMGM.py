import snowflake.connector
import pandas as pd

from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL


def get_snf_df(snf_q,user_,password_,account_,warehouse_,database_):
    snowflake_con = snowflake.connector.connect(  user=user_,
                                        password=password_,
                                        account=account_)
    snowflake_con.cursor().execute(f"USE WAREHOUSE {warehouse_}")
    snowflake_con.cursor().execute(f"USE DATABASE {database_}")

   
        
    if snf_q is None:
        return pd.DataFrame()
    
    snf_df =pd.read_sql_query(snf_q, snowflake_con) 
    
    cols = {}
    
    for each_col in snf_df.columns:
        cols[each_col] = each_col.lower()
        
    snf_df = snf_df.rename(columns=cols)
    return snf_df