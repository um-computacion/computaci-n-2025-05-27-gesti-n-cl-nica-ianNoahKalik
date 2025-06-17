from src.paciente import Paciente
from src.medico import Medico
from src.exepciones import RecetaInvalidaException
import datetime
class Receta:
    def __init__(self, paciente: Paciente, medico: Medico, medicamentos: list):
        if not medicamentos:
            raise RecetaInvalidaException("Debe haber al menos un medicamento en la receta.")
        self._paciente = paciente
        self._medico = medico
        self._medicamentos = medicamentos
        self._fecha = datetime.datetime.now()

    def _str_(self) -> str:
        medicamentos_str = ', '.join(self._medicamentos)
        fecha_str = self._fecha.strftime("%Y-%m-%d %H:%M:%S")
        return f"Receta (Paciente({self._paciente}), Medico({self._medico}), [{medicamentos_str}], {fecha_str})"