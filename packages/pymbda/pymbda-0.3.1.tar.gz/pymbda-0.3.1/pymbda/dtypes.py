from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Build:
    dockerfile: str = "Dockerfile"
    args: Dict[str, str] = field(default_factory=dict)


@dataclass
class LayerDeploy:
    compatibleRuntimes: List[str]
    compatibleArchitectures: List[str]


@dataclass
class Layer:
    name: str
    deploy: LayerDeploy
    description: str = ""
    licenseInfo: str = ""
    build: Build = field(default_factory=Build)


@dataclass
class EFSConfig:
    arn: str
    localMountPath: str


@dataclass
class VpcConfig:
    subnetIds: List[str] = field(default_factory=list)
    securityGroupIds: List[str] = field(default_factory=list)


@dataclass
class FunctionDeploy:
    runtime: str
    role: str
    handler: str
    architectures: List[str]
    timeout: int = 3
    memorySize: int = 128
    ephemeralStorageSize: int = 512
    environmentVariables: Dict[str, str] = field(default_factory=dict)
    fileSystemConfigs: List[EFSConfig] = field(default_factory=list)
    layers: List[str] = field(default_factory=list)
    vpcConfig: VpcConfig = field(default_factory=VpcConfig)


@dataclass
class Function:
    name: str
    deploy: FunctionDeploy
    description: str = ""
    build: Build = field(default_factory=Build)
