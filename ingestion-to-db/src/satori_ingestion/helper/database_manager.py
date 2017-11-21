from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from satori_ingestion.helper.time_service import TimeService


class DatabaseHandler:
    def __init__(self):
        self._engine = create_engine('sqlite:///{}'.format(self._dbPath))
        self._engine.echo = False  # print all sql commands
        self.Base.metadata.create_all(self._engine)
        self._Session = sessionmaker(bind=self._engine)
        self._session = self._Session()
        self.__lastCommitTimestamp = TimeService().getTimestampDatetimeObjectNow()

    def write_to_db(self, object):
        self._session.add(object)
        timestamp = TimeService().getTimestampDatetimeObjectNow()
        if (timestamp - self.__lastCommitTimestamp).total_seconds() > 60:
            self.flush()
            self.__lastCommitTimestamp = timestamp

    def flush(self):
        self._session.commit()


class SimpleTrainingDatabase(DatabaseHandler):
    Base = declarative_base()

    class TrainingDataModel(Base):
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


        def getColumnNamesDict(self):
            columDict = self.__table__.columns.keys()
            columDict.pop(0) # remove id column
            return columDict

    def __init__(self, dbPath):
        self._dbPath = dbPath
        super(SimpleTrainingDatabase, self).__init__()
