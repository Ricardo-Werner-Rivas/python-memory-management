"""
This hidden module internally provides useful functions for the pointers' implementation.\n
Do **NOT** import and/or use this module directly
"""
#* FUNCTIONS
# Reference finder
def ref_finder(value,vars_dict:dict[str,])->list:
    """
    Prints all the references pointing to the passed value.\n
    ---
    Arguments:
        value (`Any`): Value to track
        vars_dict (`dict[str,Any]`): Dictionary of variables of the desired enviroment
    Returns:
        list: List of references pointing to the given value
    """
    name=[]
    for key,v in vars_dict.items():
        try:
            if v is value:
                name.append(key)
        except ValueError:
            pass
        except Exception as excep:
            raise type(excep)(
                f"""A fatal error occured.
                Please report this error in our issues page: https://github.com/Ricardo-Werner-Rivas/memorymanagement/issues
                
                Include the following error message in your report: \"{excep}\"
                """
            ) from None
    return [None] if len(name)==0 else name