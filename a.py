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


'''
str = str.strip()
str = str.replace('\n', '')
str = str.replace(' ', '')
str = str.replace('.', '\n')
print(str)

((
((((([] p1) | ([] p2)) | ([] p3)) | ([] p5)) | ((((((((((((((((((((<> ((~p1) & ([] p1))) | (<> ((~p1) & ([] p3)))) | false) | ((<> ((~p2) & ([] p5))) | false)) | (((<> ((~p3) & ([] p1))) | (<> ((~p3) & ([] p3)))) | false)) | (false | false)) | (((<> ((~p5) & ([] p1))) | (<> ((~p5) & ([] p3)))) | false)) | (false | false)) | ((((<> (<> ((~p1) & ([] p1)))) | (<> (<> ((~p1) & ([] p3))))) | (<> (<> ((~p1) & ([] p5))))) | false)) | (false | ((<> ((~p4) & ([] p2))) | (<> ((~p6) & ([] p2)))))) | ((((<> (<> ((~p3) & ([] p1)))) | (<> (<> ((~p3) & ([] p3))))) | (<> (<> ((~p3) & ([] p5))))) | false)) | (false | ((<> ((~p4) & ([] p4))) | (<> ((~p6) & ([] p4)))))) | (((((<> (<> ((~p5) & ([] p1)))) | (<> (<> ((~p5) & ([] p3))))) | (<> (<> ((~p5) & ([] p2))))) | (<> (<> ((~p5) & ([] p5))))) | false)) | (false | ((<> ((~p4) & ([] p6))) | (<> ((~p6) & ([] p6)))))) | (false | false)) | (false | (((<> (<> ((~p2) & ([] p2)))) | (<> (<> ((~p4) & ([] p2))))) | (<> (<> ((~p6) & ([] p2))))))) | (false | false)) | (false | (((<> (<> ((~p2) & ([] p4)))) | (<> (<> ((~p4) & ([] p4))))) | (<> (<> ((~p6) & ([] p4))))))) | (false | false)) | (false | (((<> (<> ((~p2) & ([] p6)))) | (<> (<> ((~p4) & ([] p6))))) | (<> (<> ((~p6) & ([] p6)))))))) |
((((<> (<> (<> (~p2)))) | (<> (<> (<> (~p4))))) | (<> (<> (<> (~p2))))) | (<> (<> (<> (~p6)))))))