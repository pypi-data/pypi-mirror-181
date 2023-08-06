from peewee import *

db = SqliteDatabase('database.db')


class BaseModel(Model):
    class Meta:
        database = db
        order_by = 'abbr'


class Driver(BaseModel):
    abbr = CharField()
    name = CharField()
    team = CharField()

    class Meta:
        db_table = 'drivers'


class StartLog(BaseModel):
    abbr = ForeignKeyField(Driver, backref='start_logs')
    time_start = TimeField(3)

    class Meta:
        db_table = 'start_logs'


class EndLog(BaseModel):
    abbr = ForeignKeyField(Driver, backref='end_logs')
    time_finish = TimeField(3, null = False)

    class Meta:
        db_table = 'end_logs'
