#import redis
import sys
import time
from flask import Flask
from flask import render_template
from flask import request
from pymongo import MongoClient
from werkzeug import secure_filename

app = Flask(__name__)
#cache = redis.Redis(host='redis', port=6379)

#def get_hit_count():
#    retries = 5
#    while True:
#        try:
#            return cache.incr('hits')
#        except redis.exceptions.ConnectionError as exc:
#            if retries == 0:
#                raise exc
#            retries -= 1
#            time.sleep(0.5)

@app.route( '/' )
def home():
    version = str( sys.version_info[ 0 ] ) + '.' + str( sys.version_info[ 1 ] )
    message = 'python version: ' +  version

    user = { 'username': 'Darve' }

    return render_template( 'home.html', user=user, title='Moneys' )

@app.route( '/import' )
def importThings():
    return render_template( 'import.html' )

@app.route( '/import-transactions' )
def importTransactions():
    return render_template( 'import_transactions.html' )

@app.route( '/importTransactionsCsv', methods=['GET', 'POST'] )
def importTransactionsCsv():
    if request.method == 'POST':
        transactionsFile = request.files[ 'file' ]
        secureFilename = secure_filename( transactionsFile.filename )
        transactionsFile.save( secureFilename )

        content = 'file:'
        realFile = open( secureFilename, 'r' )
        for line in realFile:
            content += line

        mongoClient = MongoClient( 'finances-mongodb' )
        db = mongoClient.finances_db
        result = db.test_transactions.insert( { "name":"dave", "age":"34" } )

    return content

#@app.route('/hello')
#def hello():
#    count = get_hit_count()
#    return 'Hello World! I have been seen {} times.\n'.format(count)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
