# -*- coding: utf-8 -*-
from googlemaps import GoogleMapsScraper
from datetime import datetime, timedelta
import argparse
import csv
from termcolor import colored
import time
import re  # For regular expression

ind = {'most_relevant': 0, 'newest': 1, 'highest_rating': 2, 'lowest_rating': 3}
HEADER = ['place_name', 'id_review', 'caption', 'relative_date', 'retrieval_date', 'rating', 'username', 'n_review_user', 'n_photo_user', 'url_user']
HEADER_W_SOURCE = ['place_name', 'id_review', 'caption', 'relative_date', 'retrieval_date', 'rating', 'username', 'n_review_user', 'n_photo_user', 'url_user', 'url_source']

def csv_writer(source_field, ind_sort_by, path='data/'):
    outfile = ind_sort_by + '_gm_reviews.csv'
    targetfile = open(path + outfile, mode='w', encoding='utf-8', newline='\n')
    writer = csv.writer(targetfile, quoting=csv.QUOTE_MINIMAL)

    if source_field:
        h = HEADER_W_SOURCE
    else:
        h = HEADER
    writer.writerow(h)

    return writer

def extract_place_name(url):
    # Extract the place name from the URL
    # Assuming the URL contains the place name in a recognizable format
    match = re.search(r'place\/([^\/]+)', url)
    if match:
        return match.group(1).replace('-', ' ').title()  # Convert to title case
    return "Unknown Place"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Google Maps reviews scraper.')
    parser.add_argument('--N', type=int, default=5000, help='Number of reviews to scrape')
    parser.add_argument('--i', type=str, default='urls.txt', help='target URLs file')
    parser.add_argument('--sort_by', type=str, default='highest_rating', help='most_relevant, newest, highest_rating or lowest_rating')
    parser.add_argument('--place', dest='place', action='store_true', help='Scrape place metadata')
    parser.add_argument('--debug', dest='debug', action='store_true', help='Run scraper using browser graphical interface')
    parser.add_argument('--source', dest='source', action='store_true', help='Add source url to CSV file (for multiple urls in a single file)')
    parser.set_defaults(place=False, debug=False, source=False)

    args = parser.parse_args()

    # store reviews in CSV file
    writer = csv_writer(args.source, args.sort_by)

    with GoogleMapsScraper(debug=args.debug) as scraper:
        with open(args.i, 'r') as urls_file:
            for url in urls_file:
                url = url.strip()
                place_name = extract_place_name(url)  # Extract place name from URL
                print(f"Processing URL: {url} for place: {place_name}")

                if args.place:
                    print(scraper.get_account(url))
                else:
                    error = scraper.sort_by(url, ind[args.sort_by])

                    if error == 0:
                        n = 0
                        while n < args.N:
                            print(colored('[Review ' + str(n) + ']', 'cyan'))
                            reviews = scraper.get_reviews(n)
                            if len(reviews) == 0:
                                break

                            for r in reviews:
                                row_data = [place_name] + list(r.values())  # Add place name to row data
                                if args.source:
                                    row_data.append(url[:-1])

                                writer.writerow(row_data)

                            n += len(reviews)