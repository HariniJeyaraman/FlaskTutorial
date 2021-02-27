import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(20))
    password = Column(String(20))
    firstName = Column(String(20))
    lastName = Column(String(20))
    mobileNo = Column(String(10))
    login = relationship("LogIn", uselist=False, back_populates="users") #foreign key one-one mapping

    def __repr__(self):
        return "<User(FirstName = '%s', LastName = '%s', MobileNo = '%s')>" %(self.firstName, self.lastName, self.mobileNo)

class LogIn(Base):
    __tablename__ = 'login'
    id = Column(Integer, primary_key=True)
    token = Column(String(20))
    is_logged_in = Column(Boolean)
    user_id = Column(Integer, ForeignKey('users.id'))
    users = relationship("User", back_populates="login")


    def __repr__(self):
        return "<LogIn(token = '%s', isLoggedIn = '%b')>" %(self.username, self.password)

class MovieRating(Base):
    __tablename__ = 'movie'
    id = Column(Integer, primary_key=True)
    title = Column(String(20))
    rating = Column(Float)

    def __repr__(self):
        return "<MovieRating(Title = '%s', Rating = '%f')>" %(self.title, self.rating)

class MySqlDB():
    def __init__(self, database):
        self.engine = db.create_engine("mysql+mysqlconnector://harla:harla123@localhost/{}".format(database))
        self._Session = sessionmaker(bind=self.engine)
        self.session = self._Session()
        

    def query(self, table, filters):
        data = self.session.query(table)
        for filter in filters:
            data = data.filter(filter == filters[filter])
        
        return list(data)

    def insert(self, record):
        self.session.add(record)
        self.session.commit()

if __name__ == "__main__":
    db = MySqlDB("database2")
    Base.metadata.create_all(db.engine)
    my_movie = MovieRating(title = "Something1",rating = 0.109)
    db.insert(my_movie)
    my_movie = MovieRating(title = "Something2",rating = 0.209)
    db.insert(my_movie)
    my_movie = MovieRating(title = "Something3",rating = 0.309)
    db.insert(my_movie)
    my_movie = MovieRating(title = "Something4",rating = 0.409)
    db.insert(my_movie)
    my_movie = MovieRating(title = "Something5",rating = 0.709)
    db.insert(my_movie)
    # my_user = User(username = "carla", password="harla123", firstName="lsj", lastName="LS", mobileNo="98765")
    # # print(my_user)
    # my_login = LogIn(token="ee_efin990", is_logged_in=True)
    # my_user.login = my_login
    # db.insert(my_user)
    print(db.query(User, {User.lastName: "SJ"}))
 