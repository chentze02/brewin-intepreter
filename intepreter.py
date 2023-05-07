

from enum import Enum
from bparser import BParser
from intbase import InterpreterBase, ErrorType
from typing import List
import copy

# TEST


def read_file(filename):
    lines = []
    with open(filename, 'r') as file:
        for line in file:
            lines.append(line.strip())
    return lines


program_source = read_file('input.txt')


class Intepreter(InterpreterBase):
    def __init__(self, console_output=True, inp=None, trace_output=False):
        super().__init__(console_output, inp)
        self.fieldHashTable = dict()
        self.methodHashTable = dict()
        self.classHashTable = dict()

    def evaluateExpression(self, expr, classObjPtr, parameterDict):
        if not isinstance(expr, list):
            if expr.isnumeric():
                # print(f"IN NUMMERIC {expr}")
                return int(expr)
            else:

                if (expr.startswith('"') and expr.endswith('"')):
                    temp = expr.strip('"')
                    # print(f'expr strip is {temp}')
                    return temp
                else:
                    if expr in parameterDict:
                        pass
                    elif expr in classObjPtr.fieldHashTable:
                        # print(
                        #     f'expr is {expr} and self.fieldHashTable is {classObjPtr.fieldHashTable[expr].getValue()}')
                        return classObjPtr.fieldHashTable[expr].getValue()

        operator = expr[0].strip()

        print(
            f'operand1 is {expr[1]} and operand2 is {expr[2]} and operator is {operator} and parameterDict is {parameterDict}')
        try:
            if operator == '+':
                return self.evaluateExpression(expr[1], classObjPtr, parameterDict) + self.evaluateExpression(expr[2], classObjPtr, parameterDict)

            elif operator == '-':
                return int(self.evaluateExpression(expr[1], classObjPtr, parameterDict)) - int(self.evaluateExpression(expr[2], classObjPtr, parameterDict))
            elif operator == '*':

                # print(f'expr1 is {expr[1]} and expr2 is {expr[2]}')
                return int(self.evaluateExpression(expr[1], classObjPtr, parameterDict)) * int(self.evaluateExpression(expr[2], classObjPtr, parameterDict))

            elif operator == '/':
                return int(self.evaluateExpression(expr[1], classObjPtr, parameterDict)) / int(self.evaluateExpression(expr[2], classObjPtr, parameterDict))
            elif operator == '==':
                return self.evaluateExpression(expr[1], classObjPtr, parameterDict) == self.evaluateExpression(expr[2], classObjPtr, parameterDict)
            elif operator == '!=':
                return self.evaluateExpression(expr[1], classObjPtr, parameterDict) != self.evaluateExpression(expr[2], classObjPtr, parameterDict)
            elif operator == '<':
                return self.evaluateExpression(expr[1], classObjPtr, parameterDict) < self.evaluateExpression(expr[2], classObjPtr, parameterDict)
            elif operator == '>':
                return self.evaluateExpression(expr[1], classObjPtr, parameterDict) > self.evaluateExpression(expr[2], classObjPtr, parameterDict)
            elif operator == '>=':
                return self.evaluateExpression(expr[1], classObjPtr, parameterDict) >= self.evaluateExpression(expr[2], classObjPtr, parameterDict)
            elif operator == '<=':
                return self.evaluateExpression(expr[1], classObjPtr, parameterDict) <= self.evaluateExpression(expr[2], classObjPtr, parameterDict)
            elif operator == '&&':
                return self.evaluateExpression(expr[1], classObjPtr, parameterDict) and self.evaluateExpression(expr[2], classObjPtr, parameterDict)
            elif operator == '||':
                return self.evaluateExpression(expr[1], classObjPtr, parameterDict) or self.evaluateExpression(expr[2], classObjPtr, parameterDict)
            else:
                super().error(ErrorType.SYNTAX_ERROR)
        except:
            super().error(ErrorType.TYPE_ERROR)

    def reset_all_variables(self):
        self.fieldHashTable = dict()
        self.methodHashTable = dict()
        print('CLEARED')

    def run(self, program):
        result, parsed_program = BParser.parse(program)
        className, methodName = None, None
        if result:
            # print(parsed_program)
            for currClass in parsed_program:
                print(f" currClass is {currClass}")
                if (currClass[0] != InterpreterBase.CLASS_DEF):
                    raise ValueError('Invalid class declaration')
                for idx, currToken in enumerate(currClass):
                    # print(f"currToken is {currToken}")
                    # print(f"idx is {idx}")
                    if (currToken == InterpreterBase.CLASS_DEF):
                        className = currClass[idx+1]
                        print(f"class name is {className}")

                    # keeps looping if it encounters a list and we want to get the first element of tht list to see what we are dealing with wether it is a method or a field
                    if isinstance(currToken, list):
                        # print("in here")

                        # FIELD
                        if (currToken[0] == InterpreterBase.FIELD_DEF):
                            print("IN FIELD")
                            field = currToken[1:]
                            if len(field) != 2:
                                raise ValueError(
                                    "Invalid field declaration")

                            if field[0] in self.fieldHashTable:
                                raise ValueError("Duplicate field name")

                            tempFieldPtr = Field(field[0], field[1])
                            self.fieldHashTable[field[0]] = tempFieldPtr
                            # print(
                            #     f"tempFieldPtr name is {tempFieldPtr.getName()}")
                            # print(
                            # f"tempFieldPtr value is {tempFieldPtr.getValue()}")
                            print(f"field hash table is {self.fieldHashTable}")

                        # METHOD
                        if (currToken[0] == InterpreterBase.METHOD_DEF):
                            print("IN METHOD")
                            methodName = currToken[1]
                            methodParam = currToken[2]
                            methodBody = currToken[3]
                            tempMethod = Method(
                                methodName, methodParam, methodBody, self)

                            self.methodHashTable[methodName] = tempMethod

                            # print(tempMethod.getBody())
                            # print(tempMethod.getName())
                            # print(tempMethod.getParameters())
                            # tempMethod.execute()

                            # print(f"method is {method}")
                            # print(f"methodName is {methodName}")
                            # print(f"methodParam is {methodParam}")
                            # print(f"methodBody is {methodBody}")

                classObj = Class(className, self.fieldHashTable,
                                 self.methodHashTable)
                self.classHashTable[className] = classObj
                print(f"classObj is {classObj}")
                print(f"methodHashTable in run is {self.methodHashTable}")
                print(f'classHashTable in run is {self.classHashTable}')
                self.reset_all_variables()
                print(
                    f"methodHashTable AFTERRRRRRR in run is {self.methodHashTable}")
                print(
                    f'fieldHashTable AFTERRRRRR in run is {self.fieldHashTable}')

                # me = classObj.instantiate_object(self)
                # print(f"ME is {me}")
                # me.execute()

            mainClass = self.classHashTable[InterpreterBase.MAIN_CLASS_DEF]
            me = mainClass.instantiate_object(self)
            me.execute()
            print("ME ExECUTEd")

            # print(f"classObj name is {classObj.getName()}")
            # print(
            #     f"classObj fields are {classObj.getFields()['p']} and {classObj.getFields()['d']}")
            # print(f"classObj methods are {classObj.getMethods()}")

            # print(f'final is {self.classHashTable["main"].getMethods()}')


