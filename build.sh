SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd $SCRIPT_DIR
TAG="handwriting-practise-dev:latest"
docker build . -t ${TAG}
docker run -v "$(pwd)/data:/data" -v "$(pwd)/docs:/output" --entrypoint "python" --rm -it ${TAG} process.py /data /output ${UID} 1000 False

