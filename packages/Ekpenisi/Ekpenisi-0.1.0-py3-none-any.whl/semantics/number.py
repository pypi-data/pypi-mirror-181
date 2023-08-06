'''
function to convert numbers written in words to text
white space sensitive and comma strict
e.g 500,256 should be five hundred thousand,two hundred and fifty six and not five hundred thousand two hundred and fifty six  i.e commas are important 
   Example:
       from Ekpenisi_Christabell_Edu1803928 import Number 
       text = 'eight hundred thousand, two hundred and sixty two'
       Number.converts(text)
       returns 800262

'''
import re
class Number(object):
    def __init__(self):
        self.small = {'zero': 0,'one': 1,        'two': 2,        'three': 3,        'four': 4,        'five': 5,        'six': 6,        'seven': 7,        'eight': 8,        'nine': 9,        'ten': 10,        'eleven': 11,        'twelve': 12,        'thirteen': 13,        'fourteen': 14,        'fifteen': 15,        'sixteen': 16,        'seventeen': 17,        'eighteen': 18,        'nineteen': 19,        'twenty': 20,        'thirty': 30,        'forty': 40,        'fifty': 50,        'sixty': 60,        'seventy': 70,       'eighty': 80,        'ninety': 90    }      
        self.magnitude = {'hundred':100,'thousand':     1000,        'million':      1000000,        'billion':      1000000000,        'trillion':     1000000000000,        'quadrillion':  1000000000000000,        'quintillion':  1000000000000000000,        'sextillion':   1000000000000000000000,        'septillion':   1000000000000000000000000,        'octillion':    1000000000000000000000000000,        'nonillion':    1000000000000000000000000000000,        'decillion':    1000000000000000000000000000000000,    }    
        
    def converts(self,word):
        '''
        function that converts word to digit
        returns a string 
        '''
        if 'point' in word:
            b = self.text_float(word)
            if b is None:
                pass
            else:
                print(b)
        else:
            b = self.text_int(word)
            if b is None:
                pass
            else:
                print(b)
    def converted(self,word):
         if 'point' in word:
            return self.text_float(word)
         else:
            return self.text_int(word)
    def text_int(self,word):
       if self.valid(word.lower()):
        word = word.lower()
        self.token = word.split(',')
        return self.convert(self.token)
   
    def convert(self,word,x=0):
        if x == len(self.token):
            return 0
        else:
           return self.convert_fraction(self.token[x]) + self.convert(word,x=x+1)
    def convert_fraction(self,word):
            m = word.split(' and ')
            if len(m) == 1:
                m1 = word.rstrip().split(' ')
                ans = 1
                if len(m1) == 2 and m1[-1] not in self.magnitude:
                    ans = 0
                    ans = self.small[m1[0]] + self.small[m1[1]]
                    return ans
                else:
                 for x in m1:
                    if x in self.magnitude:
                        ans *= self.magnitude[x]
                    elif x in self.small:
                        ans *= self.small[x]
                return ans
            else:
                ans = self.convert_fraction(m[0])
                b = str(m[1]).split(' ')
                for x in b:
                    if x in self.small:
                        ans+= self.small [x]         
                if b[-1] in self.magnitude:
                    ans *= self.magnitude[b[-1]]
                return ans
    def text_float(self,word):
        m = re.search(r'(.*)point(.*)',word)
        ans=''
        for x in m.group(2).split(' '):
            if x in self.small:
                ans = ans + str(self.small[x])
        ans = '.' + ans
        return str(self.text_int(m.group(1))) + ans
    def valid(self,word):
        word = word.rstrip().lstrip()
        token = word.split(' ')
        temp = ''
        for x in token:
            if x ==  ' ' or x == '':
                print('Space error ---> too much spaces between words')
                return False
        for x in token:
            x = x.rstrip().lstrip()
            if ',' not in x:
                temp += f'{x} '
            else:
                temp += f'{x} '
        temp = temp.rstrip().lstrip()
        token = temp.split(',')
        for x in token:
           b = x.split(' ')
           for y in b:
               if y not in self.small and y not in  self.magnitude and y != ' ' and y!= 'and':
                   print(f'Key error --> {y} is not a valid numerical string,\n or you must have put a white space after the comma')
                   return False          
        return True 
    