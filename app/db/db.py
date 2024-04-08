from sqlalchemy import create_engine
import os

from dotenv import load_dotenv
load_dotenv()

DBHOST = os.getenv("DBHOST")
DBPASS = os.getenv("DBPASS")

import os

DBNAME = os.getenv("DBNAME",'postgres')

def get_engine(dbhost=DBHOST, dbpass=DBPASS, dbname=DBNAME):
    engine_url = f'postgresql+psycopg2://postgres:{dbpass}@{dbhost}/{dbname}'
    engine = create_engine(engine_url)
    return engine

if __name__ == "__main__":

    engine = get_engine()
    conn = engine.connect()
    print(conn)
    conn.close()

    print('connected')