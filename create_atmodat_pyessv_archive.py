"""
.. module:: write.py
   :platform: Unix, Windows
   :synopsis: Maps raw AtMoDat vocab files to normalized pyessv format.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import argparse
import datetime as dt
import json
import os
import pyessv


# Define command line options.
_ARGS = argparse.ArgumentParser('Maps raw AtMoDat vocab files to normalized pyessv CV format.')
_ARGS.add_argument(
    '--source',
    help='Path from which raw AtMoDat vocab files will be read.',
    dest='source',
    type=str
    )

# Ensure we use fixed creation date.
_CREATE_DATE = dt.datetime.today()

# CV authority = AtMoDat.
_AUTHORITY = pyessv.create_authority(
    'AtMoDat',
    'AtMoDat',
    label='AtMoDat',
    url='https://www.atmodat.de/',
    create_date=_CREATE_DATE
    )

# CV scope = AtMoDat.
_SCOPE_ATMODAT = pyessv.create_scope(
    _AUTHORITY,
    'AtMoDat',
    'Controlled Vocabularies (CVs) for use with AtMoDat',
    label='AtMoDat',
    url='https://github.com/AtMoDat/AtMoDat_CVs',
    create_date=_CREATE_DATE
    )

# Map of scopes to collections.
_SCOPE_COLLECTIONS = {
    _SCOPE_ATMODAT: {
        'realm': {
            'cim_document_type': None,
            'cim_document_type_alternative_name': None,
            'data_factory': lambda obj, name: {'description': obj[name]},
            'is_virtual': False,
            'label': None,
            'ommitted': [],
            'term_regex': None
        },
        'frequency': {
            'cim_document_type': None,
            'cim_document_type_alternative_name': None,
            'data_factory': None,
            'is_virtual': False,
            'label': None,
            'ommitted': [],
            'term_regex': None
        },
        'featureType': {
            'cim_document_type': None,
            'cim_document_type_alternative_name': None,
            'data_factory': None,
            'is_virtual': False,
            'label': None,
            'ommitted': [],
            'term_regex': None
        },
        'nominal_resolution': {
            'cim_document_type': None,
            'cim_document_type_alternative_name': None,
            'data_factory': None,
            'is_virtual': False,
            'label': None,
            'ommitted': [],
            'term_regex': r'^[a-z0-9\-\.]*$'
        },
        'required_global_attributes': {
            'cim_document_type': None,
            'cim_document_type_alternative_name': None,
            'data_factory': None,
            'is_virtual': False,
            'label': None,
            'ommitted': [],
            'term_regex': None
        },
        'source_type': {
            'cim_document_type': None,
            'cim_document_type_alternative_name': None,
            'data_factory': None,
            'is_virtual': False,
            'label': None,
            'ommitted': [],
            'term_regex': None
        },
        'variable_id': {
            'cim_document_type': None,
            'cim_document_type_alternative_name': None,
            'data_factory': None,
            'is_virtual': True,
            'label': None,
            'ommitted': [],
            'term_regex': r'^[A-Za-z0-9]*$',
        },
        'version': {
            'cim_document_type': None,
            'cim_document_type_alternative_name': None,
            'data_factory': None,
            'is_virtual': True,
            'label': None,
            'ommitted': [],
            'term_regex': r'^[0-9]{8}$',
        }
    },
}


def _main(args):
    """Main entry point.

    """
    if not os.path.isdir(args.source):
        raise ValueError('AtMoDat vocab directory does not exist')

    # Create collections.
    for scope in _SCOPE_COLLECTIONS:
        for collection in _SCOPE_COLLECTIONS[scope]:
            cfg = _SCOPE_COLLECTIONS[scope][collection]
            _create_collection(args.source, scope, collection, cfg)

    # Add to archive & persist to file system.
    pyessv.archive(_AUTHORITY)


def _create_collection(source, scope, collection_id, cfg):
    """Creates collection from a AtMoDat JSON file.

    """
    # Create collection.
    if collection_id.lower().replace('_', '-') in [collection.name for collection in scope.collections]:
        collection = scope[collection_id]
        collection.description = "AtMoDat CV collection: ".format(collection_id),
        collection.label = cfg['label'] or collection_id.title().replace('_Id', '_ID').replace('_', ' '),
        collection.create_date = _CREATE_DATE,
        collection.term_regex = cfg['term_regex'] or pyessv.REGEX_CANONICAL_NAME,
        collection.data = None if cfg['cim_document_type'] is None else {
                'cim_document_type': cfg['cim_document_type'],
                'cim_document_type_alternative_name': cfg['cim_document_type_alternative_name']
            }
    else:
        collection = pyessv.create_collection(
            scope,
            collection_id,
            "AtMoDatll"
            " CV collection: ".format(collection_id),
            label=cfg['label'] or collection_id.title().replace('_Id', '_ID').replace('_', ' '),
            create_date=_CREATE_DATE,
            term_regex=cfg['term_regex'] or pyessv.REGEX_CANONICAL_NAME,
            data=None if cfg['cim_document_type'] is None else {
                'cim_document_type': cfg['cim_document_type'],
                'cim_document_type_alternative_name': cfg['cim_document_type_alternative_name']
                }
            )

    # Load JSON data & create terms (if collection is not a virtual one).
    if not cfg['is_virtual']:
        cv_data = _get_atmodat_cv(source, scope, collection_id)
        data_factory = cfg['data_factory']
        for term_name in [i for i in cv_data if i not in cfg['ommitted']]:
            term_data = data_factory(cv_data, term_name) if data_factory else None
            _create_term(collection, term_name, term_data)


def _create_term(collection, raw_name, data):
    """Creates & returns a new term.

    """
    try:
        description = data['description']
    except (TypeError, KeyError):
        description = None
    else:
        del data['description']

    try:
        label = data['label']
    except (TypeError, KeyError):
        label = raw_name
    else:
        del data['label']

    term = pyessv.create_term(
        collection,
        raw_name,
        description=description,
        label=label,
        create_date=_CREATE_DATE,
        data=data
        )


def _get_atmodat_cv(source, scope, collection_id):
    """Returns raw AtMoDat CV data.

    """
    prefix = 'AtMoDat_' if scope.canonical_name == 'atmodat' else ''
    fname = '{}{}.json'.format(prefix, collection_id)
    fpath = os.path.join(source, fname)
    with open(fpath, 'r') as fstream:
        return json.loads(fstream.read())[collection_id]


# Entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
