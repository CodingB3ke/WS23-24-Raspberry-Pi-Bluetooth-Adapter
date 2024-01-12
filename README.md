# WS23-24-Raspberry-Pi-Bluetooth-Adapter
This is a university project for a Raspberry Pi lecture. The Raspberry Pi is used as a bluetooth adapter to upcycle old speakers that only have an AUX connection to be available with bluetooth.

Instructions for set up:
1. Download Raspberry Pi Bullseye Lite (64-bit) (or newer)
2. Enable SSH and connect to your wifi
3. echo "deb https://deb.debian.org/debian/bullseye-backports main contrib non-free" | sudo tee /etc/apt/sources.list.d/bullseye-backports.list
**deb https://deb.debian.org/debian/bullseye-backports main contrib non-free**
4. sudo -s *root-Shell opens up*
*root@bluetoothAdapter:/home/piProject#*
5. gpg --keyserver keyserver.ubuntu.com --recv-keys 04EE7237B7D453EC
6. gpg --export 04EE7237B7D453EC | sudo apt-key add -
*Warning: apt-key is deprecated. Manage keyring files in trusted.gpg.d instead (see apt-key(8)).*
*OK*
7. gpg --keyserver keyserver.ubuntu.com --recv-keys 648ACFD622F3D138
8. gpg --export 648ACFD622F3D138 | sudo apt-key add -
*Warning: apt-key is deprecated. Manage keyring files in trusted.gpg.d instead (see apt-key(8)).*
*OK*
9. exit or CTRL + D
10. sudo apt -t bullseye-backports install pipewire wireplumber libspa-0.2-bluetooth
* The value 'bullseye-backports' is invalid for APT::Default-Release as such a release is not available in the sources*
THIS IS BAD... if it worked continue at step 17 with reboot of system
11. sudo apt upgrade
12. sudo apt update
13. echo "deb http://deb.debian.org/debian bullseye-backports main contrib non-free" | sudo tee /etc/apt/sources.list.d/bullseye-backports.list
14. sudo apt update
15. sudo apt upgrade
16. sudo apt -t bullseye-backports install pipewire wireplumber libspa-0.2-bluetooth
17. Reboot
18. sudo apt install python3-dbus
19. Copy speaker-agent.py script to your Raspberry Pi
20. Create speaker-agent.service file
21. Copy the code from this git into the service file and adjust the filepath to the speaker-agent.py according to your configuration.
22. Move the service file into the systemd file: sudo mv speaker-agent.service /etc/systemd/system
23. sudo systemctl daemon-reload
24. sudo systemctl enable speaker-agent.service
25. sudo systemctl start speaker-agent.service
26. Now you should find the raspberry pi in the list of bluetooth devices
27. Connect to the raspberry pi with your smartphone/tablet
28. Connect your AUX speaker to the AUX-connector on the raspberry pi
29. Start playing music

Optional add LED for fatal errors:
This will create a service that checks if the speaker-agent.service started correctly. If it didn't the led starts blinking. This can help to check for a fatal error if SSH or a monitor is not available.
1. Connect a LED with the long leg to GPIO 13 and with the short leg to Ground
2. Copy fatalError-speaker-agent.py script to your Raspberry Pi
3. Create fatalError.service file
4. Copy the code from this git into the service file and adjust the filepath to the fatalError-speaker-agent.py according to your configuration.
5. Move the service file into the systemd file: sudo mv fatalError.service /etc/systemd/system
6. sudo systemctl daemon-reload
7. sudo systemctl enable fatalError.service
8. sudo systemctl start fatalError.service

Troubleshooting:
- I see the raspberry pi in the device list, but pairing doesn't work.
  Check with "journalctl -xe -u speaker-agent.service" if your device was connected and if maybe services have been denied. Try again.

- The music is playing from my own device not from the speaker.
  Try to change the replay device in your music app. Sometimes (especially the first time) it takes a while until your device recognizes the raspberry pi as a replay device. Try disconnecting and connecting again.
  Check with "busctl tree org.bluez" (in raspberry terminal) if your device's MAC address is listed in the tree.
  Check with "journalctl -xe -u speaker-agent.service" if your device is connected.

- There is a constant buzzing coming from my speaker.
  Easy and cheap way: Try adjusting the 3.5mm AUX by pulling it out a little bit. Play around and see if it fixes the problem.
  Else: Open the config.txt on the Raspberry Pi and change the line hdmi_force_hotplug to 1 or uncomment it if it has a # in front of it
  Else: Buy a ground loop isolator. Around 12€ on Amazon
  Alternative: you can buy a sound card for your Pi. That also improves the overall sound quality
