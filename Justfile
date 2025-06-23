build-rocm-container:
    sudo podman build -t rocm-jupyter:latest -f Dockerfile

start-rocm-container:
    sudo podman run -d --rm \
    --network=host \
    --device=/dev/kfd \
    --device=/dev/dri \
    --group-add=video \
    --ipc=host \
    --cap-add=SYS_PTRACE \
    --security-opt seccomp=unconfined \
    -v ./:/workspace \
    -w /workspace/nb \
    --name rocm-jupyter \
    localhost/rocm-jupyter:latest

stop-rocm-container:
    sudo podman stop rocm-jupyter