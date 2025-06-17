from datetime import datetime
class Paciente:
    def __init__(self, dni: str, nombre: str, apellido: str, fecha_nacimiento: datetime.date):
        if not dni or not nombre or not apellido:
            raise ValueError("DNI, nombre y apellido son obligatorios")
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.fecha_nacimiento = fecha_nacimiento
        self.historia = HistoriaClinica(self)
    @property
    def edad(self) -> int:
        hoy = datetime.date.today()
        edad = hoy.year - self.fecha_nacimiento.year - (
            (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )
        return edad
    def __str__(self):
        return f"{self.nombre} {self.apellido} (DNI: {self.dni})"


class Medico:
    def __init__(self, matricula: str, nombre: str, apellido: str, especialidad: 'Especialidad'):
        if not matricula or not nombre or not apellido or not especialidad:
            raise ValueError("Todo dato de médico es obligatorio")
        self.matricula = matricula
        self.nombre = nombre
        self.apellido = apellido
        self.especialidad = especialidad
        self.turnos = []

    def __str__(self):
        return f"Dr. {self.nombre} {self.apellido} - {self.especialidad.nombre}"


class Especialidad:
    def __init__(self, nombre: str):
        if not nombre:
            raise ValueError("Nombre de especialidad no puede estar vacío")
        self.nombre = nombre

    def __str__(self):
        return self.nombre


class Turno:
    def __init__(self, paciente: Paciente, medico: Medico, fecha_hora: datetime):
        if fecha_hora < datetime.datetime.now():
            raise ValueError("No se puede reservar un turno en el pasado")
        self.paciente = paciente
        self.medico = medico
        self.fecha_hora = fecha_hora

    def __str__(self):
        return f"Turno: {self.paciente} con {self.medico} el {self.fecha_hora}"


class Receta:
    def __init__(self, paciente: Paciente, medico: Medico, medicamentos: list, fecha: datetime.date = None):
        if not medicamentos:
            raise ValueError("Debe indicar al menos un medicamento")
        self.paciente = paciente
        self.medico = medico
        self.medicamentos = medicamentos
        self.fecha = fecha or datetime.date.today()

    def __str__(self):
        meds = ", ".join(self.medicamentos)
        return f"Receta de {self.medico} a {self.paciente} ({self.fecha}): {meds}"


class HistoriaClinica:
    def __init__(self, paciente: Paciente):
        self.paciente = paciente
        self.historial = []  # puede incluir Turno y Receta

    def agregar_entry(self, entry):
        if not isinstance(entry, (Turno, Receta)):
            raise TypeError("Solo se pueden agregar Turno o Receta")
        self.historial.append(entry)

    def __iter__(self):
        return iter(self.historial)

    def __str__(self):
        lineas = [str(e) for e in self.historial]
        return f"Historia de {self.paciente}:\n" + "\n".join(lineas)


class Clinica:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.pacientes = {}
        self.medicos = {}
        self.especialidades = {}

    def add_especialidad(self, nombre: str) -> Especialidad:
        if nombre in self.especialidades:
            return self.especialidades[nombre]
        esp = Especialidad(nombre)
        self.especialidades[nombre] = esp
        return esp

    def add_paciente(self, dni: str, nombre: str, apellido: str, fecha_nac: datetime.date) -> Paciente:
        if dni in self.pacientes:
            raise ValueError("Paciente ya registrado")
        p = Paciente(dni, nombre, apellido, fecha_nac)
        self.pacientes[dni] = p
        return p

    def add_medico(self, matricula: str, nombre: str, apellido: str, especialidad: Especialidad) -> Medico:
        if matricula in self.medicos:
            raise ValueError("Matrícula de médico ya existe")
        m = Medico(matricula, nombre, apellido, especialidad)
        self.medicos[matricula] = m
        return m

    def agendar_turno(self, dni: str, matricula: str, fecha_hora: datetime) -> Turno:
        if dni not in self.pacientes or matricula not in self.medicos:
            raise ValueError("Paciente o médico no registrado")
        t = Turno(self.pacientes[dni], self.medicos[matricula], fecha_hora)
        self.medicos[matricula].turnos.append(t)
        self.pacientes[dni].historia.agregar_entry(t)
        return t

    def prescribir_receta(self, dni: str, matricula: str, medicamentos: list) -> Receta:
        if dni not in self.pacientes or matricula not in self.medicos:
            raise ValueError("Paciente o médico no registrado")
        r = Receta(self.pacientes[dni], self.medicos[matricula], medicamentos)
        self.pacientes[dni].historia.agregar_entry(r)
        return r

    def ver_historia(self, dni: str):
        if dni not in self.pacientes:
            raise ValueError("Paciente no encontrado")
        return str(self.pacientes[dni].historia)

import datetime

class CLI:
    def __init__(self, clinica):
        self.clinica = clinica

    def menu(self):
        print(f"Bienvenido a {self.clinica.nombre}")
        opciones = {
            '1': ('Agregar paciente', self.cmd_add_paciente),
            '2': ('Agregar médico', self.cmd_add_medico),
            '3': ('Agendar turno', self.cmd_agendar_turno),
            '4': ('Prescribir receta', self.cmd_prescribir_receta),
            '5': ('Ver historia clínica', self.cmd_ver_historia),
            '6': ('Salir', None),
        }
        while True:
            for k, (txt, _) in opciones.items():
                print(f"{k}. {txt}")
            opc = input("Elegí opción: ").strip()
            if opc == '6':
                print("¡Adiós!")
                break
            accion = opciones.get(opc)
            if accion:
                accion[1]()
            else:
                print("Opción inválida")

    def cmd_add_paciente(self):
        dni = input("DNI: ")
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        f = input("Fecha de nacimiento (YYYY-MM-DD): ")
        try:
            fecha = datetime.datetime.strptime(f, "%Y-%m-%d").date()
            p = self.clinica.add_paciente(dni, nombre, apellido, fecha)
            print(f" Paciente agregado: {p}")
        except ValueError:
            print(" Formato inválido. Usá el formato: YYYY-MM-DD (ej: 1999-06-18)")
        except Exception as e:
            print(" Error:", e)

    def cmd_add_medico(self):
        matricula = input("Matrícula: ")
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        especialidad = input("Especialidad: ")
        try:
            esp = self.clinica.add_especialidad(especialidad)
            m = self.clinica.add_medico(matricula, nombre, apellido, esp)
            print(f" Médico agregado: {m}")
        except Exception as e:
            print(" Error:", e)

    def cmd_agendar_turno(self):
        dni = input("DNI del paciente: ")
        mat = input("Matrícula del médico: ")
        f = input("Fecha y hora (YYYY-MM-DD HH:MM): ")
        try:
            fecha = datetime.datetime.strptime(f, "%Y-%m-%d %H:%M")
            t = self.clinica.agendar_turno(dni, mat, fecha)
            print(" Turno agendado:", t)
        except ValueError:
            print(" Formato inválido. Usá: YYYY-MM-DD HH:MM (ej: 2025-12-15 14:30)")
        except Exception as e:
            print(" Error:", e)

    def cmd_prescribir_receta(self):
        dni = input("DNI del paciente: ")
        mat = input("Matrícula del médico: ")
        meds = input("Medicamentos (separados por coma): ").split(",")
        meds = [m.strip() for m in meds if m.strip()]
        if not meds:
            print(" Debes ingresar al menos un medicamento.")
            return
        try:
            r = self.clinica.prescribir_receta(dni, mat, meds)
            print(" Receta generada:", r)
        except Exception as e:
            print(" Error:", e)

    def cmd_ver_historia(self):
        dni = input("DNI del paciente: ")
        try:
            hist = self.clinica.ver_historia(dni)
            print(hist)
        except Exception as e:
            print(" Error:", e)

