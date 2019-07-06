#!/usr/bin/env python
""" 
Deepak Rajasekhar Karishetti
10846936
CSCI-404
"""
#-------------------------------------------------------------------------------
# Name:        logical_expression
# Purpose:     Contains logical_expression class, inference engine,
#              and assorted functions
#
# Created:     09/25/2011
# Last Edited: 07/22/2013  
# Notes:       *This contains code ported by Christopher Conly from C++ code
#               provided by Dr. Vassilis Athitsos
#              *Several integer and string variables are put into lists. This is
#               to make them mutable so each recursive call to a function can
#               alter the same variable instead of a copy. Python won't let us
#               pass the address of the variables, so put it in a list which is
#               passed by reference. We can also now pass just one variable in
#               the class and the function will modify the class instead of a
#               copy of that variable. So, be sure to pass the entire list to a
#               function (i.e. if we have an instance of logical_expression
#               called le, we'd call foo(le.symbol,...). If foo needs to modify
#               le.symbol, it will need to index it (i.e. le.symbol[0]) so that
#               the change will persist.
#              *Written to be Python 2.4 compliant for omega.uta.edu
#-------------------------------------------------------------------------------

import sys
from copy import copy

#-------------------------------------------------------------------------------
# Begin code that is ported from code provided by Dr. Athitsos
class logical_expression:
    """A logical statement/sentence/expression class"""
    # All types need to be mutable, so we don't have to pass in the whole class.
    # We can just pass, for example, the symbol variable to a function, and the
    # function's changes will actually alter the class variable. Thus, lists.
    def __init__(self):
        self.symbol = ['']
        self.connective = ['']
        self.subexpressions = []


def print_expression(expression, separator):
    """Prints the given expression using the given separator"""
    if expression == 0 or expression == None or expression == '':
        print '\nINVALID\n'

    elif expression.symbol[0]: # If it is a base case (symbol)
        sys.stdout.write('%s' % expression.symbol[0])

    else: # Otherwise it is a subexpression
        sys.stdout.write('(%s' % expression.connective[0])
        for subexpression in expression.subexpressions:
            sys.stdout.write(' ')
            print_expression(subexpression, '')
            sys.stdout.write('%s' % separator)
        sys.stdout.write(')')


def read_expression(input_string, counter=[0]):
    """Reads the next logical expression in input_string"""
    # Note: counter is a list because it needs to be a mutable object so the
    # recursive calls can change it, since we can't pass the address in Python.
    result = logical_expression()
    length = len(input_string)
    while True:
        if counter[0] >= length:
            break

        if input_string[counter[0]] == ' ':    # Skip whitespace
            counter[0] += 1
            continue

        elif input_string[counter[0]] == '(':  # It's the beginning of a connective
            counter[0] += 1
            read_word(input_string, counter, result.connective)
            read_subexpressions(input_string, counter, result.subexpressions)
            break

        else:  # It is a word
            read_word(input_string, counter, result.symbol)
            break
    return result


def read_subexpressions(input_string, counter, subexpressions):
    """Reads a subexpression from input_string"""
    length = len(input_string)
    while True:
        if counter[0] >= length:
            print '\nUnexpected end of input.\n'
            return 0

        if input_string[counter[0]] == ' ':     # Skip whitespace
            counter[0] += 1
            continue

        if input_string[counter[0]] == ')':     # We are done
            counter[0] += 1
            return 1

        else:
            expression = read_expression(input_string, counter)
            subexpressions.append(expression)


def read_word(input_string, counter, target):
    """Reads the next word of an input string and stores it in target"""
    word = ''
    while True:
        if counter[0] >= len(input_string):
            break

        if input_string[counter[0]].isalnum() or input_string[counter[0]] == '_':
            target[0] += input_string[counter[0]]
            counter[0] += 1

        elif input_string[counter[0]] == ')' or input_string[counter[0]] == ' ':
            break

        else:
            print('Unexpected character %s.' % input_string[counter[0]])
            sys.exit(1)


def valid_expression(expression):
    """Determines if the given expression is valid according to our rules"""
    if expression.symbol[0]:
        return valid_symbol(expression.symbol[0])

    if expression.connective[0].lower() == 'if' or expression.connective[0].lower() == 'iff':
        if len(expression.subexpressions) != 2:
            print('Error: connective "%s" with %d arguments.' %
                        (expression.connective[0], len(expression.subexpressions)))
            return 0

    elif expression.connective[0].lower() == 'not':
        if len(expression.subexpressions) != 1:
            print('Error: connective "%s" with %d arguments.' %
                        (expression.connective[0], len(expression.subexpressions)))
            return 0

    elif expression.connective[0].lower() != 'and' and \
         expression.connective[0].lower() != 'or' and \
         expression.connective[0].lower() != 'xor':
        print('Error: unknown connective %s.' % expression.connective[0])
        return 0

    for subexpression in expression.subexpressions:
        if not valid_expression(subexpression):
            return 0
    return 1


