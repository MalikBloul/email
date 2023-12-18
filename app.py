from flask import Flask, redirect, flash, render_template, request, session, jsonify
from flask_session import Session
from helper import get_email_template, get_db

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/settings", methods=["GET", "POST"])
def settings():
    conn = get_db()
    cur = conn.cursor()
    degrees = cur.execute("SELECT id, course_name FROM degrees").fetchall()
    return render_template("settings.html", degrees=degrees)


@app.route("/email", methods=["GET", "POST"])
def email():
    if request.method == "POST":
        course_name = request.form.get("degree")
        blocks = request.form.getlist("blocks")
        enquirer_type = request.form.get("enquirer")

        if "last_post" in session:
            session["last_post"]["degree"] = course_name
            session["last_post"]["enquirer"] = enquirer_type
            session["last_post"]["blocks"] = blocks
        else:
            session["last_post"] = {
                "degree": course_name,
                "enquirer": enquirer_type,
                "blocks": blocks,
            }

        email_template = get_email_template(course_name, enquirer_type, blocks)
        return render_template("email.html", email_template=email_template)

    if "last_post" in session:
        return render_template(
            "email.html",
            email_template=get_email_template(
                session["last_post"]["degree"],
                session["last_post"]["enquirer"],
                session["last_post"]["blocks"],
            ),
        )

    return render_template("email.html")


@app.route("/blocks/<enquirer>")
def blocks(enquirer):
    conn = get_db()
    cur = conn.cursor()
    data = cur.execute(
        "SELECT id, type FROM html_blocks WHERE enquirer = ?", (str(enquirer),)
    ).fetchall()

    block_types = []

    for block in data:
        new_block = dict(block)
        new_block["title"] = str(new_block["type"]).replace("_", " ").upper()
        block_types.append(new_block)

    return jsonify(block_types)


if __name__ == "__main__":
    app.run(debug=True)
