# db_connector
A module to help us to connect to a db, create tables and do some queries. This module use SqlAlchemy
### Connect to a database
```python
import db_connector
db = db_connector('/path/to/your/ini/config/file.ini')
```

### create table
```python
from sqlalchemy import Column, String, Integer, Text, text
class NameOfYourTable(db.Model, db.Base):
  column1 = Column(Integer)
  column2 = Column(String(255))
  
  def __init__(self, column1, column2):
    self.column1 = column1
    self.column2 = column2

db.create_all()
```

### create a record in created table
```python
record1 = NameOfYourTable(column1=a, column2=b)
db.session.add(record1)
db.session.commit()
```

### retries all records
```python
records = db.session.query(TableName).all()
```

### retries records by conditions
```python
records = db.session.query(TableName).filter_by(columnName=value).all()
```


### join 2 tables
```python
record = db.session.query(DarvaDoc.url).join(DarvaScrapper, DarvaScrapper.ref_sinistre == DarvaDoc.ref_sinistre).filter_by(ref_sinistre='222212570').first()
```


<p>All the tables created by db_connector will have automatically id(Integer), create_at(Datetime) and update_at(Datetime) columns.</p>

