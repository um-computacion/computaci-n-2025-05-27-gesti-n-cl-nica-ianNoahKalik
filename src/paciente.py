class Paciente:
    def __init__(self, nombre: str, dni: str, fecha_nacimiento: str):
        if not nombre or not dni or not fecha_nacimiento:
            raise ValueError("Todos los campos son requeridos.")
        self._nombre = nombre
        self._dni = dni
        self._fecha_nacimiento = fecha_nacimiento

    def obtener_dni(self) -> str:
        return self._dni

    def _str_(self) -> str:
        return f"{self._nombre}, {self._dni}, {self._fecha_nacimiento}"