'''
module used to solve equation  from text 
white space sensitive.
 All the string should be written in words , even the numbers 
  Example:
      from Ekpenisi_Christabell_Edu1803928 import Solver
      text = 'ten minus two'
      Solver.solve(text)
      #this prints 8 as the answer 
       # using 10 minus 2 as the string would result to an error
      
'''
from math import sqrt, sin, cos, log, tan, acos, asin, atan, e, pi, factorial ,radians
from semantics.number import Number
class Solver(object):
    def __init__(self):
        #constants
        self.constants= {        'e': e,        'E': e,        'EE': e,        'pi': pi,        'pie': pi    }
        #valid operations    
        self.operators = {        'log': log,        'sine': sin,        'sin': sin,        'cosine': cos,        'cos': cos,        'tan': tan,        'tangent': tan,        'arcsine': asin,        'arcsin': asin,        'asin': asin,        'arccosine': acos,        'arccos': acos,        'acos': acos,        'arctanget': atan,        'arctan': atan,        'atan': atan,        'sqrt': sqrt,'plus':'+','minus':'-' ,'times':'*','divide':'/','to':'**'}   
        
    def preprocess(self,input):
      '''
      function that matches users inputs
      it looks for different permutations of an operation and rearranges it into the standard type
       Example:
           ten raised to the power of 2 becomws ten to 2
           three over two becomes three divide two
      '''
      self.equation = ''
      input = input.replace('to the power','to')
      input = input.replace('raised to the power of','to')
      input = input.replace('raised to power','to')
      input = input.replace('log of', 'log')
      input = input.replace('square root of','sqrt')
      input = input.replace('root of','sqrt')
      input = input.replace('squared', 'to two')     
      input = input.replace('cubed', 'to three')
      input = input.replace('divided by', 'divide')
      input = input.replace('over', 'divide')      
      input = input.replace("arccos","acos")
      input= input.replace("arccosine","acos")
      input= input.replace("cosine","cos")
      input = input.replace("arcsine","asin")  
      input = input.replace("sine","sin")   
      input = input.replace("arcsin","asin")
      input = input.replace("arctangent","atan")   
      input = input.replace("arctan","asin")
      input = input.replace('over', 'divide')     
      input = input.replace('pie', 'pi')     
      input = input.replace('Pi','pi')
      return input
    def solve(self, word):
      '''
      the function called to solve the text
      :param : text to be solved
      it takes the returned value from the preprocess function and solves it . returns and error if  text is of invalid format
      
      '''
      word = self.preprocess(word)
      token = word.split(' ')
      temp=''
      flag = False
      flag1 = False
      b = 'to e pi tan sin cos divide minus plus times factorial asin acos atan log sqrt'
      c = 'e pi to factorial log sqrt'
      d =  ' tan sin cos asin acos atan'
      for x in token:
          if x not in b:
                  temp += f'{x} '
          else:
              if temp !='':
                  converter = Number()
                  tokens = str(converter.converted(temp.rstrip()))
                  if flag is not None:
                   if flag:
                      self.equation += tokens + ')'
                      flag = False
                   else:
                      self.equation += tokens 
                  else:
                       if flag1:
                        self.equation += tokens + '))'
                        flag1 = False
                       else:
                        self.equation += tokens 
              if x in c:
                  if flag:
                      self.equation += f' ){x}('
                      flag = False
                  else:
                      self.equation += f' {x}('
                      flag = True                 
              elif x in d:
                  flag = None
                  if flag1:
                      self.equation += f' ){x}(radians('
                      flag1 = False
                  else:
                      self.equation += f' {x}(radians('
                      flag1=True
              else:                 
                  self.equation += f' {self.operators[x]} ' 
              temp = ''      
      if temp !='':
                  converter = Number()
                  tokens = str(converter.converted(temp.rstrip()))
                  if flag is not None:
                   if flag:
                      self.equation += f'{tokens})'
                      flag = False
                   else:
                     self.equation += f'{tokens}'
                  else:
                      if flag1:
                          self.equation += f'{tokens}))'
                          flag1= False
                      else:
                         self.equation += f'{tokens}'
      return self.evaluate(self.equation)
    def evaluate(self,eq):
      '''
      prints the answer
      '''
      try: 
          b = eval(eq)
          print(f'{eq} = {b}')
          return b 
      except:
          print('The equation is invalid')
