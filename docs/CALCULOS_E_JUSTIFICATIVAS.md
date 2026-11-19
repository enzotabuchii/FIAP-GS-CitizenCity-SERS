# Memorial de Cálculos e Justificativas Técnicas — SERS

Este documento detalha passo a passo os cálculos físicos, financeiros e ambientais implementados em [`analise_consumo_alternativas.py`](../analise_consumo_alternativas.py) e integrados ao assistente [`citizen_assist_energia.py`](../citizen_assist_energia.py).

---

## 1. Fórmulas Físicas de Energia e Potência Elétrica

O consumo mensal de energia elétrica ativa ($E$, em $\text{kWh/mês}$) de cada equipamento é obtido a partir de sua potência elétrica nominal ($P$, em $\text{W}$) e do tempo médio diário de operação ($t$, em $\text{h/dia}$) ao longo de $d = 30\text{ dias}$:

$$E\,(\text{kWh/mês}) = \frac{P\,(\text{W}) \times t\,(\text{h/dia}) \times d\,(\text{dias}) \times N}{1000}$$

### Cálculo Detalhado por Equipamento (Cenário Base vs. Cenário Eficiente)

1. **Chuveiro Elétrico:**
   * **Cenário Base (Posição Inverno, $5.500\text{ W}$, 2 banhos de 15 min $= 30\text{ min/dia} = 0,50\text{ h/dia}$):**
     $$E_{\text{base}} = \frac{5500 \times 0,50 \times 30}{1000} = 82,50\text{ kWh/mês}$$
   * **Cenário Eficiente (Posição Verão/Eco, $3.800\text{ W}$, 2 banhos de 10 min $= 20\text{ min/dia} \approx 0,33\text{ h/dia}$):**
     $$E_{\text{efic}} = \frac{3800 \times 0,33 \times 30}{1000} = 37,62\text{ kWh/mês}$$
   * **Economia isolada:** $82,50 - 37,62 = 44,88\text{ kWh/mês}$ ($-54,4\%$).

2. **Geladeira 1 Porta Frost Free:**
   * Potência efetiva média considerando o ciclo térmico do compressor: $110\text{ W}$ com fator de operação de $0,5$ em $24\text{ h/dia}$ ($55\text{ W}$ médios contínuos). Na tabela de dados isso aparece como $12\text{ h/dia}$ equivalentes ($24\text{ h} \times 0,5$):
     $$E_{\text{base}} = \frac{110 \times 12 \times 30}{1000} = 39,60\text{ kWh/mês}$$
   * Com ajuste de termostato, verificação de borracha de vedação e afastamento da parede/fogão ($95\text{ W}$ equivalentes no ciclo):
     $$E_{\text{efic}} = \frac{95 \times 12 \times 30}{1000} = 34,20\text{ kWh/mês}$$

3. **Iluminação Residencial (4 pontos de luz):**
   * **Cenário Base (4 lâmpadas fluorescentes compactas de $15\text{ W}$, $5,0\text{ h/dia}$):**
     $$E_{\text{base}} = \frac{4 \times 15 \times 5,0 \times 30}{1000} = 9,00\text{ kWh/mês}$$
   * **Cenário Eficiente (Substituição por 4 lâmpadas LED Selo Procel A de $9\text{ W}$, $4,5\text{ h/dia}$):**
     $$E_{\text{efic}} = \frac{4 \times 9 \times 4,5 \times 30}{1000} = 4,86\text{ kWh/mês}$$

4. **Notebook de Estudo/Trabalho ($65\text{ W}$):**
   * Base ($6,0\text{ h/dia}$): $11,70\text{ kWh/mês}$ | Eficiente ($5,0\text{ h/dia}$ com gerenciamento de energia): $9,75\text{ kWh/mês}$.

5. **Ventilador de Mesa ($65\text{ W}$):**
   * Base ($6,0\text{ h/dia}$): $11,70\text{ kWh/mês}$ | Eficiente ($4,5\text{ h/dia}$): $8,78\text{ kWh/mês}$.

6. **Micro-ondas / Airfryer ($1.200\text{ W}$):**
   * Base ($0,20\text{ h/dia}$): $7,20\text{ kWh/mês}$ | Eficiente ($0,17\text{ h/dia}$): $6,12\text{ kWh/mês}$.

7. **Aparelhos em Stand-by e Carregadores na Tomada ($11\text{ W}$ agregados):**
   * Base ($10,0\text{ h/dia}$): $3,30\text{ kWh/mês}$ | Eficiente ($3,0\text{ h/dia}$ com filtro de linha chaveado): $0,99\text{ kWh/mês}$.

* **Consumo Total Base:** $82,50 + 39,60 + 9,00 + 11,70 + 11,70 + 7,20 + 3,30 = \mathbf{165,00\text{ kWh/mês}}$ ($\mathbf{1.980,00\text{ kWh/ano}}$).
* **Consumo Total Eficiente (Alternativa 1):** $37,62 + 34,20 + 4,86 + 9,75 + 8,78 + 6,12 + 0,99 = \mathbf{102,32\text{ kWh/mês}}$ ($\mathbf{1.227,84\text{ kWh/ano}}$).

---

## 2. Cálculo Tarifário e Comparação Financeira

