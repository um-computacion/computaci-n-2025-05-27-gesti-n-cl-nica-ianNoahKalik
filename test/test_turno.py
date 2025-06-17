import unittest
from unittest.mock import MagicMock
from datetime import datetime
from src.turno import Turno

class TestTurno(unittest.TestCase):

    def setUp(self):
        self.paciente = MagicMock()
        self.medico = MagicMock()
        self.fecha = datetime(2025, 12, 25, 10, 0, 0)
        self.especialidad = "Cardiología"

    def test_creacion_turno_valido(self):
        turno = Turno(self.paciente, self.medico, self.fecha, self.especialidad)
        self.assertEqual(turno._paciente, self.paciente)
        self.assertEqual(turno._medico, self.medico)
        self.assertEqual(turno._fecha_hora, self.fecha)
        self.assertEqual(turno._especialidad, "Cardiología")

    def test_error_fecha_hora_invalida(self):
        with self.assertRaises(ValueError):
            Turno(self.paciente, self.medico, "2025-12-25", self.especialidad)

    def test_obtener_medico(self):
        turno = Turno(self.paciente, self.medico, self.fecha, self.especialidad)
        self.assertIs(turno.obtener_medico(), self.medico)

    def test_obtener_fecha_hora(self):
        turno = Turno(self.paciente, self.medico, self.fecha, self.especialidad)
        self.assertEqual(turno.obtener_fecha_hora(), self.fecha)

    def test_especialidad_correcta(self):
        turno = Turno(self.paciente, self.medico, self.fecha, "Pediatría")
        self.assertEqual(turno._especialidad, "Pediatría")

    def test_str_formato_correcto(self):
        self.paciente.__str__.return_value = "MockPaciente"
        self.medico.__str__.return_value = "MockMedico"
        turno = Turno(self.paciente, self.medico, self.fecha, self.especialidad)
        texto = turno._str_()
        self.assertIn("MockPaciente", texto)
        self.assertIn("MockMedico", texto)
        self.assertIn("2025-12-25 10:00:00", texto)
        self.assertIn("Cardiología", texto)

    def test_str_salida_es_string(self):
        turno = Turno(self.paciente, self.medico, self.fecha, self.especialidad)
        resultado = turno._str_()
        self.assertIsInstance(resultado, str)

    def test_turno_fecha_es_datetime(self):
        turno = Turno(self.paciente, self.medico, self.fecha, self.especialidad)
        self.assertIsInstance(turno.obtener_fecha_hora(), datetime)

    def test_turno_medico_es_mock(self):
        turno = Turno(self.paciente, self.medico, self.fecha, self.especialidad)
        self.assertEqual(turno.obtener_medico(), self.medico)

    def test_turno_acepta_fechas_futuras(self):
        futura = datetime(2050, 1, 1, 8, 30)
        turno = Turno(self.paciente, self.medico, futura, self.especialidad)
        self.assertEqual(turno.obtener_fecha_hora(), futura)

if __name__ == "__main__":
    unittest.main()