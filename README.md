    1| # Sistema de Gestão de Leads e Agendamento Médico
    2| 
    3| > Sistema desenvolvido para modelar o problema de duplicidade de leads e otimizar a busca de combinações e verificações repetidas.
    4| 
    5| [![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
    6| [![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
    7| 
    8| ---
    9| 
    10| ## Sumário
    11| 
    12| - [Sobre o Projeto](#sobre-o-projeto)
    13| - [Arquitetura](#arquitetura)
    14| - [Tarefas Implementadas](#tarefas-implementadas)
    15|   - [Tarefa 1: Verificação Recursiva de Duplicidade](#tarefa-1-verificação-recursiva-de-duplicidade)
    16|   - [Tarefa 2: Uso de Memoização](#tarefa-2-uso-de-memoização)
    17|   - [Tarefa 3: Otimização de Agenda](#tarefa-3-otimização-de-agenda)
    18| - [Instalação](#instalação)
    19| - [Uso](#uso)
    20| - [Exemplos](#exemplos)
    21| - [Complexidade](#complexidade)
    22| - [Contribuição](#contribuição)
    23| 
    24| ---
    25| 
    26| ## Sobre o Projeto
    27| 
    28| Este projeto implementa um sistema completo para:
    29| 
    30| - **Verificação de duplicidade** de leads em base de dados
    31| - **Otimização de comparações** usando memoização
    32| - **Agendamento inteligente** de consultas médicas
    33| 
    34| O sistema utiliza conceitos avançados de algoritmos, incluindo:
    35| - Recursão
    36| - Memoização (caching de resultados)
    37| - Programação Dinâmica
    38| - Divisão em subproblemas
    39| 
    40| ---
    41| 
    42| ## Arquitetura
    43| 
    44| ```
    45| ┌─────────────────────────────────────────────────────────────┐
    46| │                    SISTEMA PRINCIPAL                        │
    47| ├─────────────────────────────────────────────────────────────┤
    48| │  ┌─────────────────┐  ┌─────────────────┐  ┌────────────┐ │
    49| │  │   Verificador   │  │   Verificador   │  │ Otimizador │ │
    50| │  │   Duplicidade   │  │  Memoização     │  │   Agenda   │ │
