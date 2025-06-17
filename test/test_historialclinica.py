import unittest
from unittest.mock import MagicMock
from src.historialclinica import HistoriaClinica  # Asegurate de importar bien tu clase

class TestHistoriaClinica(unittest.TestCase):

    def setUp(self):
        self.mock_paciente = MagicMock()
        self.historia = HistoriaClinica(self.mock_paciente)
        self.mock_turno = MagicMock()
        self.mock_receta = MagicMock()

    def test_inicializacion_con_paciente(self):
        self.assertEqual(self.historia._paciente, self.mock_paciente)
        self.assertEqual(self.historia._turnos, [])
        self.assertEqual(self.historia._recetas, [])

    def test_agregar_turno(self):
        self.historia.agregar_turno(self.mock_turno)
        self.assertIn(self.mock_turno, self.historia._turnos)

    def test_agregar_receta(self):
        self.historia.agregar_receta(self.mock_receta)
        self.assertIn(self.mock_receta, self.historia._recetas)

    def test_obtener_turnos_devuelve_copia(self):
        self.historia.agregar_turno(self.mock_turno)
        turnos = self.historia.obtener_turnos()
        self.assertIsNot(turnos, self.historia._turnos)
        self.assertEqual(turnos, [self.mock_turno])

    def test_obtener_recetas_devuelve_copia(self):
        self.historia.agregar_receta(self.mock_receta)
        recetas = self.historia.obtener_recetas()
        self.assertIsNot(recetas, self.historia._recetas)
        self.assertEqual(recetas, [self.mock_receta])

    def test_str_sin_turnos_ni_recetas(self):
        resultado = self.historia._str_()
        self.assertIn("No hay turnos.", resultado)
        self.assertIn("No hay recetas.", resultado)

    def test_str_con_turno_y_receta(self):
        self.mock_turno.__str__.return_value = "Turno simulado"
        self.mock_receta.__str__.return_value = "Receta simulada"
        self.historia.agregar_turno(self.mock_turno)
        self.historia.agregar_receta(self.mock_receta)
        texto = self.historia._str_()
        self.assertIn("Turno simulado", texto)
        self.assertIn("Receta simulada", texto)

    def test_agregar_multiples_turnos(self):
        turno2 = MagicMock()
        self.historia.agregar_turno(self.mock_turno)
        self.historia.agregar_turno(turno2)
        self.assertEqual(len(self.historia.obtener_turnos()), 2)

    def test_agregar_multiples_recetas(self):
        receta2 = MagicMock()
        self.historia.agregar_receta(self.mock_receta)
        self.historia.agregar_receta(receta2)
        self.assertEqual(len(self.historia.obtener_recetas()), 2)

if __name__ == "__main__":
    unittest.main()