SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
# create empty aws config file if required
mkdir -p ~/.aws && touch ~/.aws/config
# install awscli if the command is not installed
if ! command -v aws
then
pip install awscli
fi

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
  $SCRIPT_DIR/octo_latest_linux_amd64/octo login aws --profile octo
elif [[ "$OSTYPE" == "darwin"* ]]; then
  # Mac OSX
  $SCRIPT_DIR/octo_latest_mac_x86_64/octo login aws --profile octo
fi

aws ecr get-login-password --region eu-west-1 --profile octo | docker login --username AWS --password-stdin 116944431457.dkr.ecr.eu-west-1.amazonaws.com