import unittest
from unittest.mock import patch, MagicMock
from src.cli import CLI
from datetime import datetime
from src.paciente import Paciente
from src.medico import Medico
from src.especialidad import Especialidad
from src.turno import Turno
from src.receta import Receta
from src.exepciones import RecetaInvalidaException


class TestCLI(unittest.TestCase):

    def setUp(self):
        self.cli = CLI()
        self.cli.clinica = MagicMock()

    @patch('builtins.input', side_effect=["Juan", "12345678", "01/01/1990"])
    def test_agregar_paciente(self, mock_input):
        self.cli.agregar_paciente()
        self.cli.clinica.agregar_paciente.assert_called_once()

    @patch('builtins.input', side_effect=["Dr. House", "M123", "n"])
    def test_agregar_medico_sin_especialidades(self, mock_input):
        self.cli.agregar_medico()
        self.cli.clinica.agregar_medico.assert_called_once()

    @patch('builtins.input', side_effect=["12345678", "M123", "Cardiología", "2025-06-20 14:30"])
    def test_agendar_turno(self, mock_input):
        self.cli.clinica.agendar_turno.return_value = "Turno creado"
        self.cli.agendar_turno()
        self.cli.clinica.agendar_turno.assert_called_once()

    @patch('builtins.input', side_effect=["M123", "Cardiología", "lunes, martes"])
    def test_agregar_especialidad_a_medico(self, mock_input):
        medico_mock = MagicMock()
        self.cli.clinica.obtener_medico_por_matricula.return_value = medico_mock
        self.cli.agregar_especialidad()
        medico_mock.agregar_especialidad.assert_called_once()

    @patch('builtins.input', side_effect=["12345678", "M123", "Paracetamol, Ibuprofeno"])
    def test_emitir_receta(self, mock_input):
        receta_mock = Receta("Dr. X", "12345678", ["Paracetamol", "Ibuprofeno"])
        self.cli.clinica.emitir_receta.return_value = receta_mock
        self.cli.emitir_receta()
        self.cli.clinica.emitir_receta.assert_called_once()

    @patch('builtins.input', side_effect=["12345678"])
    def test_ver_historia_clinica(self, mock_input):
        self.cli.clinica.obtener_historia_clinica_por_dni.return_value = "Historial clínico..."
        self.cli.ver_historia_clinica()
        self.cli.clinica.obtener_historia_clinica_por_dni.assert_called_once()

    def test_ver_turnos_con_turnos(self):
        self.cli.clinica.obtener_turnos.return_value = ["Turno 1", "Turno 2"]
        self.cli.ver_turnos()
        self.cli.clinica.obtener_turnos.assert_called_once()

    def test_ver_turnos_sin_turnos(self):
        self.cli.clinica.obtener_turnos.return_value = []
        self.cli.ver_turnos()
        self.cli.clinica.obtener_turnos.assert_called_once()

    def test_ver_pacientes_con_pacientes(self):
        self.cli.clinica.obtener_pacientes.return_value = [Paciente("Juan", "12345678", "01/01/1990")]
        self.cli.ver_pacientes()
        self.cli.clinica.obtener_pacientes.assert_called_once()

    def test_ver_medicos_con_medicos(self):
        self.cli.clinica.obtener_medicos.return_value = [Medico("Dr. X", "M123")]
        self.cli.ver_medicos()
        self.cli.clinica.obtener_medicos.assert_called_once()

    # ---- TESTS ADICIONALES (CORREGIDOS) ----

    @patch('builtins.input', side_effect=["Juan", "12345678", "01/01/1990"])
    def test_agregar_paciente_error(self, mock_input):
        self.cli.clinica.agregar_paciente.side_effect = Exception("Error simulado")
        with patch('builtins.print') as mock_print:
            self.cli.agregar_paciente()

        # Mostrar todos los prints por si vuelve a fallar
        print("PRINTS LLAMADOS EN EL TEST:")
        for call in mock_print.call_args_list:
            print(f" - {call}")

        # Chequear que al menos uno de los prints contiene la frase buscada
        encontrado = any("Error al agregar paciente" in str(call) for call in mock_print.call_args_list)
        self.assertTrue(encontrado)


    @patch('builtins.input', side_effect=["Dr. Falso", "M000", "s", "Cardiología", "lunes", "n"])
    def test_agregar_medico_con_especialidad(self, mock_input):
        self.cli.agregar_medico()
        self.cli.clinica.agregar_medico.assert_called_once()

    @patch('builtins.input', side_effect=["12345678", "M123", "Cardiología", "fecha invalida"])
    def test_agendar_turno_fecha_invalida(self, mock_input):
        with patch('builtins.print') as mock_print:
            self.cli.agendar_turno()
            self.assertTrue(any("Error al agendar turno" in str(c[0][0]) for c in mock_print.call_args_list))

    @patch('builtins.input', side_effect=["M404", "Cardiología", "lunes, martes"])
    def test_agregar_especialidad_error_medico_inexistente(self, mock_input):
        self.cli.clinica.obtener_medico_por_matricula.side_effect = Exception("Médico no encontrado")
        with patch('builtins.print') as mock_print:
            self.cli.agregar_especialidad()
            self.assertTrue(any("Error al agregar especialidad" in str(c[0][0]) for c in mock_print.call_args_list))

    @patch('builtins.input', side_effect=["12345678", "M123", ""])
    def test_emitir_receta_sin_medicamentos(self, mock_input):
        self.cli.clinica.emitir_receta.side_effect = RecetaInvalidaException("Debe haber al menos un medicamento")
        with patch('builtins.print') as mock_print:
            self.cli.emitir_receta()
            self.assertTrue(any("Error al emitir receta" in str(c[0][0]) for c in mock_print.call_args_list))

    @patch('builtins.input', side_effect=["99999999"])
    def test_ver_historia_clinica_error(self, mock_input):
        self.cli.clinica.obtener_historia_clinica_por_dni.side_effect = Exception("Paciente no encontrado")
        with patch('builtins.print') as mock_print:
            self.cli.ver_historia_clinica()
            self.assertTrue(any("Error al obtener historia clínica" in str(c[0][0]) for c in mock_print.call_args_list))

    @patch('builtins.input', side_effect=["99", "0"])
    def test_run_opcion_invalida(self, mock_input):
        with patch('builtins.print') as mock_print:
            self.cli.run()
            self.assertTrue(any("Opción no válida" in str(c[0][0]) for c in mock_print.call_args_list))

    @patch('builtins.input', side_effect=["0"])
    def test_run_salir(self, mock_input):
        with patch('builtins.print') as mock_print:
            self.cli.run()
            self.assertTrue(any("Saliendo del sistema de la clínica" in str(c[0][0]) for c in mock_print.call_args_list))


if __name__ == '__main__':
    unittest.main()
