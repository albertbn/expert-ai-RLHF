from os import getenv
from typing import Iterable
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

DB_USERNAME = getenv('db_username')
DB_PASSWORD = getenv('db_password')
DB_HOST = getenv('db_host')
DB_PORT = int(getenv('db_port'))
DB_DATABASE = getenv('db_database')
DB_SSLMODE = getenv('db_sslmode')

UTF8 = 'utf8'


def connect() -> tuple:

    conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, user=DB_USERNAME, password=DB_PASSWORD, dbname=DB_DATABASE)
    conn.set_client_encoding(UTF8)
    cur = conn.cursor()
    return conn, cur


def disconnect(cur, conn):

    if cur:
        cur.close()
    if conn:
        conn.commit()
        conn.close()


def list_to_sql(ls: Iterable, quote: str = "'") -> str:
    """
    converts an Iterable to string representation of a list, compatible with sql in filtering
    example: (1, 2, 3) -> '1','2','3'
    the caller can then wrap in parentheses to have ('1','2','3')
    which can be used in:
    SELECT * from table whe id in ('1','2','3')
    :param quote:
    :param ls:
    :return:
    """
    if not ls:
        return ''

    ls_str = f"{quote},{quote}".join([str(o) for o in ls])
    return f"{quote}{ls_str}{quote}"


def count(tbl: str = 'text2elastic', where: str = None) -> int:

    conn, cur = None, None

    try:
        conn, cur = connect()
        sql = f'SELECT COUNT(*) FROM {tbl}'
        if where and where.strip():
            sql += f' WHERE {where}'  # !
        cur.execute(sql)
        sql_count = cur.fetchone()[0]

        return sql_count
    finally:
        disconnect(cur, conn)


def execute(sql: str = 'update text2elastic set prompt=1'):

    conn, cur = None, None

    try:
        conn, cur = connect()
        cur.execute(sql)
    finally:
        disconnect(cur, conn)


def df_to_sql(df: pd.DataFrame, sql_table: str = 'text2elastic', is_truncate: int = 0):
    """
    this generates an insert statement
    :param df:
    :param sql_table:
    :param is_truncate:
    :return:
    """
    # engine = create_engine(f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}', encoding=UTF8)
    engine = create_engine(f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}')
    # engine = create_engine(f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}',
    #                        connect_args={'charset': UTF8})

    # conn.set_client_encoding(UTF8)

    if is_truncate:
        engine.execute(f'truncate table `{sql_table}`')

    df.to_sql(con=engine, name=sql_table, if_exists='append', index=False)


def df_from_sql(sql='SELECT * FROM text2elastic', index_column_arr: list = None) -> pd.DataFrame:
    """
    reads a sql query as pandas dataframe
    :param sql:
    :param index_column_arr:
    :return:
    """

    conn, cur = None, None

    try:
        conn, cur = connect()
        cur.execute(sql)

        columns = [o.name for o in list(cur.description)]
        records = cur.fetchall()
        df = pd.DataFrame(records, columns=columns)

        if index_column_arr:
            df = df.set_index(index_column_arr, drop=False)

        return df
    finally:
        disconnect(cur, conn)


def update_when_then(df: pd.DataFrame, idd: str = 'parts_code', what: str = 'review_json',
                     sql_tbl: str = 'tl_reviews_ratings_seo') -> None:
    new_line = '\n'
    quote = "'"
    double_quote = "''"
    # f"WHEN `{idd}`='{str(row.get(idd, '')).replace(quote, double_quote)}' THEN '{str(row.get(what, '')).replace(quote, double_quote)}'"
    # f"WHEN `{idd}`='{str(row.get(idd, '')).replace(quote, double_quote)}' THEN {str(row.get(what))}"

    when_then = (
        f"WHEN `{idd}`='{str(row.get(idd, '')).replace(quote, double_quote)}' THEN CAST('{row.get(what).replace(quote, double_quote)}' as json)"
        for __, row in df.iterrows())
    ids = [str(id) for id in df[idd].tolist()]

    sql = f'''
        update `{sql_tbl}`
        set `{what}`= (CASE
        {new_line.join(when_then)}
        END)
        where `{idd}` in ('{"','".join(ids)}')
        '''

    sql = sql.replace("`", "")
    execute(sql)


if __name__ == '__main__':
    df_from_sql()
