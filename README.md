# ⚠️ Job Bot Selenium — PROJETO ARQUIVADO

> Este projeto foi cancelado intencionalmente. A documentação abaixo
> explica o que foi construído, o que foi descoberto e por que foi encerrado.

---

## O que era este projeto

Bot de automação de candidaturas a vagas de emprego, desenvolvido em Python.
Buscava vagas em múltiplas plataformas (InfoJobs, Indeed, Vagas.com) usando
Selenium, armazenava em SQLite e apresentava uma interface via Streamlit.

## Stack utilizada

- Python 3.12
- Selenium + ChromeDriver (scraping headless)
- Streamlit (interface web)
- SQLite (persistência local)
- webdriver-manager (gerenciamento automático do ChromeDriver)
- Arquitetura modular (job_bot package com scrapers por plataforma)

## Funcionalidades implementadas

- Scraper funcional para InfoJobs, Indeed e Vagas.com
- Interface Streamlit com sidebar de configuração, abas e métricas
- Banco SQLite com duas tabelas: vagas e candidaturas
- Sistema de deduplicação por link (INSERT OR IGNORE)
- Modo teste para execução sem envio real de candidaturas
- Log em tempo real na interface durante a busca
- Filtro por plataforma e exportação de histórico

## Por que foi cancelado

Durante o desenvolvimento foram identificados três problemas reais:

**1. Falha de roteamento no InfoJobs**
A URL de busca construída dinamicamente retornava páginas incorretas.
Os seletores CSS mapeados não correspondiam ao HTML real retornado.

**2. Detecção de anti-bot no Indeed**
O Indeed identificava o ChromeDriver mesmo em modo headless com
user-agent customizado, bloqueando o acesso aos resultados.

**3. Risco de violação de Termos de Serviço**
A automação de candidaturas (não apenas scraping, mas envio) viola
diretamente os ToS de plataformas como Indeed e InfoJobs.
Continuar o desenvolvimento criaria risco legal real.

## Decisão

Projeto encerrado antes de causar qualquer dano.
O problema original (rastrear candidaturas de forma organizada)
foi resolvido de forma legítima no projeto successor:

👉 [painel-candidaturas](https://github.com/CaiqueGomesn/painel-candidaturas)

## O que aprendi

- Selenium em produção tem limitações sérias com sites modernos com anti-bot
- Antes de automatizar interações com plataformas externas, ler os ToS
- Identificar o momento certo de parar um projeto é uma habilidade técnica
- Código funcional com risco legal não é código pronto

---

## Contexto do autor

Profissional com 10+ anos em operações logísticas (DHL, Amazon, Mercado Livre)
em transição para tecnologia. Este bot foi construído para resolver um problema
real que eu vivia: perder o controle de dezenas de candidaturas espalhadas
em múltiplas plataformas durante minha transição de carreira.

[LinkedIn](https://www.linkedin.com/in/caiquegomes/) |
[Projeto successor →](https://github.com/CaiqueGomesn/painel-candidaturas)