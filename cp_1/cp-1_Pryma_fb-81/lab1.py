import numpy as np
from xlwt import Workbook  # Для роботи з excel


file = open("text1.txt", "r", encoding='utf-8')
text = file.read()
symbols2remove = ['.', ',', '!', ':', ';', '-', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '—', '»', '«']
for k in range(len(symbols2remove)):
    text = text.replace(symbols2remove[k], "")
text = text.lower()
alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п',
            'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ь', 'ы', 'ъ', 'э', 'ю', 'я', ' ']
H0 = np.log2(len(alphabet))
frequency = np.zeros(len(alphabet))
frequency_of_bigrams1 = np.zeros(pow(len(alphabet), 2))  # З перетином
frequency_of_bigrams2 = np.zeros(pow(len(alphabet), 2))  # Без перетину
text_in_numbers = np.zeros(len(text), dtype=int)

for i in range(len(alphabet)):  # цикл для пвідрахунку частот монограм та перекодування тексту
    for j in range(len(text)):
        if text[j] == alphabet[i]:
            frequency[i] = frequency[i] + 1
            text_in_numbers[j] = i

for i in range(1, len(text_in_numbers)):  # цикл для пвідрахунку частот біграм (з перетином)
    char_1 = text_in_numbers[i - 1]
    char_2 = text_in_numbers[i]
    bigram_index = char_1 * len(alphabet) + char_2
    frequency_of_bigrams1[bigram_index] = frequency_of_bigrams1[bigram_index] + 1
for i in range(1, len(text_in_numbers) // 2, 2):  # цикл для пвідрахунку частот біграм (без перетинів)
    char_1 = text_in_numbers[2 * i - 2]
    char_2 = text_in_numbers[2 * i - 1]
    bigram_index = char_1 * len(alphabet) + char_2
    frequency_of_bigrams2[bigram_index] = frequency_of_bigrams2[bigram_index] + 1

frequency = frequency / sum(frequency)

frequency_of_bigrams1 = frequency_of_bigrams1 / sum(frequency_of_bigrams1)
original1 = frequency_of_bigrams1
frequency_of_bigrams1 = frequency_of_bigrams1[np.where(frequency_of_bigrams1 != 0)]

frequency_of_bigrams2 = frequency_of_bigrams2 / sum(frequency_of_bigrams2)
original2 = frequency_of_bigrams2
frequency_of_bigrams2 = frequency_of_bigrams2[np.where(frequency_of_bigrams2 != 0)]

H1 = -sum(i * j for i, j in zip(frequency, np.log2(frequency)))

H21 = -sum(i * j for i, j in zip(frequency_of_bigrams1, np.log2(frequency_of_bigrams1))) / 2

H22 = -sum(i * j for i, j in zip(frequency_of_bigrams2, np.log2(frequency_of_bigrams2))) / 2

output = Workbook()
Sheet1 = output.add_sheet('monograms')
Sheet1.write(0, 0, "Letter")
Sheet1.write(0, 1, "Frequency")
for i in range(len(alphabet)):
    Sheet1.write(i + 1, 0, alphabet[i])
    Sheet1.write(i + 1, 1, frequency[i])
Sheet1.write(1, 3, f"H1 ={H1}")


Sheet2 = output.add_sheet('Bigrams (no intersection)')
Sheet2.write(0, 1, "second letter")
Sheet2.write(1, 0, "first letter")
Sheet2.write(1, 1, "frequency of bigrams")
for i in range(len(alphabet)):
    Sheet2.write(0, i + 2, alphabet[i])
for i in range(len(alphabet)):
    Sheet2.write(i + 2, 0, alphabet[i])
for i in range(len(alphabet)):
    for j in range(len(alphabet)):
        Sheet2.write(i + 2, j + 2, original1[i * len(alphabet) + j])
Sheet2.write(0, 0, f"H2 = {H21}\n")


Sheet3 = output.add_sheet('Bigrams (with intersection)')
Sheet3.write(0, 1, "second letter")
Sheet3.write(1, 0, "first letter")
Sheet3.write(1, 1, "frequency\n of bigrams")
for i in range(len(alphabet)):
    Sheet3.write(0, i + 2, alphabet[i])
for i in range(len(alphabet)):
    Sheet3.write(i + 2, 0, alphabet[i])
for i in range(len(alphabet)):
    for j in range(len(alphabet)):
        Sheet3.write(i + 2, j + 2, original2[i * len(alphabet) + j])
Sheet3.write(0, 0, f"H2 = {H22}\n")
output.save('with_spaces.xls')

print(H1)
print(H21)
print(H22)
