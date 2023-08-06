import psycopg2

from qsct.obj_method import Sender

s = Sender()
connect_str = "dbname='gdb' host='82.146.59.244' user='qodex' password='Hect0r1337%'"
conn = psycopg2.connect(connect_str)
cursor = conn.cursor()
query_string = "select * from records where time_in>'2022-03-02' and time_in<'2022-03-05'"
cursor.execute(query_string)
data = cursor.fetchall()
cursor.close()
s.client(data)
