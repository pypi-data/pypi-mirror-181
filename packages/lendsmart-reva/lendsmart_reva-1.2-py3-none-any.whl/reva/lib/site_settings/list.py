"""
    List the site setting json files
"""
from reva.lib.site_settings.update import SiteSettingsUpdate

def list_sitesettings_json_files(sitesettings_update_obj :SiteSettingsUpdate):
    """
        list the sitesettings json files
    """
    list_of_files = sitesettings_update_obj.get_site_settings_json_paths_to_update()
    for file_path in list_of_files:
        print(file_path)
