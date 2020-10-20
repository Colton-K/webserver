# first argument has to be on or off, then client
# EX: ./control.sh off 192.168.2.1 on 192.168.10.2
for var in $@
do
    if [ $var == "on" ] || [ $var == "off" ]
    then
        state=$var
        # echo "$state"
    else
        echo "$var : $state" 
        ./tplink_smartplug.py -t $var -c $state
    fi
done