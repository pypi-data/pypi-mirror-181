# TerraScope SDK

## Description

The TerraScope Platform is a collection of tools to analyze sensor data over space and time. The TerraScope SDK 
(software development kit) is a Python package that simplifies users' interaction with the TerraScope Platform API.

## Installation

[Readme: Installation](https://terrascope.readme.io/docs/installation-1)

## Usage

TerraScope SDK is designed to simplify access to all the [terrascope-api](https://pypi.org/project/terrascope-api/) calls
that are available. 

Each API uses a client object which requires the following env variables to be set:

```shell
TERRASCOPE_HOST=terrascope-api1.orbitalinsight.com
TERRASCOPE_TOKEN=<TerraScope API Token>
TERRASCOPE_TIMEOUT=<Int timeout in seconds> defaults to 60 seconds
```

## Authors and acknowledgment

Orbital Insight

## License

[LICENSE](LICENSE)

