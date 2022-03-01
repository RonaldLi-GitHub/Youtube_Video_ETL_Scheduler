import psycopg2

def create_table():
    hostname='localhost'
    database='youtube_db'
    username='postgres'
    pwd='admin'
    port_id=5432
    table_name='Youtube_Vid'

    conn=psycopg2.connect(host=hostname, dbname=database, user=username, password=pwd, port=port_id)
    cur = conn.cursor()
    create_table = """CREATE TABLE IF NOT EXISTS %s
                    (
                        Channel VARCHAR, 
                        Video_Id VARCHAR, 
                        Upload_Date TIMESTAMP,
                        Video_Title VARCHAR,
                        Video_Description VARCHAR,
                        View_Count INTEGER,
                        Like_Count INTEGER,
                        Comment_Count INTEGER,
                        Update_Date TIMESTAMP
                    )
                    """ % table_name
    cur.execute(create_table)
    conn.commit()
    conn.close()

if __name__=="__main__":
    create_table()

