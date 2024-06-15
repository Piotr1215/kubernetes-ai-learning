---

# Learn Kubernetes with AI Assistant

---

## Goals

Our main goal is to utliize AI to help users learn Kubernetes by providing a
reliable and consistent AI Assistant that can:

- 🛠️ Use function calling to bind API routes as tools available for the AI Assistant to communicate with a Kubernetes cluster
- 🔍 Internet search APIs to provide accurate and relevant information about Kubernetes

---

## Implementation Plan

The following steps outline the plan to achieve our goals:

- 💼 Use Flowise to implement the logic flow so that the AI Assistant can help with managing and troubleshooting a Kubernetes cluster on our behalf.
- 🛠️ Create a simple Flask API that exposes functions for the AI Assistant to enable it to interact with the Kubernetes cluster.
- 💻 Use function calling to bind the API routes as tools available for the AI Assistant which enables communication with a local Kind cluster with Kubernetes running.
- 💬 Test the AI Assistant with various scenarios to ensure it can handle different Kubernetes configurations and provide accurate responses.

---

## Prerequisites

Before running the setup, ensure you have the following installed:

- Python 3.x
- Mprocs
- Just (command runner)
- Hurl (for HTTP testing)

---

## Setup

To set up the project, follow these steps:

1. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the server and flowise:

   ```bash
   mprocs --config ./llm-procs.yaml
   ```

> mprocs configuration:

```yaml
procs:
  fawit:
    cwd: "./flowise"
    shell: "docker compose up"
    stop: { send-keys: ["<C-c>"] }
  server:
    shell: "./server.py"
    autostart: false
    stop: { send-keys: ["<C-c>"] }
  ngrok:
    shell: "ngrok http --domain=cloudrumble.ngrok.app 5000"
    stop: { send-keys: ["<C-c>"] }
```

The ngrok domain is optional and should be replaced with your own.

3. Start the `flowise` UI:

   ```bash
   just flowise
   ```

4. To test the server, you can use the provided Hurl files in the `testing`
directory:

   ```bash
   hurl --file req.hurl
   ```

5. In `flowise`, create API Keys for OpenAI API and BraveAPI. Go to tools and
upload all the tools from the `flowise-chatflow` directory.
Next create a new chatflow and upload the `Kubernetes Assistant Chatflow.json`.
This should setup the base structure of the chatflow.

---

## Assistant Prompt

```markdown
You are a helpful Kubernetes Assistant specializing in helping users build, fix, and validate various Kubernetes resources YAML files.

Introduction:

    Greet the user and introduce yourself as a helpful and friendly Kubernetes Assistant.

When the User Asks for Help with YAML Files:

    If the YAML files are correct, proceed with the next steps.
    If the files are incorrect, propose fixes and correct the file yourself.
    IMPORTANT: only create one YAML file at a time and wait a few seconds before submitting another one.

For Cluster Information Requests:

    Use the get_config function to provide relevant information about the Kubernetes cluster.

For Handling YAML Files:

    Ask the user to submit one YAML file at a time or create one YAML file yourself if the user asks.
    Send the YAML content (only the YAML content) to the create_yaml function.
    If the user asks for the cluster version, use the get_version tool.

Validation and Feedback:

    Ask the user if they would like to see the validation results and inform them that it takes some time for the resources to be installed on the cluster.
    If the user responds yes, use the check_events tool to validate if everything is correct.
    If the validation passes, ask the user if they want to submit another YAML file.
    If the validation fails, propose a new corrected YAML to the user and ask if they would like to submit it for validation.
    Repeat the process with new YAML files.

For any other cluster interactions

    Use the execute_command tool to run kubectl command if other tools do not provide sufficient capabilities. Make sure that the command contains only valid kubectl commands. Make sure to also output the command you have used. When using this funciton always make sure to tell the user what command you have used.

Secondary Function - Assisting with Kubernetes Information:

    For questions about Kubernetes concepts such as pods, deployments, secrets, etc., use the Brave Search API on Kubernetes Concepts.
    For generic Kubernetes questions, use the Brave Search API on Kubernetes Documentation.
    For questions regarding Kubernetes releases and features, use the Brave Search API on Kubernetes Releases Documentation. If asked for details about a specific release, select one of the releases; otherwise, use the latest stable release.
```

---

## Deployment

To deploy the application to a Kubernetes cluster, apply the YAML configurations:

```
kubectl apply -f test-pod.yaml
kubectl apply -f test-pod-error.yaml
```

---
## Testing

In `flowise` navigate to the testing section and use the chatbot to explore the
cluster.

Additionally you can use `hurl` and run files with `*.hurl` extension to test the endpoints.

---
## Closing Thoughts

- 🚀 Potential use cases:
  - 🤖 dedicated chatbots per customer
  - 📈 help increase kuberentes adoption
  - 🌐 virtual engineer support

---
## License

This project is licensed under the MIT License - see the LICENSE.md file for details
