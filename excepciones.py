class SistemaError(Exception):
    """Excepción base para todos los errores personalizados del sistema."""
    def _init_(self, message="Ha ocurrido un error en el sistema."):
        self.message = message
        super()._init_(self.message)

class ValidacionError(SistemaError):
    """Excepción para errores de validación de datos."""
    def _init_(self, message="Error de validación de datos o formato incorrecto."):
        super()._init_(message)

class RecursoNoEncontradoError(SistemaError):
    """Excepción cuando un recurso (cliente, servicio) no se encuentra."""
    def _init_(self, message="El recurso solicitado no fue encontrado."):
        super()._init_(message)

class OperacionNoPermitidaError(SistemaError):
    """Excepción para operaciones que no están permitidas en el estado actual."""
    def _init_(self, message="Operación no permitida en este momento."):
        super()._init_(message)

class ReservaInvalidaError(SistemaError):
    """Excepción para intentos de reserva inválidos."""
    def _init_(self, message="La reserva es inválida o los parámetros son incorrectos."):
        super()._init_(message)

class ServicioNoDisponibleError(SistemaError):
    """Excepción cuando un servicio no está disponible o ya está reservado."""
    def _init_(self, message="El servicio solicitado no está disponible."):
        super()._init_(message)

class CalculoInconsistenteError(SistemaError):
    """Excepción para errores en cálculos (costos, duraciones, etc.)."""
    def _init_(self, message="Error en cálculo, resultado inconsistente."):
        super()._init_(message)
