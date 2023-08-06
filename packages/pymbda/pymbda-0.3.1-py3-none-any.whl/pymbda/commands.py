
import argparse
from datetime import datetime
import functools
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Callable, List

import boto3
import dacite

from .dtypes import Function, Layer
from .templates import (
    FUNCTION_HANDLER,
    FUNCTION_INIT_JSON,
    FUNCTION_INIT_REQUIREMENTS_TXT,
    FUNCTION_PYTHON_INIT_DOCKERFILE,
    INIT_DOCKERIGNORE,
    FUNCTION_PYTHON_INIT_DOCKERFILE,
    LAYER_INIT_JSON,
    LAYER_INIT_REQUIREMENTS_TXT,
    LAYER_PYTHON_INIT_DOCKERFILE
)
from .utils import (
    explore_aws_cfg,
    get_dir_size,
    history_append,
    history_set,
    input_choice,
    input_int,
    input_validated,
    is_valid_handler,
    is_valid_module_name,
    profile_dir_size,
    pymbda_print,
    replace_template_vars,
    resolve_work_dir,
)


def functions_init(args: List[str]):
    parser = argparse.ArgumentParser(description="Build AWS Lambda Function")
    parser.add_argument("folder_name", type=str)
    parsed_args = vars(parser.parse_args(args))

    if parsed_args['folder_name'] != "." and not is_valid_module_name(parsed_args['folder_name']):
        pymbda_print("Function name must be a valid python module name")
        return

    work_dir = resolve_work_dir("functions", parsed_args['folder_name'])
    pymbda_dir = work_dir / "__pymbda__/"

    template_vars = {
        "name": parsed_args['folder_name'],
        "description": input("> Description: "),
        "role": input("> Execution Role [format: aws_arn]: "),
        "runtime": input("> Runtime [default: python3.8]: ") or "python3.8",
        "architecture": input_choice("> Architecture [select: arm64, x86-64; default: arm64]: ", ("arm64", "x86-64", "")) or "arm64",
        "handler": input_validated("> Handler [format: {pythonFile}.{functionName}; default: index.handler]: ", is_valid_handler) or "index.handler",
        "timeout": input_int("> Timeout [unit: seconds; range: 1~inf; default: 1]: ", min=1, default=1),
        "memorySize": input_int("> Memory Size [unit: MB; range: 128~inf; default: 512]: ", min=128, default=512),
        "ephemeralStorageSize": input_int("> Ephemeral Storage Size [unit: MB; range: 512~inf; default: 512]: ", min=512, default=512),
    }
    template_vars["handlerPythonFile"], template_vars["handlerFunctionName"] = template_vars["handler"].split(".")
    work_dir.mkdir(parents=True, exist_ok=True)
    pymbda_dir.mkdir(parents=True)

    with open(work_dir / ".dockerignore", "w+") as f:
        f.write(replace_template_vars(INIT_DOCKERIGNORE, template_vars))
    with open(pymbda_dir / "Dockerfile", "w+") as f:
        alt_template_vars = template_vars.copy()
        if alt_template_vars["architecture"] == "x86-64":
            alt_template_vars["architecture"] = "amd64"
        f.write(replace_template_vars(FUNCTION_PYTHON_INIT_DOCKERFILE, alt_template_vars))
    with open(pymbda_dir / "function.json", "w+") as f:
        f.write(replace_template_vars(FUNCTION_INIT_JSON, template_vars))
    with open(work_dir / "requirements.txt", "w+") as f:
        f.write(replace_template_vars(FUNCTION_INIT_REQUIREMENTS_TXT, template_vars))
    with open(work_dir / (template_vars["handlerPythonFile"] + ".py"), "w+") as f:
        f.write(replace_template_vars(FUNCTION_HANDLER, template_vars))
    pymbda_print(f"Successfully initiated function {parsed_args['folder_name']}")
    pymbda_print(f"Further configurations can be made directly on function.json")


