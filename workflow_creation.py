from snowflake.snowpark import Session
from snowflake.snowpark.types import DataType

def register_stored_procedure(
    session: Session,
    func: callable,
    return_type: DataType,
    input_types: list[DataType],
    name: str,
    stage_location: str,
    imports_path: str,
    replace: bool = True,
    is_permanent: bool = True,
    
):
    """
    Registers a stored procedure in Snowflake from a Python function.
    
    Args:
        session (Session): Snowpark session
        func (callable): Python function to register
        return_type (DataType): Snowflake return type
        input_types (list[DataType]): List of Snowflake input types
        name (str): Name of the stored procedure
        stage_location (str): Stage where the procedure will be stored
        replace (bool): Replace if exists (default: True)
        is_permanent (bool): Whether the procedure is permanent (default: True)
    
    Returns:
        StoredProcedureRegistration: The registered sproc object
    """
    return session.sproc.register(
        func=func,
        return_type=return_type,
        input_types=input_types,
        name=name,
        replace=replace,
        is_permanent=is_permanent,
        stage_location=stage_location,
        imports=imports_path,
        execute_as="CALLER"
    )
