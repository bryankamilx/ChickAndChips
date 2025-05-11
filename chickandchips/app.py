import os
from flask import Flask, render_template, request, redirect, url_for

from utils.sms_sender import send_whatsapp_message

app = Flask(__name__)

# Lista temporal para almacenar los pedidos
pedidos = []

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

        # Guardar el pedido en la lista
        pedidos.append({'name': name, 'phone': phone, 'bebida': bebida, 'salsa': salsa})

        # Mensaje para Fabián
        #message_fabian = f"Nuevo pedido de {name}: Bebida - {bebida}, Salsa - {salsa}"
        #send_whatsapp_message(phone, message_fabian)

        print(f"Pedido recibido: {name}, {phone}, {bebida}, {salsa}")
        return render_template('confirmation.html', name=name)
    return render_template('order.html')

@app.route('/confirm', methods=['POST'])
def confirm():
    return render_template('confirmation.html')

@app.route('/admin')
def admin():
    return render_template('admin.html', pedidos=pedidos)

@app.route('/finalizar/<int:index>', methods=['POST'])
def finalizar(index):
    try:
        pedido = pedidos.pop(index)

        # Mensaje para el cliente
        message_cliente = f"Tu pedido de Chick & Chips está listo: {pedido['bebida']} con {pedido['salsa']}."
        send_whatsapp_message(pedido['phone'], message_cliente)

        print(f"Pedido finalizado: {pedido['name']}")
    except IndexError:
        print("Pedido no encontrado")
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)
