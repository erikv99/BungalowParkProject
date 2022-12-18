from flask_sqlalchemy import SQLAlchemy
import os
from __main__ import app

class DatabaseHelper():

    def __init__(self):

        self.db = SQLAlchemy(app)