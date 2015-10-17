import os
import config
from random import randint
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class photo_record(Base):

	__tablename__ = "oldgoldmtn"

	id = Column(Integer, primary_key=True)
	photo_id = Column("photo_id", String, unique=True)
	title = Column("title", String)
	date = Column("date", String)
	entry_url = Column("entry_url", String)
	image_url = Column("image_url", String)

	def __repr__(self):
		return "%s, %s, %s, %s, %s, %s" % (self.id, self.photo_id, self.title, self.date, self.entry_url, self.image_url)

class heroku(object):

	def __init__(self):
		"""fire up our database"""
		self.engine = create_engine(config.heroku_url)
		self.Session = sessionmaker(bind=self.engine)

	def create_table(self):
		Base.metadata.create_all(self.engine)

	def make_session(self):
		return self.Session()

	def check_record(self, session, photo_id):
		q = session.query(photo_record).filter(photo_record.photo_id == photo_id)
		return session.query(q.exists()).scalar()

	def add_record(self, session, record):

		new_record = photo_record(**record)
		session.add(new_record)
		session.commit()

	def get_rand_record(self, session):

		num_entries = session.query(photo_record).count()
		r = randint(0, num_entries)
		records = session.query(photo_record)
		rand_record = records[r]
		return rand_record

