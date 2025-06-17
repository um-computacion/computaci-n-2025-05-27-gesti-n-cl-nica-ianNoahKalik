from src.paciente import Paciente
from src.turno import Turno
from src.receta import Receta
class HistoriaClinica:
    def __init__(self, paciente: Paciente):
        self._paciente = paciente
        self._turnos = []
        self._recetas = []

    def agregar_turno(self, turno: Turno):
        self._turnos.append(turno)

    def agregar_receta(self, receta: Receta):
        self._recetas.append(receta)

    def obtener_turnos(self) -> list:
        return self._turnos[:]

    def obtener_recetas(self) -> list:
        return self._recetas[:]

    def _str_(self) -> str:
        turnos_str = "\n  ".join(str(turno) for turno in self._turnos) if self._turnos else "No hay turnos."
        recetas_str = "\n  ".join(str(receta) for receta in self._recetas) if self._recetas else "No hay recetas."
        return f"HistoriaClinica (Paciente({self._paciente}))\nTurnos:\n  {turnos_str}\nRecetas:\n  {recetas_str}"