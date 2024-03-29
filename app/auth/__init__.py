from flask import Flask, Blueprint

auth_bp = Blueprint('auth', __name__)

from app.auth import controller