def layers_init(args: List[str]):
    parser = argparse.ArgumentParser(description="Build AWS Lambda Layer")
    parser.add_argument("folder_name", type=str)
    parsed_args = vars(parser.parse_args(args))

    if not is_valid_module_name(parsed_args['folder_name']):
        pymbda_print("Function name must be a valid python module name")
        return

    work_dir = Path("layers") / parsed_args['folder_name']
    Path(f"layers/__init__.py").touch()
    pymbda_dir = work_dir / "__pymbda__/"

    template_vars = {
        "name": parsed_args['folder_name'],
        "description": input("> Description: "),
        "runtime": input("> Runtime [default: python3.8]: ") or "python3.8",
        "architecture": input_choice("> Architecture [select: arm64, x86-64; default: arm64]: ", ("arm64", "x86-64", "")) or "arm64",
    }
    work_dir.mkdir(parents=True, exist_ok=True)
    pymbda_dir.mkdir(parents=True)

    with open(work_dir / ".dockerignore", "w+") as f:
        f.write(replace_template_vars(INIT_DOCKERIGNORE, template_vars))
    with open(pymbda_dir / "Dockerfile", "w+") as f:
        alt_template_vars = template_vars.copy()
        if alt_template_vars["architecture"] == "x86-64":
            alt_template_vars["architecture"] = "amd64"
        f.write(replace_template_vars(LAYER_PYTHON_INIT_DOCKERFILE, alt_template_vars))
    with open(pymbda_dir / "layer.json", "w+") as f:
        f.write(replace_template_vars(LAYER_INIT_JSON, template_vars))
    with open(work_dir / "requirements.txt", "w+") as f:
        f.write(replace_template_vars(LAYER_INIT_REQUIREMENTS_TXT, template_vars))
    pymbda_print(f"Successfully initiated layer {parsed_args['folder_name']}")
    pymbda_print(f"Further configurations can be made directly on layer.json")


def _layer_read_cfg(work_dir: Path):
    with open(work_dir / "layer.json") as f:
        try:
            layer = dacite.from_dict(Layer, json.load(f), config=dacite.Config(strict=True))
        except dacite.DaciteError as e:
            pymbda_print(e)
            sys.exit(1)
    return layer


def layers_build(args: List[str]):
    parser = argparse.ArgumentParser(description="Build AWS Lambda Layer")
    parser.add_argument("folder_name", type=str)
    parser.add_argument('--size-profile', type=int, default=0)
    parsed_args = vars(parser.parse_args(args))

    work_dir = Path("layers") / parsed_args['folder_name']
    pymbda_dir = work_dir / "__pymbda__/"
    explore_aws_cfg([work_dir, Path()])
    layer = _layer_read_cfg(pymbda_dir)

    pymbda_print("Parsing build command ...")
    build_args_inject = ""
    for arg_key, arg_value in layer.build.args.items():
        if build_args_inject:
            build_args_inject += " "
        build_args_inject += f"--build-arg {arg_key}={arg_value}"
    process_cmd = f"docker build -f {layer.build.dockerfile} {build_args_inject} --progress=plain --output __pymbda__/layer ."

    try:
        pymbda_print("Building layer ...")
        build_process = subprocess.Popen(
            process_cmd,
            cwd=work_dir,
            stdout=subprocess.PIPE
        )
        for c in iter(lambda: build_process.stdout.read(1), b""):
            sys.stdout.buffer.write(c)
        build_process_code = build_process.wait()
        if build_process_code != 0:
            pymbda_print(f"Failed to build layer (code: {build_process_code})")
            sys.exit(1)
        layer_dir = pymbda_dir / 'layer'
        shutil.make_archive(layer_dir, 'zip', layer_dir)
        pymbda_print("Layer built successfully")
        layer_uncompressed_size = get_dir_size(layer_dir)
        layer_compressed_size = os.path.getsize(pymbda_dir / 'layer.zip')
        if parsed_args["size_profile"]:
            pymbda_print("Layer uncompressed size profile - top 20 big files")
            profile_dir_size(layer_dir)
        pymbda_print(f"Layer uncompressed size: {layer_uncompressed_size}")
        pymbda_print(f"Layer compressed size: {layer_compressed_size}")
        history_set(pymbda_dir / "layer-history.json", "lastBuild", {
            "uncompressedSize": layer_uncompressed_size,
            "compressedSize": layer_compressed_size,
            "createdDate": datetime.now().isoformat()
        })
        pymbda_print("Updated layer-history.json")
    finally:
        shutil.rmtree(layer_dir, ignore_errors=True)


def _functions_read_cfg(work_dir: Path):
    pymbda_print("Reading function cfg ...")
    with open(work_dir / "function.json") as f:
        try:
            function = dacite.from_dict(Function, json.load(f), config=dacite.Config(strict=True))
        except dacite.DaciteError as e:
            pymbda_print(e)
            sys.exit(1)
    return function


