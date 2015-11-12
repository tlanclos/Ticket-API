import argparse
import getpass
import re
from ticketapi.datalayer.procedures import add_auth


if __name__ == '__main__':
    try:
        # Create our argument parser
        parser = argparse.ArgumentParser(
            description='Tool to generate authorization rows and add them to the database based on a company name',
            epilog='\n'.join([
                'I would have written a nice ncurses tui instead of this cli, but I figured someone would',
                'eventually write a nice gui of some sort to add rows in the Authentication table :)'
            ])
        )

        # Add arguments to be parsed
        parser.add_argument(
            '--company', '-c',
            help='CompanyName from the Techneaux Company table'
        )
        parser.add_argument(
            '--username', '-u',
            help='CompanyID for the new company, this should be a unique string'
        )
        parser.add_argument(
            '--password', '-p',
            help='Although strongly discouraged to use on commandline, the password for the new company username'
        )

        args = parser.parse_args()

        # If we don't have a company or username in the arguments, ask for it
        company = input('Enter company name: ').strip() if not args.company else args.company
        username = input('Enter company username: ').strip() if not args.username else args.username

        # Print the company and username being used
        print('Adding company: "{company}"'.format(company=company))
        print('   Username   : "{username}"'.format(username=username))

        # If a password was not passed on the command line, ask for it
        if not args.password:
            password = getpass.getpass(prompt='Password for {username}: '.format(username=username))
            if len(password) > 16:
                print('Password too long, must be less than 16 characters')
                exit(2)

            confirm_password = getpass.getpass(prompt='Confirm password for {username}: '.format(username=username))
            if password != confirm_password:
                print('Passwords do not match')
                exit(2)
        else:
            password = args.password

        # Ask for confirmation
        cont = input('Continue (y/n)? ')
        if re.match(r'y(es)?', cont, re.IGNORECASE):
            success, reason = add_auth(companyName=company, companyID=username, password=password)
            if not success:
                print('Failed to add authentication for "{company}"'.format(company=company))
                print(reason)
        else:
            print('User said no')
    except KeyboardInterrupt as e:
        print('Exiting on user command')
