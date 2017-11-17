import math
import random
def moduloExp(nValue, nValue2, notExceed ):
    number, exponent, residue =nValue, nValue2, 1
    while(exponent > 1):
        if(exponent % 2 == 0 and exponent > 1):
            exponent=exponent//2
            number=(number * number) % notExceed

        if(exponent % 2 == 1 and exponent > 1):
            residue=(residue * number) % notExceed
            exponent-=1
            number=(number * number) % notExceed
            exponent=exponent//2

    return (number * residue) % notExceed



def avarage(password):
    sum=0
    appended=[]
    for char in password:
        value=ord(char)
        appended.append(value)
        sum+=value
        
    return (sum//len(password))

def pascalValue(password):
    nValue=len(password)
    rValue=nValue
    sum=0
    for value in password:
        numerator=(math.factorial(nValue))
        denominator=(math.factorial(nValue - rValue)) * (math.factorial(rValue)) 
        comb=numerator//denominator
        modulo=(ord(value) * comb) % 61
        rValue-=1
        sum+=modulo     
    return sum % 61


def getRandomPoint(prevCord, grad, modulo):
    xCord=(prevCord[0]**2) + (prevCord[1]**2) + (10 * prevCord[0]) + (12 * prevCord[1])
    xCord=(xCord % 22) - (modulo//2)
    yCord=((grad * xCord) - ((grad * prevCord[0]) - prevCord[1]))
    yCord=(yCord % 22) - (modulo//2)+1
    xyCord=[xCord, yCord]
    return  xyCord

def getGeneratorPoint(password, modulo):
    x=avarage(password) % modulo
    y=pascalValue(password) % modulo
    prevCord=[x,y]
    for char in password:
        grad=ord(char)
        newCord=getRandomPoint(prevCord, grad, modulo)
        prevCord[0], prevCord[1] = newCord[0], newCord[1]
        
    return prevCord

def get_char(input_number ):
    characters=["1", "2", "3", "4", "5", "6", "7", "8", "9",
                "A", "B", "C", "D", "E", "F", "G", "H", "J", 
                "K", "L", "M", "N", "P", "Q", "R", "S", "T", 
                "U", "V", "W", "X", "Y", "Z", "a", "b", "c",
                "d", "e", "f", "g", "h", "i", "j", "k", "m",
                "n", "o", "p", "q", "r", "s", "t", "u", "v", 
                "w", "x", "y", "z",
               ]
    charValue= input_number % 58
    return characters[charValue]

def get_index(char ):
    characters=["1", "2", "3", "4", "5", "6", "7", "8", "9",
                "A", "B", "C", "D", "E", "F", "G", "H", "J", 
                "K", "L", "M", "N", "P", "Q", "R", "S", "T", 
                "U", "V", "W", "X", "Y", "Z", "a", "b", "c",
                "d", "e", "f", "g", "h", "i", "j", "k", "m",
                "n", "o", "p", "q", "r", "s", "t", "u", "v", 
                "w", "x", "y", "z",
               ]
    
    if(char in characters):
        for index in range(58):
            indexChar=characters[index]
            if(indexChar==char):
                return index
    return None

def getTerm(nthTerm):
    return (2**nthTerm) -1

print(getTerm(17))

print(moduloExp(2, 30, 31))

def getValue(point, center):
    a, b = center[0], center[1]
    x, y =point[0], point[1]
    return ((x-a)**3) + ((y - b)**3)

def getPointCount(radius, center):
    count=0
    a, b = center[0], center[1] 
    for x in range(-radius+a, radius+1+a):
        for y in range(-radius + b, radius + 1 + b):
            point=[x, y]
            pointValue=getValue(point, center)
            if(pointValue <= radius):
                count+=1

    return count

def egcd(a, b):
    if a== 0:
        return (b, 0, 1)
    else:
        g, y, x=egcd(b%a, a)
        return (g, x-(b//a)*y, y)

def getInverseModulo(a, n):
    lm, hm=1, 0
    low, high= a% n, n
    while low > 1:
        ratio=high//low
        nm, new = hm -lm * ratio, high - low * ratio
        lm, low, hm, high = nm, new, lm, low
     
    return lm % n

def getNewGradient(radius, center, point, modulo):
    sign=0
    numerator=(radius**2) - (center[0]**2 + center[1]**2) - (2 * (point[0] - center[0]))
    denominator=2 * (point[1] - center[1])
    if(numerator < 0):
        sign+=1
    if(denominator < 0):
        sign+=1
    gradient=(numerator * getInverseModulo(denominator, modulo)) % modulo
    if(sign == 1):
        gradient==gradient - modulo
    return gradient

def getGradient(radius, center, prevPoint, modulo):
    prevX, prevY=prevPoint[0], prevPoint[1]
    centerX, centerY=center[0], center[1]

    upper=((radius**2) - ((centerX**2) + (centerY**2)) -(2 * (prevX -centerX))) % modulo
    lower=(2 * (prevY - centerY)) % modulo
    gradient=(upper * getInverseModulo(lower, modulo)) % modulo
    return gradient


def getNewPoint(prevPoint, gradient, center, modulo):
    prevX, prevY=prevPoint[0], prevPoint[1]
    centerX, centerY=center[0], center[1]
    newX=((gradient**2 - prevX) % modulo)-(prevX % modulo)
    newY=((gradient**2 - prevY)  % modulo)-(prevY % modulo)
    return [newX, newY]


def getHash(password):
    prevPoint=[3, 47]
    modulo=2017
    string=" "
    radius=1
    center=[5, 3]
    length=64

    for number in range(length):
        gradient=getGradient(radius, center, prevPoint, modulo)
        newPoint=getNewPoint(prevPoint, gradient, center, modulo)
        value=getValue(newPoint, center) % 61
        radius+=value
        string+=get_char(value)
        prevPoint=newPoint
    return string

def getTurningPoint(gradient, point, center, radius, modulo):
    beta=(-gradient * point[0]) + point[1]
    aValue=(1 + (gradient**2)) % modulo
    if(gradient < 0):
        aValue = aValue - modulo
    bValue=(2 * ((gradient * beta) - center[0]- (center[1]) * gradient))
    if(bValue < 0):
        bValue=bValue % modulo - modulo
    else:
        bValue=bValue % modulo
    cValue=((beta**2) + (2 * center[1] * beta) + (center[0]**2) + (center[1]**2))
    if(cValue < 0):
        cValue=cValue % modulo - modulo
    else:
        cValue=cValue % modulo
    #print(gradient,"    ",[aValue, bValue, cValue])
    xValue=((-bValue) * (getInverseModulo((2 * aValue), modulo))) % modulo
    yValue=(((4 * (aValue) * cValue) - (bValue**2)) * (getInverseModulo((4 * aValue), modulo))) % modulo
    return [(xValue % modulo) - (point[0] % modulo), (yValue % modulo) - (point[1] % modulo)]


def getPoint(center, point1, point2, radius, modulo):
    g1, g2=getNewGradient(radius, center, point1, modulo), getNewGradient(radius, point1, point2, modulo)
    numerator=((g2 * point2[0]) -(g1 * point1[0])) - (point2[1] - point1[1])
    denominator=getInverseModulo((g2 - g1), modulo)
    xValue=(numerator * denominator) % modulo
    y2Value=((g2 * (xValue - point2[0])) + point2[1]) % modulo
    y1Value=((g1 * (xValue - point1[0])) + point1[1]) % modulo
    yValue=(y2Value)
    return [(xValue-point2[0])%modulo, (yValue - point2[1])%modulo]


def getHashString(point, center, modulo):
    string=" "
    radius=1
    for value in range(64):
        gradient=getNewGradient(radius, center, point, modulo)
        newPoint=getTurningPoint(gradient, point, center, radius, modulo)
        newRadius=getValue(newPoint, center) % modulo
        newRadius-=((newPoint[0] - point[0])**2) + ((newPoint[1] - point[1])**2)
        string+=get_char(newRadius % 61)
        
        #print(str(value).ljust(10), str(newPoint).ljust(15), str(newRadius).ljust(10))
        radius=(newRadius) % modulo
        center=point
        point=newPoint
    return string

def getNthPoint(point, center, modulo, number):
    radius=modulo
    for value in range(number):
        gradient=getNewGradient(radius, center, point, modulo)
        newPoint=getTurningPoint(gradient, point, center, radius, modulo)
        newRadius=getValue(newPoint, center) % modulo
        newRadius-=((newPoint[0] - point[0])**2) + ((newPoint[1] - point[1])**2)
        radius=(newRadius) % modulo
        center=point
        point=newPoint

    return point

def getNormalGradient(point, newPoint, modulo):
    dy=newPoint[1] - point[1]
    dx=newPoint[0] -point[0]
    gradient=(dy) * (getInverseModulo(dx, modulo))
    return gradient % modulo

def getAbsent(set):
    list=[]
    for number in range(58):
        if not(number in set):
            list.append(number)
    return list

def getMixing(list1, list2):
    string=""
    for number in list2:
        string+=get_char(list1[number])

    return string

def getCycString(xyIndex, center, radius, modulus, cStart, cEnd, yRange):
    cycString=""; mappedString=""; combString=""
    mappedCount=[]
    for index in range(cStart, cEnd):
        point=[index, xyIndex]
        if(yRange == False):
            point[0], point[1] = xyIndex, index
        gradient=getNewGradient(radius, center, point, modulo)
        newPoint=getTurningPoint(gradient, point, center, radius, modulo)
        value1=getValue(point, center)
        value2=getValue(newPoint, center)
        value3=getValue([value1,value2], newPoint)
        char1=get_char(value1)
        char2=get_char(value2)
        char3=get_char(value3)
        if(char1 == "3"):
            mappedCount.append(char3)

        cycString+=char1
        mappedString+=char2
        combString+=char3

    return [cycString, mappedString, combString, mappedCount]

def getCycStringModified(xyPoint, center, radius, modulus, count, yRange):
    cycString=""; mappedString=""; combString=""
    x, y = xyPoint[0], xyPoint[1]
    mappedCount=[]
    if(yRange == True):
        for index in range(x + radius, x + radius + count):
            point=[index, y]
            gradient=getNewGradient(radius, center, point, modulo)
            newPoint=getTurningPoint(gradient, point, center, radius, modulo)
            value1=getValue(point, center)
            value2=getValue(newPoint, center)
            value3=getValue([value1,value2], newPoint)
            char1=get_char(value1)
            char2=get_char(value2)
            char3=get_char(value3)
            if(char1 == "3"):
                mappedCount.append(char3)

            cycString+=char1
            mappedString+=char2
            combString+=char3
    if(yRange == False):
        for index in range(y*29, y*29 + count):
            point=[x, index]
            gradient=getNewGradient(radius, center, point, modulo)
            newPoint=getTurningPoint(gradient, point, center, radius, modulo)
            value1=getValue(point, center)
            value2=getValue(newPoint, center)
            value3=getValue([value1,value2], newPoint)
            char1=get_char(value1)
            char2=get_char(value2)
            char3=get_char(value3)
            if(char1 == "3"):
                mappedCount.append(char3)

            cycString+=char1
            mappedString+=char2
            combString+=char3


    return [cycString, mappedString, combString, mappedCount]

def appendZero(value, modulus):
    vLen=len(str(value)); modLen=len(str(modulus))
    zero=""
    for int in range(modLen - vLen):
        zero+="0"

    return zero + str(value)


def printAll(center, radius, modulo, count, pointRange, det):
    unique=[]
    prev=0
    mappedTo=[]
    if(det == 1 or det == 3):
        for yIndex in range(pointRange):
            cyc=getCycString(yIndex, center, radius, modulo, 0, count, True)
            unique.append(cyc[2])
            index=get_index(cyc[2][len(cyc) - 1])
            deff=index - prev
            print(str([yIndex+1, "X"]).rjust(15),"  ",str(cyc[0]).rjust(12) , str(index).rjust(4), str(deff%58).rjust(4))
            print(str(((yIndex+1) % modulo)).rjust(15),"  ",str(cyc[1]).rjust(12), str(len(set(cyc[1]))).rjust(4))
            print(str((yIndex+1) % 29).rjust(15),"  ",str(cyc[2]).rjust(12), str(len(set(cyc[2]))).rjust(4))
            pointName=appendZero(yIndex, modulo)+"X"+appendZero(center[0], modulo)+appendZero(center[1], modulo)
            pointName+=appendZero(radius, modulo)+str(modulo)
            print(pointName)
            if(len(cyc[3]) > 0):
                mappedTo.append(get_index(cyc[3][0]))
            print("    ")
            prev=index
    if(det == 2 or det == 3):
        for xIndex in range(pointRange):
            cyc=getCycString(xIndex, center, radius, modulo, 0, count, False)
            unique.append(cyc[2])
            index=get_index(cyc[2][len(cyc) - 4])
            deff=index - prev
            print(str([(xIndex+1), "Y"]).rjust(15),"  ",str(cyc[0]).rjust(12) , str(index).rjust(4), str(deff%58).rjust(4))
            print(str((xIndex + 1) % modulo).rjust(15),"  ",str(cyc[1]).rjust(12), str(len(set(cyc[1]))).rjust(4))
            print(str((xIndex+1) % 29).rjust(15),"  ",str(cyc[2]).rjust(12), str(len(set(cyc[2]))).rjust(4))
            pointName=appendZero(xIndex, modulo)+"Y"+appendZero(center[0], modulo)+appendZero(center[1], modulo)
            pointName+=appendZero(radius, modulo)+str(modulo)
            print(pointName)
            if(len(cyc[3]) > 0):
                mappedTo.append(get_index(cyc[3][0]))
            print(" ")
            prev=index
    return unique

def getSetOperation(stringA, stringB):
    union=set(stringA) | set(stringB)
    intersect=set(stringA) & set(stringB)
    Adeff=set(stringA) - set(stringB)
    Bdeff=set(stringB) - set(stringA)
    symDeff=set(stringA) ^ set(stringB)
    return[union, intersect, Adeff, Bdeff, symDeff]


def getPointString(xyValue, center, radius, prime, isX):
    cyc=getCycString(xyValue, center, radius, modulo, 0, 58, isX)
    return cyc

def getPeriod(matchString, xyIndex, center, radius, modulus, upTo, yRange):
    for start in range(5, upTo):
        if(yRange==True):
            cyc=getCycString(xyIndex, center, radius, modulus, start, start+1, yRange)
            if(cyc[2] == matchString[0]):
                interval=len(matchString)
                cyc2=getCycString(xyIndex, center, radius, modulus, start, start+interval, yRange)
                if(cyc2[2] == matchString):
                    return start
        if(yRange == False):
            interval=len(matchString)
            cyc=getCycString(start, center, radius, modulus, 0, interval, yRange)
            if(cyc[2] == matchString):
                return start

def base58(message):
    string=""; remList=[]
    m=message.encode(encoding='utf_8', errors='strict')
    binaryList=bytearray(m)
    messageArray=""
    for element in binaryList:
        binzero="00000000"
        bins=bin(element)[2:]
        length=len(bins)
        array=binzero[:8 - length] + bins
        messageArray+=array
    
    mult, reminder = int(messageArray, 2), 0
    while(mult > 0):
        reminder=mult % 58
        mult=mult//58
        remList.append(reminder)
    for intValue in range(len(remList)):
        value=remList[len(remList) -1 - intValue]
        string+=get_char(value)
    return string

def getPointBase58(point):
    padding="100000000000000000000000000000000000000000000000000000000000000000000000000000000"
    pointX, pointY = bin(point[0])[2:], bin(point[1])[2:]
    lenPointX, lenPointY = len(pointX), len(pointY)
    paddedPointX=padding[:80-lenPointX] + pointX
    paddedPointY=padding[:80-lenPointY] + pointY
    pointXY="1" + paddedPointX + paddedPointY
    remList=[]; string=""
    mult, reminder = int(pointXY, 2), 0
    while(mult > 0):
        reminder=mult % 58
        mult=mult//58
        remList.append(reminder)
    for intValue in range(len(remList)):
        value=remList[len(remList) -1 - intValue]
        string+=get_char(value)
    return string

def numberBase58(value):
    remList=[]; string=""
    mult, reminder = value, 0
    while(mult > 0):
        reminder=mult % 58
        mult=mult//58
        remList.append(reminder)
    for intValue in range(len(remList)):
        value=remList[len(remList) -1 - intValue]
        string+=get_char(value)
    return string

def encrypMessage(base58, key):
    """
    key is a list contain the following in order
    xyValue---depend on boolean specification(true=x, false=y)
    center--center coordinates of a cycle
    prime & radius---prime and radius are the same, only one value needed
    boolean---for xyValue specification
    """
    mLength=len(str(base58))
    xyValue, center, prime= key[0], key[1], key[2]
    encryptedMessage=""
    x_cyc=getCycString(xyValue[0], center, prime, prime, 0, mLength, False)
    y_cyc=getCycString(xyValue[1], center, prime, prime, 0, mLength, True)
    y_eKey=y_cyc[2]; x_eKey=x_cyc[2]
    for index in range(mLength):
        mChar=base58[index]
        x_kChar, y_kChar = x_eKey[index], y_eKey[index]
        xy_kChar=get_index(x_kChar) + get_index(y_kChar)
        sum=get_index(mChar) + xy_kChar
        mkChar=get_char(sum)
        #print([x_kChar, y_kChar],"----->", [get_char(xy_kChar)],"----->",[mkChar])
        encryptedMessage+=mkChar
    return encryptedMessage

def decrypMessage(base58, key):
    """
    key is a list contain the following in order
    xyValue---depend on boolean specification(true=x, false=y)
    center--center coordinates of a cycle
    prime & radius---prime and radius are the same, only one value needed
    boolean---for xyValue specification
    """
    mLength=len(str(base58))
    xyValue, center, prime= key[0], key[1], key[2]
    encryptedMessage=""
    x_cyc=getCycString(xyValue[0], center, prime, prime, 0, mLength, False)
    y_cyc=getCycString(xyValue[1], center, prime, prime, 0, mLength, True)
    y_eKey=y_cyc[2]; x_eKey=x_cyc[2]
    for index in range(mLength):
        mChar=base58[index]
        x_kChar, y_kChar = x_eKey[index], y_eKey[index]
        xy_kChar=get_index(x_kChar) + get_index(y_kChar)
        sum=get_index(mChar) - (get_index(x_kChar) + get_index(y_kChar))
        mkChar=get_char(sum)
        #print([x_kChar, y_kChar],"----->", [get_char(xy_kChar)],"----->",[mkChar])
        encryptedMessage+=mkChar
    return encryptedMessage

def getCombString(point, center, modulo, start, length):
    x_cyc=getCycString(point[0], center, modulo, modulo, start, start+length, 0)
    y_cyc=getCycString(point[1], center, modulo, modulo, start, start+length, 1)
    xyString=""
    for index in range(length):
        xChar, yChar=x_cyc[2][index], y_cyc[2][index]
        xValue, yValue = get_index(xChar), get_index(yChar)
        xyValue=(xValue + yValue) +index
        xyChar=get_char(xyValue)
        xyString+=xyChar
    return xyString
difference=[]
def getCombStringKey(keyOne, keyTwo):
    combKey=""
    for index in range(len(keyOne)):
        val1=get_index(keyOne[index])
        val2=get_index(keyTwo[index])
        valInv1=getInverseModulo(val1, 61)
        valInv2=getInverseModulo(val2, 61)
        difference.append((valInv1 + valInv2 - val1) % 58)
        combKey+=get_char(valInv1 + valInv2 + index)
    return combKey

def getStringInv(string):
    newString=""
    for index in range(len(string)):
        inValue=get_index(string[index])
        newString+=get_char(58 - inValue)
    return newString

def getStringSum(string):
    sum=0
    for index in range(len(string)):
        indexValue=get_index(string[index])
        sum+=indexValue
    return sum

def getDestCoordinate(string, modulo):
    x, y = 0, 0
    for index in range(len(string)):
        indexValue=get_index(string[index])
        direction=indexValue % 4
        if(direction == 0):
            y+=indexValue
        if(direction == 1):
            y-=indexValue
        if(direction == 2):
            x+=indexValue
        if(direction == 3):
            x-=indexValue
    return [x % modulo,y % modulo]



center=[32124587,21123546]
modulo=9294554271129007931
radius=modulo




message="mama anakula ugali na nyama ya kuku"
print(ord("a"))
messageBase58=base58(message)
print(messageBase58)
print("   ")
b=bytearray(message.encode(encoding='utf_8', errors='strict'))
messageArray=""
for element in b:
    binzero="00000000"
    bins=bin(element)[2:]
    length=len(bins)
    array=binzero[:8 - length] + bins
    messageArray+=array
message.encode(encoding='utf_8', errors='strict')
messageBase58=base58(message)
key=[[3, 31], center, modulo]
key2=[[0, 12], center, modulo]
eMessage=encrypMessage(messageBase58, key)
print(messageBase58)
print(eMessage)
print(decrypMessage(eMessage, key2))


#point=[3, 3]
import hashlib as hash
modulo=989324828347146575663272
point=[23485975677, 46578364768]
center=[134222378689,342889765612]
repeat=modulo * 58
pointXY=getPointBase58(point)
centerXY=getPointBase58(center)
print(pointXY.ljust(35), centerXY.rjust(22))
key=getCombString(point, center, modulo, 0, 34)
print(key, "    ","P","  ", str(len(set(key)))+"   "+str(getStringSum(key)))
key2=getCombString(point, center, modulo, repeat//8, 34 )
print(key2, "    ","P","  ", str(len(set(key2)))+"   "+str(getStringSum(key2)))
print("    ")
pointHash=hash.sha256(pointXY.encode(encoding='utf_8', errors='strict')).hexdigest()
centerHash=hash.sha256(centerXY.encode(encoding='utf_8', errors='strict')).hexdigest()
print(pointHash)
print(centerHash)
print(numberBase58(int(pointHash, 16)))
print(numberBase58(int(centerHash, 16)))
print(" ")
print(getPointBase58([modulo-1, modulo-1]))
print(modulo**2)
print(58**28)
print(16**64)
print(58**58)













        








