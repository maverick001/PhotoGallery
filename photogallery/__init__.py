from flask import Flask, render_template, session
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL

mysql = MySQL()



def create_app():
    app = Flask(__name__)
    app.debug = True
    # TODO: Change this to a secure random key in production
    app.secret_key = 'your-secret-key-here-change-this'
    app.config['MYSQL_USER'] = 'root'
    # TODO: Update with your MySQL password
    app.config['MYSQL_PASSWORD'] = 'your_mysql_password'
    app.config['MYSQL_DB'] = 'gallery_database'
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

    mysql.init_app(app)


    bootstrap = Bootstrap(app)
    
  
    from . import views
    app.register_blueprint(views.bp)


    @app.errorhandler(404) 
    def not_found(e): 
      return render_template("404.html")

    @app.errorhandler(500)
    def internal_error(e):
      return render_template("500.html")

    return app

