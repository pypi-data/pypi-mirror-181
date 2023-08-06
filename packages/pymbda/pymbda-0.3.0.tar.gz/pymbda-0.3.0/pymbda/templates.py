
USAGE_TEXT = """usage: pymbda [resouce] [command] ...

resources:
  functions     AWS Lambda Functions
    init [folder_name]
    build [folder_name]
    deploy [folder_name]
    publish [folder_name]
    alias [folder_name] [alias_name] [version]

  layers        AWS Lambda Layers
    init [folder_name]
    build [folder_name]
    deploy [folder_name]
"""


INIT_DOCKERIGNORE = """.git
**/.git
__pycache__/
**/__pycache__/

.env
.venv
env/
**/env/
venv/
**/venv/
ENV/
**/ENV/
env.bak/
**/env.bak/
venv.bak/
**/venv.bak/

__pymbda__/
**/__pymbda__/

Dockerfile
layer.json
layer-history.json
layer.zip
function.json
function-history.json
function.zip
"""


LAYER_PYTHON_INIT_DOCKERFILE = """# Build using the target Amazon Linux OS
FROM --platform={{architecture}} amazonlinux:latest AS builder

# Install target python version and other dependencies (for building PIL, etc.)
RUN yum install -y amazon-linux-extras libtiff-devel libjpeg-devel libzip-devel && \
    amazon-linux-extras enable python3.8 && \
    yum install -y python3.8

# Update pip and install dependencies to target directory
RUN python3.8 -m pip install pip
COPY ./requirements.txt .
RUN python3.8 -m pip install -r requirements.txt --target=./dist/python/ --no-cache-dir

# Remove __pycache__ files to reduce build size
RUN find . -type d -name __pycache__ -prune -exec rm -rf {} \;

# Copy local packages (if any) to layer and convert the layer as module
COPY . ./dist/python/layers/{{name}}
RUN touch ./dist/python/layers/__init__.py

# Export layer, will be mounted and merged on /opt/python/
FROM scratch as exporter
COPY --from=builder ./dist/ .
"""


LAYER_BINARY_INIT_DOCKERFILE = """# Build using the target Amazon Linux OS
FROM --platform={{architecture}} amazonlinux:latest AS builder

# Example of packaging ffmpeg to layer
RUN yum install -y wget tar xz
RUN wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-5.0.1-arm64-static.tar.xz
RUN mkdir -p ./dist/bin/ && \
    tar -xf ./ffmpeg-5.0.1-arm64-static.tar.xz -C ./dist/bin/ --strip-components=1

# Export layer, will be mounted and merged on /opt/bin/
FROM scratch as exporter
COPY --from=builder ./dist/ .
"""


FUNCTION_PYTHON_INIT_DOCKERFILE = """# Build using the target Amazon Linux OS
FROM --platform={{architecture}} amazonlinux:latest AS builder

# Install target python version and other dependencies (for building PIL, etc.)
RUN yum install -y amazon-linux-extras libtiff-devel libjpeg-devel libzip-devel && \
    amazon-linux-extras enable python3.8 && \
    yum install -y python3.8

# Update pip and install dependencies to target directory
RUN python3.8 -m pip install pip
COPY ./requirements.txt .
RUN python3.8 -m pip install -r requirements.txt --target=./dist/ --no-cache-dir

# Remove __pycache__ files to reduce build size
RUN find . -type d -name __pycache__ -prune -exec rm -rf {} \;

# Copy function files and packages
COPY . ./dist/

# Export function
FROM scratch as exporter
COPY --from=builder ./dist/ .
"""


LAYER_INIT_JSON = """{
    "name": "{{name}}",
    "description": "{{description}}",
    "build": {
        "dockerfile": "__pymbda__/Dockerfile"
    },
    "deploy": {
        "compatibleRuntimes": ["{{runtime}}"],
        "compatibleArchitectures": ["{{architecture}}"]
    }
}
"""


FUNCTION_INIT_JSON = """{
    "name": "{{name}}",
    "description": "{{description}}",
    "build": {
        "dockerfile": "__pymbda__/Dockerfile"
    },
    "deploy": {
        "runtime": "{{runtime}}",
        "role": "{{role}}",
        "handler": "{{handler}}",
        "timeout": {{timeout}},
        "memorySize": {{memorySize}},
        "ephemeralStorageSize": {{ephemeralStorageSize}},
        "environmentVariables": {},
        "vpcConfig": {},
        "layers": [],
        "fileSystemConfigs": [],
        "architectures": ["{{architecture}}"]
    }
}
"""


FUNCTION_HANDLER = """
def {{handlerFunctionName}}(event, context):
    return "Hello World"
"""


FUNCTION_INIT_REQUIREMENTS_TXT = """# Function dependencies, excluding already declared in layers
"""

LAYER_INIT_REQUIREMENTS_TXT = """# Layer dependencies
"""

