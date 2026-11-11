# Roteiro do Vídeo Técnico no YouTube (Até 3 Minutos) — SERS

* **Formato exigido:** Vídeo **não listado** no YouTube, duração máxima de **3 minutos (180 segundos)**.
* **Estilo:** Vídeo técnico demonstrando o problema, os cálculos/comparações e a execução do assistente (sem formato comercial de pitch).

---

## ⏱️ 0:00 a 0:35 — 1. O Público e a Necessidade Energética Escolhida (35s)
* **Na tela:** Mostrar o `README.md` do repositório GitHub com a frase-síntese destacada.
* **Fala sugerida:**
  > *"Olá! Neste vídeo apresentamos a contribuição de Soluções em Energias Renováveis e Sustentáveis para o nosso projeto Citizen Assist AI. O nosso público-alvo são jovens de 16 a 24 anos em transição para a vida adulta — o mesmo público que busca o assistente para tirar documentos pela primeira vez e entrar no primeiro emprego. O problema real que abordamos é a primeira conta de luz no nome desse jovem, quando ele sai da casa dos pais, divide uma república ou ajuda nas contas da família. Com renda baixa de primeiro emprego ou aprendiz, ele nunca leu uma fatura de energia, não sabe o que mais pesa no consumo, desconhece a Tarifa Social e, por morar de aluguel, não pode instalar placas solares no telhado."*

---

## ⏱️ 0:35 a 1:30 — 2. Análise de Consumo e Comparação das Alternativas (55s)
* **Na tela:** Executar `python3 analise_consumo_alternativas.py` no terminal e mostrar a tabela gerada a partir de `dados/consumo_aparelhos_jovem.csv`.
* **Fala sugerida:**
  > *"Aplicando a fórmula de potência, tempo de uso e período de 30 dias com base nas tabelas do PROCEL/INMETRO e na tarifa residencial B1 da Enel SP homologada pela ANEEL (R$ 0,789/kWh sem impostos ou R$ 0,962/kWh com tributos, mais R$ 15,50 de iluminação pública), modelamos uma moradia jovem com consumo base de 165 kWh/mês e fatura de R$ 174,34/mês, onde o chuveiro elétrico responde sozinho por 50% do gasto (82,5 kWh).*
  >
  > *Comparamos duas alternativas aplicáveis a quem mora de aluguel para o mesmo período mensal e anual:*
  > *1) A Alternativa 1, de Eficiência Energética — troca de 4 lâmpadas para LED 9W, ajuste do chuveiro para o modo Verão por 10 minutos e filtro de linha contra stand-by — reduz o consumo em 38% (para 102,32 kWh/mês), gerando economia de R$ 60,34 por mês (R$ 724/ano), com investimento de R$ 48 que se paga em 24 dias e evitando 28,96 kg de CO2 por ano.*
  > *2) A Alternativa 2, com fonte renovável, é a Energia Solar por Assinatura via Geração Distribuída Compartilhada (Lei 14.300/2022). Sem obras no telhado e com investimento inicial zero, o jovem recebe créditos de uma fazenda solar com 12% de desconto sobre os 135 kWh compensáveis, economizando R$ 15,60 por mês (R$ 187,20/ano) e contratando 1.620 kWh/ano de energia limpa (62,37 kg de CO2/ano)."*

---

## ⏱️ 1:30 a 2:25 — 3. Demonstração das Funcionalidades de Energia no Assistente (55s)
* **Na tela:** Executar `python3 citizen_assist_energia.py`, navegar pelas opções `[1]` (ler a fatura), `[2]` (Tarifa Social / CadÚnico) e `[4]` (Simulador Personalizado).
* **Fala sugerida:**
  > *"Aqui no Citizen Assist AI, incorporamos essas três orientações: na opção 1, o jovem aprende a ler kWh, TUSD, TE e Bandeiras Tarifárias. Na opção 2, conectamos a Tarifa Social ao CadÚnico — o mesmo cadastro que o jovem já usa para a ID Jovem — explicando a regra atual da ANEEL de 100% de isenção na tarifa nos primeiros 80 kWh/mês.*
  >
  > *Na opção 4, temos o Simulador Personalizado: o jovem informa seu consumo em kWh, se possui CadÚnico e sua renda em salários mínimos, sem precisar digitar CPF ou dados pessoais. O sistema calcula na hora a fatura com e sem Tarifa Social e compara a Eficiência Energética com a Energia Solar por Assinatura."*

---

## ⏱️ 2:25 a 3:00 — 4. Principais Recomendações, Referências e Limitações (35s)
* **Na tela:** Destacar o bloco de recomendações e avisos de limitações no terminal e mostrar os arquivos de testes no repositório.
* **Fala sugerida:**
  > *"Como recomendação final, o assistente orienta que jovens com baixa renda no CadÚnico priorizem a Eficiência Energética para manter o consumo próximo a 80 kWh/mês e aproveitar a isenção da Tarifa Social, avisando que a taxa municipal de iluminação pública ainda é cobrada. Já para quem não tem Tarifa Social e consome acima de 120 kWh/mês no aluguel, recomendamos combinar a eficiência com a Energia Solar por Assinatura, economizando R$ 68,69 por mês. Todas as respostas trazem referências verificáveis da ANEEL, PROCEL e MCTI e alertam sobre limitações contratuais e tarifárias. Obrigado!"*
