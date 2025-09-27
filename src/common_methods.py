from snowflake.snowpark import Session

def add_numbers(session:Session, a: int, b: int) -> int:
    return a + b
