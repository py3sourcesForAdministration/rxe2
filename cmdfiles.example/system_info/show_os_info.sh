ID="`id -un`"
echo -n "Hostname              : "
hostname -f
echo -n "IP Address            : "
hostname -i
echo "Connected as          : $ID"
echo "--"
echo "OSversion             : "
if [ -e /etc/os-release ] ; then
  cat /etc/os-release
elif [ -e /etc/SuSE-release ] ; then
  cat /etc/SuSE-release
else  
  lsb_release -d
fi  
echo -n "arch                  : "
uname -m
echo -n "kernel                : "
uname -r
echo "--"
