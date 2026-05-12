import datetime

class LogManager:
    """
    Gestiona el registro de eventos y errores en un archivo de log.
    Utiliza un enfoque simplificado para escribir mensajes con diferentes niveles
    (INFO, WARNING, ERROR, CRITICAL) en un archivo 'events.log'.
    Maneja excepciones internas si no puede escribir en el archivo de log.
    """
    _log_file = "events.log" # Nombre del archivo donde se guardarán los logs

    @staticmethod
    def _write_log(level, message):
        """
        Método interno estático para escribir un mensaje en el archivo de log.
        Añade un timestamp, el nivel del mensaje y el mensaje en sí.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        try:
            # Abre el archivo en modo "append" ('a') para añadir contenido al final,
            # 'encoding="utf-8"' para manejar caracteres especiales.
            with open(LogManager._log_file, "a", encoding="utf-8") as f:
                f.write(log_entry)
        except IOError as e:
            # Si hay un error al escribir en el archivo, lo imprime en consola.
            # Este es un caso de manejo de error interno del LogManager.
            print(f"ERROR CRÍTICO del LogManager: No se pudo escribir en el archivo de log '{LogManager._log_file}': {e}")

    @staticmethod
    def info(message):
        """
        Registra un mensaje informativo.
        Se usa para eventos normales del sistema o información de seguimiento.
        """
        LogManager._write_log("INFO", message)

    @staticmethod
    def warning(message):
        """
        Registra un mensaje de advertencia.
        Indica una situación que podría ser un problema en el futuro o un comportamiento inesperado.
        """
        LogManager._write_log("WARNING", message)

    @staticmethod
    def error(message):
        """
        Registra un mensaje de error.
        Indica que una operación no pudo completarse debido a un problema.
        """
        LogManager._write_log("ERROR", message)

    @staticmethod
    def critical(message):
        """
        Registra un mensaje de error crítico.
        Indica un error grave que podría llevar a la inestabilidad del sistema o un fallo.
        """
        LogManager._write_log("CRITICAL", message)


# Ejemplo
if _name_ == "_main_":
    print(f"--- Probando LogManager. Los logs se escribirán en '{LogManager._log_file}' ---")
    LogManager.info("Sistema de logging iniciado correctamente para la prueba.")
    LogManager.warning("Se detectó un uso inusual de recursos (solo una prueba).")
    try:
        resultado = 10 / 0
    except ZeroDivisionError as e:
        LogManager.error(f"Se intentó dividir por cero en la prueba: {e}")
    LogManager.critical("Fallo crítico simulado: El disco duro virtual no responde.")
    print(f"--- Prueba de LogManager finalizada. Revisa el archivo '{LogManager._log_file}' ---")
