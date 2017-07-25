import unittest
from rules import *
from datetime import datetime, timedelta

class TestRuleEngine(unittest.TestCase):
    def setUp(self):
        self.ruleengine = RuleEngine()

    def test_string_match_success(self):
        # Should pass on validation success
        self.ruleengine.add_rule({"source_id": "ATL2", "operator": "=", "test_data": "HIGH", "type": "String"})
        test_data = [ {"signal": "ATL2", "value_type": "String", "value": "HIGH"} ]
        self.ruleengine.validate_data_stream(test_data, raise_errors=True)

    def test_string_match_fail(self):
        # Check if engine raises error on validation failure
        self.ruleengine.add_rule({"source_id": "ATL3", "operator": "=", "test_data": "HIGH", "type": "String"})
        test_data = [ {"signal": "ATL3", "value_type": "String", "value": "LOW"} ]
        with self.assertRaises(ValidationError):
            self.ruleengine.validate_data_stream(test_data, raise_errors=True)

    def test_string_notequal_success(self):
        self.ruleengine.add_rule({"source_id": "ATL10", "operator": "!=", "test_data": "LOW", "type": "String"})
        test_data = [ {"signal": "ATL10", "value_type": "String", "value": "HIGH"} ]
        self.ruleengine.validate_data_stream(test_data, raise_errors=True)


    def test_string_notequal_fail(self):
        self.ruleengine.add_rule({"source_id": "ATL10", "operator": "!=", "test_data": "LOW", "type": "String"})
        test_data = [ {"signal": "ATL10", "value_type": "String", "value": "LOW"} ]
        with self.assertRaises(ValidationError):
            self.ruleengine.validate_data_stream(test_data, raise_errors=True)


    # Some sensors can return data in more then one data type. For example in raw_data.json
    # ATL9 has its value as Datetime and Integer. We should be able to support this behaviour.
    # Next two test cases are designed to test this situation

    def test_ATL9_as_datetime(self):
        self.ruleengine.add_rule({"source_id": "ATL9", "operator": "nif", "test_data": "", "type": "Datetime"})
        test_data = [ {"signal": "ATL9", "value_type": "Datetime", "value": "2017-06-13 22:40:10"} ]
        self.ruleengine.validate_data_stream(test_data, raise_errors=True)

    def test_ATL9_as_Integer(self):
        self.ruleengine.add_rule({"source_id": "ATL9", "operator": "=", "test_data": 5.534, "type": "Integer"})
        test_data = [ {"signal": "ATL9", "value_type": "Integer", "value": "5.534"} ]
        self.ruleengine.validate_data_stream(test_data, raise_errors=True)

    #
    # following cases test NotInFuture and NotInPast comparisons
    #

    def test_notinfuture_success(self):
        pasttime = datetime.now() - timedelta(days=1) # generate a time 1 day in the past
        str_time = pasttime.strftime("%Y-%m-%d %H:%M:%S")
        self.ruleengine.add_rule({"source_id": "ATL1", "operator": "nif", "test_data": "", "type": "Datetime"})
        test_data = [ {"signal": "ATL1", "value_type": "Datetime", "value": str_time} ]
        self.ruleengine.validate_data_stream(test_data, raise_errors=True)

    def test_notinfuture_fail(self):
        futuretime = datetime.now() + timedelta(days=1) # 1 day in the future
        str_time = futuretime.strftime("%Y-%m-%d %H:%M:%S")
        self.ruleengine.add_rule({"source_id": "ATL1", "operator": "nif", "test_data": "", "type": "Datetime"})
        test_data = [ {"signal": "ATL1", "value_type": "Datetime", "value": str_time} ]
        with self.assertRaises(ValidationError):
            self.ruleengine.validate_data_stream(test_data, raise_errors=True)

    def test_notinpast_success(self):
        #changing nif to nip operator
        futuretime = datetime.now() + timedelta(days=1) # 1 day in the future
        str_time = futuretime.strftime("%Y-%m-%d %H:%M:%S")
        self.ruleengine.add_rule({"source_id": "ATL1", "operator": "nip", "test_data": "", "type": "Datetime"})
        test_data = [ {"signal": "ATL1", "value_type": "Datetime", "value": str_time} ]
        self.ruleengine.validate_data_stream(test_data, raise_errors=True)

    def test_notinpast_fail(self):
        pasttime = datetime.now() - timedelta(days=1) # 1 day in the past
        str_time = pasttime.strftime("%Y-%m-%d %H:%M:%S")
        self.ruleengine.add_rule({"source_id": "ATL1", "operator": "nip", "test_data": "", "type": "Datetime"})
        test_data = [ {"signal": "ATL1", "value_type": "Datetime", "value": str_time} ]
        with self.assertRaises(ValidationError):
            self.ruleengine.validate_data_stream(test_data, raise_errors=True)


if __name__ == '__main__':
    unittest.main()