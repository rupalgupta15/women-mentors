# Credits: https://flask-dance.readthedocs.io/en/v0.8.1/quickstarts/twitter.html

from flask import Flask, redirect, url_for
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter

app = Flask(__name__)
app.secret_key = "supersekrit"
blueprint = make_twitter_blueprint(
    api_key="",  # TODO: Add api key
    api_secret="", # TODO: Add api secret
)
app.register_blueprint(blueprint, url_prefix="/login")


@app.route("/")
def index():
    if not twitter.authorized:
        return redirect(url_for("twitter.login"))
    resp = twitter.get("account/settings.json")
    assert resp.ok
    return "You are @{screen_name} on Twitter".format(screen_name=resp.json()["screen_name"])


# if __name__ == "__main__":
#     app.run(debug=True)
