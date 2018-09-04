#!/bin/python

import sys
import finances.finances.datamodel
import finances.finances.datastore

def test01():
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
