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

Com isso, especificamos todas as palavras reservadas para a 

## Analisador sintático

## Analisador semântico

## Geração de código

## Teste

## Melhorias

## Conclusão
