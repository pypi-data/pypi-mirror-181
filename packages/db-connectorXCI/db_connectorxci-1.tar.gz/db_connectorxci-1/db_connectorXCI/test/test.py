from User import User
from db import create_all

# create all tables in database
create_all()

# # import a record into user table
# user = User('do manh dung', '30', 'en france')
# db.session.add(user)
# db.session.commit()

# # get all records in user table
# users = db.session.query(User).all()
# for user in users:
#     print(user.to_dict())

# # create an user object from dict
# # import user object into database
# user = {
#     'name':'DO Manh Dung',
#     'age':30,
#     'description':'Vietnamien'
# }
# obj = User.from_dict(user)
# db.session.add(obj)
# db.session.commit()


