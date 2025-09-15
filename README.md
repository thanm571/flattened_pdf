

### Setup
 docker build -t flattener-app .

### Example
docker run --rm `\` <br>
  -e INPUT_DIR=/custom/in `\` <br>
  -e OUTPUT_DIR=/custom/out `\` <br>
  -e INPUT_DPI="250" `\` <br>
  -e INPUT_QUALITY="80" `\` <br>
  -v /path/to/flatten:/custom/in `\` <br>
  -v /path/to/output:/custom/out `\` <br>
  flattener-app `\` <br>
  python process.py
