import app.routes.session
from flask import request, render_template, Response, Flask

from app.database import init_db
from app.routes import init_routes

app = Flask(__name__)
init_db(app)
init_routes(app)


@app.route("/", methods=["GET"])
def mainpage():
    if request.method == "GET":
        return render_template("main.html")


app.config["DEBUG"] = True
if __name__ == "__main__":
    app.run()
