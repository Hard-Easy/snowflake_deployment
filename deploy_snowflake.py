import os
import argparse
from snowflake.snowpark import Session
from snowflake.snowpark.types import IntegerType
from workflow_creation import register_stored_procedure
from src.common_methods import add_numbers


parser = argparse.ArgumentParser()
parser.add_argument("--account", required=True)
parser.add_argument("--user", required=True)
parser.add_argument("--warehouse", required=True)
parser.add_argument("--database", required=True)
parser.add_argument("--schema", required=True)
parser.add_argument("--password", required=True)
parser.add_argument("--role", required=True)

args = parser.parse_args()

# Build connection
connection_parameters = {
    "account": args.account,
    "role":  args.role,
    "password": args.password,
    "user": args.user,
    "warehouse": args.warehouse,
    "database": args.database,
    "schema": args.schema
}

# Create a session
session = Session.builder.configs(connection_parameters).create()
session.add_packages("snowflake-snowpark-python")
session.custom_package_usage_config["enabled"] = True

stage_path = '@"SANDBOX"."DATAMART_1"."FILE_SHARING"'
session.file.put("my_code.zip", stage_path, overwrite=True)


session.sql("USE DATABASE SANDBOX").collect()
session.sql("USE SCHEMA DATAMART_1").collect()

# def add_numbers(session:Session, a: int, b: int) -> int:
#     return a + b

# Register the stored procedure
sproc = register_stored_procedure(
    session=session,
    func=add_numbers,
    return_type=IntegerType(),
    input_types=[IntegerType(), IntegerType()],
    name="add_numbers",
    replace=True,
    is_permanent=True,
    stage_location='@"SANDBOX"."DATAMART_1"."FILE_SHARING"', # Ensure this stage exists
    imports=[f"{stage_path}/my_code.zip"]
)

print(f"Stored procedure '{sproc.name}' registered successfully.")
