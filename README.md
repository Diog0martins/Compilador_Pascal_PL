# Compilador Pascal - Projeto PL

## Introdução
Este projeto foi proposto com o intuito de desenvolver um **compilador** com uma arquitetura de **pipeline de compilação modular**, capaz de processar **código em Pascal (standard)**. Após todas as fases de análise que este efetuará, este deverá **gerar um output** com toda a informação processada, **numa linguagem semelhante a Assembly** (que posteriormente, terá de conseguir ser executado na máquina virtual disponibilizada pelos docentes)

Como ferramentas, utilizamos maioritariamente a API da biblioteca **Python PLY** (Python Lex-Yacc) e **regex** para implementar o **Analisador léxico** e **sintático**. 

 - **Analisador léxico**
 Efetua a análisa e reconhecimento de tokens com auxílio de expressões regulares.
 
 - **Analisador sintático**
 Após ser definida uma gramática, permite a implementação desta e a definição das regras de linguagem, que permitam o melhor funcionamento do processamento do input. Para isto, foi empregado o módulo **YACC**

Para além disto, decidimos criar uma "**tabela de símbolos**" que permite a **análise semântica** de qualquer operação esperada em Pascal (standard). Esta tabela contém informação sobre *variáveis* e *funções* definidas no código recebido, tais como:
 - O **ID** (nome atribuído) de funções e variáveis;
 - O **scope** que cada variável tem (se se trata de uma **variável global** ou **local** a uma dada função);
 - O **tipo** de uma variável;
 - A **posição** à qual uma variável se encontra na **stack** (ou relativa ao **frame pointer**, caso se trate de um **argumento de uma função**);
 - O **tipo do valor a ser devolvido** por uma função: 
   - e.g. (<u>funtion Add2Numbers(a, b: Integer): **Integer**</u>);
 - O **tipo de cada argumento** de uma função;
 - E uma **expressão** associada ao valor a ser retornado por uma dada função.


Assim, através das análises **léxica**, **sintática** e **semântica**, o compilador irá efetuar uma **tradução determinística baseada em gramáticas e semântica formal**,  processando o código de input em Pascal (standard) e gerando código numa linguagem de baixo nível (anteriormente mencionada), que será utilizada na  máquina virtual disponibilizada.

Após tudo ter sido efetuado, serão realizados testes para verificar a **integridade do código resultante** e a **correta execução das instruções geradas** (sendo que, o comportamento da execução do código resultante tem de ser semelhante à execução do código inicial em Pascal).

Por fim, serão discutidas potenciais melhorias e conclusões obtidas do desenvolvimento do projeto.

## Analisador léxico

Após especificar quais os **tokens** e **símbolos literais** que serão utilizados na gramática, o **Analisador léxico** usa as **Expressões regulares** a que estes estão associados para reconhecer cada **token** presente no código que foi fornecido. São definidos também comportamentos específicos para casos especiais já esperados pelo **lexer** (e.g. ignorar qualquer *whitespace* não associado a uma string ).

As **Expressões regulares** são processadas e trabalham com a **API** relativa ao **regex** em python, para a tal **captura de tokens**.

Com isto, conseguimos traduzir, tanto as **palavras reservadas** como também os **símbolos literais** para uma **liguagem em tokens**. Foi também aqui que foram feitos os tratamentos de erros léxicos.

### Exemplo

Para o seguinte programa, é feito parse dos tokens da presente em
[parsed tokens](Anexos/tokens.txt).

```pascal
1  |  program Tokenizer;
2  |  var
3  |     num: integer;
4  |  
5  |  begin
6  |     num := 5; 
7  |     while num < 5 do 
8  |     begin
9  |         num := num + 1;
10 |         writeln('teste'); 
11 |     end; 
12 |  end.
```

