#!/usr/bin/env python3
from flask import Flask, request, jsonify
import subprocess
import yaml
import tempfile
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("watchdog").setLevel(logging.WARNING)

def run_kubectl_command(command):
    """Helper function to run a kubectl command and return the result."""
    process = subprocess.run(command, shell=True, capture_output=True, text=True)
    if process.returncode != 0:
        return None, process.stderr
    return process.stdout, None

@app.route('/execute', methods=['POST'])
def execute_kubectl():
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"error": f"Invalid JSON data: {str(e)}"}), 400

    command = data.get("command")
    if not command:
        return jsonify({"error": "Missing 'command' key in JSON data"}), 400

    # Ensure the command starts with 'kubectl'
    if not command.startswith("kubectl"):
        return jsonify({"error": "Invalid command, must start with 'kubectl'"}), 400

    app.logger.debug(f"Executing kubectl command: {command}")

    stdout, stderr = run_kubectl_command(command)
    if stderr:
        return jsonify({"error": stderr}), 500

    return jsonify({"result": stdout})

@app.route('/config', methods=['GET'])
def get_cluster_config():
    config_cmd = "kubectl config view"
    stdout, stderr = run_kubectl_command(config_cmd)
    if stderr:
        return jsonify({"error": stderr}), 500
    return jsonify({"config": stdout})

@app.route('/validate', methods=['GET'])
def validate_kubectl():
    events_cmd = (
        "kubectl get events --all-namespaces --field-selector type=Warning "
        "-o custom-columns=TIME:.lastTimestamp,NAMESPACE:.metadata.namespace,"
        "NAME:.involvedObject.name,KIND:.involvedObject.kind,NODE:.source.host,"
        "REASON:.reason,MESSAGE:.message"
    )
    stdout, stderr = run_kubectl_command(events_cmd)
    if stderr:
        return jsonify({"error": stderr}), 500

    if stdout is None:
        return jsonify({"error": "Failed to retrieve events"}), 500

    events = stdout.splitlines()
    if len(events) > 1:
        sorted_events = sorted(events[1:], key=lambda line: line.split(',')[0])
        sorted_events.insert(0, events[0])
    else:
        sorted_events = events

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

    events_cmd = f"kubectl get events --field-selector involvedObject.name={pod_name},involvedObject.namespace={namespace} -n {namespace}"
    stdout, stderr = run_kubectl_command(events_cmd)
    if stderr:
        return jsonify({"error": stderr}), 500

    if stdout is None:
        return jsonify({"error": "Failed to retrieve events"}), 500

    events = stdout.splitlines()
    if len(events) > 1:
        sorted_events = sorted(events[1:], key=lambda line: line.split()[0])
        sorted_events.insert(0, events[0])
    else:
        sorted_events = events

    return jsonify({"events": sorted_events})

@app.route('/apply', methods=['POST'])
def apply_kubectl():
    try:
        data = request.get_json()  # Changed to get_json() to parse JSON data
    except Exception as e:
        return jsonify({"error": f"Invalid JSON data: {str(e)}"}), 400

    yaml_string = data.get("yaml")
    if not yaml_string:
        return jsonify({"error": "Missing 'yaml' key in JSON data"}), 400

    yaml_content = yaml_string.replace("\\n", "\n")
    app.logger.debug(f"Received YAML content: {yaml_content}")

    try:
        # Split the YAML content into individual documents
        yaml_docs = yaml_content.split("---")
        # Remove any empty documents
        yaml_docs = [doc for doc in yaml_docs if doc.strip() != ""]
    except Exception as e:
        return jsonify({"error": f"Failed to split YAML content: {str(e)}"}), 400

    error_messages = []
    for doc in yaml_docs:
        try:
            yaml_data = yaml.safe_load(doc)
        except yaml.YAMLError as e:
            error_messages.append(f"Error parsing YAML document: {str(e)}")
            continue

        with tempfile.NamedTemporaryFile(delete=False, suffix=".yaml", mode='w') as tmp:
            tmp.write(doc)
            tmp_filename = tmp.name

        apply_cmd = f"kubectl apply -f {tmp_filename}"
        stdout, stderr = run_kubectl_command(apply_cmd)
        if stderr:
            if "already exists" in stderr:
                error_messages.append(f"Conflict: resource already exists for document starting with {doc[:30]}")
            else:
                error_messages.append(stderr)

    if error_messages:
        return jsonify({"errors": error_messages}), 500

    return jsonify({"message": "Your YAML has been applied successfully, ask me to validate to see the events"}), 200

@app.route('/version', methods=['GET'])
def get_cluster_version():
    config_cmd = "kubectl version"
    stdout, stderr = run_kubectl_command(config_cmd)
    if stderr:
        return jsonify({"error": stderr}), 500
    return jsonify({"version": stdout})

if __name__ == '__main__':
    app.run(debug=True)
