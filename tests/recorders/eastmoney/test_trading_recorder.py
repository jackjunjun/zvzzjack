# -*- coding: utf-8 -*-
from ...context import init_test_context

init_test_context()

from zvt.consts import SAMPLE_STOCK_CODES

from zvt.recorders.eastmoney.trading.eastmoney_manager_trading_recorder import ManagerTradingRecorder
from zvt.recorders.eastmoney.trading.eastmoney_holder_trading_recorder import HolderTradingRecorder


def test_manager_trading_recorder():
    recorder = ManagerTradingRecorder(codes=SAMPLE_STOCK_CODES)
    try:
        recorder.run()
    except:
        assert False


def test_holder_trading_recorder():
    recorder = HolderTradingRecorder(codes=SAMPLE_STOCK_CODES)
    try:
        recorder.run()
    except:
        assert False
