#!/usr/bin/env python
from flask import Flask, jsonify, abort, request, make_response

import requests
import json
import os
import yaml

import signal
import pprint
from app import config, issuer,routes

class Controller(Flask):
    def __init__(self, ENV):
        print("Initializing " + __name__ + " ...")
        super().__init__(__name__)
        # self.startup_thread = issuer.startup_init(ENV)
        issuer.app_config = sample_app_config
        issuer.synced = {'cee21dfa-cd60-479b-b096-9db9552fa948': True}
        self.ENV = ENV


def create_app(ENV):
    app = Controller(ENV)
    routes.register_routes(app)
    wsgi_app = app.wsgi_app
    return app

signal.signal(signal.SIGINT, issuer.signal_issuer_shutdown)
signal.signal(signal.SIGTERM, issuer.signal_issuer_shutdown)


# Load application settings (environment)
config_root = os.environ.get('CONFIG_ROOT', './config')
ENV = config.load_settings(config_root=config_root)
app = create_app(ENV)


#####
sample_app_config = {'AGENT_ADMIN_URL': 'http://myorg-agent:8034',
 'DID': 'XZxwKKqiKaV6yZQob1UZpq',
 'TOB_CONNECTION': 'cee21dfa-cd60-479b-b096-9db9552fa948',
 'running': True,
 'schemas': {'CRED_DEF_bcgov-mines-act-permit.empr_1.0.0': 'XZxwKKqiKaV6yZQob1UZpq:3:CL:14:default',
             'CRED_DEF_my-registration.empr_1.0.0': 'XZxwKKqiKaV6yZQob1UZpq:3:CL:10:default',
             'CRED_DEF_my-relationship.empr_1.0.0': 'XZxwKKqiKaV6yZQob1UZpq:3:CL:12:default',
             'SCHEMA_bcgov-mines-act-permit.empr': {'attributes': {'corp_num': {'data_type': 'ui_text',
                                                                                'description_en': 'Registration/Incorporation '
                                                                                                  'Number '
                                                                                                  'or '
                                                                                                  'Identifying '
                                                                                                  'Number',
                                                                                'label_en': 'Registration '
                                                                                            'ID',
                                                                                'required': True},
                                                                   'effective_date': {'data_type': 'ui_date',
                                                                                      'description_en': 'Date '
                                                                                                        'Credential '
                                                                                                        'is '
                                                                                                        'effective',
                                                                                      'label_en': 'Credential '
                                                                                                  'Effective '
                                                                                                  'Date',
                                                                                      'required': True},
                                                                   'entity_name': {'data_type': 'ui_name',
                                                                                   'description_en': 'The '
                                                                                                     'legal '
                                                                                                     'name '
                                                                                                     'of '
                                                                                                     'entity',
                                                                                   'label_en': 'Name',
                                                                                   'required': True},
                                                                   'permit_id': {'data_type': 'helper_uuid',
                                                                                 'description_en': 'Permit '
                                                                                                   'Identifying '
                                                                                                   'Number',
                                                                                 'label_en': 'Permit '
                                                                                             'ID',
                                                                                 'required': True},
                                                                   'permit_issued_date': {'data_type': 'ui_date',
                                                                                          'description_en': 'Date '
                                                                                                            'Permit '
                                                                                                            'is '
                                                                                                            'issued',
                                                                                          'label_en': 'Permit '
                                                                                                      'Issued '
                                                                                                      'Date',
                                                                                          'required': True},
                                                                   'permit_status': {'data_type': 'ui_select',
                                                                                     'description_en': 'Status '
                                                                                                       'of '
                                                                                                       'the '
                                                                                                       'permit',
                                                                                     'label_en': 'Permit '
                                                                                                 'Status',
                                                                                     'required': True},
                                                                   'permit_type': {'data_type': 'ui_select',
                                                                                   'description_en': 'Status '
                                                                                                     'of '
                                                                                                     'the '
                                                                                                     'permit',
                                                                                   'label_en': 'Permit '
                                                                                               'Type',
                                                                                   'required': True}},
                                                    'description': 'The '
                                                                   'bcgov-mines-act-permit '
                                                                   'credential '
                                                                   'issued by '
                                                                   'empr',
                                                    'name': 'bcgov-mines-act-permit.empr',
                                                    'version': '1.0.0'},
             'SCHEMA_bcgov-mines-act-permit.empr_1.0.0': 'XZxwKKqiKaV6yZQob1UZpq:2:bcgov-mines-act-permit.empr:1.0.0',
             'SCHEMA_my-registration.empr': {'attributes': {'address_line_1': {'data_type': 'ui_text',
                                                                               'description': 'address_line_1',
                                                                               'required': True},
                                                            'addressee': {'data_type': 'ui_text',
                                                                          'description': 'addressee',
                                                                          'required': True},
                                                            'city': {'data_type': 'ui_text',
                                                                     'description': 'city',
                                                                     'required': True},
                                                            'corp_num': {'data_type': 'helper_uuid',
                                                                         'description_en': 'Registration/Incorporation '
                                                                                           'Number '
                                                                                           'or '
                                                                                           'Identifying '
                                                                                           'Number',
                                                                         'label_en': 'Registration '
                                                                                     'ID',
                                                                         'required': True},
                                                            'country': {'data_type': 'ui_text',
                                                                        'description': 'country',
                                                                        'required': True},
                                                            'effective_date': {'data_type': 'ui_date',
                                                                               'description_en': 'Date '
                                                                                                 'Credential '
                                                                                                 'is '
                                                                                                 'effective',
                                                                               'label_en': 'Credential '
                                                                                           'Effective '
                                                                                           'Date',
                                                                               'required': True},
                                                            'entity_name': {'data_type': 'ui_name',
                                                                            'description_en': 'The '
                                                                                              'legal '
                                                                                              'name '
                                                                                              'of '
                                                                                              'entity',
                                                                            'label_en': 'Name',
                                                                            'required': True},
                                                            'entity_name_effective': {'data_type': 'ui_date',
                                                                                      'description_en': 'Date '
                                                                                                        'current '
                                                                                                        'name '
                                                                                                        'became '
                                                                                                        'effective',
                                                                                      'label_en': 'Name '
                                                                                                  'Effective '
                                                                                                  'Date',
                                                                                      'required': True},
                                                            'entity_status': {'data_type': 'ui_select',
                                                                              'description_en': 'Status '
                                                                                                'of '
                                                                                                'the '
                                                                                                'entity '
                                                                                                '(active '
                                                                                                'or '
                                                                                                'historical)',
                                                                              'label_en': 'Registration '
                                                                                          'Status',
                                                                              'required': True},
                                                            'entity_status_effective': {'data_type': 'ui_date',
                                                                                        'description_en': 'Date '
                                                                                                          'status '
                                                                                                          'became '
                                                                                                          'effective',
                                                                                        'label_en': 'Status '
                                                                                                    'Effective '
                                                                                                    'Date',
                                                                                        'required': True},
                                                            'entity_type': {'data_type': 'ui_text',
                                                                            'description_en': 'Type '
                                                                                              'of '
                                                                                              'entity '
                                                                                              'incorporated '
                                                                                              'or '
                                                                                              'registered',
                                                                            'label_en': 'Registration '
                                                                                        'Type',
                                                                            'required': True},
                                                            'expiry_date': {'data_type': 'ui_date',
                                                                            'description_en': 'Date '
                                                                                              'Credential '
                                                                                              'expired',
                                                                            'label_en': 'Credential '
                                                                                        'Expiry '
                                                                                        'Date',
                                                                            'required': False},
                                                            'postal_code': {'data_type': 'ui_text',
                                                                            'description': 'postal_code',
                                                                            'required': True},
                                                            'province': {'data_type': 'ui_text',
                                                                         'description': 'province',
                                                                         'required': True},
                                                            'registered_jurisdiction': {'data_type': 'ui_text',
                                                                                        'description_en': 'The '
                                                                                                          'jurisdiction '
                                                                                                          'an '
                                                                                                          'entity '
                                                                                                          'was '
                                                                                                          'created '
                                                                                                          'in',
                                                                                        'label_en': 'Registered '
                                                                                                    'Jurisdiction',
                                                                                        'required': False},
                                                            'registration_date': {'data_type': 'ui_date',
                                                                                  'description_en': 'Date '
                                                                                                    'of '
                                                                                                    'Registration, '
                                                                                                    'Incorporation, '
                                                                                                    'Continuation '
                                                                                                    'or '
                                                                                                    'Amalgamation',
                                                                                  'label_en': 'Registration '
                                                                                              'Date',
                                                                                  'required': False}},
                                             'description': 'The '
                                                            'my-registration '
                                                            'credential issued '
                                                            'by empr',
                                             'name': 'my-registration.empr',
                                             'version': '1.0.0'},
             'SCHEMA_my-registration.empr_1.0.0': 'XZxwKKqiKaV6yZQob1UZpq:2:my-registration.empr:1.0.0',
             'SCHEMA_my-relationship.empr': {'attributes': {'associated_corp_num': {'data_type': 'ui_text',
                                                                                    'description_en': 'Registry '
                                                                                                      'id(s) '
                                                                                                      'of '
                                                                                                      'associated '
                                                                                                      'organizations/individuals',
                                                                                    'label_en': 'Associated '
                                                                                                'Registration '
                                                                                                'ID',
                                                                                    'required': True},
                                                            'associated_registration_name': {'data_type': 'ui_text',
                                                                                             'description_en': 'Registered '
                                                                                                               'name '
                                                                                                               'of '
                                                                                                               'associated '
                                                                                                               'organizations/individuals',
                                                                                             'label_en': 'Associated '
                                                                                                         'Registration '
                                                                                                         'Namwe',
                                                                                             'required': False},
                                                            'corp_num': {'data_type': 'ui_text',
                                                                         'description_en': 'Unique '
                                                                                           'identifer '
                                                                                           'assigned '
                                                                                           'to '
                                                                                           'entity '
                                                                                           'by '
                                                                                           'registrar',
                                                                         'label_en': 'Registration '
                                                                                     'ID',
                                                                         'required': True},
                                                            'effective_date': {'data_type': 'ui_date',
                                                                               'description_en': 'Date '
                                                                                                 'Credential '
                                                                                                 'is '
                                                                                                 'effective',
                                                                               'label_en': 'Effective '
                                                                                           'Date',
                                                                               'required': True},
                                                            'expiry_date': {'data_type': 'ui_date',
                                                                            'description_en': 'Date '
                                                                                              'Credential '
                                                                                              'expires',
                                                                            'label_en': 'Credential '
                                                                                        'Expiry '
                                                                                        'Date',
                                                                            'required': False},
                                                            'relationship': {'data_type': 'ui_text',
                                                                             'description_en': 'Name '
                                                                                               'of '
                                                                                               'the '
                                                                                               'relationship',
                                                                             'label_en': 'Relationship',
                                                                             'required': True},
                                                            'relationship_description': {'data_type': 'ui_text',
                                                                                         'description_en': 'Description '
                                                                                                           'of '
                                                                                                           'the '
                                                                                                           'relationship',
                                                                                         'label_en': 'Relationship '
                                                                                                     'Description',
                                                                                         'required': True},
                                                            'relationship_status': {'data_type': 'ui_select',
                                                                                    'description_en': 'Status '
                                                                                                      'of '
                                                                                                      'the '
                                                                                                      'relationship',
                                                                                    'label_en': 'Relationship '
                                                                                                'Status',
                                                                                    'required': True},
                                                            'relationship_status_effective': {'data_type': 'ui_date',
                                                                                              'description_en': 'Date '
                                                                                                                'the '
                                                                                                                'relationship '
                                                                                                                'became/becomes '
                                                                                                                'effective',
                                                                                              'label_en': 'Relationship '
                                                                                                          'Status '
                                                                                                          'Effective',
                                                                                              'required': False}},
                                             'description': 'The relationship '
                                                            'between two '
                                                            'organizations',
                                             'name': 'my-relationship.empr',
                                             'version': '1.0.0'},
             'SCHEMA_my-relationship.empr_1.0.0': 'XZxwKKqiKaV6yZQob1UZpq:2:my-relationship.empr:1.0.0'}
        }