import argparse
from snowflake.snowpark import Session
from snowflake.snowpark.types import IntegerType


# # Snowflake connection config
# connection_parameters = {
#     "account": "<your_account>",
#     "user": "<your_user>",
#     "password": "<your_password>",
#     "role": "<your_role>",
#     "warehouse": "<your_warehouse>",
#     "database": "<your_database>",
#     "schema": "<your_schema>"
# }

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

def add_numbers(session, a: int, b: int) -> int:
    return a + b

# Register the stored procedure
sproc = session.sproc.register(
    func=add_numbers,
    return_type=IntegerType(),
    input_types=[IntegerType(), IntegerType()],
    name="add_numbers",
    replace=True,
    is_permanent=True,
    stage_location='@"SANDBOX"."DATAMART_1"."FILE_SHARING"' # Ensure this stage exists
)

print(f"Stored procedure '{sproc.name}' registered successfully.")
