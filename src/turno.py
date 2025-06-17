from src.paciente import Paciente
from src.medico import Medico
from src.especialidad import Especialidad
from datetime import datetime
class Turno:
    def __init__(self, paciente: Paciente, medico: Medico, fecha_hora: datetime, especialidad: str):
        if not isinstance(fecha_hora, datetime):
            raise ValueError("fecha_hora debe ser un objeto datetime")
        self._paciente = paciente
        self._medico = medico
        self._fecha_hora = fecha_hora
        self._especialidad = especialidad

    def obtener_medico(self) -> Medico:
        return self._medico

    def obtener_fecha_hora(self) -> datetime:
        return self._fecha_hora

    def _str_(self) -> str:
        fecha_str = self._fecha_hora.strftime("%Y-%m-%d %H:%M:%S")
        return f"Turno (Paciente({self._paciente}), Medico({self._medico}), {fecha_str}, {self._especialidad})"