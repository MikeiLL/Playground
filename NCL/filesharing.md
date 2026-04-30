# File Sharing with VM Ware on Windows

YouTube video is _partially_ helpful. https://www.youtube.com/watch?v=lf2aefwlWe8

However: https://unix.stackexchange.com/a/694560/68860

```
cd /mnt/hgfs
```

If the folder is missing --> `sudo mkdir hgfs`

```
sudo vim /etc/fstab
```

Enter `vmhgfs-fuse /mnt/hgfs fuse defaults,allow_other,nofail 0 0` at the end of the file and save

```
sudo reboot now
ls /mnt/hgfs
```

The Shared Folder you enabled in VMware Fusion Settings will appear

This is also a good command to be aware of: `vmware-hgfsclient`


