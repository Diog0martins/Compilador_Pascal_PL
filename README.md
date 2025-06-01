# Compilador Pascal - Projeto PL

## Introdução

Para este projeto, foi solicitado o desenvolvimento de um compilador para a
linguagem Pascal standard. O compilador deve traduzir código Pascal para uma
 linguagem semelhante a Assembly, que será executada em uma máquina virtual
 fornecida pelos docentes.

Por decisão imposta, foi utilizada a biblioteca **Python PLY** (Python Lex-Yacc)
para a implementação do analisador léxico e sintático (), aproveitando suas
funcionalidades para a criação de gramáticas e análise de tokens. O módulo
**YACC** foi empregado para a definição das regras da linguagem.

Além da análise sintática e semântica, o compilador implementará a geração de
código intermediário, permitindo a conversão da lógica do programa para a
linguagem de baixo nível da máquina virtual. Durante o desenvolvimento, serão
realizados testes para validar a execução correta das instruções e otimizar
a performance do compilador.

Este documento detalha a arquitetura e funcionamento do compilador, cobrindo os
componentes essenciais como o analisador léxico, sintático, semântico, a AST,
e o processo de geração de código. Por fim, serão discutidas melhorias
potenciais e conclusões extraídas do desenvolvimento do projeto.

## Analisador léxico

O analisador léxico começa por especificar os tokens e símbolos literais que
serão utilizados na gramática. São definidos também que caracteres ignorar.
As especificações são realizadas recorrendo ao módulo para expressões regulares
de Python (**re**).

Com isso, especificamos todas as palavras reservadas para a liguagem em tokens, os símbolos literais utilizados também são definidos aqui, assim como o tratamento de erros léxicos.

### Exemplo

Para o seguinte programa, é feito parse dos tokens da presente em
[parsed tokens](output/tokens.txt).

```Pascal
program Tokenizer;

var
    num: integer;

begin
    num := 5; 
    while num < 5 do 
    begin
        num := num + 1;
        writeln('teste'); 
    end; 
end.
```

Em adição às condições da liguagem Pascal, esta carateriza-se pela não
consideração da capitalidade das letras aquando da definição de ids, denominação
dada a tudo o que não seja string, nem token e seja uma palavra.

## Analisador sintático

A componente sintática define as produções para a gramática, assim como o comportamento que os símbolos traduzem. Neste contexto, traduzem as linhas de código pascal para o código máquina.

É utilizado o parser oferecido pelo módulo, ficando a nosso cargo a criação das produções, através de docstring, e através da construção de funções para tratar as produções.

Sendo este componente caracterizado pela sua complexidade, foi necessário a separação por vários módulos, cada um com produções referentes a um tópico.

### pascal_anasin.py

Este módulo aglomera os módulos com produções, define o tratamento de erros sintáticos, cria o parser e é definido a função de reconhecimento

## Analisador semântico

Em relação a análise semântica, esta é realizada parcialmente através de um

## Geração de código

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
