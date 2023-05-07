def evaluateExpression(expr: list[str]):
    if not isinstance(expr, list):
        if expr.isnumeric():
            return int(expr)
        else:
            return expr.strip('"')
    operator = expr[0].strip()
    if operator == '+':
        return evaluateExpression(expr[1]) + evaluateExpression(expr[2])
    elif operator == '-':
        return evaluateExpression(expr[1]) - evaluateExpression(expr[2])
    elif operator == '*':
        return evaluateExpression(expr[1]) * evaluateExpression(expr[2])
    elif operator == '/':
        return evaluateExpression(expr[1]) / evaluateExpression(expr[2])
    elif operator == '==':
        return evaluateExpression(expr[1]) == evaluateExpression(expr[2])
    elif operator == '!=':
        return evaluateExpression(expr[1]) != evaluateExpression(expr[2])
    elif operator == '<':
        return evaluateExpression(expr[1]) < evaluateExpression(expr[2])
    elif operator == '>':
        return evaluateExpression(expr[1]) > evaluateExpression(expr[2])
    elif operator == '>=':
        return evaluateExpression(expr[1]) >= evaluateExpression(expr[2])
    elif operator == '<=':
        return evaluateExpression(expr[1]) <= evaluateExpression(expr[2])
    elif operator == '&&':
        return evaluateExpression(expr[1]) and evaluateExpression(expr[2])
    elif operator == '||':
        return evaluateExpression(expr[1]) or evaluateExpression(expr[2])


print(evaluateExpression(['>=', '212', ['+', ['*', '3', '5'], '6']]))
