"""
    Base class for reva
"""
from reva.conf.reva import load_conf
from reva.lib.client.builder import ClientBuilder
from reva.lib.utils.get_json_files import JsonFileGetter
from reva.lib.utils.get_paths import PathGetter
from reva.lib.base.run_query import RunQuery
from reva.exception import ConfigNotFoundError


class RevaBase(PathGetter, JsonFileGetter, RunQuery):
    """
    Reva base class
    """

    def __init__(self, argument):
        self.argument = argument
        self.conf = load_conf(argument)
        if not self.conf:
            raise ConfigNotFoundError(
                "No config found for " + argument.env
            )
        self.client_builder = ClientBuilder(self.conf)
        self.graphql_client = self.client_builder.graphql_client()
