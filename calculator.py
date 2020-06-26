variables = {}


def gather_input():
    active = True
    while active:
        user_input = input()
        if user_input:
            active = assess_input(user_input)
            continue
        else:
            continue


def assess_input(user_input):
    operators = ["+", "-", "*", "/", "^"]
    # Does input end with an operator? (Invalid if so.)
    if user_input.rstrip().endswith(("+", "-")):
        print("Invalid expression")
        return True
    # Is input a command?
    elif user_input.startswith("/"):
        return assess_command(user_input)
    # Is input a variable assignment?
    elif "=" in list(user_input):
        return assess_assignment(user_input.split("="))
    # Is user trying to query a variable value?
    elif len(user_input.split()) == 1 and user_input.strip().isalpha():
        return query_variable(user_input)
    # Is input a lone number or something other than a valid variable name?
    elif len(user_input.split()) == 1:
        try:
            print(int(user_input))
        except ValueError:
            if any(char in user_input for char in operators):
                print(resolve_expression(user_input))
                return True
            else:
                print("Invalid expression")
        return True
    else:  # Input is an operation
        print(resolve_expression(user_input))
        return True


def assess_command(user_input):
    if user_input == "/exit":
        print("Bye!")
        return False
    elif user_input == "/help":
        print("A calculator app, using postfix notation and variables!")
        return True
    else:
        print("Unknown command")
        return True


def assess_assignment(user_input):
    variable = user_input[0].strip()
    value = user_input[1].strip()
    if assess_variable(variable) and assess_value(value):
        assign_to_dictionary(variable, value)
    return True


def assess_variable(variable):
    # Variable names can only be made up of a letter or letters
    if variable.isalpha():
        return True
    print("Invalid identifier")
    return False


def assess_value(value):
    # Assignment value can be letter(s) or number, but not both
    if value.isalpha() or value.isdigit():
        return True
    print("Invalid assignment")
    return False


def assign_to_dictionary(variable, value):
    # Is current value an already existing variable?
    if value in variables:
        variables[variable] = variables[value]
    else:
        try:
            variables[variable] = int(value)
        except ValueError:
            print("Unknown variable")
    return True


def query_variable(user_input):
    try:
        print(variables[user_input])
    except KeyError:
        print("Unknown variable")
    return True


def resolve_expression(string):
    operators = ["+", "-", "*", "/", "^", "=", "(", ")"]
    last_index = 0
    formatted = []
    # Gather operands and operators up to last operand|operator pair
    for index, character in enumerate(string):
        if character in operators:
            formatted.append("".join(string[last_index:index]).strip())
            formatted.append(character)
            last_index = index + 1
    # Gather last operand|operator pair
    formatted.append(string[last_index:].strip())
    # Remove empty strings, generated when two operators are side by side
    while "" in formatted:
        formatted.remove("")
    # Check if parentheses are correct before moving on to resolve operators
    if bracket_checker(formatted):
        return resolve_operators(formatted, operators[:5])
    return "Invalid expression"


def bracket_checker(string):
    # Gather all the expression's brackets in a list
    brackets = [character for character in string if character in ("(", ")")]
    bracket_stack = []
    for bracket in brackets:
        if bracket == "(":
            bracket_stack.append(bracket)
        elif bracket == ")":
            if not bracket_stack:  # If stack is empty, must be a mismatch
                return False
            # Remove an opening bracket for every closing bracket found
            bracket_stack.pop()
    # Ultimately, the stack should be empty if all brackets match
    if bracket_stack:
        return False
    return True


def resolve_operators(formatted, operators):
    for index, item in enumerate(formatted):
        operator = ""
        # Look for pairs of operators in the expression
        if item in operators and formatted[index - 1] in operators:
            operator_pair = item + formatted[index - 1]
            # Resolve each pair of operators to one operator (or return 'Invalid')
            if operator_pair == "++" or operator_pair == "--":
                operator = "+"
            elif operator_pair == "+-" or operator_pair == "-+":
                operator = "-"
            elif operator_pair == "**" or operator_pair == "//":
                return "Invalid expression"
            formatted[index - 1 : index + 1] = operator
            # Repeat so long as pairs of operators exist in the expression
            resolve_operators(formatted, operators)
    return form_postfix(formatted)


def form_postfix(formatted):
    precedence = {"^": 4, "*": 3, "/": 3, "+": 2, "-": 2, "(": 1}
    op_stack = []
    postfix = []
    for element in formatted:
        if element.isalpha() or element.isdigit():
            postfix.append(element)
        elif element == "(":
            op_stack.append(element)
        elif element == ")":
            stack_top = op_stack.pop()
            while stack_top != "(":
                postfix.append(stack_top)
                stack_top = op_stack.pop()
        else:
            while op_stack and (precedence[op_stack[-1]] >= precedence[element]):
                postfix.append(op_stack.pop())
            op_stack.append(element)
    while op_stack:
        postfix.append(op_stack.pop())
    return postfix_result(postfix)


def postfix_result(postfix):
    stack = []
    for element in postfix:
        if element.isdigit():
            stack.append(int(element))
        elif element.isalpha():
            stack.append(variables[element])
        elif element == "+":
            stack.append(stack.pop() + stack.pop())
        elif element == "-":
            stack.append(-stack.pop() + stack.pop())
        elif element == "*":
            stack.append(stack.pop() * stack.pop())
        elif element == "/":
            divisor = stack.pop()
            dividend = stack.pop()
            stack.append(dividend / divisor)
        elif element == "^":
            number = stack.pop()
            power = stack.pop()
            stack.append(power ** number)
    result = int(sum(stack))
    return result


if __name__ == "__main__":
    gather_input()
