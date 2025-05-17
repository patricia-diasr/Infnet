package org.clinica.helpers;

import static org.junit.jupiter.api.Assertions.assertTrue;

// Helper para facilitar asserções personalizadas em testes.
public class AssertHelper {

    // Verifica se dois valores double são aproximadamente iguais, considerando uma margem de erro
    public static void assertAproximadamenteIgual(double esperado, double atual) {
        final double MARGEM_ERRO = 0.01;
        assertTrue(
                Math.abs(esperado - atual) <= MARGEM_ERRO,
                "Esperado aproximadamente: " + esperado + " mas foi: " + atual
        );
    }
}
