import unittest
from unittest.mock import MagicMock
from src.medico import Medico

class TestMedico(unittest.TestCase):

    def test_creacion_medico_sin_especialidades(self):
        medico = Medico("Ana", "1234")
        self.assertEqual(medico.obtener_matricula(), "1234")
        self.assertEqual(len(medico._especialidades), 0)

    def test_creacion_medico_con_especialidades(self):
        mock_esp = MagicMock()
        medico = Medico("Luis", "5678", [mock_esp])
        self.assertEqual(len(medico._especialidades), 1)

    def test_error_nombre_vacio(self):
        with self.assertRaises(ValueError):
            Medico("", "9999")

    def test_error_matricula_vacia(self):
        with self.assertRaises(ValueError):
            Medico("Nina", "")

    def test_agregar_especialidad_valida(self):
        esp = MagicMock()
        esp.obtener_especialidad.return_value = "Cardiología"
        medico = Medico("Sofía", "1111")
        medico.agregar_especialidad(esp)
        self.assertIn(esp, medico._especialidades)

    def test_agregar_especialidad_duplicada(self):
        esp = MagicMock()
        esp.obtener_especialidad.return_value = "pediatría"
        medico = Medico("Tomás", "2222", [esp])
        esp2 = MagicMock()
        esp2.obtener_especialidad.return_value = "  Pediatría "  # Espacio y mayúsculas
        with self.assertRaises(ValueError):
            medico.agregar_especialidad(esp2)

    def test_obtener_especialidad_para_dia_existente(self):
        esp = MagicMock()
        esp.verificar_dia.return_value = True
        esp.obtener_especialidad.return_value = "Neurología"
        medico = Medico("Laura", "3333", [esp])
        resultado = medico.obtener_especialidad_para_dia("lunes")
        self.assertEqual(resultado, "Neurología")

    def test_obtener_especialidad_para_dia_inexistente(self):
        esp = MagicMock()
        esp.verificar_dia.return_value = False
        medico = Medico("Raúl", "4444", [esp])
        resultado = medico.obtener_especialidad_para_dia("domingo")
        self.assertIsNone(resultado)

    def test_str_sin_especialidades(self):
        medico = Medico("Camila", "5555")
        self.assertIn("Camila", medico._str_())

    def test_str_con_especialidades(self):
        esp = MagicMock()
        esp.__str__.return_value = "Oftalmología (Días: lunes, miércoles)"
        medico = Medico("Mauro", "6666", [esp])
        texto = medico._str_()
        self.assertIn("Mauro", texto)
        self.assertIn("Oftalmología", texto)

if __name__ == "__main__":
    unittest.main()