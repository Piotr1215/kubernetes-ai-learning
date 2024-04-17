# TODO

Add instructions for setting up the project

## Prerequisites

Before running the setup, ensure you have the following installed:

- Python 3.x
- Just (command runner)
- Hurl (for HTTP testing)

## Setup

To set up the project, follow these steps:

1. Install the required Python packages:

   ```
   pip install -r requirements.txt
   ```

2. Run the server using the Justfile:

   ```
   just run-server
   ```

3. To test the server, you can use the provided Hurl file:

   ```
   hurl --file req.hurl
   ```

4. The `llm-procs.yaml`, `test-pod-error.yaml`, and `test-pod.yaml` files are likely used for deployment and testing in a Kubernetes environment. Make sure to configure your Kubernetes cluster accordingly before applying these configurations.

## Testing

Run the tests using the Justfile:

```
just test
```

## Deployment

To deploy the application to a Kubernetes cluster, apply the YAML configurations:

```
kubectl apply -f test-pod.yaml
kubectl apply -f test-pod-error.yaml
```

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
