"""
RAI Project

Copyright 2025 Rishiraj0100

Licensed under the Apache License, Version 2.0 (the "License");
You may not use this file except in compliance with the License.
You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0
"""


import ollama

from quart import (
    Blueprint,
    request,
    redirect,
    jsonify,
    abort,
    current_app
)
from core import render
from functools import wraps
from core.db.models import ModelRecord, User
from quart_auth import login_required, current_user


app = Blueprint("models", __name__, url_prefix='/models/')
engines = ["llama3.2"]


def check_model_existence(f):
    @wraps(f)
    async def decor(*a, **k):
        model_name = k.get("model_name", None)
        if model_name:
            model_name = model_name.lower()
            model = await ModelRecord.get_or_none(username=model_name)
            if not model:
                return abort(404)
        
        return await current_app.ensure_async(f)(*a, **k)

    return decor

@app.route("/new/", methods=["GET", "POST"])
@login_required
async def create():
    if request.method == "GET":
        return await render("models/create", engines=engines)
    
    data = await request.form
    engine = data.get("engine")
    name = data.get("name")
    description = data.get("description")
    backstory = data.get("backstory")
    
    try:
        await ModelRecord.get(username=name.lower().replace(" ", "_"))
        return await render("models/create", engines=engines, error=repr("Model with this name already exists."))
    except:
        pass

    ollama.create(
        model="rai/"+name.lower().replace(" ", "_"),
        from_=engine,
        system=f"""You are an AI assistant. The user has provided the following backstory and description for you to help you understand your purpose better.
        This is your name: {name}
        This is your description: {description}
        This is your backstory: {backstory}""",
    )
    await ModelRecord.update_or_create(
        name=name,
        username=name.lower().replace(" ", "_"),
        engine=engine,
        owner=await User.get(id=current_user.auth_id),
        description=description,
        backstory=backstory
    )
    return redirect("/")

@app.route("/<model_name>/", methods=["GET", "DELETE"])
@check_model_existence
async def model_detail(model_name):
    model_name = model_name.lower()
    try:
        model = await ModelRecord.get(username=model_name).prefetch_related("owner")
    except:
        return abort(404)

    if request.method == "GET":
        return await render("models/detail", model=model)
    
    if current_user.auth_id is None:
        return abort(401)
    
    cu = await User.get(id=current_user.auth_id)
    
    if (model.owner.id != cu.id) and not cu.admin:
        return abort(403)
    
    ollama.delete(model="rai/"+model_name)
    await model.delete()
    return redirect("/")

@app.route("/<model_name>/chat/", methods=["GET", "POST"])
@login_required
@check_model_existence
async def model_chat(model_name):
    model_name = model_name.lower()
    model = await ModelRecord.get_or_none(username=model_name).prefetch_related("owner")

    if request.method == "GET":
        return await render("models/chat", model=model)
    

    msgs = (await request.json).get('messages', '')
    response = ollama.chat(model="rai/"+model_name, messages=msgs)
    return jsonify({"response": response.message.content})

@app.route("/<model_name>/edit/", methods=["GET", "POST"])
@login_required
@check_model_existence
async def edit_model(model_name):
    model_name = model_name.lower()
    model = await ModelRecord.get(username=model_name).prefetch_related("owner")
    if model.owner.id != (await User.get(id=current_user.auth_id)).id:
        return abort(403)
    
    if request.method == "GET":
        return await render("models/edit", model=model, engines=engines)
    
    data = await request.form
    engine = data.get("engine")
    name = data.get("name")
    description = data.get("description")
    backstory = data.get("backstory")

    ollama.create(
        model="rai/"+model_name.lower().replace(" ", "_"),
        from_=engine,
        system=f"""You are an AI assistant. The user has provided the following backstory and description for you to help you understand your purpose better.
        This is your name: {name}
        This is your description: {description}
        This is your backstory: {backstory}""",
    )
    model.name=name
    model.engine=engine
    model.description=description
    model.backstory=backstory
    await model.save()
    return redirect(f"/models/{model_name}/")