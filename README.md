# BREWIN INTERPRETER IN PYTHON (VERSION 2 IS NOW OUT)

**NOW SUPPORTS INHERITANCE, PARAMETRIC POLYMORPHISM, STATIC TYPING, VARIABLE SHADOWING**

1. Clone the repository to your local machine.

2. Write a program in Brewin:

```brewin
(class obj
  (method obj obj_call ()
    (print "object")
  )
)

(class main
  (field obj object null)
  (method void main ()
    (begin
      (set object (new obj))
      (print (call me void_call))
      (print (call me null_call))
      (print (call me int_call))
      (print (call me bool_call))
      (print (call me string_call))
      (print (call object obj_call))
    )
  )
  
  (method void void_call ()
    (print "void")
  )
  (method main null_call ()
    (print "null")
  )
  (method int int_call ()
    (print "int")
  )
  (method bool bool_call ()
    (print "bool")
  )
  (method string string_call ()
    (print "string")
  )
)

3. Put the file into input.txt and run python3 interpreter.py.

4. Watch your Brewin Program get interpreted.
