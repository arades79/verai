FROM rocm/vllm-dev:main

RUN pip install jupyter

ENV RADEON_UNSLOTH=1
EXPOSE 8888

CMD jupyter-lab --ip=0.0.0.0 --port=8888 --allow-root --no-browser --NotebookApp.token='' --NotebookApp.password=''