import datetime
import sys
import time
from flask import Flask
from flask import render_template
from flask import request
from werkzeug import secure_filename

import finances.thing
import finances.datamodel
import finances.datastore
import finances.importer
import finances.transactions

app = Flask(__name__)

@app.route( '/' )
def home():
    version = str( sys.version_info[ 0 ] ) + '.' + str( sys.version_info[ 1 ] )
    message = 'python version: ' +  version

    user = { 'username': 'Rick Sanchez' }

    test = finances.thing.test01()

    # retrieve account list
    data_manager = finances.datastore.MongoDataManager()
    accounts = data_manager.get_accounts()

    monthly_evaluation_criteria_list = []

    monthly_evaluation_criteria = finances.datamodel.MonthlyEvaluationCriteria()
    monthly_evaluation_criteria.start_date = "none"
    monthly_evaluation_criteria.end_date = "none"

    monthly_evaluation_criteria_list.append( monthly_evaluation_criteria )

    monthly_income_vs_expenses_model_manager = finances.datamodel.MonthlyIncomeVsExpensesModelManager( data_manager )
    monthly_income_vs_expenses_model = monthly_income_vs_expenses_model_manager.build_monthly_income_vs_expenses_model( monthly_evaluation_criteria_list )

    chart_builder = graphs.ChartBuilder()
    path_to_monthly_income_vs_expenses_bar_chart = chart_builder.build_monthly_income_vs_expenses_bar_chart( monthly_income_vs_expenses_model )

    # DEBUG
    accounts_string = ''
    prefix = ''
    for account in accounts:
        accounts_string += prefix + account
        prefix = ','

    return render_template(
        'home.html',
        user=user,
        title=test,
        python_version=version,
        debug=path_to_monthly_income_vs_expenses_bar_chart
    )

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

    return render_template(
        'import_transactions_result.html',
        account = account,
        updated_transaction_count = result[ 'updated_transaction_count' ],
        new_transaction_count = result[ 'new_transaction_count' ]
    )

@app.route( '/report' )
def report():
    return render_template( 'report.html' )

if __name__ == "__main__":
    app.run( host="0.0.0.0", debug=True )

