import csv
import re
import os.path
import BuildSheet
from datetime import datetime

statement_directory = r"C:\Users\jacob\Desktop\Coding\Budget\Statements"

def ParseFile(filename, account):
    f = os.path.join(statement_directory, filename)

    #parsing for checking
    if account == "Checking":
        with open(f, 'rt') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                    print(f"Posting Date: {row['Posting Date']} \t Amount: {row['Amount']:<14} \t Description: {re.sub(' +', ' ',row['Description'])}\n")
                    line_count += 1
            print(f'Processed {line_count} lines.')
    #parsing for freedom card
    elif account == "Freedom":
        with open(f, 'rt') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                    print(f"Posting Date: {row['Post Date']} \t Amount: {row['Amount']:<14} \t Description: {re.sub(' +', ' ',row['Description'])}\n")
                    line_count += 1
            print(f'Processed {line_count} lines.')

    elif account == "Freedom Unlimited":
        print("parsing freedom unlimited")

def WhatAccount(filename):
    accountname = "NA"
    degen = filename.split('_')
    if(filename[5:9] == "####"):
        accountname = "Checking"
    elif(filename[5:9] == "####"):
        accountname = "Freedom"
    elif(filename[5:9] == "####"):
        accountname = "Freedom Unlimited"
    return accountname

def Prompt():
    WhatWeHave = []
    OurFiles = []
    keepgoing = True
    for filename in os.listdir(statement_directory):
        WhatWeHave.append(WhatAccount(filename));
        OurFiles.append(filename)
    
    Pre_String = "What files do you want to parse? "
    index = 1;
    for each in WhatWeHave:
        Pre_String += str(index) + ": " + each + " "
        index += 1

    Pre_String += "4: All 5: Exit | "

    while keepgoing:
        choices = input(Pre_String)
        try:
            int(choices)
            print(choices)
            print(WhatWeHave)
            print(OurFiles)
            if int(choices) >=1 and int(choices) <= len(WhatWeHave):
                print("Im in here")
                ParseFile(OurFiles[int(choices)-1], WhatWeHave[int(choices)-1])
            elif (int(choices) == len(WhatWeHave)+1):
                index = 0
                while index <len(WhatWeHave):
                    ParseFile(OurFiles[index], WhatWeHave[index])
                    index += 1
            elif (int(choices) == len(WhatWeHave)+2):
                keepgoing = False
            else:
                print("Please enter an available option")
        except:
            print("Please enter a number selection")

    



