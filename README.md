# Citizen Assist AI — Módulo de Energia e Sustentabilidade (SERS)

> **"Jovens de 16 a 24 anos que assumem sua primeira conta de luz com renda de primeiro emprego: o assistente ensina a ler a fatura, a pedir a Tarifa Social e a comparar formas de economizar, incluindo uma fonte renovável acessível a quem mora de aluguel."**

---

## 1. Identificação dos Integrantes
* **Curso / Turma:** 1º Ano de Ciência da Computação (1CC) — Global Solution 2026.2 (*CitizenTech*)
* **Disciplina:** Soluções em Energias Renováveis e Sustentáveis (SERS)
* **Integrantes:**
  * `ENZO SEIJI DELGADO TABUCHI` — RM: `573156`
  * `LUCA ALMEIDA LUCARELI` — RM: `569061`
  * `HENRIQUE ALMEIDA LUCARELI` — RM: `569183`

---

## 2. Definição do Contexto: Público-Alvo e Necessidade Energética Real

### Público Escolhido
Jovens de **16 a 24 anos** (recorte alinhado ao projeto principal de PCP e ao site do *Citizen Assist AI*, que atende jovens de 15 a 24 anos em transição para a vida adulta, tirando seus primeiros documentos civis — CPF, Título de Eleitor, Alistamento, conta Gov.br, CTPS Digital e ID Jovem — e ingressando no primeiro emprego ou programa de Jovem Aprendiz).

### Problema e Necessidade Energética Abordada
Quando esse jovem sai da casa dos pais, divide uma república/kitnet estudantil ou passa a assumir contas da família com salário de primeiro emprego ou bolsa de aprendiz, ele enfrenta pela primeira vez a **fatura de energia elétrica**. Na prática:
1. **Desconhecimento técnico sobre a fatura:** Nunca leu uma conta de luz, não compreende o significado de **kWh**, **TE**, **TUSD**, **Bandeiras Tarifárias** ou **CIP/COSIP**, nem sabe quais equipamentos realmente pesam no fim do mês.
2. **Perda de benefícios sociais por falta de orientação:** Muitos jovens já possuem (ou têm direito ao) **Cadastro Único (CadÚnico)** para emitir a **ID Jovem**, mas desconhecem que esse mesmo cadastro garante a **Tarifa Social de Energia Elétrica (TSEE)**, com **100% de isenção na tarifa de consumo até 80 kWh/mês**.
3. **Barreira do aluguel para acesso a fontes renováveis:** Como a maioria mora de aluguel ou em repúblicas, não pode fazer obras nem investir milhares de reais na instalação de painéis solares no telhado, precisando comparar alternativas acessíveis — como medidas práticas de **Eficiência Energética** versus **Energia Solar por Assinatura (Geração Distribuída Compartilhada)**.

---

## 3. Funcionalidades de Energia Incorporadas ao Citizen Assist AI

O módulo integra três frentes práticas ao assistente digital:
1. **Entender e Reduzir a Conta:** Explica em linguagem acessível a leitura da fatura (kWh, TE, TUSD, Bandeiras Tarifárias ANEEL e CIP) e apresenta o peso de cada eletrodoméstico no consumo mensal.
2. **Tarifa Social de Energia Elétrica (TSEE) + Conexão com CadÚnico/ID Jovem:** Verifica elegibilidade conforme as regras vigentes da ANEEL (**Lei nº 12.212/2010**, **MP nº 1.300/2025** e **REN ANEEL nº 1.147/2025**), detalhando a faixa de isenção de 100% até 80 kWh/mês e o Desconto Social até 120 kWh/mês.
3. **Comparador Técnico de Alternativas (Eficiência Energética vs. Energia Solar por Assinatura):** Simula custos mensais/anuais, investimento inicial, *payback* e emissões de $\text{CO}_2$ evitadas para um período de referência comum (30 dias / 12 meses).
4. **Simulador Personalizado Interativo + Proteção LGPD:** Permite ao usuário simular seu próprio consumo em kWh, bloqueia a coleta de dados pessoais (CPF/NIS/e-mail) e registra indicadores de uso em [`dados/indicadores_uso.json`](dados/indicadores_uso.json).

---

## 4. Dados Utilizados, Origem, Unidades e Premissas

Todos os dados e premissas estão documentados em [`dados/consumo_aparelhos_jovem.csv`](dados/consumo_aparelhos_jovem.csv) e [`dados/comparativo_alternativas.json`](dados/comparativo_alternativas.json).

