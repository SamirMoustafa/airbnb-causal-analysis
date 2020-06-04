import argparse

from src.scrape.scraper import AirbnbLinksScraper, AIRBNB_DATASET_FILENAME, find_airbnb_link, download_url


def scrape_and_download(info, file_name):
    print('start scrapping ')
    scraper = AirbnbLinksScraper()
    scraper(AIRBNB_DATASET_FILENAME)
    link = find_airbnb_link(info['country'], info['location'],
                            info['city'],    info['date'])
    print('scrapping done')

    print('start download')
    download_url(link, file_name)
    print('download finish')
    return True


def main(args):
    print("Setting up data directory")
    print("-" * 25)

    target_info = {'country': args.country,
                   'location': args.location,
                   'city': args.city,
                   'date': args.date,}

    output_file_name = target_info['city'] + target_info['date'] + '.csv'

    scrape_and_download(target_info, output_file_name)

    print("-" * 25)
    print('Finished!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='airbnb_causal_analysis')
    parser.add_argument('--country', type=str, help='name of the country.')
    parser.add_argument('--location', type=str, help='location or state inside the country.')
    parser.add_argument('--city', type=str, help='city name.')
    parser.add_argument('--date', type=str, help='exact data that the data scrapped on.')
    args = parser.parse_args()
    main(args)
