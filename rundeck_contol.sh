#!/bin/bash

IP_Config_file1=@option.IpListFiles1@
IP_Config_file2=@option.IpListFiles2@
username=@option.username1@
password=@option.password1@
enable_password=@option.enable_password1@

echo "your Input: "
echo "  ip:              ${ip}"
echo "  username:        ${username}"
echo "  password:        ******"
echo "  enable_password: ******"

#array=(${IP_Config_files//;/ })
#for IP_Config_file in ${array[@]}
#do
#    echo "Configure File:  $IP_Config_file"
#done
cd /appset/script/failover/test_failoverProcess/
#cat /appset/script/failover/test_failoverProcess/command/$IP_Config_file | grep -v '^#'| grep -v '^\s*$' | while read IpInfo
#do
#    Device_Name=`echo $IpInfo | awk -F ' ' '{ print $1}'`
#    ip=`echo $IpInfo | awk -F ' ' '{ print $2}'`
#    Command_File=`echo $IpInfo | awk -F ' ' '{ print $3}'`
#    echo "Device: $Device_Name  $ip  $Command_File "
#done


python /appset/script/failover/test_failoverProcess/main_kxr1.py ${username} ${password} ${enable_password} ${IP_Config_file1} ${IP_Config_file2}