| Linha de código          | Tokens do Lexer                                                                                                                                   |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `program Tokenizer;` | LexToken(**PROGRAM**,'program',1,5)<br>LexToken(ID,'Tokenizer',1,13)                                                                            |
| `var num: integer;`  | LexToken(**VAR**,'var',1,29)<br>LexToken(**ID**,'num',1,41)<br>LexToken(**:**,':',1,44)<br>LexToken(**INTEGER**\_TYPE,'integer',1,46)                      |
| `begin`              | LexToken(**BEGIN**,'begin',1,60)                                                                                                                |
| `num := 5;`          | LexToken(**ID**,'num',1,74)<br>LexToken(**ASSIGN**,':=',1,78)<br>LexToken(**INTEGER**,'5',1,81)                                                         |
| `while num < 5 do`   | LexToken(**WHILE**,'while',1,93)<br>LexToken(**ID**,'num',1,99)<br>LexToken(**<**,'<',1,103)<br>LexToken(**INTEGER**,'5',1,105)                             |
| `begin`              | LexToken(**DO**,'do',1,107)<br>LexToken(**BEGIN**,'begin',1,119)                                                                                    |
| `num := num + 1;`    | LexToken(**ID**,'num',1,137)<br>LexToken(**ASSIGN**,':=',1,141)<br>LexToken(**ID**,'num',1,144)<br>LexToken(**+**,'+',1,148)<br>LexToken(**INTEGER**,'1',1,150) |
| `writeln('teste');`  | LexToken(**ID**,'writeln',1,165)<br>LexToken(**(**,'(',1,172)<br>LexToken(**STRING**,"'teste'",1,173)<br>LexToken(**)**,')',1,180)                          |
| `end;`               | LexToken(**;**,';',1,181)<br>LexToken(**END**,'end',1,192)                                                                                          |
| `end.`               | LexToken(**;**,';',1,195)<br>LexToken(**END**,'end',1,202)<br>LexToken(**.**,'.',1,205)                                                                 |

Além das regras da linguagem Pascal, destaca-se o facto de não se distinguirem maiúsculas de minúsculas na identificação de identificadores (**IDs**). 
 Por **IDs** entende-se tudo o que não é uma string, nem um **símbolo reservado** (**token**), mas sim uma palavra definida pelo utilizador (e.g. utilizados para **variáveis** e **funções**).

 Para casos mais específicos, o uso de **Expressões Regulares** veio a ser necessário. Como exemplo, temos que, a captura de uma **string** e de um **ID** é feita com auxílio da seguinte expressão:

 ```python
 def t_STRING(t):
    r'(?P<quote>[\'\"])[^\'\"]*?(?P=quote)'
    return t

def t_ID(t):
    r'\b[A-Za-z](?:\w+?)?\b'
    return t
 ```

## Analisador sintático

Com uma gramática concreta e bem definida, o **Analisador sintático**, através do **ply.yacc**, efetua comportamentos que tenham sido definidos para cada produção criada. e permite 

A componente sintática define as produções para a gramática, assim como o comportamento que os símbolos traduzem. Neste contexto, traduzem as linhas de código pascal para o código máquina.

É utilizado o parser oferecido pelo módulo, ficando a nosso cargo a criação das produções, através de docstring, e através da construção de funções para tratar as produções.

Sendo este componente caracterizado pela sua complexidade, foi necessário a separação por vários módulos, cada um com produções referentes a um tópico.

### pascal_anasin.py

Este módulo aglomera os módulos com produções, define o tratamento de erros sintáticos, cria o parser e é definido a função de reconhecimento

## Analisador semântico

Em relação a análise semântica, esta é realizada parcialmente através de um

## Geração de código

## Teste

Para testar o nosso compilador foram usados os exemplos presentes no enunciado.

---
**Exemplo 1:**
```py
1  | program HelloWorld;
2  | var
3  |     num: integer;
4  |
5  | begin
6  |     num := 0;
7  |     while num < 1 do
8  |     begin
9  |         writeln('Ola, Mundo!', 3);
10 |         write('Ola, Mundo!', 3);
11 |         num := num + 1;
12 |     end;
13 | end.
```

