import logging

from slack_sdk import WebClient

import aprsd_slack_plugin

LOG = logging.getLogger("APRSD")


class SlackPluginBase:
    """SlackCommandPlugin.

    This APRSD plugin looks for the location command comming in
    to aprsd, then fetches the caller's location, and then reports
    that location string to the configured slack channel.

    To use this:
        Create a slack bot for your workspace at api.slack.com.
        A good source of information on how to create the app
        and the tokens and permissions and install the app in your
        workspace is here:

            https://api.slack.com/start/building/bolt-python


        You will need the signing secret from the
        Basic Information -> App Credentials form.
        You will also need the Bot User OAuth Access Token from
        OAuth & Permissions -> OAuth Tokens for Your Team ->
        Bot User OAuth Access Token.

        Install the app/bot into your workspace.

        Edit your ~/.config/aprsd/aprsd.yml and add the section
        slack:
            signing_secret: <signing secret token here>
            bot_token: <Bot User OAuth Access Token here>
            channel: <channel name here>
    """

    version = aprsd_slack_plugin.__version__

    def setup_slack(self):
        """Create the slack require client from config."""

        # signing_secret = self.config["slack"]["signing_secret"]
        try:
            self.config.exists(["services", "slack", "bot_token"])
        except Exception as ex:
            LOG.error("Failed to find config slack:bot_token {}".format(ex))
            return "No slack bot_token found"

        bot_token = self.config["services"]["slack"]["bot_token"]
        if not bot_token:
            LOG.error(
                "APRSD config is missing slack: bot_token:<token>. "
                "Please install the slack app and get the "
                "Bot User OAth Access Token.",
            )
            return False

        self.swc = WebClient(token=bot_token)
        self.slack_channels = self.config["services"]["slack"].get("channels", None)
        if not self.slack_channels:
            LOG.error(
                "APRSD config is missing slack: channels: <name> "
                "Please add a slack channel name to send messages.",
            )
            return False

        return True
