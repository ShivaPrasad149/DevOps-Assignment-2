from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime

app = Flask(
    __name__,
    template_folder='templates',  # Ensures Flask knows where HTML files are
    static_folder='static'        # Ensures Flask serves CSS, JS, etc.
)

app.secret_key = 'devops-assignment-2-secret-key-2025'

# ----------------------------------------------------------
# Sample Data
# ----------------------------------------------------------

BUS_ROUTES = [
    {
        'id': 1,
        'operator': 'TGSRTC Express',
        'type': 'AC Sleeper',
        'seating': '2+1 Seating',
        'from': 'Hyderabad',
        'to': 'Bangalore',
        'departure': '08:30 AM',
        'arrival': '02:15 PM',
        'duration': '5h 45m',
        'date': '2025-10-19',
        'price': 45.00,
        'discount_price': 40.00,
        'rating': 4.5,
        'reviews': 234,
        'available_seats': 18,
        'amenities': ['WiFi', 'Charging Port', 'Water Bottle'],
        'image': 'https://images.unsplash.com/photo-1606135673631-1ff4dda17834'
    },
    {
        'id': 2,
        'operator': 'RedBus Premium',
        'type': 'AC Semi-Sleeper',
        'seating': '2+2 Seating',
        'from': 'Hyderabad',
        'to': 'Bangalore',
        'departure': '10:15 AM',
        'arrival': '04:30 PM',
        'duration': '6h 15m',
        'date': '2025-10-19',
        'price': 38.00,
        'discount_price': 38.00,
        'rating': 4.2,
        'reviews': 156,
        'available_seats': 5,
        'amenities': ['WiFi', 'Blanket', 'Reading Light'],
        'image': 'https://images.unsplash.com/photo-1608090192135-cac58333d3c2'
    }
]

SEAT_LAYOUT = {
    'upper_deck': [
        {'id': 'U1A', 'type': 'sleeper', 'price': 45, 'available': True},
        {'id': 'U2A', 'type': 'sleeper', 'price': 45, 'available': False},
        {'id': 'U3A', 'type': 'sleeper', 'price': 45, 'available': True},
        {'id': 'U1B', 'type': 'sleeper', 'price': 45, 'available': True},
        {'id': 'U2B', 'type': 'sleeper', 'price': 45, 'available': True},
        {'id': 'U3B', 'type': 'sleeper', 'price': 45, 'available': False},
    ],
    'lower_deck': [
        {'id': 'L1A', 'type': 'semi-sleeper', 'price': 38, 'available': True},
        {'id': 'L2A', 'type': 'semi-sleeper', 'price': 38, 'available': True},
        {'id': 'L3A', 'type': 'semi-sleeper', 'price': 38, 'available': False},
        {'id': 'L1B', 'type': 'semi-sleeper', 'price': 38, 'available': True},
        {'id': 'L2B', 'type': 'semi-sleeper', 'price': 38, 'available': False},
        {'id': 'L3B', 'type': 'semi-sleeper', 'price': 38, 'available': True},
    ]
}

# ----------------------------------------------------------
# Routes
# ----------------------------------------------------------

@app.route('/')
def index():
    """Home page - redirects to route search"""
    return render_template('index.html')


@app.route('/routes')
def route_search():
    """Route search page"""
    return render_template('route_search.html', routes=BUS_ROUTES)


@app.route('/seats')
def seat_selection():
    """Seat selection page"""
    selected_route_id = request.args.get('route_id', 1)
    selected_route = next((route for route in BUS_ROUTES if route['id'] == int(selected_route_id)), BUS_ROUTES[0])
    return render_template('seat_selection.html', route=selected_route, seat_layout=SEAT_LAYOUT)


@app.route('/payment')
def payment_processing():
    """Payment processing page"""
    return render_template('payment_processing.html')


# ----------------------------------------------------------
# API Endpoints
# ----------------------------------------------------------

@app.route('/api/seats/<seat_id>/select', methods=['POST'])
def select_seat(seat_id):
    """API endpoint to select a seat"""
    data = request.json
    passenger_name = data.get('passenger_name', '')
    return jsonify({
        'success': True,
        'seat_id': seat_id,
        'passenger_name': passenger_name,
        'message': f'Seat {seat_id} selected successfully'
    })


@app.route('/api/payment/process', methods=['POST'])
def process_payment():
    """API endpoint to process payment"""
    data = request.json
    payment_success = True  # Simulate success
    if payment_success:
        return jsonify({
            'success': True,
            'transaction_id': f'TXN{datetime.now().strftime("%Y%m%d%H%M%S")}',
            'message': 'Payment processed successfully'
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Payment failed. Please try again.'
        }), 400


@app.route('/api/routes/search', methods=['POST'])
def search_routes():
    """API endpoint for route search"""
    data = request.json
    source = data.get('source', '')
    destination = data.get('destination', '')
    filtered_routes = [
        route for route in BUS_ROUTES
        if route['from'].lower() == source.lower() and route['to'].lower() == destination.lower()
    ]
    return jsonify({
        'success': True,
        'routes': filtered_routes,
        'count': len(filtered_routes)
    })


@app.route('/health')
def health_check():
    """Health check endpoint for Kubernetes"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'BusBooker Pro Flask App'
    })

# ----------------------------------------------------------
# Run Flask App
# ----------------------------------------------------------

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)
