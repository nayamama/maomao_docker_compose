import pandas as pd
import os
import psycopg2
from sqlalchemy import create_engine
import re


def import_data(file_name):
    df = pd.read_excel(file_name, encoding = "utf-8")
    df = df.rename(columns=lambda x: re.sub(u'\(元\)', '', x))

    # retrieve date
    date_object = df.iloc[0]['月份'].replace("-", "")
    if date_object == "2019-08":
        df = df.drop(df[df["结算方式"] == "对私"].index)
    table_name = 'raw_data_' + date_object

    engine = create_engine('postgresql://stage_test:1234abcd@postgres_host:5432/stage_db')
    df.to_sql(table_name, engine)

    print(file_name + " is imported into DB.")
    engine.dispose()

def import_to_anchor():
    import_data("raw_201907.xlsx")
    import_data("raw_201908.xlsx")

    conn = None
    momo_number_list = None
    try:
        conn = psycopg2.connect(host="postgres_host", database="stage_db", user="stage_test", password="1234abcd")
        cur = conn.cursor()

        query1 = """insert into anchors (momo_number, name) select  陌陌号, 播主姓名 from raw_data_201907
                    ON CONFLICT (momo_number)
                    DO NOTHING;"""
        query2 = """insert into anchors (momo_number, name) select  陌陌号, 播主姓名 from raw_data_201908
                    ON CONFLICT (momo_number)
                    DO NOTHING;"""

        query3 = """select momo_number from anchors;"""

        cur.execute(query1)
        print(f'Number of rows updated: {cur.rowcount}')
        cur.execute(query2)
        print(f'Number of rows updated: {cur.rowcount}')
        cur.execute(query3)
        momo_numbers = cur.fetchall()
        momo_number_list = [n[0] for n in momo_numbers]

        print(momo_number_list)

        #cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

    return momo_number_list

def create_user_folder(momo_list):
    upload_folder = os.getenv('UPLOAD_FOLDER')
    for momo_number in momo_list:
        directory = upload_folder + "/" + momo_number

        if not os.path.exists(directory):
            os.mkdir(directory)

if __name__ == '__main__':
    momo_list = import_to_anchor()
    print(len(momo_list))
    create_user_folder(momo_list)
    