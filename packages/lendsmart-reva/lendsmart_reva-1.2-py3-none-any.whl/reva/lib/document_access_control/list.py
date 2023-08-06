"""
    List the document access control json files
"""
from reva.lib.document_access_control.update import DocumentAccessControlUpdate


def list_document_acc_control_json_files(
    document_acc_control_update_obj: DocumentAccessControlUpdate,
):
    """
    list the document access control json files
    """
    list_of_files = document_acc_control_update_obj.get_json_paths_to_update()
    for file_path in list_of_files:
        print(file_path)
