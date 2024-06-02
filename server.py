#!/usr/bin/env python3
from flask import Flask, request, jsonify
import subprocess
import yaml
import tempfile
import logging
import json

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

@app.route('/config', methods=['GET'])
def get_cluster_config():
    # Get cluster configuration using kubectl
    config_cmd = "kubectl config view"
    process = subprocess.run(config_cmd, shell=True, capture_output=True, text=True)
    if process.returncode != 0:
        return jsonify({"error": process.stderr}), 500

    # Return the cluster configuration
    return jsonify({"config": process.stdout})

@app.route('/cleanup', methods=['DELETE'])
def cleanup_kubectl_events():
    # Delete all events using kubectl
    delete_cmd = "kubectl delete events --all"
    process = subprocess.run(delete_cmd, shell=True, capture_output=True, text=True)
    if process.returncode != 0:
        return jsonify({"error": process.stderr}), 500
    
    # Return a success message if deletion was successful
    return jsonify({"message": "Events successfully deleted"}), 200

@app.route('/validate', methods=['GET'])
def validate_kubectl():
    # Get all events, warning events will be treated as errors
    events_cmd = "kubectl get events --all-namespaces --field-selector type=Warning -o custom-columns=TIME:.lastTimestamp,NAMESPACE:.metadata.namespace,NAME:.involvedObject.name,KIND:.involvedObject.kind,NODE:.source.host,REASON:.reason,MESSAGE:.message"

    events_process = subprocess.run(events_cmd, shell=True, capture_output=True, text=True)
    if events_process.returncode != 0:
        return jsonify({"error": events_process.stderr}), 500

    # Process and sort events
    events = events_process.stdout.splitlines()
    sorted_events = sorted(events[1:], key=lambda line: line.split(',')[0])  # Skip header and sort by TIME
    sorted_events.insert(0, events[0])  # Reinsert header at the beginning

    # Return events
    return jsonify({"events": sorted_events})

@app.route('/messages', methods=['GET'])
def get_kubectl_messages():
    pod_name = request.args.get('name')
    namespace = request.args.get('namespace')
    resource_type = request.args.get('type')

    if not pod_name or not namespace or not resource_type:
        return jsonify({"error": "Missing required query parameters: name, namespace, type"}), 400

    if resource_type not in ['pod', 'deployment']:
        return jsonify({"error": "Invalid type parameter, must be 'pod' or 'deployment'"}), 400

    # Construct the kubectl command based on the provided parameters
    events_cmd = f"kubectl get events --field-selector involvedObject.name={pod_name},involvedObject.namespace={namespace} -n {namespace}"

    # Execute the kubectl command
    process = subprocess.run(events_cmd, shell=True, capture_output=True, text=True)
    if process.returncode != 0:
        return jsonify({"error": process.stderr}), 500

    # Process the events
    events = process.stdout.splitlines()
    if len(events) > 1:
        # Skip the header and sort by the first column (TIME)
        sorted_events = sorted(events[1:], key=lambda line: line.split()[0])
        sorted_events.insert(0, events[0])  # Reinsert header at the beginning
    else:
        sorted_events = events

    # Return the events
    return jsonify({"events": sorted_events})

@app.route('/apply', methods=['POST'])
def apply_kubectl():
    # Parse the incoming data as JSON
    try:
        data = json.loads(request.data)
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON data"}), 400

    # Extract the YAML string
    yaml_string = data.get("yaml")
    if not yaml_string:
        return jsonify({"error": "Missing 'yaml' key in JSON data"}), 400

    # Replace \n with actual newlines
    yaml_content = yaml_string.replace("\\n", "\n")

    # Log the received YAML content
    app.logger.debug(f"Received YAML content: {yaml_content}")

    # Convert YAML string to YAML format
    try:
        yaml_data = yaml.safe_load(yaml_content)
    except yaml.YAMLError as e:
        return jsonify({"error": str(e)}), 400

    # Write YAML content to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".yaml", mode='w') as tmp:
        tmp.write(yaml_content)
        tmp_filename = tmp.name

    # Apply the YAML using kubectl
    apply_cmd = f"kubectl apply -f {tmp_filename}"
    process = subprocess.run(apply_cmd, shell=True, capture_output=True, text=True)
    if process.returncode != 0:
        return jsonify({"error": process.stderr}), 500

    return jsonify({"message": "Your YAML has been applied successfully, aks me to validate to see the events"})

if __name__ == '__main__':
    app.run(debug=True)

