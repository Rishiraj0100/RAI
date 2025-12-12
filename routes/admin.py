"""
RAI Project

Copyright 2025 Rishiraj0100

Licensed under the Apache License, Version 2.0 (the "License");
You may not use this file except in compliance with the License.
You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0
"""

from quart import (
    Blueprint,
    request,
    redirect,
    jsonify,
    current_app,
    abort
)

from core import render
from functools import wraps
from core.db.models import User, ContactForum
from quart_auth import current_user, login_required


app = Blueprint("admin", __name__, url_prefix='/admin/')

def admin_only(f):
    @wraps(f)
    @login_required
    async def decor(*a, **k):
        user = await User.get(id=current_user._auth_id)
        if not user:
            return abort(401)
        if not user.admin:
            return abort(403)
        
        return await current_app.ensure_async(f)(*a, **k)

    return decor

@app.route("/")
@admin_only
async def dashboard():
    return await render("admin/dashboard")

@app.route("/users/")
@admin_only
async def user_management():
    users = await User.all()
    return await render("admin/users", users=users)

@app.route("/users/<int:user_id>/", methods=["GET", "DELETE"])
async def userinfo(user_id):
    user = await User.get(id=current_user._auth_id)
    if not user:
        return abort(401)
    
    if user_id != user.id and not user.admin:
        return abort(403)

    user = await User.get_or_none(id=user_id)
    if not user:
        return abort(404)
    
    if request.method == "GET":
        return await render("admin/userinfo", user_info=user)
    
    await user.delete()
    return jsonify(dict(message = "Successfully deleted user.")), 200


@app.route("/contact_messages/")
@admin_only
async def contact_messages():
    messages = await ContactForum.all().order_by('-created_at')
    return await render("admin/contact_messages", messages=messages)

@app.route("/contact_messages/<int:message_id>/", methods=["DELETE"])
@admin_only
async def delete_contact_message(message_id):
    message = await ContactForum.get_or_none(id=message_id)
    if not message:
        return abort(404)
    
    await message.delete()
    return jsonify(dict(message = "Successfully deleted contact message.")), 200