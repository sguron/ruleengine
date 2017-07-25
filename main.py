from rules import RuleEngine, MATCH, GREATERTHAN, LESSTHAN, NOTEQUAL, GREATERTHANEQUAL, LESSTHANEQUAL, NOTINFUTURE, NOTINPAST
import sys
import json
from datetime import datetime

#
# This file is just a menu wrapper on RulesEngine (rules.py)
#

try: 
	input = raw_input
	# for compatibility with python 2.7
except NameError:
	pass

STRING = "String"
INTEGER = "Integer"
DATETIME = "Datetime"

ruleengine = RuleEngine()

def main_manu():
	"""
	Displays main menu and processes item selection.

	"""
	while True:
		print("\n\nMAIN  MENU\n==========\n1) Process raw_data.json\n2) Add new rule \n3) Clear all rules\n4) Exit")
		option = input("Select an option [1, 2, 3, 4]: ")
		if option == "1":
			datastream = open('raw_data.json', 'r').read()
			datastream = json.loads(datastream)
			print("\n\nPROCESSING raw_data.json\n\n")
			ruleengine.validate_data_stream(datastream)
		elif option == "2":
			add_rule()
		elif option == "3":
			ruleengine.clear_rules()
		elif option == "4":
			sys.exit()
		else:
			print("'%s' is an invalid option. Please try again." % option)

def add_rule():
	"""
	Processes the form for adding a new rule to the ruleengine
	"""
	print("\n\nCREATE RULE\n===========\n")
	operators = []

	while True:
		signal_name = input("Signal name: ")
		if signal_name == "":
			print("Name must not be blank")
			continue
		break

	while True:
		value_type = input("Value type [1=String, 2=Integer, 3=Datetime]: ")
		if value_type == "":
			print("Value type must not be blank")
			continue
		elif value_type not in ['1', '2', '3']:
			print("Invalid value type")
			continue

		if value_type == '1':
			value_type = STRING
			operators = [ (MATCH, "Match"), (NOTEQUAL, "Must not match") ]
		elif value_type == '2':
			value_type = INTEGER
			operators = [ (MATCH, "EqualTo"), (NOTEQUAL, "NotEqualsTo"), (LESSTHAN, "LessThan"),
						 (GREATERTHAN, "GreaterThan"), (LESSTHANEQUAL, "LessThanEqual"), (GREATERTHANEQUAL, "GreaterThanEqual") ]
		elif value_type == '3':
			value_type = DATETIME
			operators = [ (NOTINFUTURE, "NotInFuture"), (NOTINPAST, "NotInPast"), (LESSTHAN, "BeforeDate"), (GREATERTHAN, "AfterDate"),  ]
		break

	items = enumerate([item[1] for item in operators])
	choices = " ".join(["%d=%s" % item for item in items] )

	while True:	
		choice = input("Select operator " + choices + ": ")
		try:
			choice = int(choice)
		except:
			print("Invalid value")
			continue

		if choice < 0 or choice > len(operators)-1:
			print("Enter a value between 0 and %d" % (len(operators)-1))
			continue

		operator = operators[choice][0]
		break

	if operator in [NOTINPAST, NOTINFUTURE]:
		ruleengine.add_rule({"source_id": signal_name, "type": value_type, "operator": operator, "test_data": ""})
		ruleengine.write_rules_file()
		print("\n\nNEW RULE ADDED")
		return

	while True :
		value = input("Enter test value: ")
		if value == "":
				print("Please enter a value")
				continue

		if value_type == STRING:
			break

		if value_type == INTEGER:
			try:
				value = float(value)
				break
			except:
				print("Invalid value. Try again.")
				continue

		if value_type == DATETIME:
			try:
				datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
				break
			except:
				print("Invalid value. Please enter date in YYYY-MM-DD HH:MM:SS format")

	ruleengine.add_rule({"source_id": signal_name, "type": value_type, "operator": operator, "test_data": value})
	ruleengine.write_rules_file()
	print("\n\nNEW RULE ADDED")

if __name__== "__main__":
	ruleengine.load_rules_file()
	main_manu()