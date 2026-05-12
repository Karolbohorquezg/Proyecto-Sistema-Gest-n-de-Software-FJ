from abc import ABC, abstractmethod
from excepciones import ValidacionError, CalculoInconsistenteError, ServicioNoDisponibleError
from entidades_base import EntidadBase

class Servicio(EntidadBase): # Hereda de EntidadBase
    """Clase abstracta base para todos los servicios ofrecidos por Software FJ."""
    def _init_(self, nombre, descripcion, costo_base):
        super()._init_() # El ID se genera automáticamente aquí
        self._nombre = self._validar_cadena(nombre, "nombre del servicio") # Validaciones
        self._descripcion = self._validar_cadena(descripcion, "descripción del servicio", puede_estar_vacia=True)
        self._costo_base = self._validar_costo(costo_base)

    # Propiedades con setters que validan (encapsulación robusta)
    @property
    def nombre(self): ...
    @nombre.setter
    def nombre(self, valor): ...
    @property
    def descripcion(self): ...
    @descripcion.setter
    def descripcion(self, valor): ...
    @property
    def costo_base(self): ...
    @costo_base.setter
    def costo_base(self, valor): ...

    # Métodos privados de validación usando ValidacionError
    def _validar_cadena(self, valor, nombre_campo, puede_estar_vacia=False): ...
    def _validar_costo(self, costo): ...

    @abstractmethod
    def calcular_costo_total(self, duracion_horas=0, **kwargs): # Método abstracto crucial
        """Método abstracto para calcular el costo total del servicio."""
        pass

    @abstractmethod
    def validar_parametros_reserva(self, **kwargs): # Método abstracto para validar antes de reservar
        """Método abstracto para validar los parámetros específicos para una reserva."""
        pass

    def describir(self): # Implementación del método abstracto de EntidadBase
        """Implementación base del método abstracto para describir el servicio."""
        return (f"Servicio ID: {self.id}, Nombre: {self.nombre}, "
                f"Descripción: {self.descripcion}, Costo Base: ${self.costo_base:.2f}")

    def _str_(self): return self.describir()

# Las clases ServicioSala, ServicioEquipo, ServicioAsesoria heredan de Servicio
# e implementan calcular_costo_total y validar_parametros_reserva con su lógica específica.
