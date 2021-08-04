import aiofiles
from termcolor import colored
from tortoise import Tortoise, run_async
from tortoise.exceptions import OperationalError
from tortoise.transactions import in_transaction


async def run():
    # Init tortoise
    await Tortoise.init(db_url="your_db_url", models={"models": ["app.models"]})

    file_number = input("Enter File Number: ")
    file_path = f"migrations/{file_number}.sql"
    try:
        async with aiofiles.open(file_path, mode="r") as sql_file:
            statement = await sql_file.read()
    except FileNotFoundError as err:
        print(colored(f"Error in opening the migration file, reason: {err}", "red"))
        quit()

    print("Executing the statement: ", colored(statement, "blue"), end="\n")
    confirmation = input(colored("Do you want to continue? Y/n: ", "yellow"))
    if confirmation != "Y":
        quit()

    try:
        # Need to get a connection. Unless explicitly specified, the name should be 'default'
        # Do it in transaction
        async with in_transaction("default") as tconn:
            await tconn.execute_query(statement)
            print(colored("Migration Done!", "green"), end="\n")
    except OperationalError as err:
        print(colored(f"Error in executing the sql statement, reason: {err}", "red"))


if __name__ == "__main__":
    run_async(run())
