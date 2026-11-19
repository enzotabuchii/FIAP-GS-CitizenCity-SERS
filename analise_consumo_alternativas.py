#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Citizen Assist AI — Módulo de Análise de Consumo e Comparação de Alternativas (SERS)
Global Solution 2026.2 — 1º Ano de Ciência da Computação (1CC)

Público-alvo:
Jovens de 16 a 24 anos que assumem sua primeira conta de luz com renda de primeiro
emprego: o assistente ensina a ler a fatura, a pedir a Tarifa Social e a comparar
formas de economizar, incluindo uma fonte renovável acessível a quem mora de aluguel.
"""

from __future__ import annotations
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

TUSD_ENEL_SP_RS_KWH: float = 0.47242
TE_ENEL_SP_RS_KWH: float = 0.31696
TARIFA_BASE_ANEEL_RS_KWH: float = round(TUSD_ENEL_SP_RS_KWH + TE_ENEL_SP_RS_KWH, 5)
ALIQUOTA_MEDIA_TRIBUTOS: float = 0.18
TARIFA_EFETIVA_COM_TRIBUTOS_RS_KWH: float = round(
    TARIFA_BASE_ANEEL_RS_KWH / (1.0 - ALIQUOTA_MEDIA_TRIBUTOS), 5
)
CIP_COSIP_MENSAL_RS: float = 15.50

BANDEIRAS_ANEEL_RS_POR_100KWH: Dict[str, float] = {
    "verde": 0.00,
    "amarela": 1.885,
    "vermelha_p1": 4.463,
    "vermelha_p2": 7.875,
}

FATOR_EMISSAO_SIN_KGCO2_KWH: float = 0.0385
CUSTO_DISPONIBILIDADE_MONOFASICO_KWH: float = 30.0
INVESTIMENTO_ALT1_EFICIENCIA_RS: float = 48.00

@dataclass
class ItemConsumoAparelho:
    """Representa um equipamento elétrico na residência/república do jovem."""
    aparelho: str
    quantidade: int
    potencia_w_base: float
    horas_dia_base: float
    dias_mes: int
    kwh_mes_base: float
    potencia_w_eficiente: float
    horas_dia_eficiente: float
    kwh_mes_eficiente: float
    tipo_dado: str
    fonte_referencia: str
    observacao: str


def calcular_energia_mensal_kwh(
    potencia_watts: float,
    horas_por_dia: float,
    dias_no_mes: int = 30,
    quantidade: int = 1,
    fator_operacao: float = 1.0,
) -> float:
    """
    Calcula o consumo mensal de energia elétrica em kWh:
        E (kWh/mês) = (P [W] * t [h/dia] * d [dias] * qtd * fator_operacao) / 1000
    """
    if potencia_watts < 0 or horas_por_dia < 0 or dias_no_mes <= 0 or quantidade <= 0:
        raise ValueError("Os parâmetros de potência, tempo, dias e quantidade devem ser positivos.")
    if horas_por_dia > 24:
        raise ValueError("O tempo de uso diário não pode ultrapassar 24 horas.")
    energia = (potencia_watts * horas_por_dia * dias_no_mes * quantidade * fator_operacao) / 1000.0
    return round(energia, 2)


def carregar_aparelhos_csv(caminho_csv: Path | None = None) -> List[ItemConsumoAparelho]:
    """Carrega a tabela de consumo de equipamentos do jovem a partir do CSV."""
    if caminho_csv is None:
        caminho_csv = Path(__file__).resolve().parent / "dados" / "consumo_aparelhos_jovem.csv"

    itens: List[ItemConsumoAparelho] = []
    with open(caminho_csv, mode="r", encoding="utf-8") as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            itens.append(
                ItemConsumoAparelho(
                    aparelho=linha["aparelho"],
                    quantidade=int(linha["quantidade"]),
                    potencia_w_base=float(linha["potencia_w"]),
                    horas_dia_base=float(linha["horas_dia_base"]),
                    dias_mes=int(linha["dias_mes"]),
                    kwh_mes_base=float(linha["kwh_mes_base"]),
                    potencia_w_eficiente=float(linha["potencia_w_eficiente"]),
                    horas_dia_eficiente=float(linha["horas_dia_eficiente"]),
                    kwh_mes_eficiente=float(linha["kwh_mes_eficiente"]),
                    tipo_dado=linha["tipo_dado"],
                    fonte_referencia=linha["fonte_referencia"],
                    observacao=linha["observacao"],
                )
            )
    validar_consumo_csv(itens)
    return itens


def validar_consumo_csv(itens: List[ItemConsumoAparelho], tolerancia_kwh: float = 0.01) -> None:
    """
    Recalcula o consumo de cada aparelho (P x t x d x qtd / 1000) e confere com os
    valores de kWh informados no CSV, para garantir que a tabela de dados e os
    cálculos estão coerentes.
    """
    for item in itens:
        base = calcular_energia_mensal_kwh(
            item.potencia_w_base, item.horas_dia_base, item.dias_mes, item.quantidade
        )
        efic = calcular_energia_mensal_kwh(
            item.potencia_w_eficiente, item.horas_dia_eficiente, item.dias_mes, item.quantidade
        )
        if abs(base - item.kwh_mes_base) > tolerancia_kwh or abs(efic - item.kwh_mes_eficiente) > tolerancia_kwh:
            raise ValueError(
                f"Consumo inconsistente no CSV para '{item.aparelho}': "
                f"calculado base={base} / eficiente={efic}, "
                f"informado base={item.kwh_mes_base} / eficiente={item.kwh_mes_eficiente}."
            )


def calcular_fatura_convencional(
    consumo_kwh: float,
    bandeira: str = "verde",
    incluir_tributos: bool = True,
    incluir_cip: bool = True,
) -> Dict[str, float]:
    """
    Calcula o valor detalhado da fatura residencial (Subgrupo B1) para um dado consumo em kWh.
    """
    if consumo_kwh < 0:
        raise ValueError("O consumo em kWh não pode ser negativo.")
    if bandeira not in BANDEIRAS_ANEEL_RS_POR_100KWH:
        raise ValueError(f"Bandeira inválida: {bandeira}. Opções: {list(BANDEIRAS_ANEEL_RS_POR_100KWH.keys())}")

    tarifa_unitaria = TARIFA_EFETIVA_COM_TRIBUTOS_RS_KWH if incluir_tributos else TARIFA_BASE_ANEEL_RS_KWH
    custo_consumo = consumo_kwh * tarifa_unitaria

    adicional_bandeira_base = (consumo_kwh / 100.0) * BANDEIRAS_ANEEL_RS_POR_100KWH[bandeira]
    adicional_bandeira = (
        adicional_bandeira_base / (1.0 - ALIQUOTA_MEDIA_TRIBUTOS)
        if incluir_tributos
        else adicional_bandeira_base
    )

    cip = CIP_COSIP_MENSAL_RS if incluir_cip and consumo_kwh > 0 else 0.0
    total = custo_consumo + adicional_bandeira + cip

    return {
        "consumo_kwh": round(consumo_kwh, 2),
        "tarifa_unitaria_rs_kwh": round(tarifa_unitaria, 5),
        "custo_energia_rs": round(custo_consumo, 2),
        "adicional_bandeira_rs": round(adicional_bandeira, 2),
        "cip_cosip_rs": round(cip, 2),
        "total_fatura_rs": round(total, 2),
    }


def simular_tarifa_social_tsee(
    consumo_kwh: float,
    inscrito_cadunico: bool,
    renda_per_capita_salarios_minimos: float,
    recebe_bpc: bool = False,
) -> Dict[str, object]:
    """
    Simula a elegibilidade e o desconto da Tarifa Social de Energia Elétrica (TSEE)
    e do Desconto Social, conforme regras da ANEEL vigentes em 2025/2026:
      - TSEE (CadÚnico renda per capita <= 0.5 SM ou BPC): 100% de desconto na tarifa
        de consumo para os primeiros 80 kWh/mês; excedente cobrado na tarifa normal.
      - Desconto Social (CadÚnico com 0.5 SM < renda per capita <= 1.0 SM): desconto
        aproximado de 12% (isenção da CDE) para o consumo até 120 kWh/mês.
    """
    if consumo_kwh < 0 or renda_per_capita_salarios_minimos < 0:
        raise ValueError("Consumo e renda não podem ser negativos.")

    fatura_normal = calcular_fatura_convencional(consumo_kwh, bandeira="verde", incluir_tributos=True, incluir_cip=True)

    elegivel_tsee = recebe_bpc or (inscrito_cadunico and renda_per_capita_salarios_minimos <= 0.5)
    elegivel_desconto_social = (not elegivel_tsee) and inscrito_cadunico and (0.5 < renda_per_capita_salarios_minimos <= 1.0)

    if elegivel_tsee:
        kwh_isentos = min(consumo_kwh, 80.0)
        kwh_excedentes = max(0.0, consumo_kwh - 80.0)
        custo_energia_tsee = kwh_excedentes * TARIFA_EFETIVA_COM_TRIBUTOS_RS_KWH
        total_tsee = custo_energia_tsee + (CIP_COSIP_MENSAL_RS if consumo_kwh > 0 else 0.0)
        economia_mensal = fatura_normal["total_fatura_rs"] - total_tsee
        modalidade = "Tarifa Social Plena (TSEE - Isenção de 100% até 80 kWh/mês)"
        orientacao = (
            "Você atende aos critérios da Tarifa Social (TSEE)! Como já possui ou pode fazer o CadÚnico "
            "(o mesmo usado na ID Jovem), os primeiros 80 kWh/mês têm 100% de desconto na tarifa de energia. "
            "Atenção: a taxa de iluminação pública (CIP) ainda pode ser cobrada pela prefeitura."
        )
    elif elegivel_desconto_social:
        kwh_com_desconto = min(consumo_kwh, 120.0)
        kwh_excedentes = max(0.0, consumo_kwh - 120.0)
        custo_energia_ds = (
            kwh_com_desconto * TARIFA_EFETIVA_COM_TRIBUTOS_RS_KWH * 0.88
            + kwh_excedentes * TARIFA_EFETIVA_COM_TRIBUTOS_RS_KWH
        )
        total_tsee = custo_energia_ds + (CIP_COSIP_MENSAL_RS if consumo_kwh > 0 else 0.0)
        economia_mensal = fatura_normal["total_fatura_rs"] - total_tsee
        modalidade = "Desconto Social (Isenção de encargos CDE até 120 kWh/mês)"
        orientacao = (
            "Você se enquadra na faixa do Desconto Social da ANEEL (CadÚnico com renda per capita entre "
            "meio e 1 salário mínimo), garantindo tarifa reduzida nos primeiros 120 kWh/mês."
        )
    else:
        total_tsee = fatura_normal["total_fatura_rs"]
        economia_mensal = 0.0
        modalidade = "Tarifa Residencial Convencional (Sem enquadramento na TSEE)"
        if not inscrito_cadunico and renda_per_capita_salarios_minimos <= 1.0:
            orientacao = (
                "Sua renda permite o benefício, mas é obrigatório estar inscrito no CadÚnico! "
                "Procure o CRAS do seu município com CPF e comprovante de residência para se cadastrar "
                "(isso também libera a ID Jovem)."
            )
        else:
            orientacao = (
                "Sua faixa de renda atual está acima do limite da Tarifa Social. Para reduzir sua conta, "
                "recomendamos as alternativas de Eficiência Energética e Energia Solar por Assinatura."
            )

    return {
        "elegivel_tsee": elegivel_tsee,
        "elegivel_desconto_social": elegivel_desconto_social,
        "modalidade": modalidade,
        "fatura_sem_beneficio_rs": round(fatura_normal["total_fatura_rs"], 2),
        "fatura_com_beneficio_rs": round(total_tsee, 2),
        "economia_mensal_rs": round(economia_mensal, 2),
        "economia_anual_rs": round(economia_mensal * 12.0, 2),
        "orientacao": orientacao,
    }


def comparar_alternativas_energia(
    consumo_base_kwh: float = 165.00,
    consumo_eficiente_kwh: float = 102.32,
    desconto_solar_assinatura_pct: float = 12.0,
    custo_disponibilidade_kwh: float = CUSTO_DISPONIBILIDADE_MONOFASICO_KWH,
) -> Dict[str, Dict[str, float | str]]:
    """
    Compara tecnicamente:
      - Cenário Base (sem intervenção)
      - Alternativa 1: Eficiência Energética e Mudança de Hábitos (LED + Chuveiro Verão/10min + Stand-by)
      - Alternativa 2 (Renovável): Energia Solar por Assinatura (GD Compartilhada - Lei 14.300/2022)
      - Estratégia Combinada (Alternativa 1 + Alternativa 2)
    """
    if consumo_base_kwh <= 0 or consumo_eficiente_kwh <= 0:
        raise ValueError("Os valores de consumo devem ser maiores que zero.")
    if consumo_eficiente_kwh > consumo_base_kwh:
        raise ValueError("O consumo eficiente não deve superar o consumo base.")

    fatura_base = calcular_fatura_convencional(consumo_base_kwh)
    custo_base_mensal = fatura_base["total_fatura_rs"]
    custo_base_anual = round(custo_base_mensal * 12.0, 2)
    emissoes_base_anual = round(consumo_base_kwh * 12.0 * FATOR_EMISSAO_SIN_KGCO2_KWH, 2)

    # eficiência energética
    fatura_alt1 = calcular_fatura_convencional(consumo_eficiente_kwh)
    custo_alt1_mensal = fatura_alt1["total_fatura_rs"]
    economia_alt1_mensal = round(custo_base_mensal - custo_alt1_mensal, 2)
    economia_alt1_anual = round(economia_alt1_mensal * 12.0, 2)
    reducao_kwh_mensal = round(consumo_base_kwh - consumo_eficiente_kwh, 2)
    payback_alt1_meses = (
        round(INVESTIMENTO_ALT1_EFICIENCIA_RS / economia_alt1_mensal, 2)
        if economia_alt1_mensal > 0
        else 0.0
    )
    co2_evitado_alt1_anual = round(reducao_kwh_mensal * 12.0 * FATOR_EMISSAO_SIN_KGCO2_KWH, 2)

    kwh_compensados_alt2 = max(0.0, consumo_base_kwh - custo_disponibilidade_kwh)
    desconto_frac = desconto_solar_assinatura_pct / 100.0
    economia_alt2_mensal = round(
        kwh_compensados_alt2 * TARIFA_EFETIVA_COM_TRIBUTOS_RS_KWH * desconto_frac, 2
    )
    custo_alt2_mensal = round(custo_base_mensal - economia_alt2_mensal, 2)
    economia_alt2_anual = round(economia_alt2_mensal * 12.0, 2)
    co2_compensado_alt2_anual = round(kwh_compensados_alt2 * 12.0 * FATOR_EMISSAO_SIN_KGCO2_KWH, 2)

    kwh_compensados_comb = max(0.0, consumo_eficiente_kwh - custo_disponibilidade_kwh)
    economia_solar_sobre_eficiente = round(
        kwh_compensados_comb * TARIFA_EFETIVA_COM_TRIBUTOS_RS_KWH * desconto_frac, 2
    )
    custo_comb_mensal = round(custo_alt1_mensal - economia_solar_sobre_eficiente, 2)
    economia_comb_mensal = round(custo_base_mensal - custo_comb_mensal, 2)
    economia_comb_anual = round(economia_comb_mensal * 12.0, 2)

    return {
        "cenario_base": {
            "descricao": "Cenário Base (Sem intervenções)",
            "consumo_mensal_kwh": round(consumo_base_kwh, 2),
            "custo_mensal_rs": custo_base_mensal,
            "custo_anual_rs": custo_base_anual,
            "investimento_inicial_rs": 0.00,
            "emissoes_anuais_kgco2": emissoes_base_anual,
        },
        "alternativa_1_eficiencia": {
            "descricao": "Alternativa 1: Eficiência Energética (LED 9W + Chuveiro Verão/10min + Fim do Stand-by)",
            "consumo_mensal_kwh": round(consumo_eficiente_kwh, 2),
            "reducao_mensal_kwh": reducao_kwh_mensal,
            "reducao_percentual": round((reducao_kwh_mensal / consumo_base_kwh) * 100.0, 2),
            "custo_mensal_rs": custo_alt1_mensal,
            "economia_mensal_rs": economia_alt1_mensal,
            "economia_anual_rs": economia_alt1_anual,
            "investimento_inicial_rs": INVESTIMENTO_ALT1_EFICIENCIA_RS,
            "payback_meses": payback_alt1_meses,
            "co2_evitado_anual_kg": co2_evitado_alt1_anual,
        },
        "alternativa_2_solar_assinatura": {
            "descricao": "Alternativa 2 (Renovável): Energia Solar por Assinatura / GD Compartilhada (12% desc.)",
            "consumo_mensal_rede_kwh": round(consumo_base_kwh, 2),
            "energia_solar_compensada_mensal_kwh": round(kwh_compensados_alt2, 2),
            "custo_mensal_rs": custo_alt2_mensal,
            "economia_mensal_rs": economia_alt2_mensal,
            "economia_anual_rs": economia_alt2_anual,
            "investimento_inicial_rs": 0.00,
            "payback_meses": 0.00,
            "co2_evitado_anual_kg": co2_compensado_alt2_anual,
        },
        "estrategia_combinada": {
            "descricao": "Estratégia Combinada (Eficiência Energética + Energia Solar por Assinatura)",
            "consumo_mensal_kwh": round(consumo_eficiente_kwh, 2),
            "energia_solar_compensada_mensal_kwh": round(kwh_compensados_comb, 2),
            "custo_mensal_rs": custo_comb_mensal,
            "economia_mensal_rs": economia_comb_mensal,
            "economia_anual_rs": economia_comb_anual,
            "investimento_inicial_rs": INVESTIMENTO_ALT1_EFICIENCIA_RS,
        },
    }


def exibir_relatorio_completo() -> None:
    """Imprime no terminal o relatório analítico completo de SERS."""
    itens = carregar_aparelhos_csv()
    soma_base = round(sum(i.kwh_mes_base for i in itens), 2)
    soma_efic = round(sum(i.kwh_mes_eficiente for i in itens), 2)

    print("=" * 88)
    print("CITIZEN ASSIST AI — ANÁLISE TÉCNICA DE ENERGIA E SUSTENTABILIDADE (SERS)")
    print("Público: Jovens de 16 a 24 anos assumindo sua primeira conta de luz (1º emprego/aluguel)")
    print("=" * 88)

    print("\n1. LEVANTAMENTO DE CONSUMO POR EQUIPAMENTO (PERÍODO DE REFERÊNCIA: 30 DIAS)")
    print("-" * 88)
    print(f"{'Equipamento':<42} | {'Pot.(W)':>7} | {'h/dia*':>6} | {'Base(kWh)':>9} | {'Efic.(kWh)':>10}")
    print("-" * 88)
    for item in itens:
        nome_curto = item.aparelho[:42]
        print(
            f"{nome_curto:<42} | {item.potencia_w_base:>7.0f} | "
            f"{item.horas_dia_base:>6.2f} | {item.kwh_mes_base:>9.2f} | {item.kwh_mes_eficiente:>10.2f}"
        )
    print("-" * 88)
    print(f"{'TOTAL MENSAL ESTIMADO':<42} | {'-':>7} | {'-':>6} | {soma_base:>9.2f} | {soma_efic:>10.2f}")
    print("* h/dia equivalentes de funcionamento no cenário base (geladeira: 24 h ligada x fator 0,5 do compressor = 12 h).")

    comp = comparar_alternativas_energia(soma_base, soma_efic)
    base = comp["cenario_base"]
    alt1 = comp["alternativa_1_eficiencia"]
    alt2 = comp["alternativa_2_solar_assinatura"]
    comb = comp["estrategia_combinada"]

    print("\n2. COMPARAÇÃO DE ALTERNATIVAS (CUSTOS, VIABILIDADE E IMPACTO AMBIENTAL)")
    print("-" * 88)
    print(f"• Cenário Base ({base['consumo_mensal_kwh']} kWh/mês):")
    print(f"  - Fatura mensal estimada (c/ tributos + CIP): R$ {base['custo_mensal_rs']:.2f}/mês (R$ {base['custo_anual_rs']:.2f}/ano)")
    print(f"  - Pegada de carbono anual (SIN): {base['emissoes_anuais_kgco2']:.2f} kg CO2e/ano")

    print(f"\n• {alt1['descricao']}:")
    print(f"  - Novo consumo: {alt1['consumo_mensal_kwh']} kWh/mês (redução de {alt1['reducao_mensal_kwh']} kWh/mês ou {alt1['reducao_percentual']}%)")
    print(f"  - Nova fatura mensal: R$ {alt1['custo_mensal_rs']:.2f}/mês | Economia: R$ {alt1['economia_mensal_rs']:.2f}/mês (R$ {alt1['economia_anual_rs']:.2f}/ano)")
    print(f"  - Investimento inicial: R$ {alt1['investimento_inicial_rs']:.2f} | Payback: {alt1['payback_meses']:.2f} mês (~24 dias)")
    print(f"  - Emissões evitadas: {alt1['co2_evitado_anual_kg']:.2f} kg CO2e/ano")

    print(f"\n• {alt2['descricao']}:")
    print(f"  - Energia compensada por créditos solares: {alt2['energia_solar_compensada_mensal_kwh']} kWh/mês (+30 kWh taxa mínima rede)")
    print(f"  - Nova fatura mensal: R$ {alt2['custo_mensal_rs']:.2f}/mês | Economia: R$ {alt2['economia_mensal_rs']:.2f}/mês (R$ {alt2['economia_anual_rs']:.2f}/ano)")
    print(f"  - Investimento inicial: R$ {alt2['investimento_inicial_rs']:.2f} (sem obras, ideal para imóvel alugado/república)")
    print(f"  - Energia renovável contratada: {alt2['energia_solar_compensada_mensal_kwh'] * 12:.0f} kWh/ano ({alt2['co2_evitado_anual_kg']:.2f} kg CO2e/ano)")

    print(f"\n• {comb['descricao']}:")
    print(f"  - Nova fatura mensal: R$ {comb['custo_mensal_rs']:.2f}/mês | Economia total: R$ {comb['economia_mensal_rs']:.2f}/mês (R$ {comb['economia_anual_rs']:.2f}/ano)")
    print("=" * 88)


if __name__ == "__main__":
    exibir_relatorio_completo()
