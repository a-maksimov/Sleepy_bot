Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)] on win32
Type "copyright", "credits" or "license()" for more information.
>>> with serial.Serial('COM7', 9600, timeout=1) as ser:
    line = ser.readline()   # read a '\n' terminated line
print(line)         # check which port was really used
ser.close()         # close port
SyntaxError: invalid syntax
>>> with serial.Serial('COM7', 9600, timeout=1) as ser:
	line = ser.readline()   # read a '\n' terminated line

	

Traceback (most recent call last):
  File "<pyshell#3>", line 1, in <module>
    with serial.Serial('COM7', 9600, timeout=1) as ser:
NameError: name 'serial' is not defined
>>> import serial
>>>  with serial.Serial('COM7', 9600, timeout=1) as ser:
	line = ser.readline()   # read a '\n' terminated line
	
  File "<pyshell#5>", line 2
    with serial.Serial('COM7', 9600, timeout=1) as ser:
    ^
IndentationError: unexpected indent
>>> with serial.Serial('COM7', 9600, timeout=1) as ser:
	line = ser.readline()   # read a '\n' terminated line
	print(line)

24.2 22.0 20.0

>>> ser.close()
>>> 
>>> 
