def isAlphabet(character):
    return (character >= "a" and character <= "z") or (character >= "A" and character <= "Z")

def isNumber(character):
    return character >= "0" and character <= "9"

def isOperator(character):
    return character == "+" or character == "-" or character == "*" or character == "/"

def tokenizer(character, currToken, currentState, isValid):
    newState = 0
    if isOperator(character):
        addToken(character, "Operator",currentState, 5, isValid)
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

tokens = []

def addToken(token, tokenType, currentState, nextState, isValid):
    if(isValid):
        tokens.append([token , tokenType, currentState, nextState])
    else:
        tokens.append([token , tokenType, 6, 6])

def engine(expression):
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
                tempCurrentState, currentToken = tokenizer(character, currentToken, currentState, isValid)
                isValid = False
        elif currentState == 2:
            if isNumber(character):
                currentToken += character
                tempCurrentState = 3
            elif character != " ":
                tempCurrentState, currentToken = tokenizer(character, currentToken, currentState, isValid)
                isValid = False
        elif currentState == 3:
            if isOperator(character):
                addToken(currentToken, "Number", currentState, 5, isValid)
                addToken(character, "Operator", currentState, 5, isValid)
                currentToken = ""
                tempCurrentState = 5
            elif isNumber(character):
                currentToken += character
                tempCurrentState = 3
            elif character == " ":
                addToken(currentToken, "Number", currentState, 7, isValid)
                currentToken = ""
                tempCurrentState = 7
            else:
                tempCurrentState, currentToken = tokenizer(character, currentToken, currentState, isValid)
                isValid = False
        elif currentState == 4:
            if isOperator(character):
                addToken(currentToken, "ID", currentState, 5, isValid)
                addToken(character, "Operator", currentState, 5, isValid)
                currentToken = ""
                tempCurrentState = 5
            elif isNumber(character) or isAlphabet(character):
                currentToken += character
                tempCurrentState = 4
            elif character == " ":
                addToken(currentToken, "ID", currentState, 7, isValid)
                currentToken = ""
                tempCurrentState = 7
            else:
                tempCurrentState, currentToken = tokenizer(character, currentToken, currentState, isValid)
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
                addToken(character, "Operator", currentStatel, 5, isValid)
                currentState = 5
                isValid = False
        elif currentState == 7:
            if isOperator(character):
                addToken(character, "Operator", currentState, 5, isValid)
                tempCurrentState = 5
            elif character != " ":
                tempCurrentState, currentToken = tokenizer(character, currentToken, currentState, isValid)
                isValid = False
        previousState = currentState
        currentState = tempCurrentState

    if(currentState == 3):
        addToken(currentToken, "Number", currentState, currentState, isValid)
    elif currentState == 4:
        addToken(currentToken, "ID", currentState, currentState, isValid)

    return isValid and (currentState == 4 or currentState == 3 or currentState == 7), tokens

def main():
    expression = input("enter ay haga: ")
    isValid, tokens = engine(expression)
    print(tokens)
    print(isValid)

if __name__ == "__main__":
    main()