* **Unidades adotadas:** Potência em Watts ($\text{W}$) e quilowatts ($\text{kW}$); tempo em horas por dia ($\text{h/dia}$); período mensal de $\text{30 dias}$ e anual de $\text{12 meses}$; energia ativa em quilowatt-hora ($\text{kWh/mês}$ e $\text{kWh/ano}$); tarifa em $\text{R\$/kWh}$; emissões em $\text{kg CO}_2\text{e/ano}$.
* **Fórmula fundamental de consumo energético:**
  $$E_{\text{mensal}}\,(\text{kWh}) = \frac{P\,(\text{W}) \times t\,(\text{h/dia}) \times d\,(\text{dias/mês}) \times N_{\text{aparelhos}}}{1000}$$
* **Parâmetros tarifários (Verificados em Novembro/2026 — Área de referência Enel Distribuição SP, Subgrupo B1 Residencial Convencional):**
  * **TUSD:** $\text{R\$ } 0,47242/\text{kWh}$ | **TE:** $\text{R\$ } 0,31696/\text{kWh}$
  * **Tarifa Base Homologada ANEEL (sem tributos):** $\text{R\$ } 0,78938/\text{kWh}$
  * **Tarifa Efetiva com Tributos Médios (PIS/COFINS + ICMS ~18%):** $\text{R\$ } 0,96266/\text{kWh}$
  * **Contribuição de Iluminação Pública (CIP/COSIP municipal estimada):** $\text{R\$ } 15,50/\text{mês}$
  * **Bandeiras Tarifárias ANEEL vigentes:** Verde ($\text{R\$ } 0,00$); Amarela ($+\text{R\$ } 1,885/100\text{ kWh}$); Vermelha Patamar 1 ($+\text{R\$ } 4,463/100\text{ kWh}$); Vermelha Patamar 2 ($+\text{R\$ } 7,875/100\text{ kWh}$).
* **Fator de emissão de $\text{CO}_2$ do SIN (MCTI):** $0,0385\text{ kg CO}_2\text{e}/\text{kWh}$.

### Levantamento de Consumo — Moradia Jovem / República (Período: 30 dias)

| Equipamento | Qtd | Potência Base (W) | Uso Base (h/dia) | Consumo Base (kWh/mês) | Consumo Eficiente (kWh/mês) | Tipo de Dado e Origem |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Chuveiro Elétrico** | 1 | 5.500 W | 0,50 h (30 min) | **82,50** | **37,62** *(3.800W / 20 min)* | Estimado sobre tabela pública PROCEL/INMETRO |
| **Geladeira 1 Porta Frost Free** | 1 | 110 W *(efet.)* | 24,0 h *(fator 0,5)* | **39,60** | **34,20** *(ajuste termostato)* | Público / Selo Procel INMETRO |
| **Notebook (Estudo/Trabalho)** | 1 | 65 W | 6,00 h | **11,70** | **9,75** *(5,0 h + suspensão)* | Estimado sobre especificação média PROCEL/EPE |
| **Ventilador de Mesa** | 1 | 65 W | 6,00 h | **11,70** | **8,78** *(4,5 h uso noturno)* | Público / Tabela INMETRO/PROCEL |
| **Lâmpadas Residenciais** | 4 | 15 W *(fluor.)* | 5,00 h | **9,00** | **4,86** *(LED 9W / 4,5 h)* | Público / Guia Eficiência PROCEL/ANEEL |
| **Micro-ondas / Airfryer** | 1 | 1.200 W | 0,20 h (12 min) | **7,20** | **6,12** *(10 min/dia)* | Estimado para preparo de marmita do trabalho |
| **Stand-by e Carregadores** | 1 | 11 W *(agreg.)* | 10,00 h | **3,30** | **0,99** *(filtro de linha)* | Estimado sobre medição média PROCEL/INMETRO |
| **TOTAL MENSAL (30 DIAS)** | — | — | — | **165,00 kWh** | **102,32 kWh** | **Redução de 62,68 kWh/mês (-37,99%)** |

---

## 5. Cálculos, Comparação de Alternativas e Justificativas Técnicas

A comparação considera a mesma necessidade energética inicial (**165,00 kWh/mês** ou **1.980,00 kWh/ano** em Bandeira Verde, com fatura base de **R$ 174,34/mês** incluindo tributos e CIP de R$ 15,50):

