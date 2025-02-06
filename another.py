# """Console script for companies_house."""

# import click


# @click.command()
# def main():
#     """Main entrypoint."""
#     click.echo("companies-house-project")
#     click.echo("=" * len("companies-house-project"))
#     click.echo("companies house api to extract companies data")


# if __name__ == "__main__":
#     main()  # pragma: no cover

import logging
import argparse

import chtools as ch

# from chtools.ch_basics import Config, CompaniesHouseAPI, CompanyData, RegisteredOffice
# from chtools.ch_utils import setup_logging, explore_nested_json, robust_nested_json_to_multi_df, play_sound_until_input

def another():
    parser = argparse.ArgumentParser(description='Get company data from Companies House API.')
    parser.add_argument('--company_number', type=str, help='The company number to retrieve data for.')
    parser.add_argument('--api_key', type=str, help='API Key for Companies House')
    parser.add_argument('--log_level', type=str, default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], help='Set logging level')
    parser.add_argument('--log_file', type=str, help='Log to a file instead of console.')
    parser.add_argument('--explore', action='store_true', help='Explore nested json data.')
    parser.add_argument('--to_df', action='store_true', help='Convert nested JSON to dataframes')
    parser.add_argument('--sound', type=str, help='play sound until return', default=None)

    args = parser.parse_args()

    log_level = getattr(logging, args.log_level.upper(), logging.INFO)
    setup_logging(log_level=log_level, log_file=args.log_file)

    config = Config(api_key=args.api_key, log_level=log_level, log_file=args.log_file)

    api = CompaniesHouseAPI(config=config)

    if args.company_number:
        logging.info(f"Retrieving data for company number: {args.company_number}")
        api_response = api.request_with_rate_limit(endpoint=f"/company/{args.company_number}")
        
        if api_response.is_ok():
            company_data = CompanyData(company_number=args.company_number, company_data=api_response.data)
            logging.info(f"Company Name: {company_data.get_name()}")
            logging.info(f"Company Status: {company_data.get_status()}")
            
            # get registered office
            registered_office_data = api_response.data.get('registered_office_address', None)
            if registered_office_data:
                  registered_office = RegisteredOffice(registered_office_data)
                  logging.info(f"Registered Office: {registered_office.get_address_string()}")
            else:
                 logging.info("No registered office address found.")

            # Check if the --explore flag is set
            if args.explore:
                 logging.info("Exploring nested json...")
                 explore_nested_json(api_response.data)
            # Check if the --to_df flag is set
            if args.to_df:
                logging.info("Creating dataframes...")
                dfs = robust_nested_json_to_multi_df(data=[api_response.data])
                for key, df in dfs.items():
                     logging.info(f"Dataframe {key} created: {df.shape[0]} rows, {df.shape[1]} columns")
        else:
            logging.error(f"API Request Failed. Status Code: {api_response.status_code}. Error: {api_response.error}")
    else:
          logging.info("No company number passed in")

    if args.sound:
         play_sound_until_input(args.sound)


if __name__ == "__main__":
    another()