def valid_symbol(symbol):
    """Returns whether the given symbol is valid according to our rules."""
    if not symbol:
        return 0

    for s in symbol:
        if not s.isalnum() and s != '_':
            return 0
    return 1

# End of ported code
#-------------------------------------------------------------------------------

# Add all your functions here

#Extracting the symbols and storing it in a mutable list with no repetitiion 
def get_symbol(expression):

    symbols = []
    #print(expression.symbol[0])
    if expression.symbol[0]:
        symbols.append(expression.symbol[0])
        
    else:
        for sub in expression.subexpressions:
            for i in get_symbol(sub):
                if i not in symbols:
                    symbols.append(i)
    #print(symbols)
    return symbols

#Model
def get_model(statement):

    model = {}
    for expression in statement.subexpressions:
        if expression.symbol[0]:
            model[expression.symbol[0]] = True
        elif expression.connective[0].lower() == 'not':
            if expression.subexpressions[0].symbol[0]:
                model[expression.subexpressions[0].symbol[0]] = False
    #print(model)
    return model

#Link symbol and model wiht its value
def link_model(model, symbol, value):

    model_new = copy.deepcopy(model)
    model_new[symbol] = value
    #print(model_new)
    return model_new

#Check the validity of a statement with its model
def valid(statement, model):

    if statement.symbol[0]:
        return model[statement.symbol[0]]
    
    elif statement.connective[0].lower() == 'and':
        result = True
        
        for i in statement.subexpressions:
            result = result and valid(i, model)
        return result
    
    elif statement.connective[0].lower() == 'or':
        result = False
        
        for i in statement.subexpressions:
            result = result or valid(i, model)
        return result
    
    elif statement.connective[0].lower() == 'xor':
        result = False
        
        for i in statement.subexpressions:
            check_valid = valid(i, model)
            result = (result and not check_valid) or (not result and check_valid)
        return result
    
    elif statement.connective[0].lower() == 'if':
        left = statement.subexpressions[0]
        right = statement.subexpressions[1]
        
        check_valid_left = valid(left, model)
        check_valid_right = valid(right, model)
        
        if (check_valid_left and not check_valid_right):
            return False
        else:
            return True
        
    elif statement.connective[0].lower() == 'iff':
        left = statement.subexpressions[0]
        right = statement.subexpressions[1]
        
        check_valid_left = valid(left, model)
        check_valid_right = valid(right, model)
        
        if (check_valid_left == check_valid_right):
            return True
        else:
            return False
        
    elif statement.connective[0].lower() == 'not':
        check_valid = valid(statement.subexpressions[0], model)
        return not check_valid

#Linking model and symbol with its value
def link_msv(model, symbol, value):

    model[symbol] = value
    #print(model)
    return model

#Verification of the knowledge-base, statement, symbols and the model using truthtable enumeration inference
def tt_verification(knowledge_base, statement, symbols, model):

    if not symbols:
        if valid(knowledge_base, model):
            return valid(statement, model)
        else:
            return True
    else:
        symbols_pop = symbols.pop(0)
        
        check_total = tt_verification(knowledge_base, statement, symbols, link_msv(model, symbols_pop, True)) and tt_verification(knowledge_base, statement, symbols, link_msv(model, symbols_pop, False))
        #print(check_total)
        return check_total

#Checking if the knowledge base entails the statement
def check_true_false(knowledge_base, statement):

    model = get_model(knowledge_base)
    symbols = get_symbol(knowledge_base)
    symbols_stat = get_symbol(statement)

    for symbol in symbols_stat:
        symbols.append(symbol)
        
    for symbol in model:
        if symbol in symbols:
            symbols.remove(symbol)
            
    statement_check = tt_verification(knowledge_base, statement, symbols, model)
    
    neg_val = logical_expression()
    neg_val.connective[0] = 'not'
    neg_val.subexpressions.append(statement)
    
    negation_check = tt_verification(knowledge_base, neg_val, symbols, model)
    
    result = open('result.txt', 'w+')
    if(statement_check and not negation_check):
        result.write('definitely true')
    
    elif(not statement_check and negation_check):
        result.write('definitely false')
        
    elif(not statement_check and not negation_check):
        result.write('possibly true, possibly false')
        
    elif(statement_check and negation_check):
        result.write('both true and false')
    result.close()
