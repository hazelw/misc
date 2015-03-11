import sys

f = open(sys.argv[1], 'r+')
unreadWords = []
currentWord = ""
readWords = []
tableNames = []

# split the input file into words, put each word into a list (prevents problems with commands running
# over multiple lines)
for line in f:
	splitLine = line.split(" ")
	for word in splitLine:
		unreadWords.append(word)
		

while (len(unreadWords) > 0):
	currentWord = unreadWords[0].lower()
	unreadWords.pop(0)
	
	if(currentWord == 'from' or currentWord == 'table' or 
		currentWord == 'join' or currentWord == 'update'):
		# we know that the next word must be of the form tablename, tablename.column, database.tablename or database.tablename.column
		fullTableName = unreadWords[0].split(".")
		if(len(fullTableName) >= 2):
			foundTable = fullTableName[0] + "." + fullTableName[1]
		else:
			foundTable = fullTableName[0]

		if foundTable not in tableNames:
			tableNames.append(foundTable)
			

print("Unqualified table names: ")			
for name in tableNames:
	print (name)
	
if(len(sys.argv) > 2):
	print("Qualified table names: ")
	
	for name in tableNames:
		print(sys.argv[2] + "." + name)
		
if(len(sys.argv) > 3):
	print("Create table statements: ")
	
	for name in tableNames:
		fullTableName = name.split(".")
	
		print("CREATE TABLE " + sys.argv[2] + "." + fullTableName[len(fullTableName) - 1] + " AS (SELECT * FROM " + name + ") " + sys.argv[3])