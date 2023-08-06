"""
    handles the site settings
"""
from reva.lib.site_settings.update import SiteSettingsUpdate
from reva.lib.site_settings.list import list_sitesettings_json_files

class SiteSettings:
    """
        handles the site settings
    """
    def __init__(self, arguments):
        self.argument = arguments

    def run(self):
        """
            THis function will separate the actions
        """
        if self.argument.action == "update":
            SiteSettingsUpdate(self.argument).start()
        if self.argument.action == "list":
            list_sitesettings_json_files(SiteSettingsUpdate(self.argument))


    def __str__(self) -> str:
        pass
