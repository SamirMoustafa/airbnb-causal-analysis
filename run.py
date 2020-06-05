import argparse
import pandas as pd

from src.causal import causal_corr_model
from src.preprocessing.clean import airbnb_data_clean
from src.scrape.scraper import AirbnbLinksScraper, AIRBNB_DATASET_FILENAME, find_airbnb_link, download_url
from src.utils import df2graph, plot_graph, random_z_estimate, roi

absolute_path = './data/'

INFLATION_RATE = 0.028
MORTGAGE_RATE = 0.036
NUM_YEARS = 1
DOWN_PAYMENT = 0.20


def scrape_and_download(info, file_name):
    print('start scrapping ')
    scraper = AirbnbLinksScraper()
    scraper(AIRBNB_DATASET_FILENAME)
    link = find_airbnb_link(info['country'], info['location'],
                            info['city'], info['date'])
    print('scrapping done')

    print('start download')
    download_url(link, file_name)
    print('download finish')
    return file_name


def clean_scrapped_data(file_name):
    df = pd.read_csv(file_name)
    print('start pre-processing and cleaning ')
    print('warning it may took a few moments and use RAMs')
    df = airbnb_data_clean(df)
    df.to_csv(file_name, index=False)
    print('pre-processing and cleaning finish')
    return df


def main(args):
    print("Setting up casual model")
    print("-" * 25)

    target_info = {'country': args.country,
                   'location': args.location,
                   'city': args.city,
                   'date': args.date, }

    output_file_name = absolute_path + target_info['city'] + target_info['date'] + '.csv'

    file_name = scrape_and_download(target_info, output_file_name)

    cleaned_df = clean_scrapped_data(file_name)
    cleaned_df['zestimate'] = random_z_estimate(cleaned_df['price'])
    cleaned_df['roi'] = roi(cleaned_df['zestimate'],
                            rental_price=cleaned_df['price'],
                            inflation_rate=INFLATION_RATE,
                            mortgage_rate=MORTGAGE_RATE,
                            num_years=NUM_YEARS,
                            down_payment_percent=DOWN_PAYMENT
                            )
    print(cleaned_df)

    method = args.method
    threshold = args.threshold

    if method == 'corr':
        causal_model = causal_corr_model(cleaned_df)

    G = df2graph(causal_model, threshold)
    plot_graph(G)

    print("-" * 25)
    print('Finished!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='airbnb_causal_analysis')
    parser.add_argument('--country', type=str, help='name of the country.')
    parser.add_argument('--location', type=str, help='location or state inside the country.')
    parser.add_argument('--city', type=str, help='city name.')
    parser.add_argument('--date', type=str, help='exact data that the data scrapped on.')

    parser.add_argument('--method', type=str, default='corr', help='exact data that the data scrapped on.')
    parser.add_argument('--threshold', type=float, default=.2, help='exact data that the data scrapped on.')

    args = parser.parse_args()
    main(args)
