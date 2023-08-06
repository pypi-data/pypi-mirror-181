"""
    List the workflow json files
"""
from reva.lib.workflow.update import WorkflowUpdate

def list_workflow_json_files(workflow_update_obj :WorkflowUpdate):
    """
        list the workflow json files
    """
    list_of_files = workflow_update_obj.get_workflow_json_paths_to_update()
    for file_path in list_of_files:
        print(file_path)
