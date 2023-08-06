# Welcome to Lydia's calculator!



## Install and Import

You can install the LydiaMFcalc package with
```sh
python -m pip install LydiaMFcalc
```

Inside Python you can import the calculator module with
```python
from LydiaMFcalc import Calc as c
```



## General Use

For working in command line/script mode you can create an instance of the 
Calc(ulator) class in the Calc module by calling the class with a starting 
number for your calculations, e.g. 4.0.
```python
a = c.Calc(4)
```
Operations with the next number, e.g. 9.6, can be called like this:
```python
a.add_to(9.6)
```
The next operation is always based on the result of the previous operation, 
i.e. the calculator has a memory. The current result/memory value can be 
accessed by 
```python
a.result
```

The Calc module offers an interactive mode that can be started with e.g.
```python
b = c.Interactive_Calc()
b.activate()
```
In this mode, you are asked to enter the numbers and the operations one 
after the other.



## Operations

The Calc module supports the following mathematical operations which can 
be called in interactive mode by typing the operation sign (string) 
followed by an input request of the number to be applied and by the 
function name with the number to be applied in command line/script mode.

| operation      | interactive mode | class function |
| -------- | -------- | -------- |
| addition       | + | ```add_to(number)```      |
| subtraction    | - | ```subtract_by(number)``` |
| multiplication | * | ```multiply_by(number)``` |
| division       | / | ```divide_by(number)```   |
| n-th root      | rt| ```root_by(number)```     |



## Reset Calculator

It is possible to reset the calculator memory/first operand:
During interactive mode, enter **R** instead of an operation and the 
operand is set to zero. In command line/script mode type
```python
a.reset(optional_number)
```
to reset the operand to an given value or to zero if left blank.



## Leave Interactive Mode

If you want to **quit** the interactive mode, enter **Q** instead of an 
operation.
    
    
    
    
**_~ Have fun! ~_**
