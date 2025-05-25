from dotenv import load_dotenv
import os
from pydantic import PostgresDsn
load_dotenv()

db_url_sync = PostgresDsn.build(
    scheme=os.environ["DB_SYNC_SCHEME"],  
    username=os.environ["DB_USERNAME"],
    password=os.environ["DB_PASSWORD"],
    host=os.environ["DB_HOST"],
    port=int(os.environ["DB_PORT"]),
    path=os.environ["DB_NAME"]  
)

api_port= int(os.environ["API_PORT"])