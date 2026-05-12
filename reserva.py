from datetime import datetime, timedelta
from excepciones import ValidacionError, ReservaInvalidaError, OperacionNoPermitidaError, ServicioNoDisponibleError, CalculoInconsistenteError, SistemaError
from entidades_base import EntidadBase
from cliente import Cliente
from servicio import Servicio
from log_manager import LogManager # Importar el LogManager

class Reserva(EntidadBase): # Hereda de EntidadBase
    """Representa una reserva de un cliente para un servicio específico."""
    ESTADO_PENDIENTE = "Pendiente"
    ESTADO_CONFIRMADA = "Confirmada"
    ESTADO_CANCELADA = "Cancelada"
    ESTADO_COMPLETADA = "Completada"

    def _init_(self, cliente: Cliente, servicio: Servicio, fecha_hora_inicio: datetime, duracion_horas: float, parametros_servicio: dict = None):
        super()._init_() # ID automático
        # Validaciones de tipos de cliente y servicio
        if not isinstance(cliente, Cliente): raise ValidacionError(...)
        if not isinstance(servicio, Servicio): raise ValidacionError(...)
        # Validaciones de fecha y duración
        if not isinstance(fecha_hora_inicio, datetime): raise ValidacionError(...)
        if not isinstance(duracion_horas, (int, float)) or duracion_horas <= 0: raise ValidacionError(...)

        self._cliente = cliente
        self._servicio = servicio
        self._fecha_hora_inicio = fecha_hora_inicio
        self._duracion_horas = duracion_horas
        self._fecha_hora_fin = self._fecha_hora_inicio + timedelta(hours=self._duracion_horas)
        self._estado = self.ESTADO_PENDIENTE
        self._costo_total = 0.0
        self._parametros_servicio = parametros_servicio if parametros_servicio is not None else {}

        # Validar parámetros del servicio usando el método del servicio (polimorfismo)
        try:
            servicio.validar_parametros_reserva(duracion_horas=self._duracion_horas, **self._parametros_servicio)
            LogManager.info(f"Reserva {self.id} creada como PENDIENTE...")
        except (ValidacionError, ServicioNoDisponibleError) as e:
            LogManager.error(f"Error de validación al crear la reserva {self.id}: {e.message}")
            raise ReservaInvalidaError(f"Error en parámetros del servicio para la reserva: {e.message}") from e

    # Propiedades (getters) para todos los atributos
    @property
    def cliente(self): return self._cliente
    @property
    def servicio(self): return self._servicio
    # ... y los demás

    def confirmar(self, **kwargs):
        """Confirma la reserva, calcula el costo total y cambia el estado."""
        if self._estado != self.ESTADO_PENDIENTE:
            raise OperacionNoPermitidaError(f"No se puede confirmar una reserva en estado '{self._estado}'.")
        try:
            # Re-validación y cálculo de costo usando el servicio (polimorfismo)
            self._servicio.validar_parametros_reserva(duracion_horas=self._duracion_horas, **self._parametros_servicio)
            self._costo_total = self._servicio.calcular_costo_total(duracion_horas=self._duracion_horas, **self._parametros_servicio, **kwargs)
            if self._costo_total < 0: raise CalculoInconsistenteError(...)
            self._estado = self.ESTADO_CONFIRMADA
            LogManager.info(f"Reserva {self.id} CONFIRMADA. Costo total: {self._costo_total:.2f}.")
            return True
        except (ValidacionError, ServicioNoDisponibleError, CalculoInconsistenteError) as e:
            LogManager.error(f"Error al intentar confirmar reserva {self.id}: {e.message}")
            raise ReservaInvalidaError(f"No se pudo confirmar la reserva debido a: {e.message}") from e
        except Exception as e:
            LogManager.critical(f"Error inesperado al confirmar reserva {self.id}: {e}")
            raise SistemaError(f"Error inesperado del sistema al confirmar reserva: {e}") from e

    def cancelar(self):
        """Cancela la reserva. Solo puede ser cancelada si está Pendiente o Confirmada."""
        if self._estado not in [self.ESTADO_PENDIENTE, self.ESTADO_CONFIRMADA]:
            raise OperacionNoPermitidaError(f"No se puede cancelar una reserva en estado '{self._estado}'.")
        try:
            # Lógica para "liberar" el servicio (ej. equipo)
            if hasattr(self._servicio, 'disponible') and not self._servicio.disponible:
                self._servicio.disponible = True
            self._estado = self.ESTADO_CANCELADA
            LogManager.info(f"Reserva {self.id} CANCELADA.")
            return True
        except Exception as e:
            LogManager.critical(f"Error inesperado al cancelar reserva {self.id}: {e}")
            raise SistemaError(f"Error inesperado del sistema al cancelar reserva: {e}") from e

    def completar(self):
        """Marca la reserva como completada. Solo puede ser completada si está Confirmada."""
        if self._estado != self.ESTADO_CONFIRMADA:
            raise OperacionNoPermitidaError(f"No se puede completar una reserva en estado '{self._estado}'.")
        try:
            # Lógica para "liberar" el servicio (ej. equipo)
            if hasattr(self._servicio, 'disponible') and not self._servicio.disponible:
                self._servicio.disponible = True
            self._estado = self.ESTADO_COMPLETADA
            LogManager.info(f"Reserva {self.id} COMPLETADA...")
            return True
        except Exception as e:
            LogManager.critical(f"Error inesperado al completar reserva {self.id}: {e}")
            raise SistemaError(f"Error inesperado del sistema al completar reserva: {e}") from e

    def describir(self): # Implementa el método abstracto de EntidadBase
        """Implementación del método abstracto para describir la reserva."""
        return (f"Reserva ID: {self.id}\n"
                f"  Cliente: {self.cliente.nombre} (ID: {self.cliente.id})\n"
                f"  Servicio: {self.servicio.nombre} (ID: {self.servicio.id})\n"
                f"  Estado: {self.estado}\n"
                f"  Costo Total: ${self.costo_total:.2f}")

    def _str_(self): return self.describir()
