import unittest
from datetime import datetime, timedelta
from src.clinica import Clinica, Paciente, Medico, Especialidad, Turno, Receta

class TestClinica(unittest.TestCase):

    def setUp(self):
        self.clinica = Clinica("Clínica Central")
        self.fecha_nac = datetime.strptime("1990-01-01", "%Y-%m-%d").date()
        self.especialidad = self.clinica.add_especialidad("Cardiología")
        self.paciente = self.clinica.add_paciente("123", "Ana", "Pérez", self.fecha_nac)
        self.medico = self.clinica.add_medico("M100", "Juan", "López", self.especialidad)

    def test_agregar_paciente(self):
        nuevo = self.clinica.add_paciente("456", "Luis", "Martínez", self.fecha_nac)
        self.assertIn("456", self.clinica.pacientes)
        self.assertEqual(nuevo.nombre, "Luis")

    def test_agregar_medico(self):
        nuevo = self.clinica.add_medico("M200", "Clara", "Gómez", self.especialidad)
        self.assertIn("M200", self.clinica.medicos)
        self.assertEqual(nuevo.apellido, "Gómez")

    def test_especialidad_sin_duplicados(self):
        esp2 = self.clinica.add_especialidad("Cardiología")
        self.assertIs(self.especialidad, esp2)

    def test_agregar_paciente_duplicado(self):
        with self.assertRaises(ValueError):
            self.clinica.add_paciente("123", "Otro", "Paciente", self.fecha_nac)

    def test_agendar_turno_valido(self):
        futuro = datetime.now() + timedelta(days=1)
        turno = self.clinica.agendar_turno("123", "M100", futuro)
        self.assertEqual(turno.paciente, self.paciente)
        self.assertIn(turno, self.medico.turnos)

    def test_agendar_turno_invalido(self):
        with self.assertRaises(ValueError):
            self.clinica.agendar_turno("999", "M100", datetime.now() + timedelta(days=1))

    def test_prescribir_receta_valida(self):
        receta = self.clinica.prescribir_receta("123", "M100", ["Ibuprofeno"])
        self.assertEqual(receta.medicamentos, ["Ibuprofeno"])
        self.assertIn(receta, self.paciente.historia.historial)

    def test_receta_sin_medicamentos(self):
        with self.assertRaises(ValueError):
            Receta(self.paciente, self.medico, [])

    def test_ver_historia_valida(self):
        r = self.clinica.prescribir_receta("123", "M100", ["Paracetamol"])
        texto = self.clinica.ver_historia("123")
        self.assertIn("Paracetamol", texto)

    def test_ver_historia_inexistente(self):
        with self.assertRaises(ValueError):
            self.clinica.ver_historia("999")

if __name__ == "__main__":
    unittest.main()