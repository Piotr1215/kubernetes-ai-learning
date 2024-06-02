# this list of available targets
default:
  @just --list --unsorted --unstable

curl:
  @curl -X POST -H "Content-Type: application/x-yaml" --data-binary "@test-pod.yaml" http://localhost:5000/apply

config:
  @curl -X GET -H "Content-Type: application/json" http://localhost:5000/config | yq -C e '.config' 

flowise:
  @xdg-open http://localhost:3003


