#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 16:28:51 2022

@author: LydiaMF
"""


from typing import Union, Tuple


class Calc:

    """
    Calculator class by Lydia Moser-Fischer
    -----------------------------------------
    How to start:
    - Initialize calulator by calling it with the first number
    e.g. a = Calc(4)

    How to calculate:
    - Proceed by choosing the operation and the next number
    e.g. a.add_to(7) -->  returns: 11.0
    - Choosing the next operation will apply it to the last result
    e.g. a.add_to(7) -->  returns: 18.0

    How to reset:
    - In order to reset the first number of the operation to zero or a
    given value, call the reset function without or with the wanted value
    e.g. a.reset()    --> resets to 0.0
    e.g. a.reset(56)  --> resets to 56.0
    - Continue with calculation as described above

    """

    def __init__(self, number1: float) -> None:
        """__init__(self, number1):
        Initializes the calculator i.e. it gives it a start value (number1).
        This value is stored in a variable self.result that is updated
        by the result of each operation (calculator memory).
        self.result can be reset by the function reset().
        number2 is a placeholder for the numbers used in the upcoming
        operations
        """
        self.result = float(number1)
        self.number2 = 0.0

    def add_to(self, number2: float) -> float:
        """add_to(self, number2):
        Sum of the last result (or initial value) and number2.
        """
        self.result += float(number2)
        return self.result

    def subtract_by(self, number2: float) -> float:
        """subtract_by(self, number2):
        Difference of the last result (or initial value) and number2.
        """
        self.result -= float(number2)
        return self.result

    def multiply_by(self, number2: float) -> float:
        """multiply_by(self, number2):
        Product of the last result (or initial value) and number2.
        """
        self.result *= float(number2)
        return self.result

    def divide_by(self, number2: float) -> Union[float, str]:
        """divide_by(self, number2):
        Ratio of the last result (or initial value) and number2.
        Exits for division by zero.
        """
        if number2 != 0.0:
            self.result /= float(number2)
            return self.result
        else:
            divide_zero = "Cannot divide by zero! \n"
            return divide_zero

    def root_by(self, number2: float) -> Union[float, str]:
        """root_by(self, number2):
        Number2th root of the last result (or initial value).
        """
        if number2 >= 0.001:
            self.result **= 1 / float(number2)
            return self.result
        else:
            exponential_catastrophe = "OverflowError: "\
                                      "Result too large to handle. \n"
            return exponential_catastrophe

    def reset(self, number1: float = 0.0) -> None:
        """
        reset(self, number1=0.0):
        Resets the first operand (initial value or old result) to 0.0 as
        default or the number that you give.
        """
        self.result = float(number1)

    def translate_operation(
        self, operation: str, number2: float
    ) -> Union[float, Tuple[str, str, str], str]:
        # return types for: regular number, unknown_operator, divide_zero
        """
        translate_operation(self, operation):
        --- For interactive mode ---
        Offers opportunity to express operations in interactive mode like
        on a real calculator.
        Allows the strings  +, -, *, /, rt and translates them to the
        functions behind them.
        """
        if operation == "+":
            return self.add_to(number2)
        if operation == "-":
            return self.subtract_by(number2)
        if operation == "*":
            return self.multiply_by(number2)
        if operation == "/":
            return self.divide_by(number2)
        if operation == "rt":
            return self.root_by(number2)

        else:
            unknown_operator = "I do not know this operator", operation, "."
            return unknown_operator


class Interactive_Calc:
    """Interactive_Calc
    Class for interactive mode
    """

    def valid_number(self) -> float:
        """valid_number():
        Checks whether input can be converted into a float. If not, it
        asks for another user input.
        """
        while True:
            try:
                number = float(input("Please enter a number:\n"))
                break
            except ValueError:
                print("Your entry is not a float or integer number.")
        return number

    def activate(self) -> None:
        """activate():
        calls an interactive mode using the calculator
        """

        welcome = """

                      Welcome to Lydia's calculator! \n
        ------------------------------------------------------------- \n
        It allows you to perform additions (+), subtractions (-),
        multiplications (*), divisions (/), and the n-th (number given
        after operator) root (rt) as operations. \n
        If you want to reset the first operand to zero,
        enter R instead of an operation, and if you want to quit, enter Q. \n
        Have fun!
        """

        print(welcome)

        # initialize calculator with starting value
        number1 = self.valid_number()
        calculation = Calc(number1)

        # loop through inputs until you enter Q for quit
        operation = "R"
        while operation != "Q":
            operation = str(
                input(
                    "Please enter an operation ( +, -, *, /, rt) "
                    "or do you want to reset (R) or quit(Q)?: \n"
                )
            )
            if operation != "Q":
                # option to reset calculator
                if operation == "R":
                    calculation.reset()
                    print("")
                    print("Resetting calculator to 0.0")
                    operation = str(
                        input("Please enter an operation "
                              "( +, -, *, /, rt ): \n")
                    )
                else:
                    pass

                number2 = self.valid_number()
                result = calculation.translate_operation(operation, number2)

                # print(f'{number1} {operation} {number2} = {result}')
                print("")
                print(f"Result: {result}")
                print("")
            else:
                pass

        print("")
        print("You pressed Q --> exiting calculator")
        print("See you next time :-)")
        print("")


if __name__ == "__main__":
    a = Interactive_Calc()
    a.activate()
