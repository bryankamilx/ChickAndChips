import os
import uuid
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

from utils.sms_sender import send_whatsapp_message

app = Flask(__name__)

# Lista temporal para almacenar los pedidos
pedidos = []
historial = []  # Lista para almacenar los pedidos finalizados

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        bebida = request.form['bebida']
        salsa = request.form['salsa']

        # Normalizar el número de teléfono para WhatsApp
        if not phone.startswith('+'):
            phone = f"+57{phone}"

        # Generar número de orden único
        order_number = str(uuid.uuid4())[:8]  # Recortar a 8 caracteres
        order_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Hora del pedido

        # Guardar el pedido en la lista (sin enviar mensaje)
        pedido = {
            'order_number': order_number,
            'name': name,
            'phone': phone,
            'bebida': bebida,
            'salsa': salsa,
            'time': order_time
        }
        pedidos.append(pedido)

        print(f"Pedido recibido: {name}, {phone}, {bebida}, {salsa}, Número de orden: {order_number}")
        return render_template('confirmation.html', name=name, order_number=order_number)
    return render_template('order.html')

@app.route('/confirm', methods=['POST'])
def confirm():
    return render_template('confirmation.html')

@app.route('/admin')
def admin():
    return render_template('admin.html', pedidos=pedidos)

@app.route('/historial')
def historial_pedidos():
    return render_template('historial.html', historial=historial)

@app.route('/finalizar/<int:index>', methods=['POST'])
def finalizar(index):
    try:
        pedido = pedidos.pop(index)
        final_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Hora de finalización

        # Añadir la hora de finalización al pedido
        pedido['final_time'] = final_time
        historial.append(pedido)

        # Mensaje solo al finalizar
        message_cliente = f"Hola {pedido['name']}, tu pedido de Chick & Chips (Orden #{pedido['order_number']}) está listo para recoger."
        # send_whatsapp_message(pedido['phone'], message_cliente)

        print(f"Pedido finalizado: {pedido['name']} - Orden #{pedido['order_number']}")
    except IndexError:
        print("Pedido no encontrado")
    return redirect('/admin')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
