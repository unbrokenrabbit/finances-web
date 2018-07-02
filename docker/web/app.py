#import redis
import datetime
import sys
import time
from flask import Flask
from flask import render_template
from flask import request
from werkzeug import secure_filename

import finances.thing
import finances.datastore
import finances.importer
import finances.transactions

app = Flask(__name__)

@app.route( '/' )
def home():
    version = str( sys.version_info[ 0 ] ) + '.' + str( sys.version_info[ 1 ] )
    message = 'python version: ' +  version

    user = { 'username': 'Laniea Lawson' }

    test = finances.thing.test01()

    #return render_template( 'home.html', user=user, title='Finances', python_version=version )
    return render_template( 'home.html', user=user, title=test, python_version=version )

@app.route( '/import' )
def import_things():
    return render_template( 'import.html' )

@app.route( '/import-transactions' )
def import_transactions():
    # retrieve account list
    data_manager = finances.datastore.MongoDataManager()
    accounts = data_manager.get_accounts()   

    return render_template( 'import_transactions.html', accounts=accounts )

@app.route( '/import-transactions-csv', methods=['GET', 'POST'] )
def import_transactions_csv():
    if request.method == 'POST':
        # Save the provided file on the filesystem
        transactions_file = request.files[ 'file' ]
        filename = secure_filename( transactions_file.filename )
        transactions_file.save( filename )

        # Import all transactions from the file
        transaction_importer = finances.importer.CsvTransactionImporter()
        transactions = transaction_importer.import_transactions( filename )

        # Insert and/or update all transactions in the database
        data_manager = finances.datastore.MongoDataManager()
        account = request.form[ "account" ]
        result = data_manager.upsert_transactions( account, transactions )

    return render_template( 'import_transactions_result.html',
                            #account = request.form[ "account" ],
                            account = account,
                            updated_transaction_count = result[ 'updated_transaction_count' ],
                            new_transaction_count = result[ 'new_transaction_count' ] )

@app.route( '/report' )
def report():
    return render_template( 'report.html' )

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
