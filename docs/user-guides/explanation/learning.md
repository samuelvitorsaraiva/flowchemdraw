# Understanding
At its core, `flowchem` is a command line application that:
1. parses a configuration file
2. connects to the lab devices described and
3. offers access to them via a RESTful API.

`flowchem-autodiscover` is a tool that helps preparing the configuration files.

## flowchem command
The `flowchem` command must be called with one parameter: the path to the device configuration file. Running
```shell
flowchem devices.toml
```
in the shell will start a flowchem server with the devices specified in the devices.toml file in the current working directory.
More information will be printed if the `--debug` option is provided, while the `--log` options can be used to specify
the filename of the log file.
A list with all the options is available via `flowchem --help`.

## Flowchem server startup
When the CLI command `flowchem` is called, the following happens:
1. The configuration file provided as argument is parsed, and the device objects are created in the order they appear in the file.
2. Communication is established concurrently for all the devices via calls to each object's `initialize()` method.
3. The components of each hardware object are collected, their routes added to the API server and advertised via mDNS.
4. Flowchem is ready to be used.

It follows that:
* All the code in components (step 3) can assume that a valid connection to the hw device is already in place (step 2).
* Components can use introspection on the relevant hardware device object, e.g. to determine if a pump has withdrawing
  capabilities or not.
* The devices are validated during the initialization and are expected to raise exceptions only during the server startup.
* For safety reasons, all exceptions thrown after the server startup, i.e. during the server lifetime, are caught.
  This ensures that potential errors on one device do not affect the operation of the other devices on the same server.
