import subprocess, platform, csv, random, string, time

lista = []
listRow = 1
command = "None"
chars = "abcdefghijklmnopqrstuvwxyz"
chars1 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
chars2 = "1234567890"
chars3 = "!%&/()=#"

try:
    filnamn = str(input("Ange .csv filnamn: "))
except:
    print("Error")
    time.sleep(1)
    exit

try:
    preExistPass = str(input("Use pre-existing passwords from CSV file? [y]/[n]: ")).lower
    if preExistPass == "y":
        preExistPass = True
    else:
        preExistPass = False
except:
    print("error")
    print("Invalid input, value set to False")
    preExistPass = False

try:
    amountOfUsers = int(input("Ange antal av användare att läsa in: ")) + 1
except:
    print("error")
    print("Antal användare automatiskt angivet som 1")
    amountOfUsers = 1

with open(str(filnamn), newline='') as myFile:
    reader = csv.reader(myFile)
    for row in reader:
        if len(row) < 4:
            del row
        else:
            lista.append(row)

def csvWriter():
    with open(str(filnamn), 'w') as myFile:
        writer = csv.writer(myFile)
        for row in lista:
            writer.writerow(row)

def listAssign():
    uName = str(lista[listRow][0])
    uGivenName = str(lista[listRow][1])
    uSurname = str(lista[listRow][2])
    uAccountName = str(lista[listRow][3])
    try:
        uPassword = str(lista[listRow][4])
    except IndexError:
        uPassword = ''
    return (uName,uGivenName,uSurname,uAccountName,uPassword)

def createPassword():
    uPassword = ""
    while len(uPassword) < 12:
        uPassword += random.choice(chars)
        uPassword += random.choice(chars1)
        uPassword += random.choice(chars2)
        uPassword += random.choice(chars3)    

    uPassword = ''.join(random.sample(uPassword,len(uPassword)))
    return uPassword




#cmd = 'New-ADUser -name "' + uName + '" -GivenName "' + uGivenName + '" -Surname "' + uSurname + '" -SamAccountName "' + uAccountName + '" -AccountPassword "' + uPassword + '" -Enable $true'

if platform.system() == "Windows":
    OpS = "windows"
    print("Windows system detected...")
    time.sleep(1.5)
elif platform.system() == "Linux":
    OpS = "linux"
    print("Linux system detected...")
    time.sleep(1.5)
else:
    print("ERR0R0R PICNIC: Köp ny dator")
    time.sleep(1)
    exit

while listRow < amountOfUsers:
    uName, uGivenName, uSurname, uAccountName, uPassword = listAssign()
    if preExistPass == False:
        uPassword = createPassword()
    else:
        pass
    cmd = 'New-ADUser -name "' + uName + '" -GivenName "' + uGivenName + '" -Surname "' + uSurname + '" -SamAccountName "' + uAccountName + '" -AccountPassword (ConvertTo-SecureString "' + uPassword + '"  -AsPlainText -force) -passThru -ChangePasswordAtLogon $True'
    unix = 'useradd -p' + uPassword + '-c "' + uName + uSurname + '" -m ' + uAccountName
    if OpS == "windows":
        command = cmd
    else:
        command = unix

    if len(lista[listRow]) > 4:
        del lista[listRow][4]
    else:
        pass

    lista[listRow].append(uPassword)
    #print(cmd)
    #returned_value = subprocess.call(command, shell=True)
    listRow += 1
csvWriter()
#print(lista)
#print("returned_value: ", returned_value)