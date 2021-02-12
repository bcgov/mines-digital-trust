# Issue GHG Annual Report Verified Credentials
These python 3 scripts issue GHG Annual Report Verified Credentials from a CSV file.

## Requirements

1. Python 3.8
2. Properly formatted CSV file for your credentials
3. Authority to issue these credentials!
4. You will need the secret key for the GHG Issuer for your target environment


### Files
We tried to make these scripts forward compatible and flexible as possible.  The current default is to handle a CSV file that has a column for each attribute in the `ggirc-act.ghg-emissions-report` schema (version `0.2.0`).

There are 2 scripts: [parse.py](./parse.py) and [issue.py](./issue.py).
Review the [examples](./examples) files for clarity and/or as templates.

`parse.py` can be run to ensure your CSV and schema match up, you can examine the output to verify.  The output of `parse.py` is the input for `issue.py`.

`issue.py` will parse the CSV data, then call the GHG Issuer API to issue those credentials.  You will need to specify the environment (`dev`, `test` or `prod`), or specify a full url. These API calls are protected, so you will need the `Issuer Secret Key` (and it is different per environment).

Both scripts have help to describe their parameters.

```sh
python3 issue.py -h

usage: issue.py [-h] [--env ENVIRONMENT] [--url URL] --issuer-key ISSUER_KEY [--csv CSV_FILE] [--year YEAR] [--schemas SCHEMA_FILE] [--name SCHEMA_NAME] [--version SCHEMA_VERSION] [--mapping CSV_SCHEMA_MAPPING] [--registry COMPANY_REGISTRY]

Issue Verified Credentials from GHG Emissions CSV

optional arguments:
  -h, --help            show this help message and exit
  --env ENVIRONMENT, -e ENVIRONMENT
                        Environment to issue (dev = default, test, prod)
  --url URL, -u URL     Full Url to Credential Issuer (instead of using --env)
  --issuer-key ISSUER_KEY, -i ISSUER_KEY
                        Issuer Secret Authorization Key
  --csv CSV_FILE, -c CSV_FILE
                        Path to CSV file (defaults to ghg-emissions.csv)
  --year YEAR, -y YEAR  Reporting Year (optional)
  --schemas SCHEMA_FILE, -s SCHEMA_FILE
                        Path to schemas file (optional)
  --name SCHEMA_NAME, -n SCHEMA_NAME
                        Schema name (optional)
  --version SCHEMA_VERSION, -v SCHEMA_VERSION
                        Schema version (optional)
  --mapping CSV_SCHEMA_MAPPING, -m CSV_SCHEMA_MAPPING
                        CSV to Schema Mappings (optional)
  --registry COMPANY_REGISTRY, -r COMPANY_REGISTRY
                        Company to BC Registration ID Mappings (optional)

```

If you are targetting this schema, then make your CSV file following the `ghg-emissions-0.2.0.csv` file.  This contains columns for each attribute.

Example

```sh
python3 issue.py -e dev -i <issuer-secret-key> -c my-ghg-emissions-data.csv
```

If you are targetting another schema, then you will need to pass that schema.yml file into the scripts, and specify the schema name and version. Your CSV data file should have a column named for each attribute in that schema.

Example

```sh
python3 issue.py -e dev -i <issuer-secret-key> -c my-ghg-emissions-0.1.0-data.csv -s schemas.yml -n ggirc-act.ghg-emissions-report -v 0.1.0
```

#### Schema
Since these scripts are set to use `ggirc-act.ghg-emissions-report / 0.2.0`, and schemas change, we can allow some future (or past!) proofing by allowing the caller to provide and specify the schema they want to produce credentials for.

When you override the schema, you need to provide the schema definition file, and specify which schema name and version you want to use (there can be many schemas in the same file).

In the following example, you have a schemas definition file that contains an older GHG schema and you want to produce credentials for that version.

REview the schemas found under [ghg_issuer_controller](../ghg_issuer_controller/config/openshift/schemas.yml)

```sh
parse.py -c ghg-emissions-0.1.0.csv -s schemas.yml -n ggirc-act.ghg-emissions-report -v 0.1.0
```

#### Schema Attribute / CSV Mapping File
When you create your emissions data file, you may have more columns that the credential needs, and/or they are named differently than the schema you are using to issue.

Create a separate CSV file with the first row being the schema attributes, and the second row having the name of your emissions column that contains the data for the attribute.

Specify that you need the mapping file when you process your CSV (use the `-m` or `--mapping` parameter and path to your mapping file).

Example:

```sh
parse.py -c ghg-emissions-needs-mapping.csv -m csv_schema_mapping.csv
```


#### Company Registry
This is a CSV File that maps a company name (as found in your CSV data) to a BC Registries Registration ID. If your source data does not have the Registration ID, you will have to determine it in the [Org Book](https://orgbook.gov.bc.ca/en/home). This allows you to mine your system for data, exporting to a CSV and not worrying about knowing the correct Business Name or Registration ID. You can do that afterward by creating a "lookup" table...

Create a CSV file with the columns: `company_name` and `registration_id`.

`company_name` should match the `company_name` in your emissions data CSV.
`registration_id` is the BC Registries Registration of the Company receiving the credential.

Specify that you need the company registry when you process your CSV (use the `-r` or `--registry` parameter and path to your registry file).

Example:

```sh
parse.py -c ghg-emissions-needs-registry.csv -r company_registry.csv
```

#### Year / Reporting Year
For each credential, we need the `reporting_year`.  This can be in your emissions csv file as a column named (or mapped to) `reporting_year`.  However, you may not have that data in your process to create your emissions data file, so you can pass that in on the command line.

```sh
parse.py -c ghg-emissions-needs-year.csv -y 2015
```

#### Activity Parsing
In some demo files, the Activity Code and Description were in a single column, with `--` as the delimiter. If your source data has the convention, you can leave that in the emissions CSV but ensure the column is named `activity`. It will be parsed into the `primary_activity_code` and `primary_activity_description` attributes.

#### Optional Columns
`reporting_year` is optional in your emissions data.  If it is not present in your emissions data file, you *MUST* set it on the command line (see above).

`issued_date` and `effective_date` are optional and will have the current day used if they are not present.
