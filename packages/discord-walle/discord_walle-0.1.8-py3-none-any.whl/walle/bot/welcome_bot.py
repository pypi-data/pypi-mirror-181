from base import BaseBot


class WelcomeBot(BaseBot):
    """Welcome Bot

    The purpose of this welcome bot
    will be a endpoint for any interaction involving
    events and/or actions that are associated with
    welcome to servers/channels/clans/groups/etc

    Parameters
    ----------

    action_config : ActionConfig(Config)
        A typed/defined action config that will
        have a predefined set of supported Primitive OPs

    event_config : EventConfig(Config)
        A typed/defined event config that will
        have a predefined set of supported Primitive OPs

    name : str
        the name of this specific bot

    Usage
    -----

    ```python

    from walle.configs import ActionConfig, EventConfig
    from walle.bot import WelcomeBot

    action_cfg = ActionConfig("welcome-actions")
    event_cfg = EventConfig("welcome-events")
    welcome_bot = WelcomeBot(
        action_config=action_cfg,
        event_cfg=event_cfg,
        name=name,
    )
    ```

    Notes
    -----

        The idea of config classes may change as we develop
            the basic idea seems sounds, but could be an entire rewrite

        We dont have a firm grasp on the scope of each bot, this is
            one direction we can go with it
    """

    def __init__(
        self,
        action_config,
        event_config,
        name="welcome-bot",
    ):
        super().__init__(
            action_config=action_config,
            event_config=event_config,
            name=name,
        )
