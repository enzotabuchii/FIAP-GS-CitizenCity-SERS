# Registro de Testes com Usuários e Ajustes Realizados — SERS

Em conformidade com os requisitos da disciplina de **Soluções em Energias Renováveis e Sustentáveis** e com a **LGPD (Lei nº 13.709/2018)**, os testes de usabilidade e compreensão das orientações foram realizados com **3 usuários reais do público-alvo (jovens de 16 a 24 anos)**, sem coleta de nome completo, CPF, NIS ou endereço.

---

## Indicadores Consolidados dos Testes
* **Taxa de acerto das orientações:** $100\%$ nos 3 cenários principais e $87,5\%$ em perguntas abertas antes do ajuste de vocabulário ($100\%$ após inclusão de sinônimos coloquiais).
* **Tempo médio para encontrar a informação:** $14,2\text{ segundos}$ via menu numerado e $8,5\text{ segundos}$ via busca inteligente por pergunta.
* **Facilidade de utilização (escala de 1 a 5):** Média **4,8 / 5,0**.

---

## Detalhamento das Situações Testadas

### Situação 1 — Leitura da Primeira Conta de Luz e Identificação de Vilões de Consumo
* **Perfil do usuário (anônimo):** 18 anos, Jovem Aprendiz administrativo, recém-mudado para república estudantil.
* **Tarefa realizada:** Consultar a opção `[1]` do assistente e fazer a pergunta livre *"por que minha conta veio cara se quase não fico em casa?"*.
* **Feedback recebido:** O usuário compreendeu rapidamente a fórmula do $\text{kWh}$, mas comentou que não sabia o significado das siglas **TUSD** e **TE** impressas na fatura da distribuidora e ficou surpreso ao ver que o chuveiro elétrico na posição Inverno representava $50\%$ do consumo ($82,5\text{ kWh}$ de $165\text{ kWh}$).
* **Ajuste implementado:** Foi adicionada a tradução explícita de **TUSD** (*Tarifa de Uso do Sistema de Distribuição*) e **TE** (*Tarifa de Energia*), além do percentual exato de peso de cada aparelho no resumo do Tópico 1.

### Situação 2 — Solicitação da Tarifa Social (TSEE) via CadÚnico / ID Jovem
* **Perfil do usuário (anônimo):** 20 anos, estudante e estagiário, inscrito no CadÚnico para uso da ID Jovem, renda familiar per capita de $0,4\text{ salário mínimo}$.
* **Tarefa realizada:** Utilizar o Simulador Personalizado (opção `[4]`) informando consumo de $75\text{ kWh/mês}$, inscrição no CadÚnico (`S`) e renda per capita de `0.4` salário mínimo.
* **Feedback recebido:** O usuário achou excelente descobrir que o mesmo CadÚnico da ID Jovem dá direito a $100\%$ de desconto até $80\text{ kWh/mês}$, mas perguntou: *"Então o boleto vai vir R$ 0,00?"*.
* **Ajuste implementado:** Reforçamos na saída do simulador e no Tópico 2 que **a fatura não chega a R$ 0,00**, pois a **CIP/COSIP** (Contribuição de Iluminação Pública da prefeitura, estimada em $\text{R\$ } 15,50$) continua sendo cobrada mesmo quando o consumo de energia tem $100\%$ de isenção.

### Situação 3 — Comparação de Alternativas para Morador de Aluguel (Eficiência vs. Solar por Assinatura)
* **Perfil do usuário (anônimo):** 23 anos, primeiro emprego CLT, divide apartamento alugado com consumo médio de $165\text{ kWh/mês}$ e sem direito à Tarifa Social (renda de $1,5\text{ salário mínimo}$).
* **Tarefa realizada:** Consultar o comparativo da opção `[3]` e simular a combinação de Eficiência Energética com Energia Solar por Assinatura na opção `[4]`.
* **Feedback recebido:** O usuário destacou que pensava que energia solar só existia instalando placas no telhado (o que seria impossível no imóvel alugado). Questionou apenas se havia pegadinha ou fidelidade ao assinar energia solar compartilhada.
* **Ajuste implementado:** Incluímos na seção de **Condições e Limitações** o alerta sobre consumo mínimo exigido pelas cooperativas ($120\text{ a } 150\text{ kWh/mês}$), necessidade de titularidade da conta sem débitos e atenção a cláusulas de aviso prévio/fidelidade contratual.
