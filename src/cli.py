import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from src.clinica import Clinica
from src.paciente import Paciente
from src.medico import Medico
from src.especialidad import Especialidad
from src.turno import Turno
from src.receta import Receta
from datetime import datetime
class CLI:
    def __init__(self):
        self.clinica = Clinica("Clínica Central")    

    def mostrar_menu(self):
        menu = """
Menú Clínica
1) Agregar paciente
2) Agregar médico
3) Agendar turno
4) Agregar especialidad a un médico
5) Emitir receta
6) Ver historia clínica
7) Ver todos los turnos
8) Ver todos los pacientes
9) Ver todos los médicos
0) Salir
        """
        print(menu)

    def run(self):
        while True:
            self.mostrar_menu()
            opcion = input("Selecciona una opción: ")
            if opcion == "1":
                self.agregar_paciente()
            elif opcion == "2":
                self.agregar_medico()
            elif opcion == "3":
                self.agendar_turno()
            elif opcion == "4":
                self.agregar_especialidad()
            elif opcion == "5":
                self.emitir_receta()
            elif opcion == "6":
                self.ver_historia_clinica()
            elif opcion == "7":
                self.ver_turnos()
            elif opcion == "8":
                self.ver_pacientes()
            elif opcion == "9":
                self.ver_medicos()
            elif opcion == "0":
                print("Saliendo del sistema de la clínica...")
                break
            else:
                print("Opción no válida.")

    def agregar_paciente(self):
        try:
            nombre = input("Nombre del paciente: ")
            dni = input("DNI del paciente: ")
            fecha_nacimiento = input("Fecha de nacimiento (dd/mm/aaaa): ")
            paciente = Paciente(nombre, dni, fecha_nacimiento)
            self.clinica.agregar_paciente(paciente)
            print("Paciente agregado exitosamente.")
        except Exception as e:
            print(f"Error al agregar paciente: {e}")

    def agregar_medico(self):
        try:
            nombre = input("Nombre del médico: ")
            matricula = input("Matrícula del médico: ")
            medico = Medico(nombre, matricula)
            agregar = input("¿Desea agregar especialidades ahora? (s/n): ").lower()
            while agregar == "s":
                tipo = input("Tipo de especialidad: ")
                dias_str = input("Días de atención (separados por coma, ej: lunes, miercoles, viernes): ")
                dias = [dia.strip() for dia in dias_str.split(",")]
                especialidad = Especialidad(tipo, dias)
                try:
                    medico.agregar_especialidad(especialidad)
                except Exception as e:
                    print(f"Error al agregar la especialidad: {e}")
                agregar = input("¿Desea agregar otra especialidad? (s/n): ").lower()
            self.clinica.agregar_medico(medico)
            print("Médico agregado exitosamente.")
        except Exception as e:
            print(f"Error al agregar médico: {e}")

    def agendar_turno(self):
        try:
            dni = input("DNI del paciente: ")
            matricula = input("Matrícula del médico: ")
            especialidad = input("Especialidad requerida: ")
            fecha_str = input("Fecha y hora del turno (YYYY-MM-DD HH:MM): ")
            fecha_hora = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M")
            turno = self.clinica.agendar_turno(dni, matricula, especialidad, fecha_hora)
            print("Turno agendado exitosamente:")
            print(turno)
        except Exception as e:
            print(f"Error al agendar turno: {e}")

    def agregar_especialidad(self):
        try:
            matricula = input("Matrícula del médico: ")
            medico = self.clinica.obtener_medico_por_matricula(matricula)
            tipo = input("Tipo de especialidad a agregar: ")
            dias_str = input("Días de atención (separados por coma): ")
            dias = [dia.strip() for dia in dias_str.split(",")]
            especialidad = Especialidad(tipo, dias)
            medico.agregar_especialidad(especialidad)
            print("Especialidad agregada exitosamente al médico.")
        except Exception as e:
            print(f"Error al agregar especialidad: {e}")

    def emitir_receta(self):
        try:
            dni = input("DNI del paciente: ")
            matricula = input("Matrícula del médico: ")
            meds_str = input("Medicamentos recetados (separados por coma): ")
            medicamentos = [med.strip() for med in meds_str.split(",") if med.strip()]
            receta = self.clinica.emitir_receta(dni, matricula, medicamentos)
            print("Receta emitida exitosamente:")
            print(receta)
        except Exception as e:
            print(f"Error al emitir receta: {e}")

    def ver_historia_clinica(self):
        try:
            dni = input("DNI del paciente: ")
            historia = self.clinica.obtener_historia_clinica_por_dni(dni)
            print(historia)
        except Exception as e:
            print(f"Error al obtener historia clínica: {e}")

    def ver_turnos(self):
        try:
            turnos = self.clinica.obtener_turnos()
            if turnos:
                for turno in turnos:
                    print(turno)
            else:
                print("No hay turnos agendados.")
        except Exception as e:
            print(f"Error al obtener turnos: {e}")

    def ver_pacientes(self):
        try:
            pacientes = self.clinica.obtener_pacientes()
            if pacientes:
                for paciente in pacientes:
                    print(paciente)
            else:
                print("No hay pacientes registrados.")
        except Exception as e:
            print(f"Error al obtener pacientes: {e}")

    def ver_medicos(self):
        try:
            medicos = self.clinica.obtener_medicos()
            if medicos:
                for medico in medicos:
                    print(medico)
            else:
                print("No hay médicos registrados.")
        except Exception as e:
            print(f"Error al obtener médicos: {e}")
if __name__ == "__main__":
    cli = CLI()
    cli.run()