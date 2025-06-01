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

A componente de geração de código tem por base a utilização das produções, e
recorre à linguagem utilizada na [VM](https://ewvm.epl.di.uminho.pt/).

Seguindo uma filosofia de programação em stack e, utilizando pointers para posições das stacks, foi nos permitido os seguintes tipos de geração de código.

### Atribuições

A geração de código para atribuições envolve colocar um valor na stack, para que ele possa ser posteriormente armazenado ou utilizado conforme necessário.

```code
PUSHS "Ola, Mundo!"
WRITES
PUSHI 3
STOREG 0
```

No exemplo, é feito um PUSH de uma string para a stack, para posteriormente ser
escrita no output da máquina, escrita essa cuja instrução varia de acordo com o
tipo do elemento que pretendemos utilizar.

Retirando as partes das nossas produções, o código é gerado com base na estrutura
definida em generalSTable, que em conformidade com os tipos de variáveis guardadas.

### Condicionais

As instruções que traduzem código referente à execução de código segundo uma
condição necessitam de usufruir de labels para a execução de saltos do PC para
a execução dessas mesmas instruções

```code
PUSHG 0
START
PUSHI 15
STOREG 0

PUSHI 10
PUSHG 0
SUP
JZ ENDIF1

PUSHI 99
STOREG 0

ENDIF1:
STOP

```

Neste exemplo, é criada uma variável global, que designamos x.

É colocado o valor 15 na posição referente a x, ou seja, x = 15.
De seguida, é comparado x com 10, sendo que caso seja superior, x passa a ter o
valor 99.

As partes do código utilizadas são geradas por produções mais atómicas, o que
leva a que a construção desta estrutura condicional seja construída quase de imediato.

### Variáveis globais

As instruções para declarar as variáveis assentam na prática de introduzir valores
para a stack, andes do programa começar.

Isto permite que o global pointer tenha acesso direto às variáveis de forma
direta.

```code
PUSHG 0
START
```

---

### While

As estruturas de repetição **while** baseiam-se na verificação de uma condição antes da execução de um bloco de código. São utilizadas instruções de salto (labels) para criar o loop e garantir que a verificação da condição ocorre a cada iteração.

```code
START
PUSHI 0
STOREG 0        ; i = 0

WHILE_START:
PUSHI 5
PUSHG 0
INF             ; i < 5
JZ WHILE_END

PUSHG 0
WRITEI
WRITELN

PUSHG 0
PUSHI 1
ADD
STOREG 0

JUMP WHILE_START
WHILE_END:
STOP
```

Neste exemplo, enquanto `i < 5`, imprime-se o valor de `i`, seguido de uma nova linha. A cada iteração, `i` é incrementado.

---

### For

Estruturas `for` podem ser vistas como uma construção compacta de um `while`, envolvendo inicialização, condição e incremento num único bloco.

```code
START
PUSHI 0
STOREG 0        ; i = 0

FOR_START:
PUSHI 5
PUSHG 0
INF             ; i < 5
JZ FOR_END

PUSHG 0
WRITEI
WRITELN

PUSHG 0
PUSHI 1
ADD
STOREG 0

JUMP FOR_START
FOR_END:
STOP
```

Apesar de ser semanticamente um `for`, a estrutura de código gerado é idêntica ao `while`, mudando apenas a forma de organização.

---

### Funções

A definição e chamada de funções envolvem operações com `CALL` e `RETURN`. A função pode ser invocada a partir de qualquer ponto do código, e o controlo é devolvido após o `RETURN`.

```code
START
PUSHA func
CALL
STOP

func:
PUSHI 42
WRITEI
WRITELN
RETURN
```

Neste exemplo, a função `func` imprime o número `42`. O endereço da função é empilhado com `PUSHA`, seguido de um `CALL`. A função é concluída com `RETURN`.

---

### Arrays

Arrays são alocados dinamicamente com a instrução `ALLOC` ou `ALLOCN`, sendo o seu acesso feito através de índices, com as instruções `LOAD` e `STORE`.

```code
START
PUSHI 5
ALLOC          ; aloca um array com 5 inteiros
STOREG 0       ; guarda o endereço do array em gp[0]

PUSHI 10
PUSHI 2
PUSHG 0
STORE          ; armazena o valor 10 na posição 2 do array

PUSHI 2
PUSHG 0
LOAD
STOREG 1       ; armazena o valor lido em gp[1]

STOP
```

Neste exemplo, um array de 5 posições é criado e armazenado na variável global `gp[0]`. A posição 2 do array é modificada e posteriormente lida.

---

## Teste

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

Com a  possibilidade de utilização de funcionalidades básicas, ficamos
satisfeitos com a aprendizagem.
