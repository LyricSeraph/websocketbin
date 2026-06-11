from flask import request
import random
import json
import logging
from itertools import cycle

# Configure logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def log_and_send(ws, data):
    if isinstance(data, str):
        byte_length = len(data.encode('utf-8'))
    elif isinstance(data, bytes):
        byte_length = len(data)
    else:
        byte_length = len(str(data).encode('utf-8'))
    
    logger.info(f"Sent {byte_length} bytes")
    ws.send(data)

def register_websockets(sock):
    @sock.route('/echo')
    def echo(ws):
        while True:
            data = ws.receive()
            if data is None:
                break
            log_and_send(ws, data)

    @sock.route('/inspect')
    def inspect(ws):
        # Collect connection information
        info = {
            'remote_addr': request.remote_addr,
            'headers': dict(request.headers),
            'args': dict(request.args),
            'url': request.url
        }
        # Send the information to the client immediately after connection
        log_and_send(ws, json.dumps(info, indent=2))
        
        # Continue as an echo server
        while True:
            data = ws.receive()
            if data is None:
                break
            log_and_send(ws, data)

    @sock.route('/random-echo')
    def random_echo_endpoint(ws):
        while True:
            data = ws.receive()
            if data is None:
                break
            
            # If text is received, convert to bytes to determine length
            if isinstance(data, str):
                length = len(data.encode('utf-8'))
            else:
                length = len(data)
                
            random_bytes = bytes([random.randint(0, 255) for _ in range(length)])
            log_and_send(ws, random_bytes)

    @sock.route('/random')
    def random_endpoint(ws):
        while True:
            data = ws.receive()
            if data is None:
                break
            
            # Determine length of input
            if isinstance(data, str):
                length = len(data.encode('utf-8'))
            else:
                length = len(data)
            
            # Return 0-100 times the length in random bytes
            multiplier = random.randint(0, 100)
            total_length = length * multiplier
            
            random_bytes = bytes([random.randint(0, 255) for _ in range(total_length)])
            log_and_send(ws, random_bytes)

    @sock.route('/random-zero')
    def random_zero_endpoint(ws):
        while True:
            data = ws.receive()
            if data is None:
                break
            
            # Determine length of input
            if isinstance(data, str):
                length = len(data.encode('utf-8'))
            else:
                length = len(data)
            
            # Return 0-100 times the length in random bytes
            multiplier = random.randint(0, 100)
            total_length = length * multiplier
            
            random_bytes = bytes([0 for _ in range(total_length)])
            log_and_send(ws, random_bytes)


    @sock.route('/json')
    def json_endpoint(ws):
        # Access the handshake request headers
        response_format = request.headers.get('Response-Format', '{}')
        
        # Verify it's valid JSON
        try:
            parsed = json.loads(response_format)
            # Normalize to a list of responses
            if isinstance(parsed, list):
                responses = parsed
            else:
                responses = [parsed]
        except json.JSONDecodeError:
            responses = [{"error": "Invalid JSON format in Response-Format header"}]
        
        # Create a cycling iterator for the responses
        response_cycle = cycle(responses)
        
        while True:
            data = ws.receive()
            if data is None:
                break
            
            # Get the next response from the cycle
            next_response = next(response_cycle)
            log_and_send(ws, json.dumps(next_response))
