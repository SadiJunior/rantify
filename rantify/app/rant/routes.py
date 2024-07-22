from flask import request

from app.rant import bp
from app.decorators.session import auth_required, validate_token
from app.services.rant import handle_rant
from app.models.llm import RantType


@bp.route("/rate", methods=["POST"])
@auth_required(from_ajax=True)
@validate_token(from_ajax=True)
def rate():
    """Generates a rate about a playlist."""
    playlist_id = request.form.get("playlist")

    return handle_rant(playlist_id, RantType.RATE)


@bp.route("/roast", methods=["POST"])
@auth_required(from_ajax=True)
@validate_token(from_ajax=True)
def roast():
    """Generates a roast about a playlist."""
    playlist_id = request.form.get("playlist")

    return handle_rant(playlist_id, RantType.ROAST)


@bp.route("/rhyme", methods=["POST"])
@auth_required(from_ajax=True)
@validate_token(from_ajax=True)
def rhyme():
    """Generates a rhyme about a playlist."""
    playlist_id = request.form.get("playlist")

    return handle_rant(playlist_id, RantType.RHYME)
