from flask import Flask, jsonify, make_response
from flask_socketio import SocketIO
import pika
from flask_cors import CORS
import pyodbc

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'mysecretkey'
    return app

app = create_app()
socketio = SocketIO(app)
CORS(app)

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

def obtener_stock_inicial_desde_base_de_datos():
    direccion_servidor = 'LAPTOP-AQP40DPT\SQLEXPRESS,1433'
    nombre_bd = 'Almacen'
    nombre_usuario = 'admin'
    password = 'admin12345678'
    try:
        conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
                              direccion_servidor+';DATABASE='+nombre_bd+';UID='+nombre_usuario+';PWD=' + password)
        # OK! conexión exitosa
    except Exception as e:
        # Atrapar error
        print("Ocurrió un error al conectar a SQL Server: ", e)
    

    try:
        with conexion.cursor() as cursor:
            # En este caso no necesitamos limpiar ningún dato
            cursor.execute("SELECT Productos_id, Productos_nombre, Productos_Stock FROM Almacen.Productos;")

            # Con fetchall traemos todas las filas
            Productos = cursor.fetchall()

            # Recorrer e imprimir
            for Producto in Productos:
                productos_stock = Producto[2]
                
    except Exception as e:
            print("Ocurrió un error al consultar: ", e)
    finally:
        conexion.close()
    
    
    return productos_stock 

def obtener_stock_de_productos():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='producto', durable=True)

        # Declara una variable para el stock inicial (puede ser un valor fijo o lo que desees)
        stock_actual = obtener_stock_inicial_desde_base_de_datos()

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

@socketio.on('update_stock')
def handle_stock_update(data):
    # Aquí actualiza el stock y envía los cambios a los clientes
    # Puedes emitir un evento que lleve el nuevo stock a los clientes
    new_stock = obtener_stock_de_productos()
    socketio.emit('stock_updated', new_stock)

@app.route('/actualizar_stock', methods=['POST'])
def actualizar_stock():
    # Lógica para actualizar el stock
    nuevo_stock = obtener_stock_de_productos()
    
    # Emite un evento para notificar a los clientes React
    socketio.emit('stock_updated', nuevo_stock)
    
    return jsonify({'success': True})

if __name__ == '__main__':
    socketio.run(app, host='192.168.1.74', port=8080, allow_unsafe_werkzeug=True)
