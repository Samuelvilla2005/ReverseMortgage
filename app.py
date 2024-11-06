from flask import Flask, render_template, request, redirect, url_for , send_from_directory
from src.ReverseMortgage.MonthlyPayment import Client, ReverseMortgage, NegativeInterest, AboveMaxInterest, NegativePropertyValue, PropertyZeroValue, InvalidAge, InvalidGender, InvalidMaritalStatus  # Aquí importa tus clases

app = Flask(__name__)

# Ruta para servir los archivos CSS
@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('css', filename)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Obtener los datos del formulario
        try:
            age = int(request.form['age'])
            gender = request.form['gender']
            marital_status = request.form['marital_status']
            spouses_age = request.form.get('spouses_age', type=int)  # Puede ser None si no está casado
            spouses_gender = request.form.get('spouses_gender')

            # Crear un cliente
            client = Client(age, gender, marital_status, spouses_age, spouses_gender)
            
            # Obtener los valores para la hipoteca inversa
            property_value = int(request.form['property_value'])
            interest_rate = float(request.form['interest_rate'])
            
            # Crear la hipoteca inversa
            reverse_mortgage = ReverseMortgage(property_value, interest_rate, client)

            # Renderizar la página de resultados
            return render_template('result.html', reverse_mortgage=reverse_mortgage)

        except (NegativeInterest, AboveMaxInterest, NegativePropertyValue, PropertyZeroValue, InvalidAge, InvalidGender, InvalidMaritalStatus) as e:
            error_message = str(e)
            return render_template('index.html', error_message=error_message)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
