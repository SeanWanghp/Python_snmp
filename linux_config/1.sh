#!/usr/bin/env bash
ip="10.245.47.10"
ip_gpon="10.245.46.208"
echo $ip
function main(){
	(sleep 3;echo "root";
	sleep 2;echo "root";
	sleep 2;echo "cli";
	sleep 2;echo "cli";
	sleep 2;echo "show card";
	sleep 2;echo "show version";
	sleep 2;echo "pag false";
	sleep 2;echo "show inter line sum";
	sleep 10;echo 'exit';
	sleep 2)|telnet $ip
}
echo "script run start, plase wait....."
echo "Start time:"
uptime
date
main
echo "script stop, please check above result"
if [ $ip_gpon -o true ]
then
	for a in {1}
		do 
			snmpwalk -v2c -cpublic $ip_gpon 1.3.6.1
		done
fi

