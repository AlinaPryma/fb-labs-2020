
import numpy as np
import math
import codecs
import sys
import re
file = open("text.txt", "r", encoding='utf-8')
text = file.read()
print(len(text))
symbols = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ".", ",", "!", "?", ";", ":", "-", "—", "»", "«", " "]
for k in range(len(symbols)):
    text = text.replace(symbols[k], "")
text = text.lower()

print(len(text))
letters = np.array(['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ь', 'ы', 'ъ', 'э', 'ю', 'я'])
rar = np.zeros(len(letters))                        # for monogram
rar2 = np.zeros(len(letters) ** 2)                  # for begram
rar2_step2 = np.zeros(len(letters) ** 2)
temp = np.zeros(len(text))                          # for recoded text - temporary
Hzero = np.log2(len(letters))
print(Hzero)

for i in range(len(letters)):
    for j in range(len(text)): 
        if text[j] == letters[i]:
            rar[i] = rar[i]+1 
            temp[j] = i                             # saving letter code
for k in range(len(temp)-1):                        # begram rarity
    temp1 = int(temp[k])                            # first letter

    temp2 = int(temp[k+1])                          # next letter

    rar2[temp1*len(letters)+temp2] += 1             # increasing rarity of begram with (temp1, temp2)
for k1 in range(0, len(temp)-1, 2):
    temp12 = int(temp[k1])                          # first letter

    temp22 = int(temp[k1+1])                        # next letter

    rar2_step2[temp12*len(letters)+temp22] += 1

#print(rar)
#print(rar2)

rar2 = rar2/(sum(rar)-1)
rar = rar/sum(rar)
rar2ed = rar2[np.nonzero(rar2)] 
rar1 = rar[np.nonzero(rar)] 
rar2_step2 = rar2_step2/sum(rar2_step2)
rar2_step2ed = rar2_step2[np.nonzero(rar2_step2)]
H1 = -np.dot(rar1, np.log2(rar1))                   # H1
H2 = -np.dot(rar2ed, np.log2(rar2ed))/2             # H2
H2step2 = -np.dot(rar2ed, np.log2(rar2ed))/2
orig_stdout = sys.stdout
f = open('out2.txt', 'w',encoding='utf-8')
sys.stdout = f

for i in range(len(letters)):
    print (letters [i]," | ","%.7f" % rar[i],'\t')

print ("\n bigrams raritys \n")
for i in range(len(letters)):
    for j in range (len(letters)):
        print (letters [i],letters [j], " | ", "%.7f" % rar2[i*len(letters)+j], "\t")
sys.stdout = orig_stdout
f.close()
print(H1)
print(H2)
print(H2step2)