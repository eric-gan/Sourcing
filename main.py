from sourcer import Sourcer

import scraper

import os

def main():
    print('Starting Email Sourcer:\n')
    hunter_api_key = input('Enter hunter.io api key: ')

    # run scraper
    print('running scraper')
    scraper.run()

    print('fetching emails')
    sourcer = Sourcer(hunter_api_key)
    sourcer.read_client_info_csv(os.getcwd() + '/sourcing.csv')
    sourcer.write_client_info_csv(os.getcwd() + '/sourcing.csv')

    print('DONE')
    print("Your file is located at: " + os.getcwd() + '/sourcing.csv')
    return 0

if __name__ == "__main__":
    main()