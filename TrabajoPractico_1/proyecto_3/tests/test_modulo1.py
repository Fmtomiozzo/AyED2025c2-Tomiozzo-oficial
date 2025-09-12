# Archivo de test para realizar pruebas unitarias del modulo1
from modules.burbuja import Burbuja
from modules.radix_sort import Radix_sort
from modules.quicksort import Quicksort
import unittest

class TestSortingAlgorithms(unittest.TestCase):
    
    def setUp(self):
        self.lista_desordenada = [5, 3, 8, 6, 2]
        self.lista_ordenada = sorted(self.lista_desordenada)

    def test_burbuja(self):
        burbuja = Burbuja(self.lista_desordenada.copy())
        resultado = burbuja.ordenar_lista()
        self.assertEqual(resultado, self.lista_ordenada)

    def test_quicksort(self):
        quicksort = Quicksort(self.lista_desordenada.copy())
        resultado = quicksort.ordenar()
        self.assertEqual(resultado, self.lista_ordenada)

    def test_radix_sort(self):
        radix = Radix_sort(self.lista_desordenada.copy())
        resultado = radix.ordenar()
        self.assertEqual(resultado, self.lista_ordenada)

    def test_sorted_function(self):
        resultado = sorted(self.lista_desordenada)
        self.assertEqual(resultado, self.lista_ordenada)

    def test_empty_list(self):
        empty_list = []
        burbuja = Burbuja(empty_list)
        quicksort = Quicksort(empty_list)
        radix = Radix_sort(empty_list)

        self.assertEqual(burbuja.ordenar_lista(), [])
        self.assertEqual(quicksort.ordenar(), [])
        self.assertEqual(radix.ordenar(), [])

    def test_single_element_list(self):
        single_element = [42]
        burbuja = Burbuja(single_element)
        quicksort = Quicksort(single_element)
        radix = Radix_sort(single_element)

        self.assertEqual(burbuja.ordenar_lista(), [42])
        self.assertEqual(quicksort.ordenar(), [42])
        self.assertEqual(radix.ordenar(), [42])

if __name__ == '__main__':
    unittest.main()