**Resultado da Compilação em Código Máquina:**
```
1  | START  
2  | PUSHS "Ola, Mundo!"  
3  | WRITES  
4  | PUSHI 3  
5  | WRITEI  
6  | WRITELN  
7  | PUSHS "Ola, Mundo!"  
8  | WRITES  
9  | PUSHI 3  
10 | WRITEI  
11 | STOP  
```
---

**Exemplo 2:**
```py
1  | program Maior3;
2  | var
3  |     num1, num2, num3, maior, num: integer;
4  |
5  | begin
6  |     num := 0;
7  |     while num < 1 do
8  |     begin
9  |         write('Introduza o primeiro número: ');
10 |         readln(num1);
11 |         write('Introduza o segundo número: ');
12 |         readln(num2);
13 |         write('Introduza o terceiro número: ');
14 |         readln(num3);
15 |         if num1 > num2 then
16 |             if num1 > num3 then
17 |                 maior := num1
18 |             else
19 |                 maior := num3
20 |         else
21 |             if num2 > num3 then
22 |                 maior := num2
23 |             else
24 |                 maior := num3;
25 |         writeln('O maior é: ', maior);
26 |         num := num + 1;
27 |     end;
28 | end.
```

**Resultado da Compilação em Código Máquina:**
```
1  | PUSHI 0  
2  | PUSHI 0  
3  | PUSHI 0  
4  | PUSHI 0  
5  | START  
6  | PUSHS "Introduza o primeiro número: "  
7  | WRITES  
8  | READ  
9  | ATOI  
10 | STOREG 0  
11 | WRITELN  
12 | PUSHS "Introduza o segundo número: "  
13 | WRITES  
14 | READ  
15 | ATOI  
16 | STOREG 1  
17 | WRITELN  
18 | PUSHS "Introduza o terceiro número: "  
19 | WRITES  
20 | READ  
21 | ATOI  
22 | STOREG 2  
23 | WRITELN  
24 | PUSHG 0  
25 | PUSHG 1  
26 | SUP  
27 | JZ ELSE3  
28 | PUSHG 0  
29 | PUSHG 2  
30 | SUP  
31 | JZ ELSE1  
32 | PUSHG 0  
33 | STOREG 3  
34 | JUMP ENDIF1  
35 | ELSE1:  
36 | PUSHG 2  
37 | STOREG 3  
38 | ENDIF1:  
39 | JUMP ENDIF3  
40 | ELSE3:  
41 | PUSHG 1  
42 | PUSHG 2  
43 | SUP  
44 | JZ ELSE2  
45 | PUSHG 1  
46 | STOREG 3  
47 | JUMP ENDIF2  
48 | ELSE2:  
49 | PUSHG 2  
50 | STOREG 3  
51 | ENDIF2:  
52 | ENDIF3:  
53 | PUSHS "O maior é: "  
54 | WRITES  
55 | PUSHG 3  
56 | WRITEI  
57 | WRITELN  
58 | STOP   
```
---

**Exemplo 3:**
```py
1  | program Fatorial;
2  | var
3  |     n, i, fat, num: integer;
4  |
5  | begin
6  |     num := 0;
7  |     while num < 1 do
8  |     begin
9  |         writeln('Introduza um número inteiro positivo:');
10 |         readln(n);
11 |         fat := 1;
12 |         for i := 1 to n do
13 |             fat := fat * i;
14 |         writeln('Fatorial de ', n, ': ', fat);
15 |         num := num + 1;
16 |     end;
17 | end.
```

