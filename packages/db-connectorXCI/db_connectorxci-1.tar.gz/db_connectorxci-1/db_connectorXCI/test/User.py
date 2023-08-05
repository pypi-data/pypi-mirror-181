from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String
import db

class User(db.Model, db.Base):
    name = Column(String(100))
    age = Column(Integer)
    description = Column(String(225))

    def __init__(self, name, age, description):
        self.name = name
        self.age = age
        self.description = description

    def __resp__(self):
        return f"<User {self.name}>"
    
    __str__ = __resp__