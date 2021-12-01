def orderedSublist(codeList, shoppingCart):
  if not codeList:
      return 1
  
  nextIndex = 0
  nextStartPoint = 0
  for x in range(len(codeList)):
    # Split each fruit codes group and search for them in the shopping cart
    foundGroup = False
    splitedGroup = codeList[x].split()
    # print("Group: ", x+1)
    while not foundGroup:
      for i in range(len(splitedGroup)):
        # Check for each of the fruits in the code, save the nextIndex to start the next search from there avoiding searching multiple times
        # each fruit
        found = False
        nextIndexSet = False
        # Clean each input to remove extra spaces or upper case letters
        cleanedFCode = splitedGroup[i].lower().strip()
        # print("outer: ", i, cleanedFCode)
        for j in range(nextStartPoint, len(shoppingCart)):
          cleanedFruit = shoppingCart[j].lower().strip()
          
          # print("inner: ", i, j, cleanedFruit)
          # If there is an anything or the fruits match then process a success
          if cleanedFCode == 'anything' or cleanedFCode == cleanedFruit:
            # If there is no new nextIndex and is the first fruit, this could be the next index to use for the next search
            if not nextIndexSet and i == 0:
              nextIndex = j + 1 
              nextIndexSet = True
            
            # If is the last fruit on the group and its a match then we start searching the next group from the this index
            if i == len(splitedGroup) - 1:
              nextIndex = j + 1
              foundGroup = True

            nextStartPoint = j + 1
            found = True
            break
          # If the fruit is not the first one and it does not match the fruit or an anything we skip the cycle and start again from the next index
          elif i > 0:
            if not nextIndexSet:
              nextStartPoint = j
            else:
              nextStartPoint = nextIndex
            break
        
        # If the group has been found we break the cycle and continue
        if foundGroup:
          break
        
        # we got to the end of the cart and nothing can be found further
        if len(splitedGroup) - i - 1 > len(shoppingCart) - nextIndex:
          return 0

        # if the first fruit has not been found in all the shopping cart then is not valid, else we keep trying
        if not found:
          if i == 0:
            return 0
          break
  
  return int(foundGroup)

# Tests
print("Results:")
print("Res: " + str(orderedSublist([], ["apple ", "orange", "banana", "apple"]))) # 1
print("Res: " + str(orderedSublist([], []))) # 1
print("Res: " + str(orderedSublist(["apple apple"], []))) # 0
print("Res: " + str(orderedSublist(["apple apple"], ["apple ", "apple"]))) # 1
print("Res: " + str(orderedSublist(["apple apple"], ["apple ", "orange"]))) # 0
print("Res: " + str(orderedSublist(["apple apple"], ["orange", "apple "]))) # 0
print("Res: " + str(orderedSublist(["apple apple"], ["apple ", "orange", "banana", "apple"]))) # 0
print("Res: " + str(orderedSublist(["apple apple"], ["apple", "orange", "banana", "apple", "apple"]))) # 1
print("Res: " + str(orderedSublist(["apple apple"], ["apple", "apple", "orange", "banana", "apple"]))) # 1
print("Res: " + str(orderedSublist(["apple apple"], ["apple", "orange", "apple", "apple ", "banana", "apple"]))) # 1

