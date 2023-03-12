import requests
import pandas as pd
import sqlite3
from flask import Flask, jsonify


app = Flask(__name__)

def save_data(external_data):
    database = 'DBcomments.db'
    conn = sqlite3.connect(database)

    #conveting json -> dictionary 

    dict_table = {
        'postId':[],
        'id':[],
        'name':[],
        'email':[],
        'body':[]
        }
    for dict_ in external_data:
        for key in dict_table.keys():
            dict_table[key].append(dict_[key])
    #dictionary -> panda table
    dataframe = pd.DataFrame(dict_table)
    dataframe.to_sql(name='Users', con=conn, if_exists='replace')

@app.route('/')
def get_external_data():
    # Make a request to the external API
    response = requests.get('https://jsonplaceholder.typicode.com/posts/1/comments')

    # Check if the request was successful
    if response.status_code != 200:
        return jsonify({'error': 'Failed to get data from external API'})

    # Extract the data from the response
    data = response.json()
    save_data(data)
    #Here I'm returning the data and status
    return jsonify(
        {'Status: ':{"Status code":response.status_code,'Progress: ':"Data downloaded to sqlite database"}})
#runs the flasks as a server
if __name__=="__main__":
    app.run()

