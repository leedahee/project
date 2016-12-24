#Importing the exponential probability distribution package from math module
from math import exp
import sys

#Get quantitative parameters: Admission Age, Temperature, Heart Rate, Pulse oximetry, systolic blood pressure
def ask(question):
    '''Checks the input value to make sure the parameter is not a non-numeric value. Returns parameter of type float'''
    counter = 0
    while True:
        counter += 1
        var = raw_input(question)
        var = var.replace("%","")
        try:
            return float(var)
        except ValueError:
            print "Invalid entry. Please try again."
            if counter >= 3:
                print "Sorry, we were unable to read your response."
                sys.exit(1)
ad_age = ask("Please input the age at admission: ")
temp = ask("Please enter the temperature in degrees Fahrenheit: ")
hr = ask("Please enter the heart rate (BPM): ")
pulse_oxi = ask("Please enter the pulse oximetry value as a percent (X%): ")
sbp = ask("Please enter the systolic blood pressure in mmHg: ")

#Get qualitative parameters: Because these parameters are not direct numeric values, we need to code the text answers so that they make sense in contributing to ascertaining the mortality score.

#Get parameter: Admission Type
a = 0
counta = 0
while a <= 0:
    ad_type = raw_input("Admission type : elective or routine? ")
    ad_type.lower()
    counta += 1
    if ad_type == 'elective':
        (ad_type, a) = (0,1)    ###Numerically code the response
    elif ad_type == 'routine':
       (ad_type, a) = (1,1)    ###Numerically code the response
    else:
        print "Invalid entry. Please try again.\n elective or routine "
    if counta >= 3:
        print "Sorry, we were unable to read your response."
        sys.exit(1)



#Admission type 'elective':0 , 'routine':1
#because they use 'elective' as a reference category.
#To help your understanding what the reference is!!
#Let's say,
#Score =18+0.6(adm_type)+0.45(ADL)- 0.14(temp)
#Score=0+1(adm_type)+2(ADL)-3(temp)
#In this paper, null hypothesis : 1=0
#   if adm_type='routine' whose value is '1',
#       Score=0+1(1)+2(ADL)-3(temp)
#   'routine'does not affect to the Score.
#  1 tells us me the chage in Score for being 'Routine' vs 'Elective'
#In this case we call 'Elective' as reference category(making the change!!)
#In the same way,
#Functional status 'No ADL :0', 'ADL' :1
#Oxygen use 'No' :0, 'Yes' :1
#I really wanted to know what it means, so that I just asked my biostat professor><

#Get parameter: ADL
b = 0
countb = 0
while b <= 0:
    adl = raw_input("Functional status as defined by difficulties with ADLs : yes or no ")
    adl.lower()
    countb += 1
    if adl == 'yes':
        (adl, b) = (1,1)
    elif adl == 'no':
        (adl, b) = (0,1)
    else:
        print "Invalid entry. Please try again.\n yes or no "
    if countb >= 3:
        print "Sorry, we were unable to read your response."
        sys.exit(1)

 #Get parameter: Oxygen administered upon admission
d = 0
countd = 0
while d <= 0:
    o2_ad = raw_input("O2 on admission : yes or no ")
    o2_ad.lower()
    countd += 1
    if o2_ad == 'yes':
        (o2_ad, d) = (1,1)
    elif o2_ad =='no':
        (o2_ad, d) = (0,1)
    else:
        print "Invalid entry. Please try again.\n yes or no "
    if countd >= 3:
        print "Sorry, we were unable to read your response."
        sys.exit(1)


## Caluclating the relative score
score = 18.2897 + 0.6013*(ad_type) + 0.4518 *(adl) + 0.0325*(ad_age) - 0.1458*(temp) + 0.019*(hr) - 0.0983*(pulse_oxi) - 0.0123*(sbp) + 0.8615*(o2_ad)

# print "The score is ",score,"."
p = exp(score)/(1+exp(score))

print "The predicted probability of death is ",p,"."