print("Res: " + str(orderedSublist(["apple apple anything", "orange"], ["apple", "orange", "apple", "apple ", "banana", "apple"]))) # 0
print("Res: " + str(orderedSublist(["apple apple anything", "orange"], ["apple", "orange", "apple", "apple ", "banana", "orange"]))) # 1
print("Res: " + str(orderedSublist(["apple apple anything", "orange"], ["apple", "apple", "orange", "apple", "apple ", "banana"]))) # 0
print("Res: " + str(orderedSublist(["apple apple anything", "orange"], ["apple", "apple", "orange", "orange", "apple", "apple ", "banana"]))) # 1
print("Res: " + str(orderedSublist(["apple apple anything", "orange"], ["apple", "apple", "guava", "orange"]))) # 1
a = [
  'orange apple apple banana orange apple banana kiwi pear orange jackfruit orange apple apple banana orange apple banana kiwi pear orange jackfruit ',
  'orange apple apple banana orange apple banana kiwi pear orange jackfruit ',
  'orange apple apple banana orange apple banana kiwi pear orange jackfruit orange apple apple banana orange apple banana kiwi pear orange jackfruit orange apple apple banana orange apple banana kiwi pear orange jackfruit ',
  'orange apple apple banana orange apple banana kiwi pear orange jackfruit ',
  'kiwi pear anything ',
  'jackfruit ',
  'anything ',
  'apple apple ', 
  'banana anything apple ',
  'banana ',
  'orange apple apple banana orange apple banana kiwi pear orange jackfruit orange apple apple banana orange apple banana kiwi pear orange jackfruit ',
  'orange apple apple banana orange apple banana kiwi pear orange jackfruit ',
  'orange apple apple banana orange apple banana kiwi pear orange jackfruit orange apple apple banana orange apple banana kiwi pear orange jackfruit orange apple apple banana orange apple banana kiwi pear orange jackfruit ',
  'orange apple apple banana orange apple banana kiwi pear orange jackfruit ',
  'kiwi pear anything ',
  'jackfruit ',
  'anything ',
  'apple apple ',
  'banana anything apple ',
  'banana ',
  'orange apple apple banana orange apple banana kiwi pear orange jackfruit orange apple apple banana orange apple banana kiwi pear orange jackfruit ',
  'orange apple apple banana orange apple banana kiwi pear orange jackfruit ',
  'orange apple apple banana orange apple banana kiwi pear orange jackfruit orange apple apple banana orange apple banana kiwi pear orange jackfruit orange apple apple banana orange apple banana kiwi pear orange jackfruit ',
  'orange apple apple banana orange apple banana kiwi pear orange jackfruit ',
  'kiwi pear anything ',
  'jackfruit ',
  'anything ',
  'apple apple ',
  'banana anything apple ',
  'banana ',
  'orange apple apple banana orange apple banana kiwi pear orange jackfruit orange apple apple banana orange apple banana kiwi pear orange jackfruit ',
  'orange apple apple banana orange apple banana kiwi pear orange jackfruit ',
  'orange apple apple banana orange apple banana kiwi pear orange jackfruit orange apple apple banana orange apple banana kiwi pear orange jackfruit orange apple apple banana orange apple banana kiwi pear orange jackfruit ',
  'orange apple apple banana orange apple banana kiwi pear orange jackfruit ',
  'kiwi pear anything ',
  'jackfruit ',
  'anything ',
  'apple apple ',
  'banana anything apple ',
  'banana ']
