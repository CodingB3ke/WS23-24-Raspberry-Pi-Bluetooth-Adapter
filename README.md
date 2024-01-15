# WS23-24-Raspberry-Pi-Bluetooth-Adapter
This is a university project for a Raspberry Pi lecture. The Raspberry Pi is used as a bluetooth adapter to upcycle old speakers that only have an AUX connection to be available with bluetooth.

# Usage
The bluetooth adapter was tested with different AUX devices:
- old, wired headphones
- speakers with AUX connector and USB-A power supply
- stereo system with AUX connector

If you encounter problems, please see the Troubleshooting section.

# Installation
1. Download Raspberry Pi Bullseye Lite (64-bit) (or newer)

*For us it didn't work with the 32-bit Version*

2. Enable SSH and connect to your wifi

3. This line adds a new software repository to the package sources. This is needed so that Pipewire and Wireplumber can be installed from the backports. In newer OS-Systems, such as bookworm, pipewire and wireplumber can be installed normally.

```
echo "deb https://deb.debian.org/debian/bullseye-backports main contrib non-free" | sudo tee /etc/apt/sources.list.d/bullseye-backports.list
```

Output on console line:

*deb https://deb.debian.org/debian/bullseye-backports main contrib non-free*

4. For the new repository GPG keys need to be added. This ensures that the packages are downloaded from a trusted source.
Open root-Shell with this command.
```
sudo -s
```
The selected directory in the terminal changes to:

*root@bluetoothAdapter:/home/piProject#*

5. Select the first key.
```
 gpg --keyserver keyserver.ubuntu.com --recv-keys 04EE7237B7D453EC
```
6. Add the key to packet manager.
```
gpg --export 04EE7237B7D453EC | sudo apt-key add -
```
In our case we got this warning on the console after adding the first key:
```
Warning: apt-key is deprecated. Manage keyring files in trusted.gpg.d instead (see apt-key(8)).
OK
```
This can be ignored.
7. Another GPG key needs to be selected
```
gpg --keyserver keyserver.ubuntu.com --recv-keys 648ACFD622F3D138
```
8. And then the key gets added.
```
gpg --export 648ACFD622F3D138 | sudo apt-key add -
```
Another warning occurs, but can be ignored:
```
Warning: apt-key is deprecated. Manage keyring files in trusted.gpg.d instead (see apt-key(8)).
OK
```
9. Now leave the root-shell by writing exit or use CTRL + D as a command
10. After that install pipewire and wireplumber by typing this in the console.
```
sudo apt -t bullseye-backports install pipewire wireplumber libspa-0.2-bluetooth
```
If this error message occurs, continue with step 11. If everything went smoothly continue with step 15: Reboot.
```
The value 'bullseye-backports' is invalid for APT::Default-Release as such a release is not available in the sources
```
11. First try the obvious
```
sudo apt upgrade
sudo apt update
```
12. Then try again adding the backports
```
echo "deb https://deb.debian.org/debian/bullseye-backports main contrib non-free" | sudo tee /etc/apt/sources.list.d/bullseye-backports.list
```
13. Now again updating and upgrading
```
sudo apt upgrade
sudo apt update
```
14. Try again installing pipewire and wireplumber. It should work now without error message.
```
sudo apt -t bullseye-backports install pipewire wireplumber libspa-0.2-bluetooth
```
15. **Reboot**

16. Install the DBus packages for Python
```
sudo apt install python3-dbus
```
17. Copy the speaker-agent.py script to your Raspberry Pi Home repository
18. Create a speaker-agent.service file
19. Copy the content of the speaker-agent.service file from this git into the service file and adjust the filepath to the speaker-agent.py according to your setup.
20. Move the service file into the systemd file
```
cd /../filepath/to/speaker-agent.service
sudo mv speaker-agent.service /etc/systemd/system
```
21. Start the service file:
```
sudo systemctl daemon-reload
sudo systemctl enable speaker-agent.service
sudo systemctl start speaker-agent.service
```
22. Now you should find your RaspberryPi in the list of bluetooth devices
23. Connect to the RaspberryPi with your smartphone/tablet/...
24. Connect your AUX speaker to the AUX-connector on the RaspberryPi
25. Start playing music

# Optional add LED for fatal errors:
This will create a service that checks if the speaker-agent.service started correctly. If it didn't the led starts blinking. This can help to check for a fatal error if SSH or a monitor is not available.
1. Connect a LED with the long leg to GPIO 13 and with the short leg to Ground
2. Copy fatalError-speaker-agent.py script to your Raspberry Pi
3. Create fatalError.service file
4. Copy the code from this git into the service file and adjust the filepath to the fatalError-speaker-agent.py according to your configuration.
5. Move the service file into the systemd file:
```
sudo mv fatalError.service /etc/systemd/system
```
7. Start the service
```
sudo systemctl daemon-reload
sudo systemctl enable fatalError.service
sudo systemctl start fatalError.service
```
# Troubleshooting:
## I see the raspberry pi in the device list, but pairing doesn't work.

Check with the follwing command if your device was paired and if services are authorized or rejected. In the journal the MAC address is used so you have to check your devices MAC address.

If services were denied, disconnect and wait for a few minutes. Afterwards connect again and also wait a little bit. Check the journal again. Your services should be authorized.
```
journalctl -xe -u speaker-agent.service
```

## The music is playing from my own device not from the speaker.

Try to change the replay device in your music app. Sometimes (especially the first time) it takes a while until your device recognizes the raspberry pi as a replay device. Try again but wait a few minutes between disconnecting and reconnecting. Also wait a few moments before trying to play music, because the authorization of services might take a moment.

- Check with the following command if your device's MAC address is listed in the tree.
```
busctl tree org.bluez
```

- Also check with journalctl if your device is connected and services are authorized.
```
journalctl -xe -u speaker-agent.service
```

## There is a constant buzzing coming from my speaker.
- Quick and dirty fix: Try adjusting the 3.5mm AUX by pulling it out a little bit. Play around and see if it fixes the problem.
- Else: Open the config.txt on the Raspberry Pi and change the line hdmi_force_hotplug to 1 or uncomment it if it has a # in front of it
- Else: Buy a ground loop isolator. Around 12€ on Amazon
- Alternative: you can buy a sound card for your Pi. That also improves the overall sound quality

  # Authors and acknowledgements
We are a group of four people who worked on this project for our RaspberryPi course at HAW Hamburg in the Wintersemester23/24.
  
This project is based on this [GitHub project](https://github.com/fdanis-oss/pw_wp_bluetooth_rpi_speaker), which was very helpful.
We also got a lot of infos from [here](https://ukbaz.github.io/howto/python_gio_1.html).
