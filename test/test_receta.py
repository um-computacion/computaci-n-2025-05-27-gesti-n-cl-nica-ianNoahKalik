import unittest
from unittest.mock import MagicMock
from src.receta import Receta
from src.exepciones import RecetaInvalidaException

class TestReceta(unittest.TestCase):

    def setUp(self):
        self.mock_paciente = MagicMock()
        self.mock_medico = MagicMock()

    def test_creacion_valida(self):
        receta = Receta(self.mock_paciente, self.mock_medico, ["Ibuprofeno"])
        self.assertEqual(receta._medicamentos, ["Ibuprofeno"])
        self.assertIsNotNone(receta._fecha)

    def test_creacion_con_multiples_medicamentos(self):
        meds = ["Paracetamol", "Amoxicilina"]
        receta = Receta(self.mock_paciente, self.mock_medico, meds)
        self.assertEqual(receta._medicamentos, meds)

    def test_error_medicamentos_vacio(self):
        with self.assertRaises(RecetaInvalidaException):
            Receta(self.mock_paciente, self.mock_medico, [])

    def test_fecha_se_establece_automaticamente(self):
        receta = Receta(self.mock_paciente, self.mock_medico, ["Corticoide"])
        self.assertTrue(hasattr(receta, "_fecha"))

    def test_str_incluye_paciente_y_medico(self):
        self.mock_paciente.__str__.return_value = "MockPaciente"
        self.mock_medico.__str__.return_value = "MockMedico"
        receta = Receta(self.mock_paciente, self.mock_medico, ["MedicamentoA"])
        texto = receta._str_()
        self.assertIn("MockPaciente", texto)
        self.assertIn("MockMedico", texto)

    def test_str_incluye_medicamento(self):
        receta = Receta(self.mock_paciente, self.mock_medico, ["Antibiótico"])
        texto = receta._str_()
        self.assertIn("Antibiótico", texto)

    def test_str_incluye_fecha_formateada(self):
        receta = Receta(self.mock_paciente, self.mock_medico, ["X"])
        texto = receta._str_()
        self.assertRegex(texto, r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")

    def test_atributo_paciente_es_correcto(self):
        receta = Receta(self.mock_paciente, self.mock_medico, ["Y"])
        self.assertEqual(receta._paciente, self.mock_paciente)

    def test_atributo_medico_es_correcto(self):
        receta = Receta(self.mock_paciente, self.mock_medico, ["Z"])
        self.assertEqual(receta._medico, self.mock_medico)

if __name__ == "__main__":
    unittest.main()