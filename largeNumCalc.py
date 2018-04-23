"""
** Purpose : To perform basic arithmetic operations on large numbers(size wise) which are greater than 5E-325 and cause underflow
** 
**
**
** Library used: decimal
**
** Features :
** 1. add two numbers
** 2. subtract two numbers
** 3. multiply two numbers
** 4. quotient divide two numbers
** 5. Compare two numbers

--Description---
The main idea is we consider the input "large numbers" as strings, using the python decimal library we tokenize the number into a tuple
consiting of the sign, the exponent and the digits after the decimal.
Using these 3 values we use basic arithmetic to calculate the results and serve as a pseudo large number calculator.
The results are also represented as strings.
--Known Issues---
1. In the addition and subtraction if the difference between the actual values is significantly large I am not yet rounding up the digits
   this is something I will do experimentally based on the datasets

_______________

Usage:
Download the file and store it in a folder,
open a python shell in the folder and do as follows:

from LargeNumCalc import LargeNumberHandler
largeNum_ins = LargeNumberHandler()

# for addition
largeNum_ins.large_num_add('100E-342','100E-340')


# for subtraction
largeNum_ins.large_num_diff('100E-342','100E-340')


# for multiplication
largeNum_ins.large_num_mul('100E-342','100E-340')


# for division
largeNum_ins.large_num_quo('100E-342','100E-340')


# for comparing two numbers
largeNum_ins.large_num_compare('100E-342','100E-340',0/1) [0 - for min, 1 - for max]
_____________
author : Saketh Saxena
Last Updated : 03/27/2018
"""
from decimal import Decimal

class LargeNumberHandler:

    # add two numbers and return a decimal result
    def large_num_add(self,a,b):
        
        # extracting exponenets, signs and digits
        s1, d1, e1 = self.componentize(a)
        s2, d2, e2 = self.componentize(b)

        if e1 == e2:
            return str(d1+d2)+'E'+str(e1)

        elif e1 < e2:
            # the value of d1 is greater than d2
            # since e1 less than e2 means that the decimal e2 occurs much before e1
            # calculate the number of zeroes to be appended to the value of e2(d2) 
            # or more clearly the number of places after decimal where d1 occurs after counting uptil the digits in d1 
            diff_places = e2-e1
            return str(d1+d2*10**diff_places)+'E'+str(e1)

        elif e2 < e1:
            # this is the reverse case of the above scheme
            diff_places = e1-e2
            return str(d1*10**diff_places+d2)+'E'+str(e2)

    # subtract two numbers and return a decimal result
    def large_num_diff(self,a,b):
        
        # extracting exponenets, signs and digits
        s1, d1, e1 = self.componentize(a)
        s2, d2, e2 = self.componentize(b)

        if e1 == e2:
            return str(d1-d2)+'E'+str(e1)

        elif e1 < e2:
            # the value of d1 is greater than d2
            # since e1 less than e2 means that the decimal e2 occurs much before e1
            # calculate the number of zeroes to be appended to the value of e2(d2) 
            # or more clearly the number of places after decimal where d1 occurs after counting uptil the digits in d1 
            diff_places = e2-e1
            return str(d1-d2*10**diff_places)+'E'+str(e1)

        elif e2 < e1:
            # this is the reverse case of the above scheme
            diff_places = e1-e2
            return str(d1*10**diff_places-d2)+'E'+str(e2)

        

    # multiple two numbers and return a decimal result
    def large_num_mul(self,a,b):

        # extracting exponenets, signs and digits
        s1, d1, e1 = self.componentize(a)
        s2, d2, e2 = self.componentize(b)
        
        # The operation to perform is -
        # a * 10^x * b * 10^y we can rewrite it as 
        # a*b *10^(x+y)
        # which in the exponents notation is (a*b)E-(x+y)

        return str(d1*d2)+'E'+str(e1+e2)

    # divide two numbers and return a decimal quotient
    def large_num_quo(self,a,b):

        # extracting exponenets, signs and digits
        s1, d1, e1 = self.componentize(a)
        s2, d2, e2 = self.componentize(b)
        
        # The operation to perform is -
        # a * 10^x / b * 10^y we can rewrite it as 
        # a/b *10^(x-y)
        # which in the exponents notation is (a/b)E-(x-y)

        return str(float(d1)/float(d2))+'E'+str(e1-e2)


    # compare two numbers and return the greater if m = 1,
    # lesser if m = 0
    def large_num_compare(self,a,b,max):

        # extracting exponenets, signs and digits
        s1, d1, e1 = self.componentize(a)
        s2, d2, e2 = self.componentize(b)

        if e1 == e2:
            if d1 == d2 or d1 > d2:
                return a
            elif d2 > d1:        
                return b
        elif e1 > e2:
            if m == 1:
                return a
            else:
                return b
        elif e2 > e1:
            if m == 1:
                return b
            else:
                return a


    # breaks the number down into tuples of sign, digits and exponential value
    def componentize(self,d):
        
        # tokenize the large number
        d = Decimal(d) 
        sign = d.as_tuple().sign
        exponent = d.as_tuple().exponent

        # converting the digits returned as a tuple into an integer
        digits = 0
        for index, digit in enumerate(reversed(d.as_tuple().digits)):
            digits += digit*10**index

        return sign, digits, exponent



