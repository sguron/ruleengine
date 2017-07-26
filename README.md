Overview
=========
Author: Sukhneer Guron ( sukhneer@guron.in)

Rate engine is implemented in class RateEngine inside rules.py along with various validators for different data types.

I have written and tested this code on an OSX Sierra system. Targeted python version is 3.5+ however it should run on python2.7 aswell.

Instructions
============

Change to source directory and execute the following

`python3 main.py`

or

`python main.py`

I have also included an example list of rules in example.json. You can simply copy paste these to rules.json to get started quickly

Tests
=====

Test cases can be executed by

`python3 tests.py`

or 

`python tests.py`


Discussion Questions
====================


**1 ) Briefly describe the conceptual approach you chose! What are the trade-offs?**

I decided to write a very clean implementation of this challenge in python. Although its possible to massively optimize the implementation I have chosen not to do so at the moment for the simple reason that I wanted to present an easily readable codebase. Every type of value has its own validator class which knows how to correctly parse the data from a string and applies any of the valid matching operators to the item. The matching operations are read from a json encoded text file at startup. Every time a new rule is added that text file is updated.

Trade offs:
Since rules are read from and stored in a text file it would not be easily possible to have multiple running instances of RuleEngine. Reason being dirty read/write on the text file. The implementation is also not as fast as possible. 


**2) What's the runtime performance? What is the complexity? Where are the bottlenecks?**

At the moment the code is processing input data linearly and for every signal there may be one or more rules that would have to be applied to it. Rules are stored in a hashtable with signal name as the key. So for every incoming datapoint only those rules are fetched and iterated through that apply to this signal specifically.

The primary bottleneck I see is the linear processing of data stream and the overhead introduced by python's interpreter.


**3) If you had more time, what improvements would you make, and in what order of priority?**

a) In a real word scenario the data stream would most likely be read from a network socket or from a unix pipe. I would like to write a multi-threaded streaming implementation that would run a separate thread for every data source in the system. The primary stream fetcher thread would read the incoming data and put the data item in the source's validator thread queue for processing. This would enable to validate more than 1 data item at a time. It will increase the concurrency of the algorithm and overall processor utilization.

b) If performance is the most important criteria I would rewrite this in a more processor efficient language like Go or C++ to squeeze out evey last bit of performance.

c) It is possible to decrease the time complexity of various validators. For example, by clever coding equal-to matching can be clubbed with greater-than-equalto operator and decrease the time complexity of IntegerValidator. There are more similar avenues for optimization in the code.

d) I would also have liked to write a GUI wrapper for RuleEngine. I had initially wanted to use PyGTK to make an interface similar to wireshark (a network packet processor). I specifically like the way it allows one to form complex matching patterns to apply to various attributes of incoming packets. However this would have required adding a huge external dependency and a lot of time to implement.

e) Write more tests cases. There can never be a shortage of tests !


Demo Output
===========

~~~~
$ python3 main.py

MAIN  MENU
==========
1) Process raw_data.json
2) Add new rule
3) Clear all rules
4) Exit

Select an option [1, 2, 3, 4]: 2

CREATE RULE
===========

Signal name: ATL5
Value type [1=String, 2=Integer, 3=Datetime]: 1
Select operator 0=Match 1=Must not match: 0

Enter test value: HIGH


NEW RULE ADDED


MAIN  MENU
===========
1) Process raw_data.json
2) Add new rule
3) Clear all rules
4) Exit
Select an option [1, 2, 3, 4]: 1


PROCESSING raw_data.json


ATL5: Signal must be HIGH was LOW

ATL5: Signal must be HIGH was LOW
~~~~


License
=======
Copyright(c) 2017 Sukhneer Guron

Source released under GPL v3 - see LICENSE file for more info
