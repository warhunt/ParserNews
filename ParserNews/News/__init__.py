from datetime import datetime
from os import link
from mongoengine import DynamicDocument, StringField, DateTimeField, ListField

MONTH = ['Jan', 'Feb', 'Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

class News(DynamicDocument):
    header = StringField(required=True)
    news_from = StringField(required=True, default="ВА РБ")
    news_to = StringField(required=True, default="Всем")
    date = DateTimeField(required=True, default=datetime.utcnow)
    text = ListField(field=StringField(), required=True)
    link = StringField(required=False)

    @staticmethod
    def generate_corrent_date(_data_string: str) -> datetime:
        date =_data_string.split(" ")

        m, d, y = int(MONTH.index(date[0]) + 1), int(date[1]), int(date[2])

        time_12 = date[-1][:-2]

        _time=time_12.split(':')

        if date[-1][-2:] == "PM":
            if int(_time[0]) < 12:
                h=12+int(_time[0])
            else:
                h=12
        else:
            if int(_time[0]) < 12:
                h = int(_time[0])
            else:
                h=0
        min = int(_time[1])

        corrent_date = datetime(y, m, d, h, min)

        return corrent_date
