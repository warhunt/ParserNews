from mongoengine import connect

def init_db(_db: str, _host: str) -> None:
    connect(
        db = _db,
        host =  _host,
    )