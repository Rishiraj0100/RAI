"""
RAI Project

Copyright 2025 Rishiraj0100

Licensed under the Apache License, Version 2.0 (the "License");
You may not use this file except in compliance with the License.
You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0
"""

from .import (
    auth,
    models,
    admin
)


def load(app):
    app.register_blueprint(auth.app)
    app.register_blueprint(models.app)
    app.register_blueprint(admin.app)