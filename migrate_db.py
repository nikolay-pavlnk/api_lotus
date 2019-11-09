from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, ARRAY, BIGINT, create_engine, MetaData
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from csv import DictReader

from app.settings import URL, DATA_FILE, TABLE_NAME

Base = declarative_base()


class Query(Base):
    __tablename__ = TABLE_NAME
    id_ = Column('id_', Integer, primary_key=True)
    query_id = Column("query_id", Integer)
    status = Column("status", Integer)
    time = Column("time", BIGINT)
    rows = Column("rows", BIGINT)
    threads = Column("threads", ARRAY(Integer), nullable=True)

    def __init__(self, row, id_):
    	self.id_ = id_
        self.query_id = row["query_id"]
        self.status = row["status"]
        self.time = row["time"]
        self.rows = row["rows"]
        if row.get("threads"):
            self.threads = [int(x) for x in row["threads"].split(",")]


class Migration:
    def __init__(self):
        self.engine = create_engine(URL)
        self.session = sessionmaker(bind=self.engine)
        meta = MetaData()
        Base.metadata.create_all(self.engine)
        meta.reflect(bind=self.engine)

    @contextmanager
    def session_scope(self):
        session = self.session()
        try:
            yield session
            session.commit()
        finally:
            session.close()

    def insert_record(self, records):
        with self.session_scope() as s:
            s.bulk_save_objects(records)
            s.commit()

    def migrate_from_file(self, data_file: str):
        with open(data_file) as csvfile:
            reader = DictReader(csvfile, delimiter="\t")
            records = [Query(row, id_) for id_, row in enumerate(reader)]
        self.insert_record(records)


if __name__ == "__main__":
    mig = Migration()
    mig.migrate_from_file(DATA_FILE)
    print("migrated succesfully")
