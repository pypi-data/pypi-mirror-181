"""JuMonC PluginManager!"""
import argparse
import importlib.util
import logging

import pluggy

from JuMonC import settings
from JuMonC.helpers.PluginManager import hookspec
from JuMonC.models import pluginInformation

logger = logging.getLogger(__name__)



plugin_manager = pluggy.PluginManager("JuMonC")
plugin_manager.add_hookspecs(hookspec)
plugin_manager.load_setuptools_entrypoints("JuMonC")


def addPluginArgs() -> argparse.ArgumentParser:
    pass

def evaluatePluginArgs(parsed:argparse.Namespace) -> None:
    logging.debug("%s", str(parsed))


def addPathPlugin(pluginPath:str) -> None:
    try:
        spec = importlib.util.spec_from_file_location("module.name", pluginPath)
        if spec is not None:
            module = importlib.util.module_from_spec(spec)
            loader = spec.loader
            if loader is not None:
                loader.exec_module(module)
            
            plugin_manager.register(module)
    except Exception:
        logger.warning("User plugin \"%s\" can not be imported", pluginPath)


def addAllPathsAsPlugins() -> None:
    for path in settings.PLUGIN_PATHS:
        addPathPlugin(path)
        
        
def initPluginsREST() -> None:
    for plugin in plugin_manager.get_plugins():
        plugin_REST_paths = plugin.needed_REST_paths()
        for path in plugin_REST_paths:
            # TODO check path
            plugin.register_REST_path(path, path)

        
def logAllPlugins() -> None:
    for plugin in plugin_manager.get_plugins():
        logger.info("Using Plugin: \"%s\" with canonical name: \"%s\"", str(plugin_manager.get_name(plugin)), str(plugin_manager.get_canonical_name(plugin)))
    
    
def setPluginsWorkingStatus() -> None:
    for plugin in plugin_manager.get_plugins():
        works = plugin.selfcheck_is_working()
        pluginInformation.addPluginStatus(str(plugin_manager.get_canonical_name(plugin)), works)
