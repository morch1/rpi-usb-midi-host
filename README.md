# rpi-usb-midi-host
turn a Raspberry Pi Zero into a USB MIDI host device for your synths and sequencers

this script was created for the following hardware specifically:
- [Raspberry Pi Zero W](https://www.raspberrypi.com/products/raspberry-pi-zero-w/)
- [Waveshare 4 port USB hub hat](https://www.waveshare.com/usb-hub-hat.htm)

it may need to be modified to work with other models

## how to use
1. create config file

    config file should be called `/boot/midihost/midihost_config.py`  
    (look below for examples)

1. make the script auto-run when Raspberry Pi boots

    ```
    # /etc/rc.local
    ...

    sudo python /home/pi/rpi-usb-midi-host/attach_midi.py

    exit 0
    ```

1. make the script auto-run when devices are connected

    one way is to create udev rules for your devices:

    ```
    # /etc/udev/rules.d/midihost.rules

    # op1
    ACTION=="add", ATTRS{idVendor}=="2573", ATTRS{idProduct}=="001a", RUN+="/home/pi/rpi-usb-midi-host/attach_midi.py"

    # keystep
    ACTION=="add", ATTRS{idVendor}=="1c75", ATTRS{idProduct}=="0288", RUN+="/home/pi/rpi-usb-midi-host/attach_midi.py"

    # circuit tracks
    ACTION=="add", ATTRS{idVendor}=="1235", ATTRS{idProduct}=="0139", RUN+="/home/pi/rpi-usb-midi-host/attach_midi.py"

    # microfreak
    ACTION=="add", ATTRS{idVendor}=="1c75", ATTRS{idProduct}=="0601", RUN+="/home/pi/rpi-usb-midi-host/attach_midi.py"
    ```

1. (optional) enable read-only filesystem using `raspi-config`

    this will let you unplug the power of your raspberry pi without having to shut it down and without having to worry about corrupting the sd card

## config examples
the file `/boot/midihost/midihost_config.py` should define a variable called `CONNECTIONS` containing a list of MIDI connections that will be made. each connection should be provided as follows:
```
((source usb port, src midi port), (destination 1 usb port, dst 1 midi port), (destination 2 usb port, dst 2 midi port), ...)
```
- the first value in each tuple is the ID of the usb port (they are labeled on the PCB of the Waveshare USB hub hat)
- the second value should usually be `0` unless the connected USB device provides more than one MIDI port

here are some examples:
```
# use device connected to usb port 1 as midi input and usb ports 2-4 as midi outputs
CONNECTIONS = [
    ((1,0), (2,0), (3,0), (4,0)),
]
```
```
# connect 4 usb ports to each other (all data coming from each usb midi port will be sent to the other usb midi ports)
CONNECTIONS = [
    ((1,0), (2,0), (3,0), (4,0)),
    ((2,0), (1,0), (3,0), (4,0)),
    ((3,0), (1,0), (2,0), (4,0)),
    ((4,0), (1,0), (2,0), (3,0)),
]
```
