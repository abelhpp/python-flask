from src.blog import blog
from flask import request, jsonify, Blueprint, abort
from flask_pymongo import ObjectId, MongoClient
from datetime import datetime
import pymongo
from flask import Blueprint
from src.extinsions import mongo

#connention_str = 'mongodb://localhost/'
#client = MongoClient(mongo)
#mongo.db = client.myBlogApp.blog

# http://localhost:5000/blog/new
@blog.route('/new', methods = ['GET'])
def new_blog():

    return "hola"

@blog.route('/get',methods = ['POST', 'GET'])
def login():
    docs = []
    for doc in db.find():
        docs.append({
            'title': doc['title'],
            'body': doc['body'],
            'date': doc['date']
        })
    return jsonify({'blogs': docs})


