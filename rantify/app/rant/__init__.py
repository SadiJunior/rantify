from flask import Blueprint


bp = Blueprint("rant", __name__)


from app.rant import routes
