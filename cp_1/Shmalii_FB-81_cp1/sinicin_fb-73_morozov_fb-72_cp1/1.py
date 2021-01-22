from math import log
import re

class GetResults:
    def __init__(self, **kwargs):
        self.space = int(kwargs['space'])
        self.file_in = str(kwargs['file'])
        self.encoding = str(kwargs['encoding'])
        
        self.text = ''
        self.length_text = 0
        self.freq = {}
        self.entropy = {} 
        self.redundancy = {}
        
        self.main()
	
    def main(self):
        self.clear_text()
	
        self.get_ngram(0, 1, 1)
        self.get_entropy(0, 1)
        self.get_redundancy(0)

        self.get_ngram(1, 2, 1)
        self.get_entropy(1, 2)
        self.get_redundancy(1)

        self.get_ngram(2, 2, 2)
        self.get_entropy(2, 2)
        self.get_redundancy(2)

        self.write_results()
	
    def clear_text(self):
        self.text = ' '.join((open(self.file_in, encoding=self.encoding).read()).split())
        cleared_text = ''

        for symbol in self.text:
            match = re.match('[а-я ]$', symbol.lower())
            if match:
                symbol = match.group(0)
                if symbol == 'ъ':
                    symbol = 'ь'
                elif symbol == 'ё':
                    symbol = 'е'

                cleared_text += str(symbol)
	
        self.text = cleared_text.replace(' ', '' if self.space == 0 else '_')
        self.text = ' '.join(self.text.split())
        self.length_text = len(self.text)
	
    def get_ngram(self, cell, num, step):
        freq = {}
        for i in range(0, self.length_text - (num + 1), step):
            n = self.text[i : i + num]
            freq[n] = (freq[n] + 1) if n in freq else 1

        for key in freq.keys():
            freq[key] *= step / self.length_text

        self.freq[cell] = freq
	
    def get_entropy(self, cell, length):
        e = 0
        for i in self.freq[cell].values():
            e += i * log(i, 2)
		
        self.entropy[cell] = -e / length
	
    def get_redundancy(self, cell):
        self.redundancy[cell] = 1 - (self.entropy[cell] / log(33, 2))
	
    def write_results(self):
        file_out = 'out_{}_{}'.format(self.space, self.file_in)
        fopen = open(file_out, 'w+', encoding=self.encoding)

        fopen.write("Пробелы: Выкл\n\n" if self.space == 0 else "Пробелы: Вкл\n\n")

        title = ['Буквы', 'Биграмма (1)', 'Биграмма (2)']
        for i in range(3):
            fopen.write(' • {}:\n  Entropy = {}\n  Redundancy =  {}\n'.format(title[i], self.entropy[i], self.redundancy[i]))

        title = ['ЧАСТОТА БУКВ', 'ЧАСТОТА БИГРАМ С СЕЧЕНИЕМ', 'ЧАСТОТА БИГРАМ БЕЗ СЕЧЕНИЯ']
        for i in range(3):
            fopen.write('\n\n{}\n'.format(title[i]))
            for s, value in sorted(self.freq[i].items()):
                if self.space == 0:
                    fopen.write('{} = {:.5f}\n'.format(s, value))
                else:
                    fopen.write('{} = {:.5f}\n'.format(s, self.freq[i][s]))

        print("\nРезультаты записаны в {}!".format(file_out))
        fopen.close()

if __name__ == '__main__':
    print("Без пробелов / С пробелами = 0 / 1: ")
    space = int(input())

    print("\nВведите файл для чтения: ")
    file = str(input())
	
    print("\nВведите кодировку файла: ")
    encoding = str(input())
	
    GetResults(space=space, file=file, encoding=encoding)
