from mysql import connector
import creds
import time
import datetime

def upload(tablename, value, tstamp=None, key="_3P"):


    db = connector.connect(
        host=creds.Creds.HOST,
        user=creds.Creds.USER,
        password=creds.Creds.PASS,
        database=creds.Creds.DBNAME,
        port=creds.Creds.PORT
    )

    if tstamp is None:
        tstamp = int(time.time())
    date = datetime.datetime.fromtimestamp(tstamp)
    date = date.strftime('%Y-%m-%d %H:00:00') # every hour, create a new row
    
    cursor = db.cursor()
    query = f"SELECT `{key}` FROM `{tablename}` WHERE tstamp=\"{date}\""
    cursor.execute(query)
    res = cursor.fetchone()
    if res is not None:
        value += float(res[0])
        query = f"UPDATE `{tablename}` SET `{key}`={value} WHERE tstamp = '{date}'"
    else:   
        print(date)
        query = f"INSERT INTO `{tablename}` (`{key}`, tstamp) VALUES ({value}, \"{date}\");"
    cursor.execute(query)
    db.commit()
    
# 354053.375
# 176985.59375
# 353971.1875