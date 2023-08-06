import yaml
from os.path import dirname, abspath, join

from typing import Any, Dict

from dependency_injector import containers, providers

from p360_export.ExportManager import ExportManager
from p360_export.config.SkeletonConfigGetter import SkeletonConfigGetter
from p360_export.containers.Core import Core
from p360_export.containers.DataPlatformContainer import DataPlatformContainer
from p360_export.containers.FacebookContainer import FacebookContainer
from p360_export.containers.GoogleAdsContainer import GoogleAdsContainer
from p360_export.containers.SFMCContainer import SFMCContainer


class Container(containers.DeclarativeContainer):
    __self__ = providers.Self()
    config = providers.Configuration()
    skeleton_config_getter = providers.Singleton(SkeletonConfigGetter)

    core = providers.Container(Core, config=config)

    dataplatform = providers.Container(DataPlatformContainer, config=config, core=core)
    facebook = providers.Container(FacebookContainer, config=config, core=core)
    sfmc = providers.Container(SFMCContainer, config=config, core=core)
    google_ads = providers.Container(GoogleAdsContainer, config=config, core=core)

    manager = providers.Singleton(ExportManager, container=__self__)


def get_local_config():
    local_config_path = join(dirname(dirname(abspath(__file__))), "_config", "config.yaml")

    with open(local_config_path, "r", encoding="utf-8") as stream:
        local_config = yaml.safe_load(stream)
        return local_config["parameters"]


def set_skeleton_config(container):
    skeleton_config = container.skeleton_config_getter().get()
    container.config.from_dict(skeleton_config)


def init_container(export_config: Dict[str, Any]):
    container = Container()

    container.config.from_dict(get_local_config())
    container.config.from_dict(export_config)

    container.wire(modules=[__name__])

    return container