**Resultado da Compilação em Código Máquina:**
```
1  | PUSHI 0
2  | PUSHI 0
3  | PUSHI 0
4  | START
5  | PUSHS "Introduza um número inteiro positivo:"
6  | WRITES
7  | WRITELN
8  | READ
9  | ATOI
10 | STOREG 0
11 | WRITELN
12 | PUSHI 1
13 | STOREG 2
14 | PUSHI 1
15 | STOREG 1
16 | PUSHG 0
17 | PUSHI 1
18 | ADD
19 | FORSTART0:
20 | PUSHL 0
21 | PUSHG 1
22 | EQUAL
23 | NOT
24 | JZ FOREND0
25 | PUSHG 2
26 | PUSHG 1
27 | MUL
28 | STOREG 2
29 | PUSHG 1
30 | PUSHI 1
31 | ADD
32 | STOREG 1
33 | JUMP FORSTART0
34 | FOREND0:
35 | POP 1
36 | PUSHS "Fatorial de "
37 | WRITES
38 | PUSHG 0
39 | WRITEI
40 | PUSHS ": "
41 | WRITES
42 | PUSHG 2
43 | WRITEI
44 | WRITELN
45 | STOP 
```
---

**Exemplo 4:**
```py
1  | program NumeroPrimo;
2  | var
3  |     num, i: integer;
4  |     primo: boolean;
5  |
6  | begin
7  |     writeln('Introduza um número inteiro positivo:');
8  |     readln(num);
9  |     primo := true;
10 |     i := 2;
11 |     while (i <= (num div 2)) and primo do
12 |     begin
13 |         if (num mod i) = 0 then
14 |             primo := false;
15 |         i := i + 1;
16 |     end;
17 |     if primo then
18 |         writeln(num, ' é um número primo')
19 |     else
20 |         writeln(num, ' não é um número primo')
21 | end.
```

**Resultado da Compilação em Código Máquina:**
```
1  | PUSHI 0  
2  | PUSHI 0  
3  | PUSHI 0  
4  | START  
5  | PUSHS "Introduza um número inteiro positivo:"  
6  | WRITES  
7  | WRITELN  
8  | READ  
9  | ATOI  
10 | STOREG 0  
11 | WRITELN  
12 | PUSHI 1  
13 | STOREG 2  
14 | PUSHI 2  
15 | STOREG 1  
16 | WHILE1:  
17 | PUSHG 1  
18 | PUSHG 0  
19 | PUSHI 2  
20 | DIV  
21 | INFEQ  
22 | PUSHG 2  
23 | AND  
24 | JZ ENDWHILE1  
25 | PUSHG 0  
26 | PUSHG 1  
27 | MOD  
28 | PUSHI 0  
29 | EQUAL  
30 | JZ ELSE1  
31 | PUSHI 0  
32 | STOREG 2  
33 | JUMP ENDIF1  
34 | ELSE1:  
35 | ENDIF1:  
36 | PUSHG 1  
37 | PUSHI 1  
38 | ADD  
39 | STOREG 1  
40 | JUMP WHILE1  
41 | ENDWHILE1:  
42 | PUSHG 2  
43 | JZ ELSE2  
44 | PUSHG 0  
45 | WRITEI  
46 | PUSHS " é um número primo"  
47 | WRITES  
48 | WRITELN  
49 | JUMP ENDIF2  
50 | ELSE2:  
51 | PUSHG 0  
52 | WRITEI  
53 | PUSHS " não é um número primo"  
54 | WRITES  
55 | WRITELN  
56 | ENDIF2:  
57 | STOP  
```
---


**Exemplo 5:**
```py
1  | program SomaArray;
2  | var
3  |     numeros: array[1..5] of integer;
4  |     i, soma: integer;
5  |
6  | begin
7  |     soma := 0;
8  |     writeln('Introduza 5 números inteiros:');
9  |     for i := 1 to 5 do
10 |     begin
11 |         readln(numeros[i]);
12 |         soma := soma + numeros[i];
13 |     end;
14 |     writeln('A soma dos números é: ', soma);
15 | end.
```