Utilizando a tarifa residencial B1 da Enel SP homologada pela ANEEL ($\text{TUSD} = \text{R\$ } 0,47242/\text{kWh}$, $\text{TE} = \text{R\$ } 0,31696/\text{kWh}$, soma $\text{R\$ } 0,78938/\text{kWh}$ sem tributos; tarifa efetiva com tributos médios de $18\%$ por dentro $= \text{R\$ } 0,96266/\text{kWh}$) e CIP municipal de $\text{R\$ } 15,50/\text{mês}$:

* **Fatura no Cenário Base ($165,00\text{ kWh/mês}$):**
  $$\text{Custo}_{\text{base}} = (165,00 \times 0,96266) + 15,50 = 158,84 + 15,50 = \mathbf{\text{R\$ } 174,34/\text{mês}}\quad (\mathbf{\text{R\$ } 2.092,08/\text{ano}})$$

* **Fatura na Alternativa 1 — Eficiência Energética ($102,32\text{ kWh/mês}$):**
  $$\text{Custo}_{\text{Alt1}} = (102,32 \times 0,96266) + 15,50 = 98,50 + 15,50 = \mathbf{\text{R\$ } 114,00/\text{mês}}$$
  $$\text{Economia}_{\text{Alt1}} = 174,34 - 114,00 = \mathbf{\text{R\$ } 60,34/\text{mês}}\quad (\mathbf{\text{R\$ } 724,08/\text{ano}})$$
  $$\text{Payback}_{\text{Alt1}} = \frac{\text{R\$ } 48,00}{\text{R\$ } 60,34/\text{mês}} = \mathbf{0,80\text{ mês}}\approx 24\text{ dias}$$

* **Fatura na Alternativa 2 — Energia Solar por Assinatura / Geração Compartilhada (Lei nº 14.300/2022):**
  * Energia compensável por créditos solares (descontando o custo de disponibilidade monofásico de $30\text{ kWh/mês}$):
    $$E_{\text{comp}} = 165,00 - 30,00 = 135,00\text{ kWh/mês}$$
  * Economia mensal com desconto de $12\%$ sobre a energia compensada:
    $$\text{Economia}_{\text{Alt2}} = 135,00 \times 0,96266 \times 0,12 = \mathbf{\text{R\$ } 15,60/\text{mês}}\quad (\mathbf{\text{R\$ } 187,20/\text{ano}})$$
  * Nova fatura total:
    $$\text{Custo}_{\text{Alt2}} = 174,34 - 15,60 = \mathbf{\text{R\$ } 158,74/\text{mês}}$$

---

## 3. Cálculo de Emissões de Gases de Efeito Estufa ($\text{CO}_2\text{e}$)

Adotando o fator médio de emissão do Sistema Interligado Nacional ($\text{FE}_{\text{SIN}} = 0,0385\text{ kg CO}_2\text{e}/\text{kWh}$, fonte MCTI/SIRENE, média anual de 2023):
* **Pegada anual no Cenário Base:** $1.980,00\text{ kWh/ano} \times 0,0385 = \mathbf{76,23\text{ kg CO}_2\text{e/ano}}$.
* **Emissões evitadas na Alternativa 1:** $62,68\text{ kWh/mês} \times 12 \times 0,0385 = \mathbf{28,96\text{ kg CO}_2\text{e/ano}}$.
* **Energia renovável contratada / compensada na Alternativa 2:** $135,00\text{ kWh/mês} \times 12 = 1.620,00\text{ kWh/ano} \implies \mathbf{62,37\text{ kg CO}_2\text{e/ano}}$.


---

## Observações sobre as Fontes e Limitações dos Cálculos

* **Tarifa:** os valores de TUSD e TE correspondem à tarifa residencial B1 da Enel SP após o Reajuste Tarifário Anual de 2026, aprovado pela ANEEL em 30/06/2026 e vigente desde 04/07/2026 (efeito médio de 10,18%). Antes do reajuste, a tarifa B1 era de R$ 725,18/MWh (TUSD R$ 0,43244 + TE R$ 0,29274). A alíquota de ICMS de 18% e a CIP de R$ 15,50 são premissas simplificadoras da equipe. Em faturas residenciais reais da Enel SP, a alíquota de ICMS aparece como 12% na faixa de cerca de 90 a 200 kWh/mês (e isenta abaixo disso); com 12%, a tarifa efetiva seria de cerca de R$ 0,897/kWh e todos os valores em reais deste estudo ficariam aproximadamente 7% menores, sem mudar a ordem das alternativas. A CIP varia por município e faixa de consumo.
* **Fator de emissão:** usamos o fator médio anual do SIN de 2023 ($0,0385\text{ kg CO}_2/\text{kWh}$), divulgado pelo MCTI. A partir de 2025 o MCTI passou a incluir usinas solares e eólicas na base de cálculo, e os fatores mensais caíram (ex.: $0,0289\text{ kg CO}_2/\text{kWh}$ em abril de 2025). Por isso, as emissões evitadas aqui podem estar **superestimadas**; o resultado deve ser lido como ordem de grandeza.
* **Tarifa Social:** a regra de 100% de desconto até 80 kWh/mês e 0% acima disso vem da Lei nº 15.235/2025, que alterou a Lei nº 12.212/2010 (conversão da MP nº 1.300/2025).
* **Solar por assinatura:** o desconto de 12% é uma média de mercado adotada como premissa; cada cooperativa ou consórcio tem condições próprias.
