from flask import Flask
from app.config import Config, load_config

config: Config = load_config()
app = Flask(__name__)