**Resultado da Compilação em Código Máquina:**
```
1  | PUSHN 5
2  | PUSHI 0
3  | PUSHI 0
4  | START
5  | PUSHI 0
6  | STOREG 6
7  | PUSHS "Introduza 5 números inteiros:"
8  | WRITES
9  | WRITELN
10 | PUSHI 1
11 | STOREG 5
12 | PUSHI 5
13 | PUSHI 1
14 | ADD
15 | FORSTART0:
16 | PUSHL 0
17 | PUSHG 5
18 | EQUAL
19 | NOT
20 | JZ FOREND0
21 | PUSHGP
22 | PUSHI 0
23 | PADD
24 | PUSHG 5
25 | PUSHI 1
26 | SUB
27 | READ
28 | ATOI
29 | STOREN
30 | WRITELN
31 | PUSHG 6
32 | PUSHGP
33 | PUSHI 0
34 | PADD
35 | PUSHG 5
36 | PUSHI 1
37 | SUB
38 | LOADN
39 | ADD
40 | STOREG 6
41 | PUSHG 5
42 | PUSHI 1
43 | ADD
44 | STOREG 5
45 | JUMP FORSTART0
46 | FOREND0:
47 | POP 1
48 | PUSHS "A soma dos números é: "
49 | WRITES
50 | PUSHG 6
51 | WRITEI
52 | WRITELN
53 | STOP
```
---

**Exemplo 6:**
```py
1  | program BinarioParaInteiro;
2  | var
3  |     bin: string;
4  |     i, valor, potencia: integer;
5  |
6  | begin
7  |     writeln('Introduza uma string binária:');
8  |     readln(bin);
9  |     valor := 0;
10 |     potencia := 1;
11 |     for i := length(bin) downto 1 do
12 |     begin
13 |         if bin[i] = '1' then
14 |             valor := valor + potencia;
15 |         potencia := potencia * 2;
16 |     end;
17 |     writeln('O valor inteiro correspondente é: ', valor);
18 | end.
```

**Resultado da Compilação em Código Máquina:**
```
1  | PUSHS ""
2  | PUSHI 0
3  | PUSHI 0
4  | PUSHI 0
5  | START
6  | PUSHS "Introduza uma string binária:"
7  | WRITES
8  | WRITELN
9  | READ
10 | STOREG 0
11 | WRITELN
12 | PUSHI 0
13 | STOREG 2
14 | PUSHI 1
15 | STOREG 3
16 | PUSHG 0
17 | STRLEN
18 | STOREG 1
19 | PUSHI 1
20 | PUSHI 1
21 | SUB
22 | FORSTART0:
23 | PUSHL 0
24 | PUSHG 1
25 | EQUAL
26 | NOT
27 | JZ FOREND0
28 | PUSHG 0
29 | PUSHG 1
30 | PUSHI 1
31 | SUB
32 | CHARAT
33 | PUSHS "1"
34 | CHRCODE
35 | EQUAL
36 | JZ ELSE1
37 | PUSHG 2
38 | PUSHG 3
39 | ADD
40 | STOREG 2
41 | JUMP ENDIF1
42 | ELSE1:
43 | ENDIF1:
44 | PUSHG 3
45 | PUSHI 2
46 | MUL
47 | STOREG 3
48 | PUSHG 1
49 | PUSHI 1
50 | SUB
51 | STOREG 1
52 | JUMP FORSTART0
53 | FOREND0:
54 | POP 1
55 | PUSHS "O valor inteiro correspondente é: "
56 | WRITES
57 | PUSHG 2
58 | WRITEI
59 | WRITELN
60 | STOP
```
---

