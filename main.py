from datetime import datetime, timedelta
from log_manager import LogManager # Nuestro LogManager
from excepciones import ValidacionError, ReservaInvalidaError, OperacionNoPermitidaError, RecursoNoEncontradoError, SistemaError, ServicioNoDisponibleError, CalculoInconsistenteError # Nuestras excepciones
from entidades_base import EntidadBase # Nuestra EntidadBase
from cliente import Cliente # Nuestra clase Cliente
from servicio import ServicioSala, ServicioEquipo, ServicioAsesoria, Servicio # Nuestras clases Servicio
from reserva import Reserva # Nuestra clase Reserva
import sys # Para salir del programa si hay un error crítico

class SistemaGestion:
    """
    Clase principal que gestiona clientes, servicios y reservas.
    Simula el comportamiento de una aplicación integral.
    """
    def _init_(self):
        self._clientes = []
        self._servicios = []
        self._reservas = []
        LogManager.info("Sistema de Gestión inicializado.")

    # --- Gestión de Clientes --- (métodos para registrar, obtener, listar)
    def registrar_cliente(self, nombre, email, telefono):
        try:
            cliente = Cliente(nombre, email, telefono) # El ID se genera automáticamente
            # Validar unicidad (ejemplo)
            if any(c.email == cliente.email for c in self._clientes):
                raise ValidacionError(f"Ya existe un cliente con el email '{email}'.")
            # ... otras validaciones ...
            self._clientes.append(cliente)
            LogManager.info(f"Cliente registrado exitosamente: {cliente.describir()}")
            return cliente
        except ValidacionError as e:
            LogManager.error(f"Fallo al registrar cliente: {e.message}")
            print(f"ERROR: No se pudo registrar el cliente: {e.message}")
            return None
        except Exception as e:
            LogManager.critical(f"Error inesperado al registrar cliente: {e}")
            print(f"ERROR CRÍTICO: {e}")
            return None
    
    def obtener_cliente_por_id(self, cliente_id): # Usa RecursoNoEncontradoError
        for cliente in self._clientes:
            if cliente.id == cliente_id:
                return cliente
        LogManager.warning(f"Cliente con ID '{cliente_id}' no encontrado.")
        raise RecursoNoEncontradoError(f"Cliente con ID '{cliente_id}' no encontrado.")
    
    def listar_clientes(self): # ...

    # --- Gestión de Servicios --- (métodos para agregar, obtener, listar)
    def agregar_servicio(self, servicio: Servicio): # ...
    def obtener_servicio_por_id(self, servicio_id): # Usa RecursoNoEncontradoError
        for servicio in self._servicios:
            if servicio.id == servicio_id:
                return servicio
        LogManager.warning(f"Servicio con ID '{servicio_id}' no encontrado.")
        raise RecursoNoEncontradoError(f"Servicio con ID '{servicio_id}' no encontrado.")
    def listar_servicios(self): # ...

    # --- Gestión de Reservas --- (métodos para crear, confirmar, cancelar, completar, listar)
    def crear_reserva(self, cliente_id, servicio_id, fecha_hora_inicio_str, duracion_horas, parametros_servicio=None):
        try:
            cliente = self.obtener_cliente_por_id(cliente_id)
            servicio = self.obtener_servicio_por_id(servicio_id)
            fecha_hora_inicio = datetime.strptime(fecha_hora_inicio_str, '%Y-%m-%d %H:%M')
            
            reserva = Reserva(cliente, servicio, fecha_hora_inicio, duracion_horas, parametros_servicio)
            self._reservas.append(reserva)
            LogManager.info(f"Reserva creada para cliente '{cliente.nombre}' y servicio '{servicio.nombre}'. ID: {reserva.id}")
            print(f"Reserva creada exitosamente (Pendiente): {reserva.id}")
            return reserva
        except (RecursoNoEncontradoError, ValidacionError, ReservaInvalidaError) as e:
            LogManager.error(f"Fallo al crear reserva: {e.message}")
            print(f"ERROR: No se pudo crear la reserva: {e.message}")
            return None
        except ValueError as e: # Error al parsear la fecha
            LogManager.error(f"Fallo al crear reserva: Formato de fecha/hora incorrecto. {e}")
            print(f"ERROR: Formato de fecha/hora incorrecto. Use YYYY-MM-DD HH:MM. {e}")
            return None
        except Exception as e:
            LogManager.critical(f"Error inesperado al crear reserva: {e}")
            print(f"ERROR CRÍTICO: {e}")
            return None
    
    def obtener_reserva_por_id(self, reserva_id): # ...
    
    def confirmar_reserva(self, reserva_id, **kwargs):
        try:
            reserva = self.obtener_reserva_por_id(reserva_id)
            reserva.confirmar(**kwargs) # Llama al método confirmar de la clase Reserva
            print(f"Reserva {reserva.id} CONFIRMADA. Costo: ${reserva.costo_total:.2f}")
            return True
        except (RecursoNoEncontradoError, OperacionNoPermitidaError, ReservaInvalidaError) as e:
            LogManager.error(f"Fallo al confirmar reserva {reserva_id}: {e.message}")
            print(f"ERROR: No se pudo confirmar la reserva: {e.message}")
            return False
        except Exception as e:
            LogManager.critical(f"Error inesperado al confirmar reserva {reserva_id}: {e}")
            print(f"ERROR CRÍTICO: {e}")
            return False

    def cancelar_reserva(self, reserva_id): # ...
    def completar_reserva(self, reserva_id): # ...
    def listar_reservas(self): # ...


def ejecutar_simulacion():
    print("\n=== INICIANDO SIMULACIÓN DE SISTEMA DE GESTIÓN SOFTWARE FJ ===\n")
    sistema = SistemaGestion()

    # --- 1. Clientes ---
    print("\n--- Registro de Clientes ---")
    cliente1 = sistema.registrar_cliente("Karol Daniela", "karol@softwarefj.com", "3001234567")
    cliente2 = sistema.registrar_cliente("Juan Perez", "juan@softwarefj.com", "3017654321")
    cliente3 = sistema.registrar_cliente("Ana Lopez", "ana@softwarefj.com", "3029876543")
    
    # Intento fallido: Cliente con email inválido (ValidacionError)
    cliente_invalido = sistema.registrar_cliente("Pedro Gomez", "pedro@.com", "3031112233")
    # Intento fallido: Cliente con nombre muy corto (ValidacionError)
    cliente_invalido2 = sistema.registrar_cliente("Pe", "pe@softwarefj.com", "3044445566")
    # Intento fallido: Cliente con email ya existente (ValidacionError personalizado en SistemaGestion)
    cliente_duplicado = sistema.registrar_cliente("Nuevo Cliente", "karol@softwarefj.com", "3050001122")
    
    sistema.listar_clientes()

    # --- 2. Servicios ---
    print("\n--- Agregando Servicios ---")
    sala1 = ServicioSala("Sala Conferencia A", "Sala equip