class Class:
    def __init__(self, name, fields, methods):
        self.name = name
        self.fields = fields
        self.methods = methods

    def getFields(self):
        return self.fields

    def getMethods(self):
        return self.methods

    def getName(self):
        return self.name

    def setName(self, name):
        if name[0].isalpha() or name[0] == "_":
            self.name = name
        else:
            raise ValueError("Invalid class name")

    def execute(self):
        pass

    def instantiate_object(self, intepreterPtr):
        obj = Object(intepreterPtr, self)
        print(self.getMethods())
        obj.add_method(self.getMethods())
        obj.add_field(self.getFields())
        return obj


class Object:
    def __init__(self, intepreterPtr, classPtr):
        self.fieldHashTable = {}
        self.methodHashTable = {}
        self.instantiatedObjects = {}
        self.intetepreterPtr = intepreterPtr
        self.classPtr = classPtr

    def add_field(self, fieldHashMap):
        fieldHashMap_copy = copy.deepcopy(fieldHashMap)
        self.fieldHashTable = fieldHashMap_copy

    def get_field(self, name):
        if name in self.fieldHashTable:
            return self.fieldHashTable[name]
        else:
            self.intetepreterPtr.error(ErrorType.NAME_ERROR)

    def add_method(self, methodHashMap):
        methodHashMap_copy = copy.deepcopy(methodHashMap)
        self.methodHashTable = methodHashMap_copy

    def get_method(self, name):
        if name in self.methodHashTable:
            return self.methodHashTable[name]
        else:
            self.intetepreterPtr.error(ErrorType.NAME_ERROR)

    def execute(self):
        try:
            # print(f"FIELDS IN OBJECTS IS {self.fieldHashTable}")
            # print(f"METHODS IN OBJECTS IS {self.methodHashTable}")
            methodBody = self.methodHashTable["main"].getBody()
            methodParam = self.methodHashTable["main"].getParameters()
            # print(f"METHOD BODY IS {methodBody}")
            # print(f"METHOD PARAM IS {methodParam}")
            self.__run_statement(
                methodBody, self, self.intetepreterPtr, methodParam)
        except KeyError:
            self.intetepreterPtr.error(ErrorType.NAME_ERROR)

    def __run_statement(self, statement, classObjPtr, intepreterPtr, parameterDict):
        print(f"statement is {statement}")
        if statement[0] == InterpreterBase.BEGIN_DEF:
            for statementAfterBegin in statement[1:]:
                self.__run_statement(statementAfterBegin, classObjPtr,
                                     intepreterPtr, parameterDict)
        # if statement[0] == InterpreterBase.PRINT_DEF:
        #     output = ""
        #     print(f"PARAMETER DICT IN EXECUTE IS {parameterDict}")
        #     for sub_statement in statement[1:]:
        #         if isinstance(sub_statement, list):
        #             print(f'OPERATION IS {sub_statement}')
        #             if sub_statement[0] in {'+', '-', '*', '/', '==', '!=', '<', '>', '>=', '<=', '&&', '||'}:
        #                 print("ITS A EXPPPPPPPPPPP")
        #                 result = intepreterPtr.evaluateExpression(
        #                     sub_statement, classObjPtr, parameterDict)
        #                 print(f'RESULT IS {result}')
        #                 output += str(result)
        #             elif sub_statement[0] == InterpreterBase.CALL_DEF:
        #                 print("IN LIST SUBSTATEMENT WITH RECRUSION CALL")
        #                 self.__run_statement(
        #                     sub_statement, classObjPtr, intepreterPtr, parameterDict)

        #         else:
        #             output += sub_statement
        #     print(f'YAYYYYYYYY {output}')
        elif statement[0] == InterpreterBase.PRINT_DEF:
            output = ""
            print(f"PARAMETER DICT IN PRINT IS {parameterDict}")
            for sub_statement in statement[1:]:
                if isinstance(sub_statement, list):
                    print(f'OPERATION IS {sub_statement}')
                    if sub_statement[0] in {'+', '-', '*', '/', '==', '!=', '<', '>', '>=', '<=', '&&', '||'}:
                        print("ITS A EXPPPPPPPPPPP")
                        result = intepreterPtr.evaluateExpression(
                            sub_statement, classObjPtr, parameterDict)
                        # print(f'RESULT IS {result}')
                        output += str(result)
                    elif sub_statement[0] == InterpreterBase.CALL_DEF:
                        # print("IN LIST SUBSTATEMENT WITH RECRUSION CALL")
                        self.__run_statement(
                            sub_statement, classObjPtr, intepreterPtr, parameterDict)

                else:
                    sub_statement.strip('')
                    print(f'SUBBBB IS {sub_statement}')
                    # if it is a string it should be in ""
                    if (sub_statement.startswith('"') and sub_statement.endswith('"')):
                        output += sub_statement.strip('"')
                    else:
                        if sub_statement in parameterDict:
                            tempVar = parameterDict[sub_statement]
                        elif sub_statement in classObjPtr.fieldHashTable:
                            tempVar = classObjPtr.fieldHashTable[sub_statement]

                        if isinstance(tempVar, Field):
                            tempVar = tempVar.getValue()
                            print(f'BANANNNA {tempVar}')
                            if isinstance(tempVar, str):
                                output += str(tempVar.strip('"'))
                        elif isinstance(tempVar, str):
                            output += str(tempVar.strip('"'))
            print(f'YAYYYYYYYY {output}')
            intepreterPtr.output(output)

        elif statement[0] == InterpreterBase.SET_DEF:
            print("set statement")
            try:
                if isinstance(statement[2], list):
                    # print("LIST")
                    # this would give the part of (new className) in (set variableName (new className))
                    tempNewObj = statement[2]

                    # IF ITS A NEWWWW
                    if tempNewObj[0] == InterpreterBase.NEW_DEF:
                        print("NEW")
                        objToInstantiate = tempNewObj[1]
                        instantiatedObj = None
                        if objToInstantiate in self.instantiatedObjects:
                            print("I CACHEDDD ITTTT")
                            instantiatedObj = self.instantiatedObjects[objToInstantiate]
                        # print(f"OBJECT TO INSTANTIATE IS {objToInstantiate}")
                        else:
                            print("FAILED TO CACHE RIP BOOOO")
                            instantiatedObj = intepreterPtr.classHashTable[objToInstantiate].instantiate_object(
                                intepreterPtr)
                            self.instantiatedObjects[objToInstantiate] = instantiatedObj
                        # print(f"INSTANTIATED OBJ IS {instantiatedObj}")
                        classObjPtr.fieldHashTable[statement[1]].set(
                            instantiatedObj)

                else:
                    variableName = statement[1]
                    valueThatCouldBeActualValueOrParameterOrAnotherVar = statement[2]

                    # IF WE ARE SETTING BASED ON A PARAMETER
                    if valueThatCouldBeActualValueOrParameterOrAnotherVar in parameterDict:
                        valueThatCouldBeActualValueOrParameterOrAnotherVar = parameterDict[
                            valueThatCouldBeActualValueOrParameterOrAnotherVar]

                    # IF it is another fields name
                    elif valueThatCouldBeActualValueOrParameterOrAnotherVar in classObjPtr.fieldHashTable:
                        valueThatCouldBeActualValueOrParameterOrAnotherVar = classObjPtr.fieldHashTable[
                            valueThatCouldBeActualValueOrParameterOrAnotherVar]

                    classObjPtr.fieldHashTable[variableName].set(
                        valueThatCouldBeActualValueOrParameterOrAnotherVar)

                    # classObjPtr.fieldHashTable[statement[1]].set(
                    #     statement[2])
            except:
                intepreterPtr.error(ErrorType.NAME_ERROR)

        elif statement[0] == InterpreterBase.INPUT_INT_DEF:
            value = intepreterPtr.get_input()
            # print(f'VALUE OF INPUT IS {value}')
            try:
                classObjPtr.fieldHashTable[statement[1]].set(
                    value)
            except:
                intepreterPtr.error(ErrorType.NAME_ERROR)

        elif statement[0] == InterpreterBase.INPUT_STRING_DEF:
            value = intepreterPtr.get_input()
            # print(f'VALUE OF INPUT IS {value}')
            try:
                classObjPtr.fieldHashTable[statement[1]].set(
                    '"'+value+'"')
            except:
                intepreterPtr.error(ErrorType.NAME_ERROR)

        elif statement[0] == InterpreterBase.CALL_DEF:
            callOnWhichObject = statement[1]
            parameters = statement[3:]
            print(f"MAPPED PARAMETERS IS {parameters}")
            if callOnWhichObject == InterpreterBase.ME_DEF:
                meMethod = classObjPtr.methodHashTable[statement[2]]
                meParam = meMethod.getParameters()
                meBody = meMethod.getBody()
                parameter_dict = None
                print(f"ME METHOD IS PARAM {meMethod.getParameters()}")
                print(f"ME METHOD BODY IS {meMethod.getBody()}")
                if len(parameters) != len(meParam):
                    intepreterPtr.error(ErrorType.FAULT_ERROR)
                else:
                    parameter_dict = dict(
                        zip(meParam, parameters))
                print(f"PARAMETER DICT IN MEEEEEE IS {parameter_dict}")
                self.__run_statement(
                    meBody, classObjPtr, intepreterPtr, parameter_dict)
            else:
                try:
                    newObjectPtr = classObjPtr.fieldHashTable[callOnWhichObject].getValue(
                    )
                    print
                    methodToBeCalled = newObjectPtr.get_method(statement[2])
                    methodToBeCalledParam = methodToBeCalled.getParameters()
                    methodToBeCalledBody = methodToBeCalled.getBody()

                    # NEEDS TO FIX
                    if len(parameters) != len(methodToBeCalledParam):
                        intepreterPtr.error(ErrorType.FAULT_ERROR)
                    else:
                        parameter_dict = dict(
                            zip(methodToBeCalledParam, parameters))
                    print(f"PARAMETER DICT IN NOT ME IS {parameter_dict}")

                    # print(
                    #     f"method to be called body is {methodToBeCalledBody}")
                    self.__run_statement(
                        methodToBeCalledBody, newObjectPtr, intepreterPtr, parameter_dict)
                    # print(f"METHOD to be called is {methodToBeCalled}")
                    # print(f"NEW OBJECT POINTER IS {newObjectPtr}")
                    # print(f'call list is {statement}')
                    # print("CALL ON NOT ME")
                    # print(f"calOnWHICHOBJECT IS {callOnWhichObject}")
                    # print(
                    #     f"field HASH TABLE IN CALL IS {classObjPtr.fieldHashTable[callOnWhichObject]}")
                    # print(
                    #     f"new object pointer methods ARE {newObjectPtr.methodHashTable}")
                except:
                    intepreterPtr.error(ErrorType.NAME_ERROR)

            # print(f"PARAMETERS is {parameters}")

        # elif statement[0] == InterpreterBase.WHILE_DEF:


