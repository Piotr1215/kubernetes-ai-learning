---

# Improve AI Reliability and Consistency in Kubernetes

## Problem Statement

Let's state the issue we do have with AI in the context of Kubernetes:

- 🤖 AI faces issues with consistency and reliability when dealing with large YAML files.
- 🧠 AIs can have "hallucinations," generating illogical outputs that become more problematic as the input size increases.
- 📈 This inconsistency makes working with AI models non-deterministic and error prone

---

## Goals

Our main goal is to increase reliability and consistency in AI responses. We use two main techniques to achieve this:

- 🛠️ Function calling to bind API routes as tools available for the AI Assistant to communicate with a Kubernetes cluster
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
