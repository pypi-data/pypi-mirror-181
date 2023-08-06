from sqlalchemy import Column, JSON, String, BigInteger, DateTime, MetaData, create_engine
from sqlalchemy.orm import declarative_base

db = create_engine('mysql+pymysql://root:secret@db/lucas')
metadata = MetaData(db)
Base = declarative_base(metadata=metadata)

class CallEventLog(Base):
    __tablename__ = 'call_event_logs'

    id = Column(BigInteger, primary_key=True)
    tenant_id = Column(String)
    account_sid = Column(String)
    call_sid = Column(String)
    status = Column(String)
    caller = Column(String)
    caller_country = Column(String)
    caller_state = Column(String)
    caller_city = Column(String)
    caller_zip = Column(String)
    callee = Column(String)
    callee_country = Column(String)
    callee_state = Column(String)
    callee_city = Column(String)
    callee_zip = Column(String)
    payload = Column(JSON)

