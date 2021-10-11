from mongoengine import connect

def init_db(DB: str, HOST: str, USER: str, PASSWORD: str, AUTHENTICATION_SOURCE: str) -> None:
    connect(
        db = DB,
        host =  HOST,
        username = USER,
        password = PASSWORD,
        authentication_source = AUTHENTICATION_SOURCE
    )