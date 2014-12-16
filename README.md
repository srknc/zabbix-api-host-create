zabbix-host-create
==================

creates host at the zabbix server thanks to zabbix api


- it gets all parameters from command line, just execute it to see usage
- if there is http authentication in front of zabbix api, you need to pass credential, otherwise just pass something, it won't fail.
- last function creates maintanence for 10 minutes to avoid from initial alert.
