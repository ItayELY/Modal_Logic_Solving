
# The Molver - Modal Logic Solver
## Description
This project utilizes the Pysmt library and the Z3 solver to solve Modal Logic Formulas.

# Installation
To install the necessary dependencies, follow the steps below:  

1. Install Pysmt library:  

```bash
pip install pysmt
```  
For more detailed installation instructions, refer to the Pysmt documentation:  
https://github.com/pysmt/pysmt  

2. Install Z3 solver:  

For Linux systems, download the appropriate binary from the Z3 releases page and follow the installation instructions provided in the documentation.
For Windows systems, download the precompiled binary from the Z3 releases page and extract it to a desired location. Add the Z3 binary directory to your system's PATH variable.
# Usage
Enter a formula that complies with the syntax rules detailed bellow.
Use the following flags:  
`-l [number]` : level of satisfiability  
`-non-incremental` : try to solve using a large QBF formula  
`-incremental` : default case, solve by adding constraints incrementally each level  
`-get-model` : print valuation of satisfying assignment for each sub-formula  
`-print-final` : print the final formula that was passed to the solver, this formula should be satisfiable in Bolean Propositional Logic iff the original formula is satisfiable in Modal Logic  

Furmula Syntax Rules:  

PROPOSITIONAL SYMBOLS: an alphanumeric sequence starting with a letter: p, p1, p_1  
NOT: -, ~, not  
AND: &, and  
OR: |, or  
IMPLICATION: ->, =>, then  
ONLY IF: <-, <=  
DOUBLE IMPLICATION: <->, <=>, ifonlyif  
BOX: box, []  
DIAMOND: dia, <>  

example:  
```bash
python main.py "([](p or ~p))" -l 20 -incremental -get-model -print-final
```  

## Original Paper We Implemented
https://u.cs.biu.ac.il/~zoharyo1/ijcar22-modal.pdf
