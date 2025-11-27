"""
This hidden module provides useful functions for the pointers' implementation
"""
#* FUNCTIONS
# Reference finder
def ref_finder(value,vars_dict:dict[str,])->str:
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
    return name