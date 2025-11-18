┌──(kali㉿kali)-[~/username-anarchy-master]
└─$ ./username-anarchy Betty Jayde       
betty
bettyjayde
betty.jayde
bettyjay
bettjayd
bettyj
b.jayde
bjayde
jbetty
j.betty
jaydeb
jayde
jayde.b
jayde.betty
bj


┌──(kali㉿kali)-[~/test]
└─$ sudo netexec ssh 10.129.234.116 -u usery  -p 'Texas123!@#'                       
[sudo] password for kali: 
SSH         10.129.234.116  22     10.129.234.116   [*] SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.13
SSH         10.129.234.116  22     10.129.234.116   [-] betty:Texas123!@#
SSH         10.129.234.116  22     10.129.234.116   [-] bettyjayde:Texas123!@#
SSH         10.129.234.116  22     10.129.234.116   [-] betty.jayde:Texas123!@#
SSH         10.129.234.116  22     10.129.234.116   [-] bettyjay:Texas123!@#
SSH         10.129.234.116  22     10.129.234.116   [-] bettjayd:Texas123!@#
SSH         10.129.234.116  22     10.129.234.116   [-] bettyj:Texas123!@#
SSH         10.129.234.116  22     10.129.234.116   [-] b.jayde:Texas123!@#
SSH         10.129.234.116  22     10.129.234.116   [-] bjayde:Texas123!@#
SSH         10.129.234.116  22     10.129.234.116   [+] jbetty:Texas123!@#  Linux - Shell access!


┌──(kali㉿kali)-[~]
└─$ ssh jbetty@10.129.234.116  


jbetty@DMZ01:~$ cat .bash_history 
cd ~/projects
ls
git status
git pull origin main
vim README.md
cat ~/.bashrc
sudo apt update
sudo apt upgrade -y
clear
cd ~/Downloads
ls -lh
rm -rf old_project/
mkdir temp
cd temp
touch test.py
nano test.py
python3 test.py
pip install requests
pip install flask
history
df -h
free -m
top
htop
sshpass -p "dealer-screwed-gym1" ssh hwilliam@file01
sudo systemctl status apache2
sudo systemctl restart apache2
cd /etc/nginx/sites-available
ls
cat default
sudo nano default
sudo nginx -t
sudo systemctl reload nginx
cd ~
mkdir scripts
cd scripts
vim backup.sh
chmod +x backup.sh
./backup.sh
ssh user@192.168.0.101
scp file.txt user@192.168.0.101:~/Documents/
logout
exit
cd /var/log
ls -ltr
sudo tail -f syslog
sudo journalctl -xe
sudo dmesg | less
ps aux | grep python
kill -9 13245
git clone https://github.com/example/repo.git
cd repo
ls -a
code .
npm install
npm run dev
cd ..
rm -rf repo/
curl https://ipinfo.io
ping google.com
traceroute github.com
whoami
groups
sudo adduser testuser
sudo usermod -aG sudo testuser
su - testuser
exit
passwd
uptime
reboot
mkdir ~/backup
rsync -av ~/Documents/ ~/backup/
du -sh *
alias ll='ls -alF'
unalias ll
history | grep ssh
find . -name "*.log"
grep -r "ERROR" /var/log/
awk '{print $1}' access.log | sort | uniq -c | sort -nr | head
chmod 755 script.sh
chown user:user script.sh
git checkout -b feature/login
git commit -am "Add login feature"
git push origin feature/login
git merge main
git push
git log --oneline
docker ps
docker images
docker run -it ubuntu bash
exit
cd /tmp
touch index.html
echo "<h1>Hello World</h1>" > index.html
cat index.html
python3 -m http.server
curl localhost:8000
ctrl+c
tmux
tmux new -s dev
tmux ls
tmux attach -t dev
tmux kill-session -t dev
man rsync
man chown
crontab -e
lsblk
mount
umount /dev/sdb1
lsusb
lscpu
sudo apt install tree
tree
zip -r archive.zip folder/
unzip archive.zip
wget http://example.com/file.zip
tar -xzvf file.tar.gz
tar -czvf archive.tar.gz folder/
logout

clear
ls -l
clear
ls -l
clear
nano .bash_history
su
clear
ls -l
nano .bash_history
echo > .bash_history
nano .bash_history
less .bash_history 
clear
exit
pwd
cat .bash_history 
exit
