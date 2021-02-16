import argparse
import json
import requests
import parse as csv_parser

ENVIRONMENT_URLS = {
    'dev': 'https://ghg-emissions-issuer-a3e512-dev.apps.silver.devops.gov.bc.ca/issue-credential',
    'test': 'https://ghg-emissions-issuer-a3e512-test.apps.silver.devops.gov.bc.ca/issue-credential',
    'prod': 'https://ghg-emissions-issuer-a3e512-prod.apps.silver.devops.gov.bc.ca/issue-credential'
}

ISSUER_SECRET_HEADER = 'Issuer-Secret-Key'

parser = argparse.ArgumentParser(
    description='Issue Verified Credentials from GHG Emissions CSV')

parser.add_argument('--env', '-e',
                    dest='environment',
                    help='Environment to issue (dev = default, test, prod)',
                    default='dev')
parser.add_argument('--url', '-u',
                    dest='url',
                    help='Full Url to Credential Issuer (instead of using --env)')
parser.add_argument('--issuer-key', '-i',
                    dest='issuer_key',
                    help='Issuer Secret Authorization Key',
                    required=True)
#
# These are passed on to the csv parsing routine
#
parser.add_argument('--csv', '-c',
                    dest='csv_file',
                    help='Path to CSV file (defaults to ghg-emissions.csv)',
                    default='ghg-emissions.csv')
parser.add_argument('--year', '-y',
                    dest='year',
                    help='Reporting Year (optional)')
parser.add_argument('--schemas', '-s',
                    dest='schema_file',
                    help='Path to schemas file (optional)')
parser.add_argument('--name', '-n',
                    dest='schema_name',
                    help='Schema name (optional)')
parser.add_argument('--version', '-v',
                    dest='schema_version',
                    help='Schema version (optional)')
parser.add_argument('--mapping', '-m',
                    dest='csv_schema_mapping',
                    help='CSV to Schema Mappings (optional)')
parser.add_argument('--registry', '-r',
                    dest='company_registry',
                    help='Company to BC Registration ID Mappings (optional)')

def issue_credentials(environment, url, issuer_key, data):
    result = []
    _url = ENVIRONMENT_URLS[environment]

    if url:
        # override the environment url
        _url = url
    print(f"Issuing {len(data)} credentials to '{_url}'")
    for d in data:
        # get some tracking data...
        registration_id = d['attributes']['registration_id']
        facility_name = d['attributes']['facility_name']
        # request needs to be an array...
        body = [d]
        response = requests.post(_url,
                                 json=body,
                                 headers={ISSUER_SECRET_HEADER: issuer_key})
        if response.ok:
            res = {'registration_id': registration_id,
                   'facility_name': facility_name,
                   'success': response.json()[0]['success'],
                   'result': response.json()[0]['result']
                   }
            result.append(res)
        else:
            print(f"Error issuing credential for registration_id = '{registration_id}', facility_name = '{facility_name}'. ({response.status_code}) - {response.reason}")

    return json.dumps(result)

def main():
    args = parser.parse_args()

    json_data = csv_parser.parse_csv(csv_file=args.csv_file,
                       year=args.year,
                       schema_file=args.schema_file,
                       schema_name=args.schema_name,
                       schema_version=args.schema_version,
                       csv_schema_mapping=args.csv_schema_mapping,
                       company_registry=args.company_registry)

    py_data = json.loads(json_data)

    result = issue_credentials(environment=args.environment,
                               url=args.url,
                               issuer_key=args.issuer_key,
                               data=py_data)

    print(json.dumps(json.loads(result), indent=4))


if __name__ == "__main__":
    main()
