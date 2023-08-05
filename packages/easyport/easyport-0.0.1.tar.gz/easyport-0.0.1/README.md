This tool allows for connecting your Festo Didactic Easyport to your machine.

`from easyport import epconnector as Ep`

USB Connection:
You have to make sure you can read / write your USB device. Either give group permissions to your user or add user to dialout group. 

`Ep.FtdiConnector(setup=True)`:
class for hardware connection to the Easyport. Only needed if usb connection is not possible.

`Ep.BasicEasyport(filepath=Savefile)`:
Basic class to send/receive from EasyPort.