"""
RAI Project

Copyright 2025 Rishiraj0100

Licensed under the Apache License, Version 2.0 (the "License");
You may not use this file except in compliance with the License.
You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0
"""

import routes

from quart import (
    Quart,
    redirect,
    request,
)
from core import render, db
from core.db.models import User, ContactForum
from quart_auth import QuartAuth, login_required, current_user


app = Quart(__name__)

DEBUG = __name__ == "__main__"
app.config['DEBUG'] = DEBUG
app.config["QUART_AUTH_SECRET_KEY"] = app.secret_key = "ghjkl"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SESSION_COOKIE_SECURE'] = True

db.init(app)
QuartAuth(app)
routes.load(app)

@app.route("/")
@login_required
async def index():
    return await render("dashboard")

if DEBUG:
    @app.route("/x")
    async def generate_admin_user():
        await User.create(username="admin", password="admin", role="admin", email="admin@admin")

        return "Created admin user"

@app.route("/privacy_policy")
async def privacy_policy():
    return await render("privacy_policy")

@app.route("/tos")
async def terms_of_service():
    return await render("tos")

@app.route("/contact", methods=["GET", "POST"])
async def contact():
    if request.method == "GET":
        return await render("contact")
    
    form = await request.form
    name = form.get("name")
    email = form.get("email") or (await User.get(id=current_user.auth_id)).email
    message = form.get("message")
    subject = form.get("subject") or "No Subject"

    await ContactForum.create(name=name, email=email, message=message, subject=subject)
    return await render("contact", success=repr("Your message has been sent successfully!"))

@app.errorhandler(403)
async def forbidden(e):
    return redirect("/")

@app.errorhandler(401)
async def unauthorized(e):
    return redirect("/login")

@app.errorhandler(404)
async def not_found(e):
    return await render("404"), 404

if DEBUG:
    app.run("localhost", 8090, debug=DEBUG)