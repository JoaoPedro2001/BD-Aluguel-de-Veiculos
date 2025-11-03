from database import engine, DBModel
from models import *

DBModel.metadata.create_all(bind=engine)