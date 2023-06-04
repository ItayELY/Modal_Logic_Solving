str = '''
 Satisfiable.

 Unsatisfiable.

 Satisfiable.

 Unsatisfiable.

 
 Satisfiable.

 
 Unsatisfiable.

 
 Satisfiable.

 
 Unsatisfiable.

 
 Satisfiable.

 
 Unsatisfiable.

 
 Satisfiable.

 
 Unsatisfiable.

 Satisfiable.

 Unsatisfiable.

 
 Satisfiable.

 
 Unsatisfiable.

 
 Satisfiable.

 Unsatisfiable.

 Unsatisfiable.

 Unsatisfiable.

 Unsatisfiable.

 Satisfiable.

 Satisfiable.

 Satisfiable.

 Unsatisfiable.

 Satisfiable.

 Satisfiable.

 Satisfiable.

 Unsatisfiable.

 Satisfiable.

 Satisfiable.

 Satisfiable.

 Satisfiable.

 Satisfiable.

 Satisfiable.

 Satisfiable.

 Satisfiable.

 Satisfiable.

 Satisfiable.

 Unsatisfiable.

 Satisfiable.

 Satisfiable.

 Satisfiable.

 Satisfiable.

 Satisfiable.

 Satisfiable.

 Satisfiable.

 Satisfiable.

 Satisfiable.

 Unsatisfiable.

 
 Satisfiable.

 Unsatisfiable.

 Unsatisfiable.

 Unsatisfiable.

 
 Satisfiable.
'''
str = str.strip()
str = str.replace('\n', '')
str = str.replace(' ', '')
str = str.replace('.', '\n')
print(str)
