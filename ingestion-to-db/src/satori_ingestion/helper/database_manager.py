from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from satori_ingestion.helper.utils import Utils
import datetime


class DatabaseHandler:
    def __init__(self):
        self._engine = create_engine('sqlite:///{}'.format(self._db_path))
        self._engine.echo = False  # print all sql commands
        self.Base.metadata.create_all(self._engine)
        self._Session = sessionmaker(bind=self._engine)
        self._session = self._Session()
        self.__lastCommitTimestamp = datetime.datetime.now()
        self.__satori_buffer_time = Utils().get_configuration('SATORI_BUFFER_TIME', ['ingestor', 'save_buffer_time'])

    def write_to_db(self, object):
        self._session.add(object)
        timestamp = datetime.datetime.now()
        if (timestamp - self.__lastCommitTimestamp).total_seconds() > int(self.__satori_buffer_time):
            self.flush()
            self.__lastCommitTimestamp = timestamp

    def flush(self):
        self._session.commit()


class SimpleDatabase(DatabaseHandler):
    Base = declarative_base()

    class DataModel(Base):
        __tablename__ = "SatoriBikeData"
        key = Column(Integer, primary_key=True, autoincrement=True)
        id = Column(INTEGER)
        stationName = Column(String)
        availableDocks = Column(INTEGER)
        totalDocks = Column(INTEGER)
        latitude = Column(REAL)
        longitude = Column(REAL)
        statusValue = Column(String)
        statusKey = Column(INTEGER)
        availableBikes = Column(INTEGER)
        lastCommunicationTime = Column(String)

        def get_column_names_dict(self):
            colum_dict = self.__table__.columns.keys()
            colum_dict.pop(0)
            return colum_dict

    def __init__(self, db_path):
        self._db_path = db_path
        super(SimpleDatabase, self).__init__()
