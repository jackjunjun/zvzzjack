# -*- coding: utf-8 -*-
from ...context import init_test_context

init_test_context()

from zvt.consts import SAMPLE_STOCK_CODES

from zvt.recorders.eastmoney.finance.eastmoney_finance_factor_recorder import ChinaStockFinanceFactorRecorder
from zvt.recorders.eastmoney.finance.eastmoney_cash_flow_recorder import ChinaStockCashFlowRecorder
from zvt.recorders.eastmoney.finance.eastmoney_balance_sheet_recorder import ChinaStockBalanceSheetRecorder
from zvt.recorders.eastmoney.finance.eastmoney_income_statement_recorder import ChinaStockIncomeStatementRecorder


def test_finance_factor_recorder():
    recorder = ChinaStockFinanceFactorRecorder(codes=SAMPLE_STOCK_CODES)
    try:
        recorder.run()
    except:
        assert False


def test_cash_flow_recorder():
    recorder = ChinaStockCashFlowRecorder(codes=SAMPLE_STOCK_CODES)
    try:
        recorder.run()
    except:
        assert False


def test_balance_sheet_recorder():
    recorder = ChinaStockBalanceSheetRecorder(codes=SAMPLE_STOCK_CODES)
    try:
        recorder.run()
    except:
        assert False


def test_income_statement_recorder():
    recorder = ChinaStockIncomeStatementRecorder(codes=SAMPLE_STOCK_CODES)
    try:
        recorder.run()
    except:
        assert False
