# Enhancing Verification with Artificial Intelligence


## Problem Statement

- 🤖 AI faces issues with consistency and reliability when dealing with large YAML files.
- 🧠 AIs can have "hallucinations," generating illogical outputs that become more problematic as the input size increases.
- 📈 This inconsistency makes working with AI models non-deterministic and error
  prone

---

## Goals

- 💪 Enhancing AI chatbot reliability
- 🔬 Using OpenAI's latest model with function calling
- 📚 Utilizing document retrieval systems as knowledge base
- 🧠 Connect everything into one cohesive pattern

---

## Implementation

- 💼 Implementing the draft using Flowise
- 🛠️ Creating an API using Python Flask
- 💻 Communicating with a local Kind cluster that has Crossplane installed.
- 💬 Embedding a chatbot on a web page.

---

## Prerequisites

Before running the setup, ensure you have the following installed:

- Python 3.x
- Mprocs
- Just (command runner)
- Hurl (for HTTP testing)

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

4. To test the server, you can use the provided Hurl file:

   ```bash
   hurl --file req.hurl
   ```

## Deployment

To deploy the application to a Kubernetes cluster, apply the YAML configurations:

```
kubectl apply -f test-pod.yaml
kubectl apply -f test-pod-error.yaml
```

## Testing

In `flowise` navigate to the testing section and use the chatbot to explore the
cluster.

## Closing Thoughts

- 💭 Debate between model fine-tuning and chain of reasoning
- 🚀 Potential use cases:
  - 🤖 dedicated chatbots per customer
  - 📈 help increase crossplane adoption
  - 🌐 virtual platform engineer
- 📚 Needs more research and resources


## License

This project is licensed under the MIT License - see the LICENSE.md file for details
