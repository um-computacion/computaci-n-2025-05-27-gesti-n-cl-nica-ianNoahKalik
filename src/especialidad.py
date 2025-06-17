class Especialidad:
    def __init__(self, tipo: str, dias: list):
        if not tipo:
            raise ValueError("Tipo es requerido")
        if not dias:
            raise ValueError("Días son requeridos")
        self._tipo = tipo.strip()
        # Se eliminan espacios extras y se normaliza a minúsculas
        self._dias = [d.strip().lower() for d in dias]

    def obtener_especialidad(self) -> str:
        return self._tipo

    def verificar_dia(self, dia: str) -> bool:
        return dia.strip().lower() in self._dias

    def __str__(self) -> str:
        dias_formatted = ", ".join(self._dias)
        return f"{self._tipo} (Días: {dias_formatted})"