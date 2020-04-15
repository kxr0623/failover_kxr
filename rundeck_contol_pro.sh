#!binbash

IP_Config_file1=@option.IpListFile1@
IP_Config_file2=@option.IpListFile2@
username=@option.username@
password1=@option.password1@   #password
enable_password=@option.password2@    #enable_password

echo "your Input: "
echo   username        ${username}
echo   password1    ****
echo   password2    ****

if [ 'a'${password1} != 'a'${enable_password} ]; then
    echo "[Password Error] The Second Password != The First Password!!!"
    exit 1
fi

#array=(${IP_Config_files; })
#for IP_Config_file in ${array[@]}
#do
#    echo Configure File  $IP_Config_file
#done

cd /appset/script/failover
#cat appsetscriptfailovertest_failoverProcesscommand$IP_Config_file  grep -v '^#' grep -v '^s$'  while read IpInfo
#do
#    Device_Name=`echo $IpInfo  awk -F ' ' '{ print $1}'`
#    ip=`echo $IpInfo  awk -F ' ' '{ print $2}'`
#    Command_File=`echo $IpInfo  awk -F ' ' '{ print $3}'`
#    echo Device $Device_Name  $ip  $Command_File
#done


python /appset/script/failover/main.py ${username} ${password1} ${enable_password} ${IP_Config_file1}  ${IP_Config_file2}