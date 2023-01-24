from flask_app import app

from flask_app.controllers import coachs

from flask_app.controllers import teams

from flask_app.controllers import players

from flask_app.controllers import games

if __name__ == "__main__":
    app.run(debug=True)