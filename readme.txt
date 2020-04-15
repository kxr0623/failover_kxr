Project: Failover
History:
    v1.0 -20190707
    v1.2 -20191914: Device.py add special handle method for [juniper Device].

Structure:
    rundeck_control.sh: the shell is run on rundeck to strike the Main.py everyday.
    Main-kxr.py :  the main program of this project.
    Command.py: Get commands from configure files. and ensure the command is valid.
    Device.py: connect network divices.
    Globle_Variables.py: set globle variables.  (unused)
    Write_To_Log.py: record all output log of the program in Log files. 
Usage:
    1. configure what network divices you are going to run in device-list-file
        [DeviceName]  [Device_IP]   [ Full Path to Commands_file]

        (Note: all devices in this device-list-file will run concurrently.)
        You can config a couple of device-list-files to make them run serially.

    2. write the commands that need to be run on Device in Command_file.
    3. Run the program:
    python main.py <username> <password> <enable_password>  <device list file>*n



Progress:
1. testing Envirnment
    Python code: done; 
    rundeck deployment: done; 
    But it was cancelled, because the net is so complicated, can not change from HK to ShenZhen.
    SFTP net change Configure Files: DONE

2. Product Envirnment
    Python code: done; 
    rundeck deployment: put test job of UPI_HKQWSW01547/548  UPI_CNSZSW01547/1548, in order to test python code can run.
    SFTP net change Configure Files: DONE
    TODO: get net-code from ZhuBinQuan and deploy them on Rundeck Job.

