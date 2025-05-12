import os
import uuid
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for

from utils.sms_sender import send_whatsapp_message

app = Flask(__name__)

# Listas para almacenar los pedidos
pedidos = []
historial = []
programados = []

@app.route('/')
def user_home():
    """Página principal del usuario"""
    return render_template('user_home.html')

@app.route('/admin_login')
def admin_login():
    """Página de acceso del administrador"""
    return render_template('admin_login.html')

@app.route('/admin')
def admin():
    """Panel del administrador"""
    actualizar_cola()
    return render_template('admin.html', pedidos=pedidos, programados=programados)

@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        bebida = request.form['bebida']
        salsa = request.form['salsa']

        if not phone.startswith('+'):
            phone = f"+57{phone}"

        order_number = str(uuid.uuid4())[:8]
        order_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        pedido = {
            'order_number': order_number,
            'name': name,
            'phone': phone,
            'bebida': bebida,
            'salsa': salsa,
            'time': order_time
        }
        pedidos.append(pedido)

        print(f"Pedido recibido: {pedido}")
        return render_template('confirmation.html', name=name, order_number=order_number)
    return render_template('order.html')

@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        bebida = request.form['bebida']
        salsa = request.form['salsa']
        hora = int(request.form['hora'])
        minuto = int(request.form['minuto'])

        if not phone.startswith('+'):
            phone = f"+57{phone}"

        order_number = str(uuid.uuid4())[:8]
        order_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pickup_time = datetime.now().replace(hour=hora, minute=minuto, second=0)
        entrada_cola = pickup_time - timedelta(minutes=20)

        pedido = {
            'order_number': order_number,
            'name': name,
            'phone': phone,
            'bebida': bebida,
            'salsa': salsa,
            'time': order_time,
            'pickup_time': pickup_time.strftime("%H:%M"),
            'queue_time': entrada_cola.strftime("%H:%M")
        }
        programados.append(pedido)

        print(f"Pedido programado: {pedido}")
        return render_template('confirmation.html', name=name, order_number=order_number, programado=True)
    return render_template('schedule.html')

def actualizar_cola():
    """Actualizar la cola de pedidos programados"""
    now = datetime.now().strftime("%H:%M")
    for pedido in programados[:]:
        if pedido['queue_time'] <= now:
            pedidos.append(pedido)
            programados.remove(pedido)
            print(f"Pedido programado agregado a la cola: {pedido['order_number']}")

@app.route('/historial')
def historial_pedidos():
    """Ruta para visualizar el historial de pedidos finalizados"""
    return render_template('historial.html', historial=historial)

@app.route('/actualizar')
def actualizar():
    """Ruta para actualizar manualmente la cola"""
    actualizar_cola()
    print("Cola actualizada manualmente")
    return redirect('/admin')

@app.route('/finalizar/<int:index>', methods=['GET', 'POST'])
def finalizar(index):
    if request.method == 'POST' or request.method == 'GET':
        try:
            pedido = pedidos.pop(index)
            final_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            pedido['final_time'] = final_time
            historial.append(pedido)
            print(f"Pedido finalizado: {pedido['name']} - Orden #{pedido['order_number']}")
        except IndexError:
            print("Pedido no encontrado")
        return redirect('/admin')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
