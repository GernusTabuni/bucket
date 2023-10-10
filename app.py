from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import os
from os.path import join,dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("dbsparta")

client = MongoClient("mongodb+srv://nusyoman:manis@cluster0.wjeaswn.mongodb.net/?retryWrites=true&w=majority")
db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form['bucket_give']
    count = db.bucket.count_documents({})
    num = count + 1
    doc = {
        'num': num,
        'bucket': bucket_receive,
        'done': 0
    }
    db.bucket.insert_one(doc)
    return jsonify({'msg':'data saved!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
   num_receive = request.form['num_give']
   db.bucket.update_one(
      {'num': int(num_receive) },
      {'$set': {'done': 1 }}
   )
   return jsonify({'msg': 'Update done!'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    bucket_list = list(db.bucket.find({}, {'_id': False}))
    return jsonify({'buckets': bucket_list})

@app.route("/bucket/delete", methods=["DELETE"])
def delete_bucket():
    num_to_delete = request.form.get('num_give')
    db.bucket.delete_one({'num': num_to_delete})
    return jsonify({'msg': 'Item deleted successfully'})


if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)