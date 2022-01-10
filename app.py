rom flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

host = os.environ.get("DB_URL")
client = MongoClient(host=host)

db = client.autocentral

#RESOURCES
users = db.users
comments = db.comments

app = Flask(__name__)

app.secret_key = '9a5c0aaf287745d3b21bb5a22e6dahewfef0e9c8fbr3bc39e34474f2f400f57'