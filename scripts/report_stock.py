# -*- coding: utf-8 -*-
from examples.data_runner.kdata_runner import record_stock_data
from examples.reports.report_tops import report_top_stocks, report_top_blocks
from examples.reports.report_vol_up import report_vol_up_stocks

if __name__ == "__main__":
    record_stock_data()

    report_top_stocks()
    report_top_blocks()
    report_vol_up_stocks()
