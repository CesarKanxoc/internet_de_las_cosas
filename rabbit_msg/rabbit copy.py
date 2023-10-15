import pika
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configura la conexión a RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='producto', durable=True)

# Configura la conexión SMTP para el correo electrónico
email_address = 'whitehokst@gmail.com'  # Cambia esto a tu dirección de correo
password = 'pzjw txjm lvdg ivwj'  # Cambia esto a tu contraseña de correo
smtp_server = 'smtp.gmail.com'
smtp_port = 587

productos_stock = 100

def enviar_correo(destinatario, asunto, mensaje):
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = destinatario
    msg['Subject'] = asunto

    body = MIMEText(mensaje, 'plain')
    msg.attach(body)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_address, password)
        server.sendmail(email_address, destinatario, msg.as_string())
        server.quit()
        print(f" [x] Correo enviado a {destinatario}: {mensaje}, Stock de productos: {productos_stock}")
    except smtplib.SMTPAuthenticationError:
        print(" [!] Error: Autenticación SMTP fallida. Verifica la contraseña del correo.")
    except smtplib.SMTPException as e:
        print(f" [!] Error al enviar el correo: {str(e)}")

def callback(ch, method, properties, body):
    global productos_stock
    mensaje = body.decode('utf-8')
    if productos_stock <= 20:
        # Cambia esto a la dirección de correo del destinatario
        destinatario = '200300581@ucaribe.edu.mx'
        asunto = "Alerta: Stock de productos se agota"
        enviar_correo(destinatario, asunto, mensaje)
    else:
        print(f" [x] Mensaje: {mensaje}, Stock de productos: {productos_stock}")
    
    # Actualiza el stock de productos
    productos_stock = int(mensaje)

channel.basic_consume(queue='producto', on_message_callback=callback, auto_ack=True)

print('Esperando notificaciones. Para salir, presiona CTRL+C')
channel.start_consuming()
