
import re
from datetime import datetime, timedelta
import json
import sys

def extract_ip_addresses(text):
    ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
    return ip_pattern.findall(text)

def extract_time_range(text):
    text_lower = text.lower()
    if 'last 1 hour' in text_lower or '1 hour' in text_lower:
        return 'last_1_hour', '-1h'
    elif 'last 24 hours' in text_lower or '24 hours' in text_lower or 'today' in text_lower:
        return 'last_24_hours', '-24h'
    elif 'last 7 days' in text_lower or '7 days' in text_lower or 'last week' in text_lower:
        return 'last_7_days', '-7d'
    # Add more time formats as needed
    return None, None

def extract_port_numbers(text):
    # Improved regex to specifically look for 'port XXXX' or ':XXXX' or stand-alone numbers preceded by 'and' or 'or'
    port_pattern = re.compile(r'(?:port\s+|:)(\d+)\b|\b(?:and|or)\s+(\d+)\b')
    ports = []
    for match in port_pattern.finditer(text.lower()):
        if match.group(1):
            ports.append(match.group(1))
        elif match.group(2):
            ports.append(match.group(2))
    return list(set(ports)) # Return unique ports

def detect_protocol(text):
    text_lower = text.lower()
    protocols = {
        'tcp': ['tcp'],
        'udp': ['udp'],
        'http': ['http', 'web'],
        'https': ['https', 'secure web'],
        'ssh': ['ssh', 'secure shell'],
        'ftp': ['ftp', 'file transfer'],
        'dns': ['dns', 'domain name system']
    }
    detected = []
    for proto, keywords in protocols.items():
        for keyword in keywords:
            if keyword in text_lower:
                detected.append(proto)
                break
    return list(set(detected))

def determine_source_destination_ips(text, ips):
    source_ip = None
    destination_ip = None
    text_lower = text.lower()

    # Prioritize 'from X to Y' or 'to Y from X'
    if 'from' in text_lower and 'to' in text_lower:
        from_index = text_lower.find('from')
        to_index = text_lower.find('to')

        if from_index < to_index:
            # 'from X to Y'
            for ip in ips:
                if source_ip is None and text_lower.find(ip.lower(), from_index, to_index) != -1:
                    source_ip = ip
                elif destination_ip is None and text_lower.find(ip.lower(), to_index) != -1:
                    destination_ip = ip
        else:
            # 'to Y from X'
            for ip in ips:
                if destination_ip is None and text_lower.find(ip.lower(), to_index, from_index) != -1:
                    destination_ip = ip
                elif source_ip is None and text_lower.find(ip.lower(), from_index) != -1:
                    source_ip = ip
    # Handle 'to Y' or 'from X' when only one IP is present
    elif 'to' in text_lower and len(ips) == 1:
        destination_ip = ips[0]
    elif 'from' in text_lower and len(ips) == 1:
        source_ip = ips[0]
    # If two IPs are found without 'from/to', assume first is source, second is destination
    elif len(ips) == 2:
        source_ip = ips[0]
        destination_ip = ips[1]
    # If only one IP and no 'from/to', assume it's the source (can be refined with more context)
    elif len(ips) == 1:
        source_ip = ips[0]

    return source_ip, destination_ip

def parse_user_input(user_input):
    ips = extract_ip_addresses(user_input)
    source_ip, destination_ip = determine_source_destination_ips(user_input, ips)
    time_range_str, splunk_time = extract_time_range(user_input)
    ports = extract_port_numbers(user_input)
    protocols = detect_protocol(user_input)

    intent = {
        "source_ip": source_ip,
        "destination_ip": destination_ip,
        "time_range": time_range_str,
        "ports": ports,
        "protocols": protocols
    }
    return intent, splunk_time

def generate_splunk_query(intent, splunk_time):
    query = ["index=firewall"]
    if intent["source_ip"]:
        query.append(f"src_ip=\"{intent['source_ip']}\"")
    if intent["destination_ip"]:
        query.append(f"dest_ip=\"{intent['destination_ip']}\"")
    if intent["ports"]:
        # Assuming either src_port or dest_port, or both
        port_queries = []
        for port in intent["ports"]:
            port_queries.append(f"src_port={port} OR dest_port={port}")
        query.append(f"({' OR '.join(port_queries)})")
    if intent["protocols"]:
        protocol_queries = []
        for proto in intent["protocols"]:
            protocol_queries.append(f"protocol=\"{proto.upper()}\"") # Splunk often uses uppercase for protocols
        query.append(f"({' OR '.join(protocol_queries)})")
    if splunk_time:
        query.append(f"earliest={splunk_time}")
    return " ".join(query)

def generate_firewall_api_query(intent):
    payload = {"action": "search"}
    if intent["source_ip"]:
        payload["src_ip"] = intent["source_ip"]
    if intent["destination_ip"]:
        payload["dst_ip"] = intent["destination_ip"]
    if intent["time_range"]:
        # Map human-readable time range to API specific format
        time_map = {
            "last_1_hour": "last_1_hour",
            "last_24_hours": "last_24_hours",
            "last_7_days": "last_7_days"
        }
        payload["time_range"] = time_map.get(intent["time_range"], "all_time")
    # Firewall API might not directly support port/protocol in this simple example, extend if needed
    return payload

def generate_router_logs_query(intent):
    query_params = []
    if intent["source_ip"]:
        query_params.append(f"src={intent['source_ip']}")
    if intent["destination_ip"]:
        query_params.append(f"dst={intent['destination_ip']}")
    if intent["time_range"]:
        # Convert time range to minutes for Router Logs API
        time_in_minutes = {
            "last_1_hour": 60,
            "last_24_hours": 1440,
            "last_7_days": 10080
        }
        minutes = time_in_minutes.get(intent["time_range"], None)
        if minutes is not None:
            query_params.append(f"time={minutes}")
    return f"/logs?{'&'.join(query_params)}"

def generate_cloudwatch_query(intent):
    filters = []
    if intent["source_ip"]:
        filters.append(f'/{intent["source_ip"]}/')
    if intent["destination_ip"]:
        filters.append(f'/{intent["destination_ip"]}/')
    if intent["ports"]:
        for port in intent["ports"]:
            filters.append(f"/{port}/")
    if intent["protocols"]:
        for proto in intent["protocols"]:
            filters.append(f"/{proto}/")

    if filters:
        return f"filter @message like {' and '.join(filters)}"
    return ""

def generate_all_queries(user_input):
    intent, splunk_time = parse_user_input(user_input)

    queries = {
        "Splunk": generate_splunk_query(intent, splunk_time),
        "Firewall API": generate_firewall_api_query(intent),
        "Router Logs": generate_router_logs_query(intent),
        "CloudWatch": generate_cloudwatch_query(intent)
    }

    return intent, queries

if __name__ == '__main__':
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
    else:
        user_input = input("Please enter your security query: ")

    intent, queries = generate_all_queries(user_input)

    output = {
        "intent": intent,
        "queries": queries
    }

    print(json.dumps(output, indent=2))


================================================================

import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from src.models.user import db
from src.routes.user import user_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

app.register_blueprint(user_bp, url_prefix='/api')

# uncomment if you need to use database
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
