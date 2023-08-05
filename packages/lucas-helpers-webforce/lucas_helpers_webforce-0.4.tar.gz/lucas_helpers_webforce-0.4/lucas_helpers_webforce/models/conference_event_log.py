from sqlalchemy import Column, JSON, Boolean, String, BigInteger, Integer, DateTime, MetaData, create_engine
from sqlalchemy.orm import declarative_base

db = create_engine('mysql+pymysql://root:secret@db/lucas')
metadata = MetaData(db)
Base = declarative_base(metadata=metadata)

class ConferenceEventLog(Base):
    __tablename__ = 'conference_event_logs'

    id = Column(BigInteger, primary_key=True)
    tenant_id = Column(String)
    account_sid = Column(String)
    conference_sid = Column(String)
    call_sid=Column(String)
    friendly_name=Column(String)
    sequence_number = Column(Integer)
    status_callback_event = Column(String)
    payload = Column(JSON)

