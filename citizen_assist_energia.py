#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Citizen Assist AI — Assistente Digital de Energia e Sustentabilidade (SERS)
Global Solution 2026.2 — 1º Ano de Ciência da Computação (1CCPQ)

Frase-síntese:
"Jovens de 16 a 24 anos que assumem sua primeira conta de luz com renda de primeiro
emprego: o assistente ensina a ler a fatura, a pedir a Tarifa Social e a comparar
formas de economizar, incluindo uma fonte renovável acessível a quem mora de aluguel."
"""

from __future__ import annotations
from datetime import datetime
import json
from pathlib import Path
import re
import time
from typing import Dict, List, Tuple

from analise_consumo_alternativas import (
    BANDEIRAS_ANEEL_RS_POR_100KWH,
    calcular_energia_mensal_kwh,
    calcular_fatura_convencional,
    carregar_aparelhos_csv,
    comparar_alternativas_energia,
    exibir_relatorio_completo,
    simular_tarifa_social_tsee,
)


DIRETORIO_BASE = Path(__file__).resolve().parent
ARQUIVO_BASE_JSON = DIRETORIO_BASE / "dados" / "base_orientacoes_energia.json"
ARQUIVO_INDICADORES = DIRETORIO_BASE / "dados" / "indicadores_uso.json"

# regex pa proteger os dados pessoaias
PADRAO_DADOS_PESSOAIS = re.compile(
    r"(\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b|\b\d{11}\b|[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
)


class CitizenAssistEnergia:
    """
    Assistente digital educativo focado em orientar jovens de 16 a 24 anos
    sobre sua primeira conta de luz, Tarifa Social (CadÚnico/ID Jovem) e
    comparação entre eficiência energética e energia solar por assinatura.
    """

    def __init__(self) -> None:
        with open(ARQUIVO_BASE_JSON, mode="r", encoding="utf-8") as f:
            self.base = json.load(f)
        self.aviso_geral: str = self.base["aviso_geral"]
        self.topicos: List[Dict[str, object]] = self.base["topicos"]

    @staticmethod
    def contem_dados_pessoais(texto: str) -> bool:
        """Verifica se o usuário digitou CPF, NIS ou e-mail para proteger sua privacidade (LGPD)."""
        return bool(PADRAO_DADOS_PESSOAIS.search(texto))

    def buscar_orientacao_por_pergunta(self, pergunta: str) -> Tuple[Dict[str, object] | None, float]:
        """
        Realiza busca inteligente baseada em regras e palavras-chave com nível de confiança.
        Retorna (topico_encontrado, nivel_confianca).
        """
        texto = pergunta.strip().lower()
        if not texto:
            return None, 0.0

        melhor_topico = None
        maior_pontuacao = 0

        for topico in self.topicos:
            palavras = topico.get("palavras_chave", [])
            acertos = sum(1 for p in palavras if p in texto)
            if acertos > maior_pontuacao:
                maior_pontuacao = acertos
                melhor_topico = topico

        if maior_pontuacao == 0:
            return None, 0.0

        confianca = min(0.95, 0.45 + 0.20 * maior_pontuacao)
        return melhor_topico, round(confianca, 2)

    def formatar_resposta_topico(self, topico: Dict[str, object], confianca: float | None = None) -> str:
        """Formata um tópico da base verificável com explicação, referências e limitações."""
        linhas = [
            "\n" + "=" * 84,
            (
                f"{topico['titulo']}  [Correspondência com a sua pergunta: {confianca * 100:.0f}%]"
                if confianca is not None
                else str(topico["titulo"])
            ),
            "=" * 84,
            f"\nRESUMO ACESSÍVEL:\n   {topico['resumo_acessivel']}\n",
            "📋 ORIENTAÇÕES PASSO A PASSO E DADOS TÉCNICOS:",
        ]
        for item in topico["explicacao_detalhada"]:
            linhas.append(f"   • {item}")

        linhas.append("\nREFERÊNCIAS VERIFICÁVEIS:")
        for ref in topico["referencias"]:
            linhas.append(f"   [{ref}]")

        linhas.append(f"\nCONDIÇÕES E LIMITAÇÕES:\n   {topico['limitacoes']}")
        linhas.append(f"\nAVISO INSTITUCIONAL:\n   {self.aviso_geral}")
        linhas.append("=" * 84)
        return "\n".join(linhas)

    @staticmethod
    def registrar_indicador(
        acao: str,
        tempo_segundos: float,
        orientacao_correta: bool,
        nota_facilidade_1_a_5: int,
    ) -> None:
        """Salva indicadores de uso (tempo de resposta, acerto e facilidade) sem dados pessoais."""
        historico: List[Dict[str, object]] = []
        if ARQUIVO_INDICADORES.exists():
            try:
                with open(ARQUIVO_INDICADORES, mode="r", encoding="utf-8") as f:
                    historico = json.load(f)
            except (json.JSONDecodeError, OSError):
                historico = []

        historico.append(
            {
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "acao_consultada": acao,
                "tempo_encontrar_info_s": round(tempo_segundos, 2),
                "orientacao_util_correta": orientacao_correta,
                "nota_facilidade_1_a_5": max(1, min(5, nota_facilidade_1_a_5)),
            }
        )
        with open(ARQUIVO_INDICADORES, mode="w", encoding="utf-8") as f:
            json.dump(historico, f, ensure_ascii=False, indent=2)


def ler_float_seguro(mensagem: str, minimo: float = 0.0, maximo: float = 10000.0) -> float:
    """Lê um número real do usuário tratando entradas inválidas."""
    while True:
        entrada = input(mensagem).strip().replace(",", ".")
        if CitizenAssistEnergia.contem_dados_pessoais(entrada):
            print("[LGPD] Por segurança, não digite CPF, NIS, telefone ou e-mail! Digite apenas o número solicitado.")
            continue
        try:
            valor = float(entrada)
            if minimo <= valor <= maximo:
                return valor
            print(f"Valor fora do intervalo permitido ({minimo} a {maximo}). Tente novamente.")
        except ValueError:
            print("Entrada inválida! Por favor, digite apenas um valor numérico (ex.: 150 ou 0.5).")


def ler_sim_nao_seguro(mensagem: str) -> bool:
    """Lê uma confirmação S/N tratando entradas inválidas."""
    while True:
        entrada = input(mensagem).strip().lower()
        if entrada in ("s", "sim", "1", "y", "yes"):
            return True
        if entrada in ("n", "nao", "não", "0", "no"):
            return False
        print("Entrada inválida! Digite 'S' para Sim ou 'N' para Não.")


def executar_simulador_interativo(assistente: CitizenAssistEnergia) -> None:
    """Simulador personalizado da primeira conta de luz para o jovem de 16 a 24 anos."""
    inicio = time.time()
    print("\n" + "=" * 84)
    print("SIMULADOR PERSONALIZADO: SUA PRIMEIRA CONTA DE LUZ (JOVENS 16 A 24 ANOS)")
    print("=" * 84)
    print("Nota de privacidade (LGPD): Não coletamos nome, CPF, NIS ou endereço.\n")

    consumo_kwh = ler_float_seguro(
        "1) Qual é o consumo mensal da sua conta de luz em kWh? (Dica: uma kitnet/república costuma gastar ~165 kWh): ",
        minimo=1.0,
        maximo=5000.0,
    )
    inscrito_cadunico = ler_sim_nao_seguro(
        "2) Você ou sua família estão inscritos no CadÚnico (o mesmo cadastro da ID Jovem)? (S/N): "
    )
    renda_sm = ler_float_seguro(
        "3) Qual é a renda mensal por pessoa da residência em salários mínimos? (Ex.: 0.5 para meio salário, 1.0 para 1 salário): ",
        minimo=0.0,
        maximo=50.0,
    )
    mora_aluguel = ler_sim_nao_seguro(
        "4) Você mora de aluguel ou divide república (sem poder fazer obras no telhado)? (S/N): "
    )

    res_tsee = simular_tarifa_social_tsee(consumo_kwh, inscrito_cadunico, renda_sm)
    consumo_eficiente_estimado = round(consumo_kwh * 0.6201, 2)
    comp = comparar_alternativas_energia(consumo_kwh, consumo_eficiente_estimado)

    alt1 = comp["alternativa_1_eficiencia"]
    alt2 = comp["alternativa_2_solar_assinatura"]
    comb = comp["estrategia_combinada"]

    print("\n" + "=" * 84)
    print("RESULTADO DA SUA ANÁLISE PERSONALIZADA")
    print("=" * 84)
    print(f"• Consumo analisado: {consumo_kwh:.2f} kWh/mês")
    print(f"• Fatura convencional estimada (Enel SP c/ tributos + CIP): R$ {res_tsee['fatura_sem_beneficio_rs']:.2f}/mês")

    print("\n[A] VERIFICAÇÃO DE DIREITO À TARIFA SOCIAL (TSEE / CADÚNICO):")
    print(f"  - Enquadramento: {res_tsee['modalidade']}")
    print(f"  - Fatura com benefício social: R$ {res_tsee['fatura_com_beneficio_rs']:.2f}/mês "
          f"(Economia: R$ {res_tsee['economia_mensal_rs']:.2f}/mês | R$ {res_tsee['economia_anual_rs']:.2f}/ano)")
    print(f"  - Orientação: {res_tsee['orientacao']}")

    print("\n[B] COMPARAÇÃO DE ALTERNATIVAS TÉCNICAS (PERÍODO MENSAL E ANUAL):")
    print(f"  1) Alternativa 1 — Eficiência Energética (Troca para LED 9W + Chuveiro Verão/10min + Fim Stand-by):")
    print(f"     • Novo consumo estimado: {alt1['consumo_mensal_kwh']:.2f} kWh/mês (-{alt1['reducao_percentual']:.1f}%)")
    print(f"     • Nova fatura: R$ {alt1['custo_mensal_rs']:.2f}/mês | Economia: R$ {alt1['economia_mensal_rs']:.2f}/mês (R$ {alt1['economia_anual_rs']:.2f}/ano)")
    print(f"     • Custo inicial: R$ {alt1['investimento_inicial_rs']:.2f} | Tempo de retorno (Payback): {alt1['payback_meses']:.2f} mês")
    print(f"     • Impacto ambiental: Evita {alt1['co2_evitado_anual_kg']:.2f} kg de CO2e por ano.")

    print(f"\n  2) Alternativa 2 (Fonte Renovável) — Energia Solar por Assinatura (GD Compartilhada - Lei 14.300/2022):")
    print(f"     • Energia renovável compensada: {alt2['energia_solar_compensada_mensal_kwh']:.2f} kWh/mês (12% de desconto nos créditos)")
    print(f"     • Nova fatura: R$ {alt2['custo_mensal_rs']:.2f}/mês | Economia: R$ {alt2['economia_mensal_rs']:.2f}/mês (R$ {alt2['economia_anual_rs']:.2f}/ano)")
    print(f"     • Custo inicial: R$ 0,00 (sem obras e sem placas no telhado — {'perfeito para quem mora de aluguel!' if mora_aluguel else 'adesão 100% digital'})")
    print(f"     • Impacto ambiental: {alt2['energia_solar_compensada_mensal_kwh'] * 12:.0f} kWh/ano de matriz solar ({alt2['co2_evitado_anual_kg']:.2f} kg CO2e/ano).")

    print("\n[C] RECOMENDAÇÃO FINAL E LIMITAÇÕES:")
    if res_tsee["elegivel_tsee"] and consumo_eficiente_estimado <= 80.0:
        print(
            "  DICA DE OURO: Aplicando a Alternativa 1 (Eficiência Energética), seu consumo cai para perto ou abaixo "
            "de 80 kWh/mês, permitindo aproveitar quase 100% de isenção na Tarifa Social (TSEE)! Nesse caso, NÃO assine "
            "energia solar compartilhada, pois a TSEE já garante desconto muito maior."
        )
    elif consumo_kwh < 110.0:
        print(
            "  RECOMENDAÇÃO: Priorize a Alternativa 1 (Eficiência Energética). Como seu consumo já é baixo, "
            "muitas cooperativas de Energia Solar por Assinatura exigem consumo mínimo de 120 a 150 kWh/mês."
        )
    else:
        print(
            f"  RECOMENDAÇÃO: Comece pela Alternativa 1 (que economiza R$ {alt1['economia_mensal_rs']:.2f}/mês imediatamente) "
            f"e combine com a Alternativa 2 (Energia Solar por Assinatura) para usar energia 100% renovável sem precisar de telhado "
            f"próprio, alcançando economia combinada de R$ {comb['economia_mensal_rs']:.2f}/mês (R$ {comb['economia_anual_rs']:.2f}/ano)!"
        )

    print("\nAVISO DE LIMITAÇÕES E FONTES:")
    print("  • Cálculos baseados na tarifa residencial B1 da Enel SP (ANEEL 2026: R$ 0,78938/kWh s/ impostos; ~R$ 0,96266/kWh c/ tributos).")
    print("  • Fontes: Lei nº 12.212/2010 alterada pela Lei nº 15.235/2025 (TSEE); Lei nº 14.300/2022 (GD Compartilhada); PROCEL/INMETRO; MCTI.")
    print("  • Estimativas não representam garantia de resultado financeiro e este assistente não é canal oficial do governo.")
    print("=" * 84)

    tempo_gasto = time.time() - inicio
    assistente.registrar_indicador("simulador_primeira_conta_luz", tempo_gasto, True, 5)


def menu_interativo() -> None:
    """Loop principal de navegação simples e acessível do Citizen Assist AI (Módulo SERS)."""
    assistente = CitizenAssistEnergia()

    while True:
        print("\n" + "=" * 84)
        print("CITIZEN ASSIST AI — MÓDULO DE ENERGIA E SUSTENTABILIDADE (SERS)")
        print("   Apoio ao jovem (16 a 24 anos) na sua primeira conta de luz e primeiro emprego")
        print("=" * 84)
        print("  [1] Como ler sua primeira conta de luz (kWh, Bandeiras Tarifárias e aparelhos que mais pesam)")
        print("  [2] Tarifa Social de Energia Elétrica (TSEE): quem tem direito via CadÚnico / ID Jovem")
        print("  [3] Comparar Alternativas: Eficiência Energética (LED/Hábitos) vs. Energia Solar por Assinatura")
        print("  [4] Simulador Personalizado: Calcule sua fatura, Tarifa Social e economia das alternativas")
        print("  [5] Ver Relatório Técnico Completo (Tabelas de consumo PROCEL, cálculos e emissões de CO2)")
        print("  [6] Fazer uma pergunta livre ao Assistente (Busca Inteligente)")
        print("  [0] Sair")
        print("-" * 84)

        escolha = input("Escolha uma opção (0 a 6): ").strip()

        if assistente.contem_dados_pessoais(escolha):
            print("\n[PROTEÇÃO DE DADOS - LGPD] Não digite CPF, NIS ou dados pessoais no assistente!")
            continue

        inicio = time.time()
        if escolha == "1":
            print(assistente.formatar_resposta_topico(assistente.topicos[0]))
            assistente.registrar_indicador("topico_1_ler_fatura", time.time() - inicio, True, 5)
        elif escolha == "2":
            print(assistente.formatar_resposta_topico(assistente.topicos[1]))
            assistente.registrar_indicador("topico_2_tarifa_social", time.time() - inicio, True, 5)
        elif escolha == "3":
            print(assistente.formatar_resposta_topico(assistente.topicos[2]))
            assistente.registrar_indicador("topico_3_comparar_alternativas", time.time() - inicio, True, 5)
        elif escolha == "4":
            executar_simulador_interativo(assistente)
        elif escolha == "5":
            exibir_relatorio_completo()
            assistente.registrar_indicador("relatorio_tecnico_completo", time.time() - inicio, True, 5)
        elif escolha == "6":
            pergunta = input("\nDigite sua dúvida sobre conta de luz, Tarifa Social ou energia solar: ").strip()
            if assistente.contem_dados_pessoais(pergunta):
                print("\n[LGPD] Detectamos um possível dado pessoal (CPF/NIS/e-mail). Sua pergunta não foi gravada.")
                continue
            topico, confianca = assistente.buscar_orientacao_por_pergunta(pergunta)
            if topico is not None:
                print(assistente.formatar_resposta_topico(topico, confianca=confianca))
                assistente.registrar_indicador("pergunta_livre_respondida", time.time() - inicio, True, 5)
            else:
                print(
                    "\nNão encontrei uma resposta exata na base verificável para esses termos.\n"
                    "   Tente perguntar sobre: 'como ler a fatura', 'bandeiras', 'chuveiro', "
                    "'tarifa social', 'cadunico', 'id jovem', 'energia solar por assinatura' ou 'aluguel'."
                )
                assistente.registrar_indicador("pergunta_livre_sem_correspondencia", time.time() - inicio, False, 4)
        elif escolha == "0":
            print("\nObrigado por utilizar o Citizen Assist AI! Use a energia de forma consciente.")
            break
        else:
            print("\nOpção inválida! Por favor, digite apenas um número entre 0 e 6.")


if __name__ == "__main__":
    menu_interativo()
