# Configuration File

The configuration file is the only input required by the package. It is built in an easily editable `.toml` format. 
For more details about this file format, please visit [TOML](https://toml.io/en/). The configuration file should look 
like this:
```toml
[device.test-device]
type = "FakeDevice"
```

In this file, the term `device` indicates that the device is implemented in the package. The term `test-device` is the
device name chosen by the user, and `FakeDevice` is the device type corresponding to the class implemented in the 
package source code. Depending on the type of device specified in the file, additional attributes may be required. All 
necessary attributes for each device type can be found in the 
[Device configuration guides](../reference/devices/supported_devices.md).

## Running flowchem

After create a file as the example above (or get it from the [examples folder](https://github.
com/cambiegroup/flowchem/tree/main/examples)) run the `flowchem` command followed by the name of the file.
```shell
flowchem flowchem_config.toml
```
```{warning}
Please note the correct file address and the name of the file you named.
```

In your terminal, you will see some debug information, ending with a line like this one:
```shell
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

This means that the flowchem server has been started correctly.
You can visit [http://127.0.0.1:8000](http://127.0.0.1:8000) to see a list of commands available for your test device.

```{note}
The device name is used as first subdirectory in the URL of the commands relative to this device.
For example, in this case, the commands relative to our test device will be available under `http://localhost:8000/example1/`.
```
```{note}
For every request sent to the flowchem server, you will see some diagnostic output in the terminal.
While you can normally ignore this output, it can provide useful information in case of errors.
```

If the user want to run a example file to operate a simulated device for educational purposes without 
requiring any connected device, simply execute:

```shell
flowchem example
```

## Device autoconfiguration
To be able to write a configuration file, you need to know the type of device you want to connect to and some connection
parameters.

Flowchem is capable of auto-detecting some devices and instrument, and to generate a valid configuration stub for them.
To find any device already connected to the PC where flowchem is installed, run the autodiscover tool:
```shell
flowchem-autodiscover
```
And reply to the prompts.
If any device that supports autodiscovery is found, a `flowchem_config.toml` file will be created.

```{note}
Some additional information is generally still necessary even for auto-detected devices.
```

Complete the missing information (if any) in this file, and then you will be ready to use flowchem!

```{note}
`flowchem_config.toml` is written in [TOML format](https://en.wikipedia.org/wiki/TOML),
the syntax of this language is intuitive and designed to be human-editable.
If you follow this guide you will not need to learn anything about the TOML syntax, but you can just copy and modify the
examples provided.
```

:::{note}
Not all the devices supported by flowchem can be auto discovered, so you might need to edit the configuration
file manually for some device types.
:::