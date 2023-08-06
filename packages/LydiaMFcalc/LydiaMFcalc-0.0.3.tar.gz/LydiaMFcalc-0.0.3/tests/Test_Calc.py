# execute with: python -m unittest Test_Calc.py
"""
Created on Sun Dec 11 16:28:51 2022

@author: LydiaMF
"""

import unittest
import sys

sys.path.append("../src/LydiaMFcalc/")
from Calc import *


class Test_Calc(unittest.TestCase):

    """
    Tests to check the Calculator class by Lydia Moser-Fischer
    """

    def setUp(self):
        """setUp(self):
        Generate input data.
        """
        self.number1s = [4.0, 1e20, 0, -34567]
        self.number2s = [3.0, 1e30, 0, -8913789]
        self.operations = ["+", "-", "*", "/", "rt", "cijofewouh", "Q", "R"]

    def test_Calc__init__(self):
        """test___init__(self, number1):
        Check if self.result is initialized to number 1 and self.number2
        is set to 0.0
        """

        for number1 in self.number1s:
            for number2 in self.number2s:
                a = Calc(number1)
                self.assertEqual(a.result, float(number1))
                self.assertEqual(a.number2, 0.0)

    def test_add_to(self):
        """test_add_to(self):
        Sum of the last result (or initial value) and number2.
        """

        for number1 in self.number1s:
            for number2 in self.number2s:
                a = Calc(number1)
                self.assertEqual(
                    a.add_to(number2), float(number1) + float(number2)
                )
                self.assertEqual(
                    a.add_to(number2),
                    float(number1) + float(number2) + float(number2),
                )

    def test_subtract_by(self):
        """test_subtract_by(self):
        Difference of the last result (or initial value) and number2.
        """
        for number1 in self.number1s:
            for number2 in self.number2s:
                a = Calc(number1)
                self.assertEqual(
                    a.subtract_by(number2), float(number1) - float(number2)
                )
                self.assertEqual(
                    a.subtract_by(number2),
                    float(number1) - float(number2) - float(number2),
                )

    def test_multiply_by(self):
        """test_multiply_by(self):
        Product of the last result (or initial value) and number2.
        """
        for number1 in self.number1s:
            for number2 in self.number2s:
                a = Calc(number1)
                self.assertEqual(
                    a.multiply_by(number2), float(number1) * float(number2)
                )
                self.assertEqual(
                    a.multiply_by(number2),
                    float(number1) * float(number2) * float(number2),
                )

    def test_divide_by(self):
        """test_divide_by(self):
        Ratio of the last result (or initial value) and number2.
        Exits for division by zero.
        """
        for number1 in self.number1s:
            for number2 in self.number2s:
                a = Calc(number1)
                if number2 == 0.0:
                    self.assertEqual(
                        a.divide_by(number2), "Cannot divide by zero! \n"
                    )
                else:
                    self.assertEqual(
                        a.divide_by(number2), float(number1) / float(number2)
                    )
                    self.assertEqual(
                        a.divide_by(number2),
                        float(number1) / float(number2) / float(number2),
                    )

    def test_root_by(self):
        """test_root_by(self):
        Number2th root of the last result (or initial value).
        """
        for number1 in self.number1s:
            for number2 in self.number2s:
                if number2 >= 0.001:
                    a = Calc(number1)
                    self.assertEqual(
                        a.root_by(number2),
                        float(number1) ** (1 / float(number2)),
                    )
                    self.assertEqual(
                        a.root_by(number2),
                        (float(number1) ** (1 / float(number2)))
                        ** (1 / float(number2)),
                    )
                else:
                    self.assertEqual(
                        a.root_by(number2),
                        "OverflowError: Result too large to handle. \n",
                    )

    def test_reset(self):
        """test_reset(self):
        Resets the first operand (initial value or old result) to 0.0 as
        default or the number that you give.
        """
        for number1 in self.number1s:
            for number2 in self.number2s:
                a = Calc(number1)
                a.reset(number2)
                self.assertEqual(a.result, number2)
                a.reset()
                self.assertEqual(a.result, 0.0)

    def test_translate_operation(self):
        """test_translate_operation(self):
        Offers opportunity to express operations in interactive mode
        like on a real calculator. Allows the strings  +, -, *, / and
        translates them to the functions behind them.
        """
        for number1 in self.number1s:
            for number2 in self.number2s:
                for operation in self.operations:

                    a = Calc(number1)

                    result = number1

                    if operation == "+":
                        result += float(number2)
                        self.assertEqual(
                            a.translate_operation(operation, number2), result
                        )

                    elif operation == "-":
                        result -= float(number2)
                        self.assertEqual(
                            a.translate_operation(operation, number2), result
                        )

                    elif operation == "*":
                        result *= float(number2)
                        self.assertEqual(
                            a.translate_operation(operation, number2), result
                        )

                    elif operation == "/":
                        if number2 == 0.0:
                            self.assertEqual(
                                a.divide_by(number2),
                                "Cannot divide by zero! \n",
                            )
                        else:
                            result /= float(number2)
                            self.assertEqual(
                                a.translate_operation(operation, number2),
                                result,
                            )

                    elif operation == "rt":
                        if number2 >= 0.001:
                            result **= 1 / float(number2)
                            self.assertEqual(
                                a.translate_operation(operation, number2),
                                result,
                            )
                        else:
                            self.assertEqual(
                                a.translate_operation(operation, number2),
                                "OverflowError: "
                                "Result too large to handle. \n",
                            )

                    else:
                        result = "I do not know this operator", operation, "."
                        self.assertEqual(
                            a.translate_operation(operation, number2), result
                        )


if __name__ == "__main__":
    unittest.main()
