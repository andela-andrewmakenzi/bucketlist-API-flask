from flask import Flask


app = Flask(__name__)
app.config["SECRET_KEY"] = "A0Zr98j/3yX R~XHH!jmN]LWX/,?RT"

from . import models
from . import views
