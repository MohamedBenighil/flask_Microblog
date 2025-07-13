from flask import Flask, render_template, request, redirect, url_for
import datetime
from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv(override=True)


# create_app() to use factory pattern: avoid multiple db connections, tests etc...
def create_app():
    app = Flask(__name__)
    client = MongoClient(os.environ.get("MONGODB_URI"))
    app.db = client.blog

    # si on veut ajouter des données de test (sans utiliser la base de données  )
    # entries = [] 

    @app.route("/" , methods=["GET", "POST"] )
    def home():

        if request.method == "POST":
            entry = request.form.get("entry")
            if entry:
                date = datetime.datetime.now().strftime("%Y-%m-%d")
                # si données de test
                # entries.append((entry, date, date_format))
                app.db.entries.insert_one({"entry": entry, "date": date})
                return redirect(url_for("home"))
        entries = [( entry["entry"], entry["date"], datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")) for entry in app.db.entries.find() if entry.get("entry")]
        return render_template("home.html", entries=entries)

    return app


if __name__ == "__main__":
    create_app().run(debug=True)