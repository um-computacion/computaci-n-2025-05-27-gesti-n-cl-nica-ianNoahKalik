import unittest
from src.paciente import Paciente

class TestPaciente(unittest.TestCase):

    def test_creacion_paciente_valido(self):
        paciente = Paciente("Juan", "12345678", "1990-01-01")
        self.assertEqual(paciente._nombre, "Juan")
        self.assertEqual(paciente._dni, "12345678")
        self.assertEqual(paciente._fecha_nacimiento, "1990-01-01")

    def test_obtener_dni(self):
        paciente = Paciente("Ana", "87654321", "1985-12-31")
        self.assertEqual(paciente.obtener_dni(), "87654321")

    def test_error_nombre_vacio(self):
        with self.assertRaises(ValueError):
            Paciente("", "123", "2000-01-01")

    def test_error_dni_vacio(self):
        with self.assertRaises(ValueError):
            Paciente("Lucía", "", "2000-01-01")

    def test_error_fecha_vacia(self):
        with self.assertRaises(ValueError):
            Paciente("Lucía", "123", "")

    def test_str_formato_correcto(self):
        paciente = Paciente("Marta", "1111", "1995-05-05")
        esperado = "Marta, 1111, 1995-05-05"
        self.assertEqual(paciente._str_(), esperado)

    def test_dni_es_string(self):
        paciente = Paciente("Leo", "0001", "1999-12-12")
        self.assertIsInstance(paciente.obtener_dni(), str)

    def test_fecha_nacimiento_string(self):
        paciente = Paciente("Sofi", "9012", "1992-02-02")
        self.assertIsInstance(paciente._fecha_nacimiento, str)

    def test_nombre_almacenado(self):
        paciente = Paciente("Nicolás", "5555", "2001-06-06")
        self.assertEqual(paciente._nombre, "Nicolás")

    def test_instancia_correcta(self):
        paciente = Paciente("Paula", "6789", "1991-08-08")
        self.assertIsInstance(paciente, Paciente)

if __name__ == "__main__":
    unittest.main()