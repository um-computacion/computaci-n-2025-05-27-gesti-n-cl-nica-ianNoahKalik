import unittest
from datetime import datetime, timedelta, date
from src.clinica import Clinica, Paciente, Medico, Especialidad, Turno, Receta, HistoriaClinica

class TestClinica(unittest.TestCase):

    def setUp(self):
        self.clinica = Clinica("Clínica Central")
        self.fecha_nac = datetime.strptime("1990-01-01", "%Y-%m-%d").date()
        self.especialidad = self.clinica.add_especialidad("Cardiología")
        self.paciente = self.clinica.add_paciente("123", "Ana", "Pérez", self.fecha_nac)
        self.medico = self.clinica.add_medico("M100", "Juan", "López", self.especialidad)

    # TUS 10 TESTS
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

    # 10 TESTS NUEVOS
    def test_turno_en_el_pasado(self):
        pasado = datetime.now() - timedelta(days=1)
        with self.assertRaises(ValueError):
            Turno(self.paciente, self.medico, pasado)

    def test_medico_sin_datos(self):
        with self.assertRaises(ValueError):
            Medico("", "", "", self.especialidad)

    def test_paciente_sin_datos(self):
        with self.assertRaises(ValueError):
            Paciente("", "", "", self.fecha_nac)

    def test_especialidad_vacia(self):
        with self.assertRaises(ValueError):
            Especialidad("")

    def test_agregar_entry_invalido_a_historia(self):
        with self.assertRaises(TypeError):
            self.paciente.historia.agregar_entry("no es válido")

    def test_historia_clinica_iterable(self):
        receta = Receta(self.paciente, self.medico, ["Aspirina"])
        self.paciente.historia.agregar_entry(receta)
        self.assertIn(receta, list(self.paciente.historia))

    def test_add_medico_duplicado(self):
        with self.assertRaises(ValueError):
            self.clinica.add_medico("M100", "Juan", "López", self.especialidad)

    def test_receta_str(self):
        receta = Receta(self.paciente, self.medico, ["Amoxicilina"])
        texto = str(receta)
        self.assertIn("Amoxicilina", texto)
        self.assertIn(self.paciente.nombre, texto)

    def test_turno_str(self):
        fecha = datetime.now() + timedelta(days=2)
        turno = Turno(self.paciente, self.medico, fecha)
        texto = str(turno)
        self.assertIn(self.paciente.nombre, texto)
        self.assertIn("Turno", texto)

    def test_edad_paciente(self):
        hoy = date.today()
        esperado = hoy.year - self.fecha_nac.year - ((hoy.month, hoy.day) < (self.fecha_nac.month, self.fecha_nac.day))
        self.assertEqual(self.paciente.edad, esperado)

if __name__ == "__main__":
    unittest.main()
