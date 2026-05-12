from excepciones import ValidacionError # Importamos nuestra excepción específica
from entidades_base import EntidadBase # Importamos nuestra clase base

import re # Para validar correos electrónicos

class Cliente(EntidadBase):
    """
    Representa a un cliente en el sistema.
    Extiende EntidadBase para tener un ID único y un método de descripción.
    """
    def _init_(self, nombre, email, telefono):
        super()._init_() # Inicializa la EntidadBase para obtener un ID ÚNICO Y AUTOMÁTICO

        # Encapsulación de datos y validación usando nuestros métodos y excepciones
        self._nombre = self._validar_nombre(nombre)
        self._email = self._validar_email(email)
        self._telefono = self._validar_telefono(telefono)

    @property
    def nombre(self):
        """Obtiene el nombre del cliente."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        """Establece el nombre del cliente con validación."""
        self._nombre = self._validar_nombre(valor)

    @property
    def email(self):
        """Obtiene el email del cliente."""
        return self._email

    @email.setter
    def email(self, valor):
        """Establece el email del cliente con validación."""
        self._email = self._validar_email(valor)

    @property
    def telefono(self):
        """Obtiene el teléfono del cliente."""
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        """Establece el teléfono del cliente con validación."""
        self._telefono = self._validar_telefono(valor)

    def _validar_nombre(self, nombre):
        """Método interno para validar el nombre."""
        if not isinstance(nombre, str) or len(nombre.strip()) < 3:
            raise ValidacionError("El nombre del cliente debe ser una cadena de al menos 3 caracteres.")
        return nombre.strip()

    def _validar_email(self, email):
        """Método interno para validar el formato del email."""
        if not isinstance(email, str) or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValidacionError("El formato del correo electrónico es inválido.")
        return email.lower()

    def _validar_telefono(self, telefono):
        """Método interno para validar el formato del teléfono."""
        # Asumimos un formato simple de dígitos, podríamos hacerlo más complejo
        if not isinstance(telefono, str) or not telefono.isdigit() or len(telefono) < 7:
            raise ValidacionError("El teléfono debe contener solo dígitos y tener al menos 7.")
        return telefono

    def describir(self):
        """Implementación del método abstracto para describir al cliente."""
        return (f"Cliente ID: {self.id}, Nombre: {self.nombre}, "
                f"Email: {self.email}, Teléfono: {self.telefono}")

    def _str_(self):
        return self.describir()
