import os
from flaskr.auth import Auth
from flask import Flask, request
from flaskr.db import User, LogIn, MySqlDB, MovieRating

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # a simple page that says hello
    @app.route('/login', methods = ['POST'])
    def login():
        data = request.get_json() 
        username = data["username"]
        password = data["password"]
        my_auth = Auth()
        my_token = my_auth.login(username, password)
        if my_token ==None:
            return {"status": "Access Denied", "token": "NULL"}
        return {"status": "Success", "token": my_token}

    @app.route('/logout', methods = ['POST'])
    def logout():
        data = request.get_json()
        username = data["username"]
        password = data["password"]
        my_auth = Auth()
        my_auth.logout(username, password)
        return "Success"

    @app.route('/movie_rating', methods = ['POST'])
    def get_ratings():
        data = request.get_json()
        username = data["username"]
        token = data["token"]
        movie_name = data["title"]
        my_db = MySqlDB("database2")
        user_list = my_db.query(User, {User.username: username})
        if(len(user_list) == 1):
            user = user_list[0]
            db_token = user.login.token
            if(db_token == token):
                my_movie = my_db.query(MovieRating, {MovieRating.title : movie_name})
                movie_title = my_movie[0].title
                movieRating = my_movie[0].rating
                return {"title" : movie_title, "rating" : movieRating}
        return {"Status" : "Error"}

    @app.route('/get_user_details', methods = ['POST'])
    def get_details():
        request.get_json()

    return app