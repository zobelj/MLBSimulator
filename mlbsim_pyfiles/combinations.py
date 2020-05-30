from itertools import permutations


def findCombinationsUtil(arr, index, num, reducedNum, allCombos):

    # Base condition
    if (reducedNum < 0):
        return
    # If combination is found, print it
    if (reducedNum == 0):
        if(index <= 9):
            allCombos.append([arr[n] for n in range(index)])
        else:
            pass
        return

    prev = 1 if(index == 0) else arr[index - 1]

    for k in range(prev, num + 1):
        arr[index] = k
        findCombinationsUtil(arr, index + 1, num, reducedNum - k, allCombos)
    
def findCombinations(n):
    # array to store the combinations
    allCombos = []
    arr = [0] * n

    # find all combinations
    findCombinationsUtil(arr, 0, n, n, allCombos)
    return allCombos

def addZeros(inputList):
    for i in range(len(inputList)):
        zeros = 9 - len(inputList[i])
        zerosList = [0] * zeros
        for j in zerosList:
            inputList[i].append(j)
        
    return inputList
