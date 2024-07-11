from flask import render_template


def apology(description, code=400):
    """Render message as an apology to user."""
    return render_template("apology.html", code=code, description=description), code
