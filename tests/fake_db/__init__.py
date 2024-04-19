from dotenv import load_dotenv
import os

load_dotenv(
    dotenv_path=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.env.test')
)

from db.models import *
from db.database import Base, get_db


