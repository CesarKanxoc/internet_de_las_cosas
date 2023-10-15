from flask import Flask, jsonify, make_response
from flask_socketio import SocketIO, send
import pika

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'mysecretkey'
    return app

app = create_app()
socketio = SocketIO(app)

# Configurar encabezados para deshabilitar el almacenamiento en caché
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# Configura la conexión a RabbitMQ para publicar mensajes
rabbit_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
rabbit_channel = rabbit_connection.channel()
rabbit_channel.queue_declare(queue='notificaciones', durable=True)

@app.route('/productos_stock', methods=['GET'])
def obtener_productos():
    # Realiza tu lógica para obtener el stock de productos
    stock_actual = obtener_stock_de_productos()  # Asegúrate de implementar esta función
    
    if stock_actual is not None:
        if stock_actual <= 20:
            # Publica un mensaje en la cola si el stock es igual o menor a 20
            mensaje = f"Alerta: Stock de productos es bajo ({stock_actual})"
            rabbit_channel.basic_publish(exchange='', routing_key='notificaciones', body=mensaje)

        response = jsonify({'producto_stock': stock_actual})
        return make_response(response)
    else:
        return 'No se pudo obtener el stock de productos', 500

def obtener_stock_de_productos():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='producto', durable=True)

        # Declara una variable para el stock inicial (puede ser un valor fijo o lo que desees)
        stock_actual = 100

        # Consumir los mensajes de la cola y actualizar el stock
        method_frame, header_frame, body = channel.basic_get(queue='producto')
        while method_frame:
            mensaje = int(body.decode('utf-8'))
            stock_actual = mensaje
            print(f"Stock actualizado: {stock_actual}")
            method_frame, header_frame, body = channel.basic_get(queue='producto')

        return stock_actual
    except Exception as e:
        print(f"Error al obtener el stock: {str(e)}")
        return None  # Maneja el error de la forma que consideres apropiada

@socketio.on('connect')
def handle_connect():
    print('Cliente conectado')
    # Envía un mensaje inicial al cliente
    send('Conectado al servidor de actualizaciones')

if __name__ == '__main__':
    socketio.run(app, host='192.168.1.74', port=8080, allow_unsafe_werkzeug=True)
