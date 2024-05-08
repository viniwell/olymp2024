import pwinput
#comand to install : pip install -r requirements.txt in the /3 directory
passwords = []
for i in range(3):
    passwords.append(pwinput.pwinput("Enter a password to check >> "))

for password in passwords:
    checks = {
        'a-z':False,
        'A-Z':False,
        '0-9':False,
        '$#@':False,
        'minlen':False,
        'maxlen':False
    }

    for letter in password:
        if 'a'<letter<'z':
            checks['a-z']=True
            
        if 'A'<letter<'Z':
            checks['A-Z']=True
        
        if '0'<letter<'9':
            checks['0-9']=True

        if letter in "$#@":
            checks['$#@']=True
    if len(password)>=8:
        checks['minlen'] = True
    if len(password)<=12:
        checks['maxlen']=True

    allTrue = True
    for value in checks.values():
        if not value:
            allTrue = False

    print("Valid" if allTrue else "Invalid")