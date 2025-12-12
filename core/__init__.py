"""
RAI Project

Copyright 2025 Rishiraj0100

Licensed under the Apache License, Version 2.0 (the "License");
You may not use this file except in compliance with the License.
You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0
"""

from .db.models import User
from quart_auth import current_user, login_required
from quart import (
    request,
    current_app,
    render_template,
    abort,
    redirect
)
from functools import wraps


async def render(content, **context):
    user = context.get("user", current_user)
    if user.auth_id != None:
        try:
            user = await User.get(id=user.auth_id)
        except:
            return redirect("/logout")
        
        context['user'] = user
        context['ais'] = await user.models.all()
        context['is_admin'] = (user.role == "admin")

    return await render_template(content+".jinja", **context)
