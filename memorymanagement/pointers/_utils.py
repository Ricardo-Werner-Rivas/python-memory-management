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
            )
    if len(name)>1:
        print(f"{name}\nMultiple references found for the \"value\" parameter. First one was chosen")
        name=name[0]
    elif len(name)==1:
        name=name[0]
    elif len(name)==0:
        name=None
    return name