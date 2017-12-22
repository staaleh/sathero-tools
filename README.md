# SatHero tools

Some tools to read and write transponder-lists for Sathero SAT/DVB signal meters. Currently SH1x0HD and SH3x0HD series is "supported".

## Motivation

To update transponder-lists for these satellite meters, only a Windows tool is provided by the manufacturer. That tool converts Excel files to their binary format, and did not wan't to function in my case, neither in Windows10 nor Linux(wine).

The file-format is mostly deciphered and a generator implemented in Python. Due to the lack of documentation of the format problems might occur, however it seem to work as expected.


## Prerequisites

* Satellite transponder data (.ini or xml)
* Python3
* python3-lxml if you use xml files

## Getting started

Download (or create) and edit your preferred satellites and transponders using data from e.g. http://satellites-xml.eu or http://www.fastsatfinder.com.
Both .ini and .xml is supported.

### For .ini files, place them in a folder and run the command:

./ini2bin.py &lt;version of meter&gt; &lt;folder-name with ini files&gt;

e.g.


```
./ini2bin.py sh300hd examples/ini/

```

The should result in a file named sh300hd_<todays date> in the bin folder. This file can now be transferred to the meter.


### For .xml files, place them in a folder and run the command:

./xml2bin.py &lt;version of meter&gt; &lt;xml-file&gt;

e.g.

```
./xml2bin.py sh300hd examples/satellites.xml

```

This should result in a file named sh300hd_<todays date> in the bin folder. This file can now be transferred to the meter.

**Note: Some meters (SH1x0HD) will have very limited space for transponders (max 255), and the software will fail to generate files if there are too many**


### Transferring file to the Satellite meter

#### For devices with USB interface:

* Connect the USB cable between the computer and meter while the meter is turned off. 
* Turn the meter on, the computer should detect it as a new disk drive. 
* Copy the file from the computer to the new disk
* Wait some seconds, then unmount (safe removal) the drive from your computer
* Disconnect the USB cable
* Turn off the satellite meter
* Turn the meter back on, the file should now be loaded

**Note: For some reason the method sometimes fails on my meter on Ubuntu Linux, and the new file is not loaded even if everything goes according to plan. Often it seem help to try to unplug the USB after un-mounting the drive, re-insetting the cable and transferring the file once more before turning the meter off and on.**


#### For devices with Serial interface:

No solution provided as of now. Try the Windows tool.


## Authors

* **Staale Helleberg** (https://github.com/staaleh)


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
