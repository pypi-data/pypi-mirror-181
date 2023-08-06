"""
    List the loan products json files
"""
from reva.lib.loan_productus.update import LoanProductsUpdate

def list_loanproducts_json_files(loan_products_update_obj :LoanProductsUpdate):
    """
        list the loan products json files
    """
    list_of_files = loan_products_update_obj.get_loan_productus_json_paths_to_update()
    for file_path in list_of_files:
        print(file_path)
