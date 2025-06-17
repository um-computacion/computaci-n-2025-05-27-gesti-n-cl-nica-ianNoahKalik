import unittest
from src.especialidad import Especialidad

class TestEspecialidad(unittest.TestCase):

    def test_creacion_valida(self):
        esp = Especialidad("Cardiología", ["Lunes", "Miércoles"])
        self.assertEqual(esp.obtener_especialidad(), "Cardiología")

    def test_dias_en_minuscula_y_limpios(self):
        esp = Especialidad("Pediatría", [" lunes ", "MiÉrColes "])
        self.assertIn("lunes", esp._dias)
        self.assertIn("miércoles", esp._dias)

    def test_verificar_dia_existente(self):
        esp = Especialidad("Traumatología", ["viernes"])
        self.assertTrue(esp.verificar_dia(" Viernes "))

    def test_verificar_dia_inexistente(self):
        esp = Especialidad("Traumatología", ["martes"])
        self.assertFalse(esp.verificar_dia("jueves"))

    def test_str_de_especialidad(self):
        esp = Especialidad("Neurología", ["lunes", "miércoles"])
        resultado = str(esp)
        self.assertIn("Neurología", resultado)
        self.assertIn("lunes", resultado)
        self.assertIn("miércoles", resultado)

    def test_tipo_requerido(self):
        with self.assertRaises(ValueError):
            Especialidad("", ["lunes"])

    def test_dias_requeridos(self):
        with self.assertRaises(ValueError):
            Especialidad("Dermatología", [])

    def test_dia_invalido_cadena_vacia(self):
        esp = Especialidad("Oncología", ["lunes", "viernes"])
        self.assertFalse(esp.verificar_dia(""))

    def test_dias_se_normalizan(self):
        esp = Especialidad("Reumatología", [" JUEVES ", " MARTES "])
        self.assertEqual(esp._dias, ["jueves", "martes"])

    def test_obtener_especialidad_devuelve_tipo_limpio(self):
        esp = Especialidad("   Ginecología   ", ["lunes"])
        self.assertEqual(esp.obtener_especialidad(), "Ginecología")

if __name__ == "__main__":
    unittest.main()