class Field:
    def __init__(self, field_name, initial_value):
        if not isinstance(field_name, str) or not field_name[0].isalpha():
            raise ValueError(
                "Field names must start with a letter and contain only letters, underscores and numbers.")
        if initial_value == InterpreterBase.NULL_DEF:
            initial_value = 'None'
        self.name = field_name
        self.value = initial_value

    def getValue(self):
        return self.value

    def set(self, value):
        self.value = value

    def getName(self):
        return self.name

    def __str__(self):
        return f"Field('{self.name}', {self.value})"


class BeginStatement:
    def __init__(self, statements):
        self.statements = statements

    def getStatement(self):
        return self.statements

    # def execute(self, classObjPtr, intepreterPtr, parameterDict):
    #     result = None
    #     for statement in self.statements:
    #         if statement[0] == "print":
    #             output = ""
    #             print(f"PARAMETER DICT IN EXECUTE IS {parameterDict}")
    #             for sub_statement in statement[1:]:
    #                 if isinstance(sub_statement, list):
    #                     print(f'OPERATION IS {sub_statement}')
    #                     if sub_statement[0] in {'+', '-', '*', '/', '==', '!=', '<', '>', '>=', '<=', '&&', '||'}:
    #                         print("ITS A EXPPPPPPPPPPP")
    #                         result = Intepreter.evaluateExpression(
    #                             sub_statement, classObjPtr, parameterDict)
    #                         print(f'RESULT IS {result}')
    #                         output += str(result)
    #                     elif sub_statement[0] == InterpreterBase.CALL_DEF:
    #                         print("IN LIST SUBSTATEMENT WITH RECRUSION CALL")
    #                         self.execute(
    #                             classObjPtr, intepreterPtr, parameterDict)

    #                 else:
    #                     sub_statement.strip('')
    #                     print(f'SUBBBB IS {sub_statement}')
    #                     # if it is a string it should be in ""
    #                     if (sub_statement.startswith('"') and sub_statement.endswith('"')):
    #                         output += sub_statement.strip('"')
    #                     else:
    #                         if sub_statement in parameterDict:
    #                             tempVar = parameterDict[sub_statement]
    #                         elif sub_statement in classObjPtr.fieldHashTable:
    #                             tempVar = classObjPtr.fieldHashTable[sub_statement]

    #                         if isinstance(tempVar, Field):
    #                             tempVar = tempVar.getValue()
    #                             print(f'BANANNNA {tempVar}')
    #                             if isinstance(tempVar, str):
    #                                 output += str(tempVar.strip('"'))
    #                         elif isinstance(tempVar, str):
    #                             output += str(tempVar.strip('"'))
    #             print(f'YAYYYYYYYY {output}')

    #         # SET
    #         elif statement[0] == InterpreterBase.SET_DEF:
    #             print("set statement")
    #             try:
    #                 if isinstance(statement[2], list):
    #                     print("LIST")
    #                     tempNewObj = statement[2]

    #                 else:
    #                     classObjPtr.fieldHashTable[statement[1]].set(
    #                         statement[2])
    #             except:
    #                 intepreterPtr.error(ErrorType.NAME_ERROR)

    #         # INPUT AS INT

    #         elif statement[0] == InterpreterBase.INPUT_INT_DEF:
    #             value = intepreterPtr.get_input()
    #             print(f'VALUE OF INPUT IS {value}')
    #             try:
    #                 classObjPtr.fieldHashTable[statement[1]].set(
    #                     value)
    #             except:
    #                 intepreterPtr.error(ErrorType.NAME_ERROR)

    #         # INPUT AS STRING

    #         elif statement[0] == InterpreterBase.INPUT_STRING_DEF:
    #             value = intepreterPtr.get_input()
    #             print(f'VALUE OF INPUT IS {value}')
    #             try:
    #                 classObjPtr.fieldHashTable[statement[1]].set(
    #                     '"'+value+'"')
    #             except:
    #                 intepreterPtr.error(ErrorType.NAME_ERROR)

    #         # CALL

    #         elif statement[0] == InterpreterBase.CALL_DEF:
    #             callOnWhichObject = statement[1]
    #             parameters = statement[3:]
    #             # mapped_parameters = list(
    #             #     map(lambda x: '"' + x + '"', parameters))
    #             print(f"MAPPED PARAMETERS IS {parameters}")
    #             if callOnWhichObject == InterpreterBase.ME_DEF:
    #                 classObjPtr.methodHashTable[statement[2]].execute(
    #                     classObjPtr, parameters)

    #             print(f"PARAMETERS is {parameters}")
    #             try:

    #                 print(f'call list is {statement}')
    #             except:
    #                 intepreterPtr.error(ErrorType.NAME_ERROR)

    #         # elif statement == "call":
    #         #     self.call_statement(statement, environment)
    #         # ... add handling for other statement types ...


