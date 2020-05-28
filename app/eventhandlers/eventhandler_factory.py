from typing import List
import importlib

import dacite

from app.eventhandlers.eventhandler import EventHandler
from app import config


_eventhandlers: List[EventHandler] = []


def build_eventhandlers() -> List[EventHandler]:
    """
    For each eventhandler in the config.eventhandlers list this should do the following:
    * Attempt to find the class of the eventhandler from MetaEventHandler.eventhandler_script
    * Attempt to find the generic type for the eventhandlers config object
    * Attempt to deserialized the config object from the MetaEventhandler.config to the generic type
    * Attempt to instanciate the EventHandler, passing in the name from MetaEventHandler.name and deserialized config object
    @return: The list of instanciated EventHandler objects.
    """
    global _eventhandlers

    _eventhandlers = []

    for meta_eventhandler in config.eventhandlers:
        class_name = meta_eventhandler.eventhandler_script.split('.')[-1]
        module_name = '.'.join(meta_eventhandler.eventhandler_script.split('.')[:-1])
        module = importlib.import_module(module_name)
        clazz = getattr(module, class_name)

        eventhandler_config_class = clazz.__orig_bases__[0].__args__[0]

        eventhandler_config = dacite.from_dict(eventhandler_config_class, meta_eventhandler.config)

        eventhandler = clazz(meta_eventhandler.name, eventhandler_config)
        _eventhandlers.append(eventhandler)

    return _eventhandlers
