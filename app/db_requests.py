from sqlalchemy import MetaData, create_engine, cast, Date
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func


class DBRequests:
    def __init__(self, URL: str, TABLE_NAME: str):
        engine = create_engine(URL)
        self.session = sessionmaker(bind=engine)
        meta = MetaData()
        meta.reflect(bind=engine)
        self.table = meta.tables.get(TABLE_NAME)

    @contextmanager
    def session_scope(self):
        session = self.session()
        try:
            yield session
            session.commit()
        finally:
            session.close()

    def get_avg_queries_time_per_day(self, date: str):
        with self.session_scope() as s:
            query_durations = (
                s.query(
                    self.table.c.query_id,
                    ((func.max(self.table.c.time) - func.min(self.table.c.time))).label(
                        "duration"
                    ),
                )
                .filter(
                    func.to_timestamp(self.table.c.time / 1000.0).cast(Date)
                    == cast(date, Date)
                )
                .group_by(self.table.c.query_id)
                .having(func.max(self.table.c.status) == 1)
                .subquery()
            )
            response = s.query(func.avg(query_durations.c.duration)).scalar()
        return response

    def get_avg_rows_per_second(self, time_start: int, time_end: int):
        with self.session_scope() as s:
            response = (
                s.query(
                    func.sum(self.table.c.rows) / ((time_end - time_start) / 1000) + 1
                )
                .filter(self.table.c.time.between(time_start, time_end))
                .scalar()
            )
        return response

    def get_avg_rows_per_thread(self, time_start: int, time_end: int):
        with self.session_scope() as s:
            response = (
                s.query(self.table.c.threads, self.table.c.rows)
                .filter(self.table.c.time.between(time_start, time_end))
                .filter(self.table.c.status == 1)
                .all()
            )

        if response is not None:
            return sum([i[1] for i in response]) / sum([len(i[0]) for i in response])
        return response

    def get_avg_threads_per_second(self, time_start: int, time_end: int):
        with self.session_scope() as s:
            response = (
                s.query(self.table.c.threads)
                .filter(self.table.c.time.between(time_start, time_end))
                .filter(self.table.c.status == 1)
                .all()
            )

        if response is not None:
            return sum([len(i[0]) for i in response]) / (
                ((time_end - time_start) / 1000) + 1
            )
        return response
