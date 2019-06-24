# StarletCompiler
This is a compiler in a program language, called Starlet.

ΙΝΤΡΟ
Programming exercise aims to create a compiler. 
Implementation language is called the programming language in which the compiler is implemented. 
Python programming language is used in this programming exercise.

ABOUT STARLET
The Starlet alphabet consists of:
• the small and capital letters of the Latin alphabet ('A' - 'Z', 'a' - 'z'),
• the digits ('0' - '9'),
• the symbols of the numerical operations ('+', '-', '*', '/'),
• the correlation operators ('<', '>', '=', '<=', '> =', '<>')
• the assignment symbol (': ='),
• separators (';', ',', ':'),
• the grouping symbols ('(', ')', '[', ']'),
• and the comment splitting symbols ('/ *', '* /', '//').

Reserved words:
• program, endprogram,
• declaring,
• if, then, else, endif,
• while, endwhile, dowhile, enddowhile,
• loop, endloop, exit,
• forcase, endforcase, incase, endincase, when, default, enddefault,
• function, endfunction, return, in, inout, inandout,
• and, or, not,
• input, print.
These words can not be used as variables. 
The language constants are integral constants consisting of an optional sign and a sequence of numerals.

Starlet's grammar:
1.	<program> ::= program id <block> endprogram
2.	<block> ::= <declarations> <subprograms> <statements>
3.	<declarations> ::= (declare <varlist>;)*
4.	<varlist> ::= ε | id ( , id )*
5.	<subprograms> ::= (<subprogram>)*
6.	<subprogram> ::= function id <funcbody> endfunction
7.	<funcbody> ::= <formalpars> <block>
8.	<formalpars> ::= ( <formalparlist> )
9.	<formalparlist> ::= <formalparitem> ( , <formalparitem> )* | ε
10.	<formalparitem> ::= in id | inout id | inandout id
11.	<statements> ::= <statement> ( ; <statement> )*
12.	<statement> ::= ε |<assignment-stat> |<if-stat> |<while-stat> |<do-while-stat> |<loop-stat> |<exit-stat> |<forcase-stat> |<incase-stat> |<return-stat> |<input-stat> |<print-stat>
13.	<assignment-stat> ::= id := <expression>
14.	<if-stat> ::= if (<condition>) then <statements> <elsepart> endif
15.	<elsepart> ::= ε | else <statements>
16.	<while-stat> ::= while (<condition>) <statements> endwhile
17.	<do-while-stat> ::= dowhile <statements> enddowhile (<condition>)
18.	<loop-stat> ::= loop <statements> endloop
19.	<exit-stat> ::= exit
20.	forcase-stat> ::= forcase( when (<condition>) : <statements> )* default: <statements> enddefault endforcase
21.	<incase-stat> ::= incase( when (<condition>) : <statements> )* endincase
22.	<return-stat> ::= return <expression>
23.	<print-stat> ::= print <expression>
24.	<input-stat> ::= input id
25.	<actualpars> ::= ( <actualparlist> )
26.	<actualparlist> ::= <actualparitem> ( , <actualparitem> )* | ε
27.	<actualparitem> ::= in <expression> | inout id | inandout id
28.	<condition> ::= <boolterm> (or <boolterm>)*
29.	<boolterm> ::= <boolfactor> (and <boolfactor>)*
30.	<boolfactor> ::=not [<condition>] | [<condition>] | <expression> <relational-oper> <expression>
31.	<expression> ::= <optional-sign> <term> ( <add-oper> <term>)*
32.	<term> ::= <factor> (<mul-oper> <factor>)*
33.	<factor> ::= constant | (<expression>) | id <idtail>
34.	<idtail> ::= ε | <actualpars>
35.	<relational-oper> ::= = | <= | >= | > | < | <>
36.	<add-oper> ::= + | -
37.	<mul-oper> ::= * | /
38.	<optional-sign> ::= ε | <add-oper>


NOTES:
The compiler follows the semantic analysis as:
• each function has at least one return in it
• there is no return out of function
• there is an exit only within loop-endloop loops.

It also follows the following requirements:
• any declared variable or function or process not declared more than once at the depth of the nest in which it is located
• any variable, function, or process used has been declared, and indeed the way it is used (as a variable or as a function)
• the parameters with which the functions are called are exactly the ones with which they are declared and in the correct order.

We have only integers.

The comments,which must be within the /* and */ or after the //.
It is forbidden to open two comments before they are first closed. 
Comments inside comments are not allowed.

Starlet's files are .stl
