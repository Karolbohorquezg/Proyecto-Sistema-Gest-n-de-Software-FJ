from abc import ABC, abstractmethod
import uuid # Módulo para generar IDs únicos

class EntidadBase(ABC):
    """
    Clase abstracta base para todas las entidades del sistema.
    Define un identificador único (ID) para cada entidad automáticamente.
    """
    def _init_(self):
        # Genera un ID único universal (UUID) para cada entidad automáticamente
        self._id = str(uuid.uuid4())

    @property
    def id(self):
        """Propiedad para obtener el ID de la entidad."""
        return self._id

    @abstractmethod
    def describir(self):
        """
        Método abstracto que las clases derivadas deben implementar
        para describir la entidad.
        """
        pass

    def _str_(self):
        """Representación en cadena de la entidad, útil para imprimir."""
        return f"Entidad ID: {self.id}"

    def _eq_(self, other):
        """Define la igualdad entre dos entidades basada en su ID."""
        if not isinstance(other, EntidadBase): # Si no es del mismo tipo, no son iguales
            return NotImplemented
        return self.id == other.id # Dos entidades son iguales si tienen el mismo ID

    def _hash_(self):
        """Define el hash de la entidad basado en su ID para uso en conjuntos y diccionarios."""
        return hash(self.id)
