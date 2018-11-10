from flask import Flask
import os

template_dir = os.path.abspath('/frontend/javasc/templates')

app = Flask(__name__, template_folder='/Users/shantanu/Documents/hackAD18/app/frontend/javasc/templates/')


from app import routes
