import argparse
import json
import pathlib
from datetime import date

import pandas as pd
import yaml

DEFAULT_SCHEMA_NAME = 'ggirc-act.ghg-emissions-report'
DEFAULT_SCHEMA_VERSION = '0.2.0'
DEFAULT_ATTRIBUTES = [
    'registration_id',
    'facility_name',
    'facility_latitude',
    'facility_longitude',
    'primary_activity_code',
    'primary_activity_description',
    'co2_fossil_emissions',
    'co2_biomass_emissions',
    'ch4_emissions',
    'n2o_emissions',
    'hfcs_emissions',
    'pfcs_emissions',
    'sf6_emissions',
    'verification_body',
    'verification_result',
    'reporting_year',
    'issued_date',
    'effective_date'
]


parser = argparse.ArgumentParser(
    description='Parse GHG Emissions CSV to Verified Credentials')

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


def parse_csv(csv_file,
              year,
              schema_file,
              schema_name,
              schema_version,
              csv_schema_mapping,
              company_registry):

    _today = date.today().isoformat()

    _schema_name = DEFAULT_SCHEMA_NAME
    _schema_version = DEFAULT_SCHEMA_VERSION
    _schema_attributes = DEFAULT_ATTRIBUTES

    _mappings = None
    _company_registry = None

    if not pathlib.Path(csv_file).exists():
        print(f'CSV File \'{csv_file}\' not found. Exiting.')
        exit(1)

    if schema_file and pathlib.Path(schema_file).exists():
        # we want to override the schema, we need
        schemas = yaml.safe_load(open(schema_file, 'r', encoding='utf-8'))
        schema = next(filter(lambda x: x['name'] == schema_name and x['version'] == schema_version, schemas), None)

        if schema is None:
            print(f"Schema '{schema_name}/{schema_version}' not found in Schemas File. Exiting.")
            exit(1)
        else:
            _schema_name = schema['name']
            _schema_version = schema['version']
            _schema_attributes = schema['attributes']

    if csv_schema_mapping and pathlib.Path(csv_schema_mapping).exists():
        _mappings = pd.read_csv(csv_schema_mapping, index_col=False)

    if company_registry and pathlib.Path(company_registry).exists():
        co_reg = pd.read_csv(company_registry, index_col=0, header=0, skiprows=0,
                             keep_default_na=False)
        _company_registry = co_reg.to_dict()

    _emissions = pd.read_csv(csv_file, index_col=False, header=0, skiprows=0, keep_default_na=True)

    if 'activity' in _emissions.columns:
        # split the activity column into primary_activity_code and primary_activity_description
        # let's hope those attributes do not get their names changed from version to version.
        _emissions[['primary_activity_code',
            'primary_activity_description']] = _emissions.activity.str.split('--', expand=True, )

    def nice_value(value):
        # for our purposes, we cannot have None or null
        # and everything is a string...
        if pd.isna(value) or value is None:
            return ''

        return str(value)

    def parse_value(name, data, default_value=None):
        value = None
        try:
            value = data[name]
        except KeyError:
            if default_value is None:
                # better be a mapping...
                # ok, there should be a mapping for it then
                # find the column name mapping used for this schema attribute...
                csv_name = _mappings.iloc[0:1][name].values[0]
                # grab the value
                value = data[csv_name]
            else:
                value = default_value

        return nice_value(value)

    def parse_registration_id(data):
        value = None
        try:
            value = data['registration_id']
        except KeyError:
            co_name = data['company_name']
            value = _company_registry['registration_id'][co_name]

        return nice_value(value)

    def get_value(name, data):
        value = None

        if name == 'registration_id':
            value = parse_registration_id(data)
        elif name == 'reporting_year':
            value = parse_value(name, data, year)
        elif name == 'issued_date':
            value = parse_value(name, data, _today)
        elif name == 'effective_date':
            value = parse_value(name, data, _today)
        else:
            value = parse_value(name, data)

        return value

    def get_attributes(names, data):
        result = {}
        for name in names:
            result[name] = get_value(name, data)

        return result

    vcs = []
    for index, row in _emissions.iterrows():
        try:
            vc = {'schema': _schema_name,
                  'version': _schema_version,
                  'attributes': get_attributes(_schema_attributes, row)
                  }
            vcs.append(vc)
        except KeyError as e :
            print(f'Error creating VC for line {index+2}, {str(e)}')

    return json.dumps(vcs)


def main():
    args = parser.parse_args()

    result = parse_csv(csv_file=args.csv_file,
                       year=args.year,
                       schema_file=args.schema_file,
                       schema_name=args.schema_name,
                       schema_version=args.schema_version,
                       csv_schema_mapping=args.csv_schema_mapping,
                       company_registry=args.company_registry)

    print(json.dumps(json.loads(result), indent=4))


if __name__ == "__main__":
    main()