| Indicador (Referência: 30 dias / 12 meses) | Cenário Base (Sem ação) | Alternativa 1: Eficiência Energética (LED + Chuveiro Verão + Stand-by) | Alternativa 2 (Renovável): Energia Solar por Assinatura (GD Compartilhada - 12% desc.) | Estratégia Combinada (Alt. 1 + Alt. 2) |
| :--- | :---: | :---: | :---: | :---: |
| **Consumo da Rede (kWh/mês)** | 165,00 kWh | **102,32 kWh** (-37,99%) | 165,00 kWh *(135 kWh compensados por solar)* | **102,32 kWh** *(72,32 kWh compensados)* |
| **Investimento Inicial (R$)** | R$ 0,00 | **R$ 48,00** *(4 LEDs 9W + 1 filtro de linha)* | **R$ 0,00** *(adesão digital sem obras)* | **R$ 48,00** |
| **Custo Mensal Total (R$/mês)** | R$ 174,34 | **R$ 114,00** | **R$ 158,74** | **R$ 105,65** |
| **Economia Mensal Estimada (R$/mês)** | R$ 0,00 | **R$ 60,34 / mês** | **R$ 15,60 / mês** | **R$ 68,69 / mês** |
| **Economia Anual Estimada (R$/ano)** | R$ 0,00 | **R$ 724,08 / ano** | **R$ 187,20 / ano** | **R$ 824,28 / ano** |
| **Retorno do Investimento (Payback)** | — | **0,80 mês (~24 dias)** | **Imediato (0 meses)** | **0,70 mês (~21 dias)** |
| **Emissões Evitadas / Compensadas** | 0,00 kg $\text{CO}_2\text{e}$ | **28,96 kg $\text{CO}_2\text{e}$/ano** | **62,37 kg $\text{CO}_2\text{e}$/ano** *(1.620 kWh solares)* | **62,37 kg $\text{CO}_2\text{e}$/ano** |

### Justificativa das Recomendações (Custos, Viabilidade e Impactos Ambientais)
1. **Alternativa 1 (Eficiência Energética e Mudança de Hábitos):** Apresenta o **maior impacto financeiro direto** ($\text{R\$ } 60,34/\text{mês}$ de economia), essencial para a renda restrita de primeiro emprego. O investimento de $\text{R\$ } 48,00$ (4 lâmpadas LED 9W Selo Procel A + filtro de linha com interruptor) paga-se em apenas **24 dias** e reduz fisicamente o desperdício de energia. Se o jovem tiver direito à **Tarifa Social (TSEE)** via CadÚnico, a redução de consumo aproxima a fatura do limite de **80 kWh/mês**, faixa em que a tarifa de consumo tem **100% de isenção**.
2. **Alternativa 2 — Fonte Renovável (Energia Solar por Assinatura / Geração Compartilhada — Lei nº 14.300/2022):** Resolve a principal barreira de quem mora de aluguel ou divide república: **não exige telhado próprio, obras nem investimento inicial ($\text{R\$ } 0,00$)**. Por meio de consórcio ou cooperativa de geração distribuída remota, $135\text{ kWh/mês}$ ($165\text{ kWh}$ menos $30\text{ kWh}$ de custo de disponibilidade monofásico) são compensados com créditos solares e desconto de $12\%$, gerando economia de $\text{R\$ } 15,60/\text{mês}$ ($\text{R\$ } 187,20/\text{ano}$) e contratando $1.620\text{ kWh/ano}$ de fonte 100% renovável.
3. **Limitações explicitadas ao usuário:**
   * A Energia Solar por Assinatura exige consumo mínimo na maioria das cooperativas (geralmente $> 120\text{ a } 150\text{ kWh/mês}$), titularidade do CPF sem inadimplência e atenção a cláusulas de fidelidade/aviso prévio.
   * Quem já é beneficiário da **Tarifa Social (TSEE)** com consumo até $80\text{ kWh/mês}$ **não deve contratar** assinatura solar, pois já possui 100% de isenção na tarifa de energia.
   * Na TSEE, mesmo consumindo até $80\text{ kWh/mês}$, a fatura não zera integralmente devido à cobrança da **CIP/COSIP** municipal.

---

## 6. Instruções para Executar e Testar a Solução

### Pré-requisitos
* Python 3.10 ou superior (utiliza apenas bibliotecas padrão do Python — não requer instalação de pacotes externos).

