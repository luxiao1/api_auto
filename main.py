import unittest
import unittestreport
import setting

if __name__ == "__main__":
    ts = unittest.defaultTestLoader.discover(setting.TEST_CASE_DIR)
    runner = unittestreport.TestRunner(ts,**setting.REPORT_CONFIG)
    runner.run()
