'''module used to convert different units 
white space sensitive
all strings should be written in words 
syntax  --> convert {quantity} {unit} to {unit}
    Example:
        from Ekpenisi_Christabell_Edu1803928 import Units
        text = 'convert five cm to m'
        Units.convert(text)
        
'''
from semantics.number import Number
class Units(object):
    def __init__(self):
        self.fro = None
        self.fro_unit = None
        self.to = None
        self.to_unit = None
        #dictionaries of possible conversions
        self.length = {'m':1,'cubit':0.5,'inch':0.0254,'ft':0.3046,'mile':1853.79,'yard':0.9144,'km':1000,'cm':0.01,'mm':0.001}
        self.area = {'m2':1,'acre':4046.856,'hectare':10000,'sqft':0.09290304,'sqinch':0.00064516,'sqkm':10000000}
        self.time ={'sec':1,'min':60,'hour':3600,'day':86400,'week':604800,'month':2419200,'year':29030400}
    def preprocess(self,input):
        '''
      function that matches users inputs
      it looks for different permutations of an operation and rearranges it into the standard type
       Example:
           convert five seconds to minuites becomes convert five cm to min
      '''
        input = input.replace('cubits','cubit')
        input = input.replace('inches','inch')
        input = input.replace('foot','ft')
        input = input.replace('feet','ft')
        input = input.replace('miles','mile')
        input = input.replace('yards','yard')
        input = input.replace('acres','acre')
        input = input.replace('hectares','hectare')
        input = input.replace('square foot','sqft')
        input = input.replace('sq ft','sqft')
        input = input.replace('square inch','sqinch')
        input = input.replace('sq inch','sqinch')
        input = input.replace('seconds','sec')
        input = input.replace('second','sec')
        input = input.replace('secs','sec')
        input = input.replace('minuite','min')
        input = input.replace('minuites','min')
        input = input.replace('hours','hour')
        input = input.replace('hrs','hour')
        input = input.replace('days','day')
        input = input.replace('wk','week')
        input = input.replace('wks','week')
        input = input.replace('weeks','week')
        input = input.replace('months','month')
        input = input.replace('years','year')
        return input 
    def convert(self,word):
       '''
       function for conversion
       '''
       self.fro = None
       self.fro_unit = None
       self.to = None
       self.to_unit = None
       word = self.preprocess(word).lower()
       a = ''
       if 'convert ' not  in word or ' to ' not in word:
        print('Invalid syntax\n Syntax --> "convert {quantity} {unit1} to {unit2}')
       else:
        c = word.split('convert ')
        for x in c:
            a+=x
        a = a.lstrip().rstrip()
        c = a.split(' to ')
        check = 'cubit inch ft mile yard km cm mm acre hectare sqft sqinch sqkm min hour days weeks months years sec m2'
        d = c[0].split(' ')
        temp = ''
        for x in d :
            if x not in check:
                temp += f'{x} '                
            else:
                if temp!='':
                    converter = Number()
                    self.fro = int(converter.converted(temp.rstrip()))
                    self.fro_unit = str(x)
                    self.to_unit = str(c[1])
        return self.evaluate(self.unit())
    def unit(self):
       try:
        if self.to_unit and self.fro_unit in self.length:
            if self.to_unit !='m' or self.fro_unit != 'm':
                self.to = 1
                self.to *= (self.fro *self.length[self.fro_unit])/self.length[self.to_unit]
                return self.to
            else:
                if self.to_unit == 'm':
                    self.to = 1
                    self.to *= self.length[self.fro_unit] * self.fro
                    return self.to
                elif self.fro_unit =='m':
                    self.to = 1
                    self.to *= self.length[self.fro_unit]/self.fro
                    return self.to
        elif self.to_unit and self.fro_unit in self.area:
            if self.to_unit !='m2' or self.fro_unit != 'm2':
                self.to = 1
                self.to *= (self.fro *self.area[self.fro_unit])/self.area[self.to_unit]
                return self.to
            else:
                if self.to_unit == 'm2':
                    self.to = 1
                    self.to *= self.area[self.fro_unit] * self.fro
                    return self.to
                elif self.fro_unit =='m2':
                    self.to = 1
                    self.to *= self.area[self.fro_unit]/self.fro
                    return self.to
        elif self.to_unit and self.fro_unit in self.time:
            if self.to_unit !='sec' or self.fro_unit != 'sec':
                self.to = 1
                self.to *= (self.fro *self.time[self.fro_unit])/self.time[self.to_unit]
                return self.to
            else:
                if self.to_unit == 'sec':
                    self.to = 1
                    self.to *= self.time[self.fro_unit] * self.fro
                    return self.to
                elif self.fro_unit =='sec':
                    self.to = 1
                    self.to *= self.time[self.fro_unit]/self.fro
                    return self.to
       except:
           print(f'cannot convert from {self.fro_unit} to {self.to_unit}')

    def evaluate(self,word):
        # prints the answer to the screen
        if word is not None:
            print(f'{self.to} {self.to_unit}')
        else:
            print(f'Error: either one of the units is not convertible or you missed a number')
      
                                
                
        
        
        
        
        