### Comandos de Execução
```bash
# 1. Executar o Assistente Digital Interativo (Menu + Simulador + Busca Inteligente)
python3 citizen_assist_energia.py

# 2. Exibir o Relatório Analítico Completo no Terminal (Tabelas e Cálculos)
python3 analise_consumo_alternativas.py

# 3. Executar a Suíte de Testes Automatizados
python3 test_citizen_assist_energia.py -v
```

---

## 7. Registros dos Testes com Usuários e Ajustes Realizados

Os testes foram conduzidos com jovens do público-alvo (16 a 24 anos) sem coleta de dados pessoais sensíveis. O detalhamento completo encontra-se em [`docs/TESTES_COM_USUARIOS.md`](docs/TESTES_COM_USUARIOS.md):

| Caso de Teste | Perfil do Usuário (Anônimo) | Situação Testada | Comentário Recebido | Ajuste Realizado no Sistema |
| :---: | :--- | :--- | :--- | :--- |
| **Teste 1** | Jovem de 18 anos (Jovem Aprendiz, divide kitnet) | Dúvida sobre por que a primeira conta veio R$ 175 e o que significa "TUSD" e "TE". | *"Não sabia que o chuveiro no modo inverno gastava metade da conta nem o que era TUSD."* | Adicionado destaque visual em percentual (`50% do consumo no chuveiro`) e tradução direta das siglas TUSD e TE no Tópico 1. |
| **Teste 2** | Jovem de 20 anos (possui ID Jovem / CadÚnico) | Simulação de Tarifa Social para consumo de 75 kWh/mês e dúvida se a conta viria R$ 0,00. | *"Achei que abaixo de 80 kWh a conta zerava totalmente, bom avisar da taxa de iluminação da prefeitura."* | Incluído alerta explícito na simulação da TSEE explicando que a CIP/COSIP municipal (~R$ 15,50) continua sendo cobrada mesmo com 100% de desconto no consumo. |
| **Teste 3** | Jovem de 22 anos (primeiro emprego CLT, mora de aluguel) | Comparação entre troca de lâmpadas/hábitos e Energia Solar por Assinatura para 165 kWh/mês. | *"Não sabia que existia assinatura solar sem instalar placa no telhado, mas queria saber se vale a pena junto com a Tarifa Social."* | Criada regra automática no simulador que desaconselha a assinatura solar quando o usuário já tem isenção pela TSEE abaixo de 80 kWh/mês. |

---

## 8. Referências Verificáveis Utilizadas

1. **ANEEL (Agência Nacional de Energia Elétrica):** *Tarifa Social de Energia Elétrica (TSEE) — Lei nº 12.212/2010, MP nº 1.300/2025 e Resolução Normativa ANEEL nº 1.000/2021 / nº 1.147/2025*. Disponível em: `https://www.gov.br/aneel`. Consultado em: nov/2026.
2. **ANEEL / Enel Distribuição São Paulo:** *Resolução Homologatória de Tarifas Residenciais Subgrupo B1 (TUSD R$ 0,47242/kWh + TE R$ 0,31696/kWh = R$ 0,78938/kWh) e Valores das Bandeiras Tarifárias 2026*. Disponível em: `https://www.enel.com.br` e `https://www.gov.br/aneel`. Consultado em: nov/2026.
3. **Brasil — Marco Legal da Geração Distribuída:** *Lei Federal nº 14.300, de 6 de janeiro de 2022, e Resolução Normativa ANEEL nº 1.059/2023 (Geração Compartilhada por Consórcio ou Cooperativa)*. Disponível em: `https://www.planalto.gov.br`. Consultado em: nov/2026.
4. **PROCEL / INMETRO:** *Tabelas de Consumo e Eficiência Energética de Eletrodomésticos Residenciais (Chuveiros, Refrigeradores, Lâmpadas LED e Ventiladores)*. Disponível em: `https://www.gov.br/inmetro` e Portal Procel Info. Consultado em: nov/2026.
5. **MCTI (Ministério da Ciência, Tecnologia e Inovação) / SIRENE:** *Fatores Médios Anuais de Emissão de $\text{CO}_2$ pela Geração de Energia Elétrica no Sistema Interligado Nacional (SIN)*. Disponível em: `https://www.gov.br/mcti`. Consultado em: nov/2026.
6. **MDS (Ministério do Desenvolvimento e Assistência Social):** *Cadastro Único (CadÚnico) e Programa ID Jovem*. Disponível em: `https://www.gov.br/mds`. Consultado em: nov/2026.
