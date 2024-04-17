# this list of available targets
default:
  @just --list --unsorted --unstable

curl:
  @curl -X POST -H "Content-Type: application/x-yaml" --data-binary "@test-pod.yaml" http://localhost:5000/apply

config:
  @curl -X GET -H "Content-Type: application/json" http://cloudrumble.ngrok.app/config

flowise:
  @xdg-open http://localhost:3003


