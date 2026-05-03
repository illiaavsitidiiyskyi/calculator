import peewee as pw

db = pw.SqliteDatabase('calculator.db')

class BaseModel(pw.Model):
    class Meta:
        database = db

class User(BaseModel):
    username = pw.CharField(unique=True, max_length=50)
    password_hash = pw.CharField()

class Calculation(BaseModel):
    user = pw.ForeignKeyField(User, backref='calculations')
    expression = pw.CharField()
    result = pw.CharField()
    created_at = pw.DateTimeField()

def init_db():
    db.connect()
    db.create_tables([User, Calculation], safe=True)
    db.close()