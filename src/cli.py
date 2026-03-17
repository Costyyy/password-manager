import argparse
import getpass
from vault import Vault

def main():
    parser = argparse.ArgumentParser(description="Password Manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # add
    p_add = subparsers.add_parser("add", help="Add a new entry")
    p_add.add_argument("site")
    p_add.add_argument("username")

    # get
    p_get = subparsers.add_parser("get", help="Retrieve a password")
    p_get.add_argument("site")

    # delete
    p_del = subparsers.add_parser("delete", help="Delete an entry")
    p_del.add_argument("site")

    # list
    subparsers.add_parser("list", help="List all entries")

    args = parser.parse_args()

    master_password = getpass.getpass("Master password: ")

    try:
        vault = Vault(master_password)
    except ValueError as e:
        print(f"Error: {e}")
        return

    if args.command == "add":
        password = getpass.getpass("Password to store: ")
        vault.add(args.site, args.username, password)
        print(f"Saved entry for {args.site}")

    elif args.command == "get":
        try:
            username, password = vault.get(args.site)
            print(f"Username: {username}")
            print(f"Password: {password}")
        except ValueError as e:
            print(f"Error: {e}")

    elif args.command == "delete":
        vault.delete(args.site)
        print(f"Deleted entry for {args.site}")

    elif args.command == "list":
        entries = vault.list_entries()
        if not entries:
            print("No entries found.")
        else:
            for site, username in entries:
                print(f"  {site} : {username}")

if __name__ == "__main__":
    main()