class Method:
    def __init__(self, name: str, parameters: List[str], body, intepreter_super):
        self.name = name
        self.parameters = parameters
        self.body = body
        self.intepreter_super = intepreter_super

    def getName(self):
        return self.name

    def getParameters(self):
        return self.parameters

    def getBody(self):
        return self.body

    def checkIfBodyHasBegin(self):
        if self.body[0] != InterpreterBase.BEGIN_DEF:
            print("body doesnt have begin")
            return None
        else:
            remaining_body = self.body[1:]
            begin = BeginStatement(remaining_body)
            return begin

    def execute(self, classObjPtr, parameter_values={}):
        parameter_dict = dict(zip(self.parameters, parameter_values))
        print(f"PARAMETER_DICT IS {parameter_dict}")
        begin = self.checkIfBodyHasBegin()
        if begin is not None:
            print(f"beginStatement is {begin.getStatement()}")
            # begin.execute(classObjPtr, self.intepreter_super, parameter_dict)

        for idx, statement in enumerate(self.body):
            if statement == "print":
                output = ""
                for sub_statement in self.body[self.body.index(statement)+1:]:
                    if isinstance(sub_statement, str):
                        output += sub_statement.strip('"')
                print(output)
            # elif statement == "inputi":
            #     self.input_statement(statement)
            # elif statement == "call":
            #     self.call_statement(statement)

    def __str__(self):
        return f"(method {self.name} ({' '.join(self.parameters)}) {' '.join(map(str, self.body))})"

    def __repr__(self):
        return str(self)


class Value:
    def __init__(self) -> None:
        self.value = None

    def set(self, value):
        self.value = value

    def get(self):
        return self.value


if __name__ == '__main__':
    intepreter = Intepreter()
    intepreter.run(program_source)

    print(f"FULLL OUTPUTTTT {intepreter.get_output()}")
