# Python script for Stresing cameras

In this repository you can find the python module *stresing* for operating [Stresing](https://stresing.de) cameras. This is located in the folder `stresing/`. You can find examples how to use this module in the folder `example/`

![screenshot of the plot](./screenshot/graph.png)

## Dependencies
* [Python 3](https://www.python.org/)
* [Microsoft Visual C++ Redistributable](https://aka.ms/vs/16/release/vc_redist.x64.exe) to use the DLL
* [ctypes](https://pypi.org/project/ctypes/)
* [matplotlib](https://pypi.org/project/matplotlib/)

## DLL source
The source code of the DLL ESLSCDLL.dll can be found in the repository [EBST_CAM](https://github.com/Entwicklungsburo-Stresing/EBST_CAM).

## Documentation
The script is following the basic operation as described in the chapter *How to operate Stresing cameras* of the [software documentation](https://entwicklungsburo-stresing.github.io/). The settings must match your camera system. You can find a description of every setting [here](https://entwicklungsburo-stresing.github.io/structmeasurement__settings.html).

## Examples
You can run examples with
```
python -m examples.simple_blocking_measurement
```

## Installing as module
You can install the module stresing with
```
pip install -e .
```

## License
The python module *stresing* is licened under the LPGL-3. All examples in the folder `examples/` are published as public domain under the Unlicense.
