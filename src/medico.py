from src.especialidad import Especialidad
from typing import Optional

class Medico:
    def __init__(self, nombre: str, matricula: str, especialidades: list = None):
        if not nombre or not matricula:
            raise ValueError("Nombre y matrícula son requeridos.")
        self._nombre = nombre
        self._matricula = matricula
        self._especialidades = especialidades if especialidades is not None else []

    def agregar_especialidad(self, especialidad: Especialidad):
        for esp in self._especialidades:
            if esp.obtener_especialidad().strip().lower() == especialidad.obtener_especialidad().strip().lower():
                raise ValueError("La especialidad ya existe para este médico.")
        self._especialidades.append(especialidad)

    def obtener_matricula(self) -> str:
        return self._matricula

    def obtener_especialidad_para_dia(self, dia: str) -> Optional[str]:
        for esp in self._especialidades:
            if esp.verificar_dia(dia):
                return esp.obtener_especialidad()
        return None

    def _str_(self) -> str:
        esp_str_list = [str(esp) for esp in self._especialidades]
        return f"{self._nombre}, {self._matricula}, [{', '.join(esp_str_list)}]"