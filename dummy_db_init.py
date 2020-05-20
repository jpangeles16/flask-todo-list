# Run this script to set up the database with some dummy

from flaskr import db
from flaskr.models import User, TodoPost

db.create_all()

user_1 = User(username='John', email='j@demo.com', password='password')
user_2 = User(username='Corey', email='c@demo.com', password='password')

db.session.add(user_1)
db.session.add(user_2)
db.session.commit()

post_1 = TodoPost(title='Blog 1', content='First Post Content!', user_id=user_1.id)
post_2 = TodoPost(title='Blog 2', content='Second post context!', user_id=user_1.id)

db.session.add(post_1)
db.session.add(post_2)
db.session.commit()

print("Successfully initialized database!")
