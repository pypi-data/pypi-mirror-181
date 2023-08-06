import logging

from aprsd import messaging, packets, plugin

import aprsd_slack_plugin
from aprsd_slack_plugin import base_plugin

LOG = logging.getLogger("APRSD")


class SlackNotifyPlugin(
    base_plugin.SlackPluginBase,
    plugin.APRSDWatchListPluginBase,
):
    """SlackNotifyPlugin."""

    version = aprsd_slack_plugin.__version__

    def process(self, packet):
        LOG.info("SlackCommandPlugin")

        fromcall = packet["from"]
        # message = packet["message_text"]

        is_setup = self.setup_slack()
        if not is_setup:
            return

        wl = packets.WatchList()
        if wl.is_old(packet["from"]):
            # get last location of a callsign, get descriptive name from weather service
            callsign_url = "<http://aprs.fi/info/a/{}|{}>".format(fromcall, fromcall)

            message = {}
            message["username"] = "APRSD - Slack Notification Plugin"
            message["icon_emoji"] = ":satellite_antenna:"
            message["attachments"] = [{}]
            message["text"] = "{} - Is now on APRS".format(callsign_url)
            message["channel"] = "#hemna"

            LOG.debug(message)

            # self.swc.chat_postMessage(**message)
            for channel in self.slack_channels:
                message["channel"] = channel
                self.swc.chat_postMessage(**message)

        # Don't have aprsd try and send a reply
        return messaging.NULL_MESSAGE
