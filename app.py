import os
from flask import Flask, request, abort, jsonify, render_template
from flask_cors import CORS
from models import setup_db, Movie, db_drop_and_create_all


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    """ run cron.py first to create tables in Heroku """
    # heroku run python3 cron.py --app <app_name>

    @app.route('/', methods=['GET'])
    def home():
        try:
            rows = Movie.query.distinct(Movie.source).all()
            uniq_sources = [r.source for r in rows]
            result = {}

            for src in uniq_sources:
                result[src] = Movie.query.filter(Movie.source == src)

            return render_template("index.html", data=result)
        except:
            abort(500)

    
    @app.route("/movies")
    def get_movies():
        try:
            movies = Movie.query.order_by(Movie.id).all()
            movie=[]
            movie=[m.title for m in movies]
            return jsonify(
                {
                    "titles": movie
                }
            ), 200
        except:
            abort(500)
    
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "server error"
        }), 500
    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get("PORT",5000))
    app.run(host='127.0.0.1',port=port,debug=False)