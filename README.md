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
| `program Tokenizer;` | LexToken(**PROGRAM**,'program',1,5)<br>LexToken(**ID**,'Tokenizer',1,13)                                                                            |
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

Com uma gramática concreta e bem definida, o **Analisador sintático**, através do **ply.yacc**, efetua comportamentos que tenham sido definidos para cada produção criada. Estas funcionam com auxílio dos tokens devolvidos pelo **Analisador léxico**.

Antes de efetuar alguma tradução (de código Pascal para o código da linguagem de baixo nível), com apoio da **Tabela de símbolos**, será feita uma **análise semântica** do input processado pelo **Analisador sintático**. Caso esta tabela verifique que não existe qualquer erro ou conflito **semântico**, o programa irá acumular o código resultante pelas produções e este será "levado" até que todas as produções sejam interpretadas.

Utilizando o parser presente na **API** do **ply.yacc**, criámos uma gramática que deverá ser lida segundo a metodologia **LALR(1)**. Tendo isto em conta, apesar de existirem alguns conflitos *shift/reduce*, estes acabam por ser insignificantes, pelo **lookahead de 1**. Isto não tira a importância de conflitos *reduce/reduce*, sendo que estes podem levar a maiores problemas no futuro.

Como apoio visual, temos aqui a representação gráfica do autónomo criado pela nossa [gramática](Anexos/automaton.png).

![gramática](Anexos/automaton.png)

Iremos muito sucintamente explicar o processo de tradução de **Expressões** e de **Instruções Globais**

#### Expressão

Neste projeto, criamos as produções de **Expressões** com base no que foi sugerido durante o periodo letivo. 
Todas as **Expressões**, retornam um triplo. Caso seja uma constante, retornará:
 - O seu **valor**
 - O seu **tipo**
 - Uma **string vazia**

Caso se trate de uma **variável** ou uma **expressão composta** (<u>3 * 3</u>, <u>(3 - 4) * (3 / 2)</u>)
 - O seu **nome da variável** (ou vazio caso se trate de uma expressão composta)
 - O seu **tipo** da variável (ou do resultado da expressão)
 - O **código** que irá colocar na **stack** os valores a ter em causa (fará *PUSH* do valor da varíavel ou irá gerar código da linguagem resultante, de maneira a devolver o valor do resultado da **expressão composta** no topo da stack) 

#### Instruções Globais
Na construção da gramática, tornou-se clara a necessidade de separar os diferentes tipos de **Instruções** que poderiam ser feitos em cada programa, dependendo do **scope** atual de cada **Instrução**.

Isto é, apesar de se poderem declarar (for-/while-)**Loops**, **Instruções Condicionais**, **Atribuições** e **Expressões** (e até combinações de **Begin** <u>Instrução</u> **End**) dentro de funções e dentro do "Begin" e "End" relativos ao "pseudo-Main" de Pascal, isto não é possível fora destes **scopes**.
Declarando estas de "**Instruções Locais**":

```py
    Instrucao : While
              | CicloFor
              | InstrucaoCondicional
              | Atribuicao 
              | Expressao
```

(É importante salientar também que decidimos que combinações **Begin** <u>Instrução</u> **End** podiam fazer parte destas dentro de certas condições, visto que é possível encapsular um bloco de **x** **Instruções** sem qualquer problema, sintáticamente, em Pascal).

No que vem a declaração de **Funções**, **Procedures** e **Variáveis**, estas só podiam ser feitas num **scope** global. No caso da declaração de **Variáveis**, dentro de outras **Instruções** deste tipo, mas fora de combinações **Begin** <u>Instrução</u> **End**.

Sendo assim, chegou a criação de "**Instruções Globais**":

```py
    GlobalInst : Dfuncao
               | Dprocedimento
               | Dvariaveis 
```

Aqui há um pequeno problema. 
Em Pascal, as **Funções** têm de ser definidas antes do bloco "**Begin** <u>Instrução</u> **End**" final, mas, no código final esperado, as **Funções** são esperadas no <u>FIM</u> do código. Para isto, as produções de **Funções** devolvem uma lista de tuplos, em que cada tuplo tem o seguinte formato:
- Uma string com o valor `"Func"`
- O código final esperado da **função**

E as produções de **Declaração de Variáveis** adicionam a esta mesma lista, tuplos com o seguinte formato:
- Uma string com o valor `"Var"`
- O código final esperado de **declaração de variáveis**

No fim da **analisade sintática** e **semântica**, o compilador irá organizar o código de maneira a priviligiar a **declaração de variáveis globais**, seguido do código dentro do último bloco **Begin** <u>Instrução</u> **End**, e finalmente, após estes, serão escritas todas as definições de funções lidas.

## Analisador semântico
De maneira a prevenir que houvesse um acesso a alguma variável local a uma função, dentro do bloco **Begin** <u>Instrução</u> **End** relativo à "main" do programa, ou de maneira a que uma variável global, possa ter o mesmo "nome" que uma variável local a uma função anteriormente definida, criámos uma "**Tabela de símbolos**"[¹](./Anexos/STable.png)

![Tabela de símbolos](./Anexos/STable.png)

Esta serve como um "ficheiro de logs" para o programa, capaz de reter informação específica sobre os **tipos** de uma variável (para caso seja tentada uma **Atribuição** cuja **Expressão** tenha um resultado que difira do **tipo** da variável a que o valor à de ser atribuído).

Esta é também caraterizada pelo facto de poder apresentar resultados diferentes, dependendo do estado em que se encontra.
Verificar se uma variável de "nome" "x" já foi declarada ou não, pode ser feita de 2 maneiras:

- Pode ser verificada num **scope** global, ignorando qualquer **variável** local declarada dentro de qualquer **função**;
- Pode ser verificada num **scope** local, ignorando qualquer **variável** local declarada dentro de outras funções **função**, mas tendo em conta **variáveis** globais já declaradas.

Para além disto, esta tabela também verifica o tipo dos argumentos que uma dada **função** recebe e devolve, se já foi declarada alguma função com esse mesmo nome e se o valor a ser retornado por uma função é consistente com o valor passado.

Muitas features não foram mencionadas, mas através desta ferramenta, foi-nos possível garantir uma **análise semântica** robusta e consistente. 

## Geração de código

## Teste

## Melhorias

Apesar de não termos implementado a tradução de **Procedures**, estes acabam por se basear muito na definição de **Funções**, onde a única diferença aparente é que um **Procedure** pode alterar o valor original do argumento que lhe foi passado (tal como em C, quando passamos um pointer como argumento a uma função).
Podia ter havido alguma otimização na tradução de código, no que vem a alguma redundância gerada. 
(e.g.  Ao declarar uma variável, em vez de passar logo a instrução "**PUSHG 0**", podiamos esperar a que lhe fosse atribuído um valor e <u>SÓ AÍ</u> seria realmente passada para a stack).


## Conclusão

Este projeto permitiu-nos aprofundar os conhecimentos adquiridos nas aulas de
Processamento de Linguagens de uma forma prática e interessante. Fez-nos perceber como é efetuado o trabalho de um compilador e deu um novo significado a "memory management". 

Gostaríamos de ter implementado mais funcionalidades, porém, fizemos tudo o que nos foi possível com o tempo e recursos dados.

Temos ainda no Anexo A alguns exemplos de execução do nosso projeto para alguns programas-fonte escritos na nossa linguagem de programação.
