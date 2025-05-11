# utils/sms_sender.py
import pywhatkit
from datetime import datetime
import time

def send_whatsapp_message(to, message):
    try:
        # Obtener la hora actual
        now = datetime.now()
        # Asegurarnos de que el envío sea al menos 1 minuto después
        hour = now.hour
        minute = now.minute + 2  # Aumentamos el tiempo en 2 minutos

        # Ajustar los minutos si se pasan de 59
        if minute >= 60:
            minute = minute % 60
            hour = (hour + 1) % 24

        print(f"Enviando mensaje a {to} a las {hour}:{minute}")

        # Enviar el mensaje por WhatsApp
        pywhatkit.sendwhatmsg(to, message, hour, minute)
        print(f"Mensaje enviado a {to}")
        
        # Esperar unos segundos para que el navegador procese el envío
        time.sleep(10)
    except Exception as e:
        print(f"Error al enviar el mensaje: {e}")
