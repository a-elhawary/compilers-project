def isAlphabet(character):
    return (character >= "a" and character <= "z") or (character >= "A" and character <= "Z")

def isNumber(character):
    return character >= "0" and character <= "9"

def isOperator(character):
    return character == "+" or character == "-" or character == "*" or character == "/"

def addToken(token, tokenType):
    print(token + " " + tokenType)

def tokenizer(character, currToken):
    newState = 0
    if isOperator(character):
        addToken(character, "Operator")
        newState = 5
    elif isAlphabet(character):
        currToken += character
        newState = 4
    elif isNumber(character):
        currToken += character
        newState = 3
    elif character == "-":
        currToken += character
        newState = 2
    return newState, currToken

# get input
expression = input("Please enter an Expression: ")

isValid = True
currentState = 1
tempCurrentState = 1
currentToken = ""
previousState = None

# loop over expression character by character
for character in expression:
    if currentState == 1:
        if character == "-":
            currentToken += character
            tempCurrentState = 2
        elif isNumber(character):
            currentToken += character
            tempCurrentState = 3
        elif isAlphabet(character):
            currentToken += character
            tempCurrentState = 4
        elif character != " ":
            tempCurrentState, currentToken = tokenizer(character, currentToken)
            isValid = False
    elif currentState == 2:
        if isNumber(character):
            currentToken += character
            tempCurrentState = 3
        elif character != " ":
            tempCurrentState, currentToken = tokenizer(character, currentToken)
            isValid = False
    elif currentState == 3:
        if isOperator(character):
            addToken(currentToken, "Number")
            addToken(character, "Operator")
            currentToken = ""
            tempCurrentState = 5
        elif isNumber(character):
            currentToken += character
            tempCurrentState = 3
        elif character == " ":
            addToken(currentToken, "Number")
            currentToken = ""
            tempCurrentState = 7
        else:
            tempCurrentState, currentToken = tokenizer(character, currentToken)
            isValid = False
    elif currentState == 4:
        if isOperator(character):
            addToken(currentToken, "ID")
            addToken(character, "Operator")
            currentToken = ""
            tempCurrentState = 5
        elif isNumber(character) or isAlphabet(character):
            currentToken += character
            tempCurrentState = 4
        elif character == " ":
            addToken(currentToken, "ID")
            currentToken = ""
            tempCurrentState = 7
        else:
            tempCurrentState, currentToken = tokenizer(character, currentToken)
            isValid = False
    elif currentState == 5:
        if isNumber(character):
            currentToken += character
            tempCurrentState = 3
        elif character == "-":
            currentToken += character
            tempCurrentState = 2
        elif isAlphabet(character):
            currentToken += character
            tempCurrentState = 4
        elif character != " ":
            addToken(character, "Operator")
            currentState = 5
            isValid = False
    elif currentState == 7:
        if isOperator(character):
            addToken(character, "Operator")
            tempCurrentState = 5
        elif character != " ":
            tempCurrentState, currentToken = tokenizer(character, currentToken)
            isValid = False
    previousState = currentState
    currentState = tempCurrentState

if(currentState == 3):
    addToken(currentToken, "Number")
elif currentState == 4:
    addToken(currentToken, "ID")

if isValid and (currentState == 4 or currentState == 3):
    print("Valid Expression")
else:
    print("Invalid Expression")