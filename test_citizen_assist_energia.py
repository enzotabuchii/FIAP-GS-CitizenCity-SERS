#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testes automatizados do módulo de Soluções em Energias Renováveis e Sustentáveis (SERS)
integrado ao Citizen Assist AI.
"""

import unittest
from analise_consumo_alternativas import (
    calcular_energia_mensal_kwh,
    calcular_fatura_convencional,
    carregar_aparelhos_csv,
    comparar_alternativas_energia,
    simular_tarifa_social_tsee,
    validar_consumo_csv,
)
from citizen_assist_energia import CitizenAssistEnergia


class TestCitizenAssistEnergiaSERS(unittest.TestCase):
    def test_calculo_energia_mensal_chuveiro(self) -> None:
        # Chuveiro 5500W, 0.5h/dia, 30 dias = 82.5 kWh/mês
        kwh = calcular_energia_mensal_kwh(5500, 0.5, 30)
        self.assertAlmostEqual(kwh, 82.50, places=2)

    def test_carregar_aparelhos_csv_totais(self) -> None:
        itens = carregar_aparelhos_csv()
        self.assertEqual(len(itens), 7)
        soma_base = round(sum(i.kwh_mes_base for i in itens), 2)
        soma_efic = round(sum(i.kwh_mes_eficiente for i in itens), 2)
        self.assertAlmostEqual(soma_base, 165.00, places=2)
        self.assertAlmostEqual(soma_efic, 102.32, places=2)

    def test_csv_inconsistente_e_detectado(self) -> None:
        itens = carregar_aparelhos_csv()
        itens[0].kwh_mes_base = 999.0
        with self.assertRaises(ValueError):
            validar_consumo_csv(itens)

    def test_tarifa_social_ate_80kwh_isencao_consumo(self) -> None:
        res = simular_tarifa_social_tsee(
            consumo_kwh=75.0,
            inscrito_cadunico=True,
            renda_per_capita_salarios_minimos=0.4,
        )
        self.assertTrue(res["elegivel_tsee"])
        # Até 80 kWh paga apenas a CIP municipal estimada (R$ 15,50)
        self.assertAlmostEqual(res["fatura_com_beneficio_rs"], 15.50, places=2)
        self.assertGreater(res["economia_mensal_rs"], 70.0)

    def test_comparacao_alternativas_165kwh(self) -> None:
        comp = comparar_alternativas_energia(165.00, 102.32)
        alt1 = comp["alternativa_1_eficiencia"]
        alt2 = comp["alternativa_2_solar_assinatura"]
        self.assertAlmostEqual(alt1["reducao_mensal_kwh"], 62.68, places=2)
        self.assertGreater(alt1["economia_mensal_rs"], alt2["economia_mensal_rs"])
        self.assertEqual(alt2["investimento_inicial_rs"], 0.00)
        self.assertAlmostEqual(alt2["energia_solar_compensada_mensal_kwh"], 135.00, places=2)

    def test_busca_assistente_e_protecao_lgpd(self) -> None:
        assistente = CitizenAssistEnergia()
        self.assertTrue(assistente.contem_dados_pessoais("Meu CPF é 123.456.789-00"))
        self.assertFalse(assistente.contem_dados_pessoais("Como pedir tarifa social pelo cadunico?"))

        topico, confianca = assistente.buscar_orientacao_por_pergunta("tenho id jovem e cadunico, consigo tarifa social?")
        self.assertIsNotNone(topico)
        self.assertEqual(topico["id"], "tarifa_social")
        self.assertGreaterEqual(confianca, 0.80)


if __name__ == "__main__":
    unittest.main()