def functions_build(args: List[str]):
    parser = argparse.ArgumentParser(description="Build AWS Lambda Function")
    parser.add_argument("folder_name", type=str)
    parser.add_argument('--size-profile', type=int, default=0)
    parsed_args = vars(parser.parse_args(args))

    work_dir = resolve_work_dir("functions", parsed_args['folder_name'])
    pymbda_dir = work_dir / "__pymbda__/"
    explore_aws_cfg([work_dir, Path()])
    function = _functions_read_cfg(pymbda_dir)

    pymbda_print("Parsing build command ...")
    build_args_inject = ""
    for arg_key, arg_value in function.build.args.items():
        if build_args_inject:
            build_args_inject += " "
        build_args_inject += f"--build-arg {arg_key}={arg_value}"
    process_cmd = f"docker build -f {function.build.dockerfile} {build_args_inject} --progress=plain --output __pymbda__/function ."

    try:
        pymbda_print("Building function ...")
        build_process = subprocess.Popen(
            process_cmd,
            cwd=work_dir,
            stdout=subprocess.PIPE
        )
        for c in iter(lambda: build_process.stdout.read(1), b""):
            sys.stdout.buffer.write(c)
        build_process_code = build_process.wait()
        if build_process_code != 0:
            pymbda_print(f"Failed to build function (code: {build_process_code})")
            sys.exit(1)
        function_dir = pymbda_dir / 'function'
        shutil.make_archive(function_dir, 'zip', function_dir)
        pymbda_print("Function built successfully")
        function_uncompressed_size = get_dir_size(function_dir)
        function_compressed_size = os.path.getsize(pymbda_dir / 'function.zip')
        if parsed_args["size_profile"]:
            pymbda_print("Function uncompressed size profile - top 20 big files")
            profile_dir_size(function_dir)
        pymbda_print(f"Function uncompressed size: {function_uncompressed_size}")
        pymbda_print(f"Function compressed size: {function_compressed_size}")
        history_set(pymbda_dir / "function-history.json", "lastBuild", {
            "uncompressedSize": function_uncompressed_size,
            "compressedSize": function_compressed_size,
            "createdDate": datetime.now().isoformat()
        })
        pymbda_print("Updated function-history.json")
    finally:
        shutil.rmtree(function_dir, ignore_errors=True)


def layers_deploy(args: List[str]):
    parser = argparse.ArgumentParser(description="Deploy AWS Lambda Layer")
    parser.add_argument("folder_name", type=str)
    parsed_args = vars(parser.parse_args(args))

    work_dir = Path("layers") / parsed_args['folder_name']
    pymbda_dir = work_dir / "__pymbda__/"
    explore_aws_cfg([work_dir, Path()])
    client = boto3.client("lambda")

    layer = _layer_read_cfg(pymbda_dir)

    with open(pymbda_dir / "layer.zip", "rb") as zip:
        pymbda_print("Deploying layer ...")
        aws_layer = client.publish_layer_version(
            LayerName=layer.name,
            Description=layer.description,
            Content={'ZipFile': zip.read()},
            CompatibleRuntimes=layer.deploy.compatibleRuntimes,
            LicenseInfo=layer.licenseInfo,
            CompatibleArchitectures=layer.deploy.compatibleArchitectures
        )
        pymbda_print("Layer deployed successfully")
        aws_layer.pop("ResponseMetadata", None)
        pymbda_print(f"Layer version ARN: {aws_layer['LayerVersionArn']}")
        history_append(pymbda_dir / "layer-history.json", "deployments", aws_layer)
        pymbda_print("Updated layer-history.json")


