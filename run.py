import time

from los_support.report_sale import ReportSale

with ReportSale() as reportSale:
    reportSale.login()
    reportSale.go_to_sale_report()
    time.sleep(10000000)
