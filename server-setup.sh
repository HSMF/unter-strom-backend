#!/bin/bash
serviceName="UMD-reader"
# probably: serviceFile=/etc/systemd/system/${serviceName}.service
serviceFile=
# touch $serviceFile

username=
srcPath=

if [[ -z "$username" || -z "$srcPath" || -z "$serviceName" || -z "$serviceFile" ]];then
    echo "[x] Please set the variables in $0" >&2
    exit 1
fi

cat << EOS > $serviceFile
[Unit]
Description=[en] Script to download current power measurements and upload them to a mysql database | [de] Skript, welches Produktion der Solarzellen liest und auf eine Mysql Datenbank hochlädt
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=3
User=$username
ExecStart=$(which python3) $srcPath

[Install]
WantedBy=multi-user.target
EOS


systemctl start $serviceName
systemctl enable $serviceName