def functions_deploy(args: List[str]):
    parser = argparse.ArgumentParser(description="Deploy AWS Lambda Function")
    parser.add_argument("folder_name", type=str)
    parsed_args = vars(parser.parse_args(args))

    work_dir = resolve_work_dir("functions", parsed_args['folder_name'])
    pymbda_dir = work_dir / "__pymbda__/"
    explore_aws_cfg([work_dir, Path()])
    client = boto3.client("lambda")

    function = _functions_read_cfg(pymbda_dir)

    try:
        client.get_function(FunctionName=function.name)
        function_exists = True
    except client.exceptions.ResourceNotFoundException:
        function_exists = False

    with open(pymbda_dir / "function.zip", "rb") as zip:
        pymbda_print("Deploying function ...")
        if not function_exists:
            aws_function = client.create_function(
                FunctionName=function.name,
                Role=function.deploy.role,
                Runtime=function.deploy.runtime,
                Handler=function.deploy.handler,
                Code={'ZipFile': zip.read()},
                Description=function.description,
                Timeout=function.deploy.timeout,
                MemorySize=function.deploy.memorySize,
                Publish=False,
                VpcConfig={"SubnetIds": function.deploy.vpcConfig.subnetIds, "SecurityGroupIds": function.deploy.vpcConfig.securityGroupIds},
                Environment={"Variables": function.deploy.environmentVariables},
                Layers=function.deploy.layers,
                FileSystemConfigs=[{"Arn": fsc.arn, "LocalMountPath": fsc.localMountPath} for fsc in function.deploy.fileSystemConfigs],
                Architectures=function.deploy.architectures,
                EphemeralStorage={"Size": function.deploy.ephemeralStorageSize}
            )
            client.get_waiter('function_active').wait(
                FunctionName=function.name,
            )
        else:
            client.update_function_configuration(
                FunctionName=function.name,
                Role=function.deploy.role,
                Runtime=function.deploy.runtime,
                Handler=function.deploy.handler,
                Description=function.description,
                Timeout=function.deploy.timeout,
                MemorySize=function.deploy.memorySize,
                VpcConfig={"SubnetIds": function.deploy.vpcConfig.subnetIds, "SecurityGroupIds": function.deploy.vpcConfig.securityGroupIds},
                Environment={"Variables": function.deploy.environmentVariables},
                Layers=function.deploy.layers,
                FileSystemConfigs=[{"Arn": fsc.arn, "LocalMountPath": fsc.localMountPath} for fsc in function.deploy.fileSystemConfigs],
                EphemeralStorage={"Size": function.deploy.ephemeralStorageSize}
            )
            client.get_waiter('function_updated').wait(
                FunctionName=function.name,
            )
            aws_function = client.update_function_code(
                FunctionName=function.name,
                ZipFile=zip.read(),
                Architectures=function.deploy.architectures,
                Publish=False
            )
            client.get_waiter('function_updated').wait(
                FunctionName=function.name,
            )
        pymbda_print("Function deployed successfully")
        pymbda_print(f"Function ARN: {aws_function['FunctionArn']}")
        aws_function.pop("ResponseMetadata", None)
        history_append(pymbda_dir / "function-history.json", "deployments", aws_function)
        pymbda_print("Updated function-history.json")


def functions_publish(args: List[str]):
    parser = argparse.ArgumentParser(description="Publish AWS Lambda Function")
    parser.add_argument("folder_name", type=str)
    parsed_args = vars(parser.parse_args(args))

    work_dir = resolve_work_dir("functions", parsed_args['folder_name'])
    pymbda_dir = work_dir / "__pymbda__/"
    explore_aws_cfg([work_dir, Path()])
    client = boto3.client("lambda")

    function = _functions_read_cfg(pymbda_dir)

    pymbda_print("Publishing function version ...")
    aws_function = client.publish_version(FunctionName=function.name)
    pymbda_print("Function version published successfully")
    pymbda_print(f"Function version ARN: {aws_function['FunctionArn']}")
    aws_function.pop("ResponseMetadata", None)
    history_append(pymbda_dir / "function-history.json", "publishments", aws_function)
    pymbda_print("Updated function-history.json")


def functions_alias(args: List[str]):
    parser = argparse.ArgumentParser(description="Alias AWS Lambda Function")
    parser.add_argument("folder_name", type=str)
    parser.add_argument("alias_name", type=str)
    parser.add_argument("version", type=str)
    parsed_args = vars(parser.parse_args(args))

    work_dir = resolve_work_dir("functions", parsed_args['folder_name'])
    pymbda_dir = work_dir / "__pymbda__/"
    explore_aws_cfg([work_dir, Path()])
    client = boto3.client("lambda")

    function = _functions_read_cfg(pymbda_dir)

    try:
        client.get_alias(FunctionName=function.name, Name=parsed_args['alias_name'])
        alias_exists = True
    except client.exceptions.ResourceNotFoundException:
        alias_exists = False

    pymbda_print(f"Creating function alias '{parsed_args['alias_name']}' with version '{parsed_args['version']}' ...")
    if not alias_exists:
        aws_function_alias = client.create_alias(
            FunctionName=function.name,
            Name=parsed_args['alias_name'],
            FunctionVersion=parsed_args['version']
        )
    else:
        aws_function_alias = client.update_alias(
            FunctionName=function.name,
            Name=parsed_args['alias_name'],
            FunctionVersion=parsed_args['version']
        )
    pymbda_print("Function alias created successfully")
    aws_function_alias.pop("ResponseMetadata", None)
    history_append(pymbda_dir / "function-history.json", "aliases", aws_function_alias)
    pymbda_print("Updated function-history.json")


def resolve_command(resource: str, command: str) -> Callable[[List[str]], None]:
    if f"{resource}_{command}" in globals():
        return globals()[f"{resource}_{command}"]
    if f"hybrid_{resource}" in globals():
        return functools.partial(globals()[f"hybrid_{resource}"], resource)
    raise ValueError(resource, command)
