---
theme: ./theme.json
author: Piotr Zaniewski
paging: Slide %d / %d
---

# About me

```bash
~~~./aboutme.sh

~~~
```
- 🏢 Head of Engineering Enablement @ **Loft Labs, Inc**
- 💬 Ask me about **Docker, Kubernetes, Azure, vCluster, Microservices, Neovim, Linux**
- 🤖 [](https://cloudrumble.net)
- 📧 [](mailto:piotrzan@gmail.com) 

---

# Learn Kubernetes with AI Assistant


```bash
~~~./intro.sh

~~~
```

---

## Goals

Our main goal is to utilize AI to help users learn Kubernetes by providing a
reliable and consistent AI Assistant that can:

- 🛠️ Bind API routes as tools for AI Assistant to communicate with Kubernetes
- 🔍 Use Internet search APIs for accurate Kubernetes information
- 📊 Monitor and analyze Kubernetes cluster performance metrics
- 🔄 Automate Kubernetes deployment and scaling processes
- 🔐 Implement security best practices for Kubernetes environments
- 📦 Manage Kubernetes configurations and secrets efficiently

---

## Implementation Plan

The following steps outline the plan to achieve our goals:

- 💼 Implement logic flow with Flowise for AI Assistant to manage and troubleshoot a Kubernetes cluster.
- 🛠️ Create a Flask API to expose functions for AI Assistant interaction with the Kubernetes cluster.
- 💻 Bind API routes as tools for AI Assistant to communicate with a local Kind cluster.
- 💬 Test AI Assistant with various Kubernetes configurations for accurate responses.

---

## Prerequisites

Before running the setup, ensure you have the following installed:

- Python 3.x
- Mprocs
- Just (command runner)

---

## Run

Run the server and flowise:

`mprocs --config ./llm-procs.yaml`

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
```

---

## Learn 

- 🔄 **Create & Validate:** Ask the assistant to create or validate Kubernetes resources like Pods or Deployments.
- ✅ **Deployment Feedback:** The assistant will validate your deployments and suggest fixes.
- 📊 **Cluster Info:** Request cluster status, node health, or pod details anytime.
- 🚀 **Scaling:** Learn how to scale your applications with the assistant’s guidance.
- 🔐 **Security:** Get help applying security best practices to your cluster.
- ⚙️ **Automation:** Automate deployment and scaling tasks with AI suggestions.

---

## Assistant

```markdown
- Greet user and introduce yourself.
- Validate and correct one YAML file at a time.
- For cluster info, use get_config.
- For cluster version, use get_version.
- Validate using check_events; propose corrections if needed.
- For other kubectl commands, use execute_command and inform the user.
- Use Brave Search API for Kubernetes concepts, docs, and releases.
```

---

## Function Calling


### What is AI Function Calling?
AI function calling allows AI models to **invoke specific functions** during conversation based on user input. The AI uses pre-defined functions to provide **precise responses** and perform **actions**, making it more interactive and capable.

### How it works:
1. 🧠 **Detects Intent**: AI understands the user's request.
2. 🛠 **Calls a Function**: It selects the appropriate function from a set of pre-defined ones.
3. 📊 **Returns Results**: The function is executed, and the AI presents the results to the user.

