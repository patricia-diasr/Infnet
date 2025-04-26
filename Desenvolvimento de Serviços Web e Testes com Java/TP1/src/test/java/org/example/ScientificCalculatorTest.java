package com.example;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.example.ScientificCalculator;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

public class ScientificCalculatorTest {

    private ScientificCalculator calculadora;

    // Setup => prepara o cenário do teste
    @BeforeEach
    public void setUp() {
        calculadora = new ScientificCalculator();
    }

    // ------------------------
    // Testes de Operações Básicas
    // ------------------------

    @Test
    public void testAdd_TwoPositiveNumbers_ReturnsCorrectSum() {
        // Execution => executa o método a ser testado
        double resultado = calculadora.add(5, 3);

        // Assertion => verifica se o resultado é o esperado
        assertEquals(8, resultado);
    }

    @Test
    public void testSubtract_TwoPositiveNumbers_ReturnsCorrectDifference() {
        // Execution => executa o método a ser testado
        double resultado = calculadora.subtract(8, 3);

        // Assertion => verifica se o resultado é o esperado
        assertEquals(5, resultado);

        // Teardown => não aplicável, não há recursos externos para liberar
    }

    @Test
    public void testMultiply_TwoNumbers_ReturnsCorrectProduct() {
        // Execution => executa o método a ser testado
        double resultado = calculadora.multiply(4, 5);

        // Assertion => verifica se o resultado é o esperado
        assertEquals(20, resultado);
    }

    @Test
    public void testDivide_DivisorIsZero_ThrowsIllegalArgumentException() {
        // Assertion + Execution => executa método a ser testado ao mesmo tempo que verifica se retorno é o esperado
        assertThrows(IllegalArgumentException.class, () -> {
            calculadora.divide(5, 0);
        });
    }

    // ------------------------
    // Testes de Funções Trigonométricas
    // ------------------------

    @Test
    public void testSin_ReturnsCorrectSine() {
        // Execution => executa o método a ser testado
        double resultado = calculadora.sin(90);

        // Assertion => verifica se o resultado é o esperado
        assertEquals(1, resultado, 0.0001);
    }

    @Test
    public void testCos_ReturnsCorrectCosine() {
        // Execution => executa o método a ser testado
        double resultado = calculadora.cos(60);

        // Assertion => verifica se o resultado é o esperado
        assertEquals(0.5, resultado, 0.0001);
    }

    // ------------------------
    // Testes de Potência e Raiz
    // ------------------------

    @Test
    public void testPower_ReturnsCorrectResult() {
        // Execution => executa o método a ser testado
        double resultado = calculadora.power(2, 3);

        // Assertion => verifica se o resultado é o esperado
        assertEquals(8, resultado);
    }

    @Test
    public void testSquareRoot_PositiveNumber_ReturnsCorrectRoot() {
        // Execution
        double resultado = calculadora.squareRoot(25);

        // Assertion
        assertEquals(5, resultado);
    }

    @Test
    public void testSquareRoot_NegativeNumber_ThrowsIllegalArgumentException() {
        // Assertion + Execution
        assertThrows(IllegalArgumentException.class, () -> {
            calculadora.squareRoot(-9);
        });
    }

    // ------------------------
    // Testes de Funções Logarítmicas
    // ------------------------

    @Test
    public void testLog_PositiveNumber_ReturnsCorrectLogarithm() {
        // Execution => executa o método a ser testado
        double resultado = calculadora.log(1);

        // Assertion => verifica se o resultado é o esperado
        assertEquals(0, resultado, 0.0001);
    }
}
