import os
try: import json
except ImportError: import simplejson as json
import agent_util
import datetime

class PiHolePlugin(agent_util.Plugin):

    # TODO: Replace textkey and label with appropriate values
    textkey = "pihole"
    label = "Pi Hole"

    @classmethod
    def get_metadata(self, config):

        status = agent_util.SUPPORTED
        msg = None

        if not True:
            status = agent_util.MISCONFIGURED
            msg = "Status message"

        metadata = {
            "blocked.today": {
                "label": "Number of ads blocked today",
                "options": None,
                "status": status,
                "error_message": msg,
                "unit": None
            },
            "ad_traffic.today": {
                "label": "Percent of network traffic from ads",
                "options": None,
                "status": status,
                "error_message": msg,
                "unit": "percent"
            },
            "blacklisted_domains": {
                "label": "Number of known ad domains",
                "options": None,
                "status": status,
                "error_message": msg,
                "unit": None
            }
        }
        return metadata

    def check(self, textkey, data, config):
        ret, blocked = agent_util.execute_command("1m=$(date \"+%b %e\");cat /var/log/pihole.log | awk  '/\/etc\/pihole\/gravity.list/ {print $6}' | wc -l")
        ret, queries = agent_util.execute_command("today=$(date \"+%b %e\");cat /var/log/pihole.log | awk '/query/ {print $6}' | wc -l")
        ret, bldom = agent_util.execute_command("wc -l /etc/pihole/gravity.list")
        # Should really make this a bit faster/leaner but this is pretty fast and uncomplicated.
        if textkey == 'blocked.today':
            return float(blocked)

        if textkey == 'ad_traffic.today':
            return ((float(blocked) / float(queries)) * 100.0)

        if textkey == 'blacklisted_domains':
            return float(bldom.split()[0])

        return 0
