SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd $SCRIPT_DIR
TAG="handwriting-practise-dev:latest"
docker build . -t ${TAG}
docker run -v "$(pwd)/data:/data" -v "$(pwd)/site/pdfs:/output" --rm -it ${TAG} ${UID} 1000
