from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, scoped_session 
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref


engine = create_engine("postgresql+psycopg2://saima:Hermione9@localhost/government", echo=False)
session = scoped_session(sessionmaker(bind=engine,
									  autocommit = False,
									  autoflush = False))

Base = declarative_base()
# Base.query = session.query_property()

### Class declarations go here
class Official(Base):
    __tablename__ = "officials"

    id = Column(Integer, primary_key = True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    state = Column(String(25), nullable=True)
    title = Column(String(50), nullable=True)
    chamber = Column(String(25), nullable=True)
    party_affiliation = Column(String(25), nullable=True)
    email = Column(String(100), nullable=True) 
    phone = Column(String(25), nullable=True)
    address = Column(String(100), nullable=True)
    facebook = Column(String(100),nullable=True)
    twitter = Column(String(100), nullable=True)
    rank = Column(Integer, nullable=True)


class Bill(Base):
	__tablename__ = "bills"

	id = Column(Integer, primary_key = True)
	official_id = Column(Integer, ForeignKey('officials.id'))
	name = Column(String(2000), nullable=True)
	description = Column(Text, nullable=True)

	official = relationship("Official", backref=backref("bills", order_by=id))

class Voting_Record(Base):
	__tablename__ = "voting_records"

	id = Column(Integer, primary_key = True)
	official_id = Column(Integer, ForeignKey('officials.id'))
	bill_id = Column(Integer, ForeignKey('bills.id'))
	name = Column(String(1000), nullable=True)
	outcome = Column(String(25), nullable=True)
	question = Column(String(1000), nullable=True)
	
	official = relationship("Official", backref=backref("voting_records", order_by=id))
	bill = relationship("Bill", backref=backref("voting_records", order_by=id))

class Zip_code(Base):
	__tablename__ = "zip_codes"

	id = Column(Integer, primary_key = True)
	official_id = Column(Integer, ForeignKey('officials.id'))
	zip = Column(Integer, nullable=False)
	official = relationship("Official", backref=backref("zip_codes", order_by=id))
	
### End class declarations


def main():
    """In case we need this for something"""
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    main()

