<div align="center">

# Citizen Assist AI
### Módulo de Energia e Sustentabilidade — SERS

**Uma experiência educativa para ajudar jovens a entender a conta de luz, acessar benefícios sociais e tomar decisões mais sustentáveis.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-Global%20Solution%202026.2-0A7EA4)](https://github.com/enzotabuchii/FIAP-GS-CitizenCity-SERS)
[![LGPD](https://img.shields.io/badge/dados-LGPD%20friendly-2E8B57)](https://www.gov.br/esocial/pt-br/assuntos/lei-geral-de-protecao-de-dados-pessoais-lgpd)

</div>

---

## Sobre o projeto

O **Citizen Assist AI — SERS** é um módulo do projeto **Citizen Assist AI**, criado para orientar jovens que estão assumindo sua primeira conta de energia elétrica durante a transição para a vida adulta.

A solução transforma conceitos técnicos em explicações simples e simulações práticas, ajudando o usuário a:

- entender os principais itens da fatura;
- identificar oportunidades de economia;
- verificar informações sobre a Tarifa Social de Energia Elétrica;
- comparar eficiência energética com energia solar por assinatura;
- estimar custos, economia e emissões evitadas;
- simular cenários sem informar CPF, NIS, e-mail ou outros dados pessoais.

> **Público-alvo:** jovens de 16 a 24 anos, especialmente aqueles que moram de aluguel, dividem uma república ou assumiram sua primeira conta com renda de primeiro emprego ou bolsa de aprendiz.

## 🧭 Navegação

- [Contexto e problema](#-contexto-e-problema)
- [Funcionalidades](#-funcionalidades)
- [Dados e premissas](#-dados-e-premissas)
- [Resultados principais](#-resultados-principais)
- [Como executar](#-como-executar)
- [Testes com usuários](#-testes-com-usuários)
- [Integrantes](#-integrantes)
- [Referências](#-referências)

---

## 🎯 Contexto e problema

Ao sair da casa dos pais, morar em uma kitnet ou dividir uma república, o jovem geralmente entra em contato pela primeira vez com conceitos como **kWh**, **TE**, **TUSD**, **bandeiras tarifárias** e **CIP/COSIP**.

Além da dificuldade para interpretar a fatura, também existem dois desafios importantes:

1. **Benefícios pouco conhecidos:** pessoas que possuem ou têm direito ao CadÚnico podem não saber que ele também se relaciona à Tarifa Social de Energia Elétrica (TSEE).
2. **Barreira do aluguel:** quem não possui imóvel próprio normalmente não pode instalar painéis solares no telhado e precisa conhecer alternativas sem obras ou alto investimento inicial.

O projeto responde a esses desafios com linguagem acessível, comparação de cenários e transparência sobre limitações e custos.

---

## Funcionalidades

### Entender e reduzir a conta

Explicações diretas sobre leitura da fatura, consumo em kWh, TE, TUSD, bandeiras tarifárias, CIP/COSIP e impacto dos principais eletrodomésticos.

### Tarifa Social de Energia Elétrica

Orientações sobre elegibilidade e regras relacionadas ao CadÚnico e à ID Jovem, incluindo:

- isenção de 100% na tarifa de consumo até 80 kWh/mês, conforme as premissas adotadas no projeto;
- desconto social para faixas de consumo superiores;
- alerta de que a CIP/COSIP municipal pode continuar sendo cobrada.

### Comparador de alternativas

Compara três estratégias para o mesmo perfil de consumo:

- eficiência energética e mudança de hábitos;
- energia solar por assinatura, em geração distribuída compartilhada;
- estratégia combinada.

O comparador apresenta custo mensal, economia anual, investimento inicial, *payback* e emissões evitadas ou compensadas.

### Simulador personalizado

Permite informar o consumo estimado em kWh e testar cenários de forma interativa, sem coletar dados pessoais. Indicadores de uso são registrados em [`dados/indicadores_uso.json`](dados/indicadores_uso.json).

---

## Dados e premissas

As premissas são detalhadas em:

- [`dados/consumo_aparelhos_jovem.csv`](dados/consumo_aparelhos_jovem.csv)
- [`dados/comparativo_alternativas.json`](dados/comparativo_alternativas.json)

### Fórmula de consumo mensal

```text
E mensal (kWh) = [P (W) × t (h/dia) × d (dias/mês) × quantidade] / 1000
```

### Perfil de consumo analisado

| Cenário | Consumo mensal | Redução |
| --- | ---: | ---: |
| Moradia jovem / república — uso base | **165,00 kWh** | — |
| Moradia jovem / república — uso eficiente | **102,32 kWh** | **62,68 kWh (-37,99%)** |

### Equipamentos com maior impacto

| Equipamento | Consumo base | Consumo eficiente |
| --- | ---: | ---: |
| Chuveiro elétrico | 82,50 kWh/mês | 37,62 kWh/mês |
| Geladeira | 39,60 kWh/mês | 34,20 kWh/mês |
| Notebook | 11,70 kWh/mês | 9,75 kWh/mês |
| Ventilador | 11,70 kWh/mês | 8,78 kWh/mês |
| Lâmpadas | 9,00 kWh/mês | 4,86 kWh/mês |

> Os valores completos, as fontes dos dados e as premissas tarifárias estão disponíveis nos arquivos da pasta [`dados`](dados/).

---

## Resultados principais

Referência: 30 dias, 12 meses e consumo inicial de 165,00 kWh/mês.

| Indicador | Cenário base | Eficiência energética | Solar por assinatura | Estratégia combinada |
| --- | ---: | ---: | ---: | ---: |
| Consumo da rede | 165,00 kWh | **102,32 kWh** | **165,00 kWh*** | **102,32 kWh*** |
| Investimento inicial | R$ 0,00 | **R$ 48,00** | **R$ 0,00** | **R$ 48,00** |
| Custo mensal total | R$ 174,34 | **R$ 114,00** | **R$ 158,74** | **R$ 105,65** |
| Economia mensal | — | **R$ 60,34** | **R$ 15,60** | **R$ 68,69** |
| Economia anual | — | **R$ 724,08** | **R$ 187,20** | **R$ 824,28** |
| *Payback* estimado | — | **24 dias** | **imediato** | **21 dias** |
| Emissões evitadas/compensadas | — | **28,96 kg CO₂e/ano** | **62,37 kg CO₂e/ano** | **62,37 kg CO₂e/ano** |

\* Parte do consumo é compensada por créditos solares, conforme as premissas do projeto.

### Recomendação resumida

- **Eficiência energética:** apresenta o maior impacto financeiro direto e exige baixo investimento.
- **Energia solar por assinatura:** pode ser adequada para quem mora de aluguel, pois não exige instalação no telhado.
- **Estratégia combinada:** oferece o melhor resultado estimado no cenário analisado.
- **Tarifa Social:** deve ser considerada antes da contratação de uma assinatura solar; para quem já possui isenção pela TSEE, a assinatura pode não ser vantajosa.

### Limitações importantes

- Cooperativas e consórcios de energia solar podem exigir consumo mínimo, titularidade regular e atenção a cláusulas de fidelidade.
- A Tarifa Social não elimina necessariamente a CIP/COSIP municipal.
- Valores tarifários, descontos e regras podem mudar; as simulações são educativas e não substituem a consulta à distribuidora ou aos órgãos oficiais.

---

## Como executar

### Pré-requisitos

- Python **3.10 ou superior**
- Nenhuma biblioteca externa: o projeto utiliza apenas a biblioteca padrão do Python.

### Comandos

```bash
# Assistente interativo com menu, simulador e busca inteligente
python3 citizen_assist_energia.py

# Relatório analítico com tabelas e cálculos
python3 analise_consumo_alternativas.py

# Suíte de testes automatizados
python3 test_citizen_assist_energia.py -v
```

---

## Testes com usuários

Os testes foram realizados com jovens do público-alvo, sem coleta de dados pessoais sensíveis. O relatório completo está em [`docs/TESTES_COM_USUARIOS.md`](docs/TESTES_COM_USUARIOS.md).

| Caso | Situação observada | Ajuste realizado |
| :---: | --- | --- |
| **1** | Dúvidas sobre TUSD, TE e o impacto do chuveiro na primeira conta. | Destaque visual para as siglas e para o percentual de consumo do chuveiro. |
| **2** | Expectativa de que uma conta abaixo de 80 kWh ficaria totalmente zerada. | Alerta sobre a cobrança da CIP/COSIP municipal. |
| **3** | Comparação entre economia doméstica, assinatura solar e Tarifa Social. | Regra que desaconselha a assinatura solar quando já existe isenção pela TSEE. |

---

## ntegrantes

**FIAP — 1º Ano de Ciência da Computação (1CCPQ)**  
Global Solution 2026.2 · CitizenTech  
Disciplina: **Soluções em Energias Renováveis e Sustentáveis (SERS)**

| Integrante | RM |
| --- | ---: |
| **Enzo Seiji Delgado Tabuchi** | `573156` |
| **Luca Almeida Lucareli** | `569061` |
| **Henrique Almeida Lucareli** | `569183` |

---

## Referências

1. [ANEEL — Tarifa Social de Energia Elétrica](https://www.gov.br/aneel)
2. [Enel Distribuição São Paulo](https://www.enel.com.br)
3. [Lei nº 14.300/2022 — Marco Legal da Geração Distribuída](https://www.planalto.gov.br)
4. [INMETRO — Eficiência energética](https://www.gov.br/inmetro)
5. [MCTI — Fatores de emissão](https://www.gov.br/mcti)
6. [MDS — Cadastro Único e ID Jovem](https://www.gov.br/mds)

> Consultas e parâmetros utilizados no trabalho: **novembro de 2026**. Consulte sempre as fontes oficiais para obter regras e tarifas atualizadas.

---

<div align="center">

**Citizen Assist AI · Energia acessível, informação clara e escolhas sustentáveis.**

</div>
