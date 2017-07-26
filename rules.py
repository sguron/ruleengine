import json
from datetime import datetime
import sys


MATCH = "="
GREATERTHAN = ">"
LESSTHAN = "<"
NOTEQUAL = "!="
GREATERTHANEQUAL = ">="
LESSTHANEQUAL = "<="
NOTINFUTURE = "nif"
NOTINPAST = "nip"


class ValidationError(Exception):
	pass

class StringValidator(object):
	@staticmethod
	def convert_data(data):
		"""
		data => str
		
		Returns => str
		"""
		# Just check if data is a string type
		return data

	@classmethod
	def validate(cls, operator, test_data, data):
		"""
		Validates data according to given parameters

		operator => string
		test_data => string
		data => string

		Returns => boolean;  True if data is valid
		Raises => ValidationError on invalid data

		"""
		if operator == MATCH:
			if test_data == data:
				return True
			else:
				raise ValidationError("Signal must be " + test_data + " was " + data)
		
		elif operator == NOTEQUAL:
			if test_data != data:
				return True
			else:
				raise ValidationError("Signal must not be " + test_data + " was " + data)
		
		else:
			return True


class DatetimeValidator(object):
	@staticmethod
	def convert_data(data):
		"""
		data is in string format and must be converted to a python datetime object
		
		data => str
		
		Returns => datetime.datetime instance
		"""
		if data == '':
			return None
		
		try:
			return datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
		except:
			raise ValidationError("Signal data was in invalid format")

	@classmethod
	def validate(cls, operator, test_data, data):
		"""
		Validates data according to given parameters

		operator => string
		test_data => string, format=datetime
		data => string, format=datetime

		Returns => boolean;  True if data is valid
		
		raises => ValidationError on invalid data

		"""
		time_now = datetime.now()
		data = cls.convert_data(data)
		str_data = str(data)

		if operator == NOTINPAST:
			if data >= time_now:
				return True
			else:
				raise ValidationError("Date must not be in past WAS " + str_data )	

		elif operator == NOTINFUTURE:
			if data <= time_now:
				return True
			else:
				raise ValidationError("Date must not be in future WAS " + str_data )	

		str_test_data = str(test_data)
		

		if operator == GREATERTHAN:
			if data > test_data:
				return True
			else:
				raise ValidationError("Date must be after " + str_test_data + " NOT " + str_data)	

		elif operator == LESSTHAN:
			if data < test_data:
				return True
			else:
				raise ValidationError("Date must be before " + str_test_data + " NOT " + str_data)	

class IntegerValidator(object):
	@staticmethod
	def convert_data(data):
		"""
		data is provided in string format and must be converted to float before validation
		
		data => str
		
		Returns float instance
		"""
		try:
			return float(data)
		except:
			raise ValidationError("Signal data was in invalid format")

	@classmethod
	def validate(cls, operator, test_data, data):
		"""
		Validates data according to given parameters

		operator => string
		test_data => float
		data => string, format=float

		Returns => boolean;  True if data is valid

		raises => ValidationError on invalid data

		"""
		str_data = data
		data = cls.convert_data(data)
		str_test_data = str(test_data)

		if operator == MATCH:
			if data == test_data:
				return True
			else:
				raise ValidationError("Signal must be " + str_test_data + " NOT " + str_data)

		elif operator == NOTEQUAL:
			if data != test_data:
				return True
			else:
				raise ValidationError("Signal must be " + str_test_data + " NOT " + str_data)		

		elif operator == GREATERTHAN:
			if data > test_data:
				return True
			else:
				raise ValidationError("Signal must be greater than " + str_test_data + " NOT " + str_data)	

		elif operator == LESSTHAN:
			if data < test_data:
				return True
			else:
				raise ValidationError("Signal must be less than " + str_test_data + " NOT " + str_data)	

		elif operator == GREATERTHANEQUAL:
			if data >= test_data:
				return True
			else:
				raise ValidationError("Signal must be greater or equal to " + str_test_data + " NOT " + str_data)	

		elif operator == LESSTHANEQUAL:
			if data <= test_data:
				return True
			else:
				raise ValidationError("Signal must be less then or equal to " + str_test_data + " NOT " + str_data)	


class Rule(object):
	VALIDATORS = {
					"String" : StringValidator,
					"Datetime": DatetimeValidator,
					"Integer": IntegerValidator
	}

	def __init__(self, type, operator, test_data):
		self.type = type
		self.validator = self.VALIDATORS[type]
		self.operator = operator
		# self.test_data = test_data

		# parse value of test date from string
		self.test_data = self.validator.convert_data(test_data)

	def validate(self, data):
		return self.validator.validate(self.operator, self.test_data, data)  
		# This will either return True or raise a validation error

class RuleEngine(object):
	def __init__(self):
		self.rules = { }  # {"Signal1": [ *List of rules*], "Signal2": [*List of Rules* ]}
		pass

	def load_rules_file(self, filename = 'rules.json'):
		"""
		Function loads and parses a json encoded rules file. 
		Adds parsed rules to the engine

		filename => str; path to rules file

		Returns => None
		"""

		f = open(filename, 'r')
		filedata = f.read()
		f.close()

		rules = json.loads(filedata)

		for rule in rules:
			self.add_rule(rule)

	def write_rules_file(self, filename = 'rules.json'):
		rules_list = []
		for source_id, rules in self.rules.items():
			for item in rules:
				rule = { 'source_id': source_id, 'type': item.type, "operator": item.operator, "test_data": item.test_data  }
				rules_list.append(rule)

		data = json.dumps(rules_list)

		f = open(filename, 'w')
		f.write(data)
		f.close()

	def add_rule(self, rule):
		"""
		Adds rule to engine

		rule => dictionary; format = {"source_id": "ATL5", "type": "Integer", "operator": "<", "test_data": 25.5}

		Returns => None
		"""
		source_id = rule['source_id']
		rule = Rule( rule['type'], rule['operator'], rule['test_data'] )
		
		if source_id not in self.rules:
			self.rules[source_id] = []

		self.rules[source_id].append(rule)

	def clear_rules(self):
		self.rules = { }
		self.write_rules_file()

	def validate_data_stream(self, data_stream, raise_errors=False):
		"""
		This function takes data, determines source name and applies a set of rules to the signal value

		data_stream => iterable type; (currently just a list of dictionaries)

		Returns => None
		"""
		for item in data_stream:
			signal_name = item['signal']
			value = item['value']
			if signal_name in self.rules:
				try:
					for rule in self.rules[signal_name]:
						if rule.type == item['value_type']:
							rule.validate(value)
				except ValidationError as e:
					if raise_errors:
						raise
					else:
						print(signal_name + ": " + str(e))

if __name__ == "__main__":
	ruleengine = RuleEngine()
	ruleengine.load_rules_file()

	datastream = open('raw_data.json', 'r').read()
	datastream = json.loads(datastream)

	#ruleengine.validate_data_stream(datastream)
	