**Exemplo 7:**
```py
1  | program BinarioParaInteiro;
2  |
3  | function BinToInt(bin: string): integer;
4  | var
5  |     i, valor, potencia: integer;
6  | begin
7  |     valor := 0;
8  |     potencia := 1;
9  |     for i := length(bin) downto 1 do
10 |     begin
11 |         if bin[i] = '1' then
12 |             valor := valor + potencia;
13 |         potencia := potencia * 2;
14 |     end;
15 |     BinToInt := valor;
16 | end;
17 |
18 | var
19 |     bin: string;
20 |     valor: integer;
21 |
22 | begin
23 |     writeln('Introduza uma string binária:');
24 |     readln(bin);
25 |     valor := BinToInt(bin);
26 |     writeln('O valor inteiro correspondente é: ', valor);
27 | end.
```

**Resultado da Compilação em Código Máquina:**
```
1  | PUSHS ""
2  | PUSHI 0
3  | START
4  | PUSHS "Introduza uma string binária:"
5  | WRITES
6  | WRITELN
7  | READ
8  | STOREG 3
9  | WRITELN
10 | PUSHG 3
11 | PUSHA BinToInt
12 | CALL
13 | STOREG 4
14 | PUSHS "O valor inteiro correspondente é: "
15 | WRITES
16 | PUSHG 4
17 | WRITEI
18 | WRITELN
19 | STOP
20 | BinToInt:
21 | PUSHI 0
22 | PUSHI 0
23 | PUSHI 0
24 | PUSHI 0
25 | STOREG 1
26 | PUSHI 1
27 | STOREG 2
28 | PUSHFP
29 | LOAD -1
30 | STRLEN
31 | STOREG 0
32 | PUSHI 1
33 | PUSHI 1
34 | SUB
35 | FORSTART0:
36 | PUSHL 0
37 | PUSHG 0
38 | EQUAL
39 | NOT
40 | JZ FOREND0
41 | PUSHL -1
42 | PUSHG 0
43 | PUSHI 1
44 | SUB
45 | CHARAT
46 | PUSHS "1"
47 | CHRCODE
48 | EQUAL
49 | JZ ELSE1
50 | PUSHG 1
51 | PUSHG 2
52 | ADD
53 | STOREG 1
54 | JUMP ENDIF1
55 | ELSE1:
56 | ENDIF1:
57 | PUSHG 2
58 | PUSHI 2
59 | MUL
60 | STOREG 2
61 | PUSHG 0
62 | PUSHI 1
63 | SUB
64 | STOREG 0
65 | JUMP FORSTART0
66 | FOREND0:
67 | POP 1
68 | PUSHG 1
69 | RETURN
```
---


## Melhorias

Reconhecê-mos que existem features que não foram implementadas por opções
tomadas relativas a gestão temporal para o projeto. Com isso, seria uma melhoria
a inclusão de procedures, por ser uma funcionalidade proposta como opção pelo enunciado.

Seria também uma melhoria o foco na otimização de redundância do código gerado. Isto
aplica-se, por exemplo, quando se "declara" uma váriavel através da instrução
**PUSHG 0**, e, em execução, se atribui um valor para essa variável,
levando à execução de mais duas instruções. Seria uma melhoria se a atribuição
do primeiro valor da variável durante o programa fosse feito recorrendo ao PUSHG
inicial, como esse mesmo valor, eliminando 2 instruções posteriores
desnecessárias (push do valor e store do valor).

## Conclusão

Este projeto permitiu-nos aprofundar os conhecimentos adquiridos nas aulas de
Processamento de Linguagens de uma forma prática e interessante. O projeto
transmitiu-nos a ideia do processo efetuado por um compilador como gcc, ao
compilar código para uma representação intermédia em assembly.

Gostaríamos de ter implementado mais funcionalidades, como a possibilidade de definir sub-programas na linguagem de programação, apesar de procedures não terem sido implementadas. Porém, fizemos tudo o que foi pedido no enunciado, por isso estamos bastante satisfeitos com o nosso projeto final.

Temos ainda no Anexo A alguns exemplos de execução do nosso projeto para alguns programas-fonte escritos na nossa linguagem de programação.