b = ['banana', 'kiwi', 'pear', 'orange', 'jackfruit', 'orange', 'apple', 'apple', 'banana', 'orange', 'apple', 'banana', 'kiwi', 'pear', 'orange', 'jackfruit', 'orange', 'apple', 'apple', 'banana', 'orange', 'apple', 'banana', 'kiwi', 'pear', 'orange', 'jackfruit', 'orange', 'apple', 'apple', 'banana', 'orange', 'apple', 'banana', 'kiwi', 'pear', 'orange', 'jackfruit', 'kiwi', 'pear', 'kiwi', 'jackfruit', 'grapes', 'apple', 'apple', 'banana', 'apple', 'apple', 'banana', 'orange', 'apple', 'apple', 'banana', 'orange', 'apple', 'banana', 'kiwi', 'pear', 'orange', 'jackfruit', 'orange', 'apple', 'apple', 'banana', 'orange', 'apple', 'banana', 'kiwi', 'pear', 'orange', 'jackfruit', 'orange', 'apple', 'apple', 'banana', 'orange', 'apple', 'banana', 'kiwi', 'pear', 'orange', 'jackfruit', 'orange', 'apple', 'apple', 'banana', 'orange', 'apple', 'banana', 'kiwi', 'pear', 'orange', 'jackfruit', 'orange', 'apple', 'apple', 'banana', 'orange', 'apple', 'banana', 'kiwi', 'pear', 'orange', 'jackfruit', 'orange', 'apple', 'apple', 'banana', 'orange', 'apple', 'banana', 'kiwi', 'pear', 'orange', 'jackfruit', 'orange', 'apple', 'apple', 'banana', 'orange', 'apple', 'banana', 'kiwi', 'pear', 'orange', 'jackfruit', 'kiwi', 'pear', 'kiwi', 'jackfruit', 'grapes', 'apple', 'apple', 'banana', 'apple', 'apple', 'banana', 'orange', 'apple', 'apple', 'banana', 'orange', 'apple', 'banana', 'kiwi', 'pear', 'orange', 'jackfruit', 'orange', 'apple', 'apple', 'banana', 'orange', 'apple', 'banana', 'kiwi', 'pear', 'orange', 'jackfruit', 'orange', 'apple', 'apple', 'banana', 'orange', 'apple', 'banana', 'kiwi', 'pear', 'orange', 'jackfruit', 'orange', 'apple', 'apple', 'banana', 'orange', 'apple', 'banana', 'kiwi', 'pear', 'orange', 'jackfruit', 'orange', 'apple', 'apple', 'banana', 'orange', 'apple', 'banana', 'kiwi', 'pear', 'orange', 'jackfruit', 'orange', 'apple', 'apple', 'banana', 'orange', 'apple', 'banana', 'kiwi', 'pear', 'orange', 'jackfruit', 'orange', 'apple', 'apple', 'banana', 'orange', 'apple', 'banana', 'kiwi', 'pear', 'orange', 'jackfruit', 'kiwi', 'pear', 'kiwi', 'jackfruit', 'grapes', 'apple', 'apple', 'banana', 'apple', 'apple', 'banana', 'orange', 'apple', 'apple', 'banana', 'orange', 'apple', 'banana', 'kiwi', 'pear', 'orange', 'jackfruit', 'orange', 'apple', 'apple', 'banana', 'orange', 'apple', 'banana', 'kiwi', 'pear', 'orange', 'jackfruit', 'orange', 'apple', 'apple', 'banana', 'orange', 'apple', 'banana', 'kiwi', 'pear', 'orange', 'jackfruit', 'orange', 'apple', 'apple', 'banana', 'orange', 'apple', 'banana', 'kiwi', 'pear', 'orange', 'jackfruit', 'orange', 'apple', 'apple', 'banana', 'orange', 'apple', 'banana', 'kiwi', 'pear', 'orange', 'jackfruit', 'orange', 'apple', 'apple', 'banana', 'orange', 'apple', 'banana', 'kiwi', 'pear', 'orange', 'jackfruit', 'orange', 'apple', 'apple', 'banana', 'orange', 'apple', 'banana', 'kiwi', 'pear', 'orange', 'jackfruit', 'kiwi', 'pear', 'kiwi', 'jackfruit', 'grapes', 'apple', 'apple', 'banana', 'apple', 'apple', 'kiwi', 'apple', 'kiwi', 'apple', 'apple', 'banana', 'orange', 'apple', 'banana', 'kiwi', 'pear', 'jackfruit', 'orange', 'apple', 'apple', 'banana', 'orange', 'apple', 'banana', 'kiwi', 'pear', 'orange', 'jackfruit', 'orange', 'apple', 'apple', 'banana', 'orange', 'apple', 'banana', 'kiwi', 'pear', 'orange', 'jackfruit', 'orange', 'apple', 'apple', 'banana', 'orange', 'apple']
print("Res: " + str(orderedSublist(a, b))) # 0
