"""
RAI Project

Copyright 2025 Rishiraj0100

Licensed under the Apache License, Version 2.0 (the "License");
You may not use this file except in compliance with the License.
You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0
"""

from tortoise.contrib.quart import register_tortoise


TORTOISE_CONFIG = {
    'connections': {
        'default': 'sqlite://core/db/db.sqlite'
    },
    'apps': {
        'models': {
            'models': ['core.db.models', 'aerich.models'],
            'default_connection': 'default',
        }
    }
}

def init(app):
    register_tortoise(app, config=TORTOISE_CONFIG, config_file=None, db_url=None, modules=None, generate_schemas=True)