# 🚀 Automação de Regressão Web com Playwright 

Este é o meu primeiro projeto de automação de testes, desenvolvido com muito orgulho com o objetivo principal de ajudar a empresa onde estou estagiando a otimizar o tempo gasto nas validações de rotina pós-deploy e em outras checagens manuais.

Buscando evoluir tecnicamente e dar o próximo passo rumo à Automação, resolvi colocar a mão no código e deixar o robô fazer esse trabalho.

## 🎯 Objetivo e Inspiração

Embora este projeto tenha sido desenhado sob medida para resolver o meu cenário atual (validar a Home, páginas de times, tabelas e artigos do portal Lance!), eu estruturei o código de uma forma bem limpa. 

A ideia é que ele sirva como **template ou inspiração para qualquer Q.A. Web** que queira:
* Automatizar uma regressão simples (como um fluxo de checkout ou login).
* Poupar tempo em checagens visuais cansativas.
* Gerar evidências automáticas (logs e prints) para reportar bugs ou atestar o sucesso de um deploy sem estresse.

## ✨ O que o robô faz?
* **Navegação Inteligente:** Acessa dezenas de URLs mapeadas automaticamente.
* **Validação de UI:** Checa se elementos críticos (Header, Footer, Tabelas) estão visíveis.
* **Scroll Humanizado:** Lida com *Lazy Loading*, rolando a página para garantir que as imagens pesadas carreguem antes do teste.
* **Emulação Mobile:** Simula a tela de um iPhone para testar comportamentos responsivos (como o Menu Hambúrguer).
* **Geração de Evidências:** Cria automaticamente uma pasta com a data/hora do teste, salvando um relatório em `.txt` e os `.png` dos elementos validados ou dos erros encontrados.

## 🛠️ Tecnologias Utilizadas
* **[Python 3]** - Linguagem base do projeto.
* **[Playwright]** - Framework de automação web super rápido e confiável.
* **[Git/GitHub]** - Para versionamento e organização do código.

## 🚀 Como usar este projeto como Template

Se você quiser clonar este projeto para testar na sua máquina ou adaptar para a sua empresa, siga os passos abaixo:

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/kauediaszz/Q.A-Lance.git](https://github.com/kauediaszz/Q.A-Lance.git)
