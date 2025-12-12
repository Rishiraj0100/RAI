"""
RAI Project

Copyright 2025 Rishiraj0100

Licensed under the Apache License, Version 2.0 (the "License");
You may not use this file except in compliance with the License.
You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0
"""

from quart import (
    Blueprint,
    redirect,
    request
)

from core import render
from core.db.models import User
from quart_auth import login_user, logout_user, current_user


app = Blueprint('auth', __name__, url_prefix="/")

@app.route('/login', methods=['GET', 'POST'])
async def login():
    if current_user.auth_id is not None:
        return redirect("/")
    if request.method=="GET":
        return await render("auth/login")
    
    form = await request.form
    u = await User.get_or_none(username=form['username'].lower())
    if u and u.verify_password(form['password']):
        login_user(u)
        return redirect(request.referrer or request.headers.get("Referer") or "/")
    
    return await render("auth/login", user=current_user, error=repr("Invalid Credentials"))
    
@app.route('/register', methods=['GET', 'POST'])
async def register():
    if current_user.auth_id is not None:
        return redirect("/")
    if request.method=="GET":
        return await render("auth/register")
    
    form = await request.form
    if await User.get_or_none(username=form["username"].lower()):
        return await render("auth/register", user=current_user, error=repr("Username already taken"))
    
    if await User.get_or_none(email=form["email"].lower()):
        return await render("auth/register", user=current_user, error=repr("Email already registered"))
    
    u=await User.create(username=form["username"].lower(), password=form["password"], role="user", email=form["email"].lower())
    login_user(u)
    return redirect("/")

@app.route("/logout")
async def logout():
    logout_user()
    return redirect("/")
