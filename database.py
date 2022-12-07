from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://root:Kowshik@2001@127.0.0.1:3306/library',echo=True)
conn = engine.connect()


metadata = db.MetaData()


Base = automap_base()
Base.prepare(engine, reflect=True)

user_details = db.Table('user_details', metadata, autoload=True, autoload_with=engine)
book_details = db.Table('book_details', metadata, autoload=True, autoload_with=engine)
admin_table = db.Table('admin_table', metadata, autoload=True, autoload_with=engine)


Session = sessionmaker(bind=engine)
session = Session()