# path
logPath="/opt/logs/dinglive"
if [ ! -d "$logPath" ]; then
    mkdir "$logPath"
fi

# supervidord
supervisord -c /opt/dinglive/supervisord.conf
