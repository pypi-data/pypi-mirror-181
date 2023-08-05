"""GDN data connector source for C8 Collections."""
from collections import Counter

import pkg_resources
import singer
from c8 import C8Client
from c8connector import C8Connector, Sample, ConfigProperty, ConfigAttributeType, Schema, SchemaAttributeType, \
    SchemaAttribute
from singer import utils
from singer.catalog import Catalog, CatalogEntry
from singer.schema import Schema as SingerSchema

from c8_source_c8collection.client import C8CollectionClient

LOGGER = singer.get_logger('c8_source_c8collection')

REQUIRED_CONFIG_KEYS = [
    'region',
    'fabric',
    'api_key',
    'source_collection'
]


class C8CollectionSourceConnector(C8Connector):
    """C8CollectionSourceConnector's C8Connector impl."""

    def name(self) -> str:
        """Returns the name of the connector."""
        return "c8collection"

    def package_name(self) -> str:
        """Returns the package name of the connector (i.e. PyPi package name)."""
        return "c8-source-c8collection"

    def version(self) -> str:
        """Returns the version of the connector."""
        return pkg_resources.get_distribution('c8_source_c8collection').version

    def type(self) -> str:
        """Returns the type of the connector."""
        return "source"

    def description(self) -> str:
        """Returns the description of the connector."""
        return "GDN data connector source for C8 Collections"

    def validate(self, integration: dict) -> None:
        """Validate given configurations against the connector.
        If invalid, throw an exception with the cause.
        """
        config = self.get_config(integration)
        C8Client(
            "https",
            host=config["region"],
            port=443,
            geofabric=config["fabric"],
            apikey=config["api_key"]
        ).collection(config["source_collection"])
        pass

    def samples(self, integration: dict) -> list[Sample]:
        """Fetch sample data using the given configurations."""
        config = self.get_config(integration)
        schema, data = get_schema_and_data(C8Client(
            "https",
            host=config["region"],
            port=443,
            geofabric=config["fabric"],
            apikey=config["api_key"]
        ), config["source_collection"], 10)
        return [Sample(
            schema=Schema(config["source_collection"],  # TODO: support other data types.
                          [SchemaAttribute(attrib, SchemaAttributeType.OBJECT) for attrib in schema]),
            data=data
        )]

    def schemas(self, integration: dict) -> list[Schema]:
        """Get supported schemas using the given configurations."""
        config = self.get_config(integration)
        schema, data = get_schema_and_data(C8Client(
            "https",
            host=config["region"],
            port=443,
            geofabric=config["fabric"],
            apikey=config["api_key"]
        ), config["source_collection"], 50)
        return [Schema(config["source_collection"],  # TODO: support other data types.
                       [SchemaAttribute(attrib, SchemaAttributeType.OBJECT) for attrib in schema])]

    def config(self) -> list[ConfigProperty]:
        """Get configuration parameters for the connector."""
        return [
            ConfigProperty('region', ConfigAttributeType.STRING, True, False,
                           description="Fully qualified region URL.", example="api-sample-ap-west.eng.macrometa.io"),
            ConfigProperty('fabric', ConfigAttributeType.STRING, True, False,
                           description="Fabric name.", example="_system"),
            ConfigProperty('api_key', ConfigAttributeType.STRING, True, False,
                           description="API key.", example="dmi.yzpqqc8DmmdN4adferwe32aN9msnlulMr3sijJGt0..."),
            ConfigProperty('source_collection', ConfigAttributeType.STRING, True, True,
                           description="Source collection name", example="SampleCollection"),
            ConfigProperty('schemas', ConfigAttributeType.ARRAY, True, True,
                           description="Schemas found in source collection as JSON Schemas",
                           example='[{"name":"hello","primary_keys":"_key","properties":{"hello":{"type":"string"}}}]'),
        ]

    def capabilities(self) -> list[str]:
        """Return the capabilities[1] of the connector.
        [1] https://docs.meltano.com/contribute/plugins#how-to-test-a-tap
        """
        return ['catalog', 'discover', 'state']

    @staticmethod
    def get_config(integration: dict) -> dict:
        try:
            return {
                # Required config keys
                'region': integration['region'],
                'api_key': integration['api_key'],
                'fabric': integration['fabric'],
                'source_collection': integration['source_collection']
            }
        except KeyError as e:
            raise KeyError(f'Integration property `{e}` not found.')


def get_schema_and_data(client: C8Client, collection: str, sample_size: int):
    cursor = client.execute_query(f"FOR d IN {collection} LIMIT 0, {sample_size} RETURN d")
    schemas = []
    schema_map = {}
    data_map = {}
    while not cursor.empty():
        rec = cursor.next()
        h = str(hash(rec.keys().__str__()))
        schema_map[h] = rec.keys()
        schemas.append(h)
        if h in data_map:
            data_map[h].append(rec)
        else:
            data_map[h] = [rec]
    most_common, _ = Counter(schemas).most_common(1)[0]
    return schema_map[most_common], data_map[most_common]


def do_discovery(schemas):
    entries = []
    for s in schemas:
        cols: dict = s.get('properties')

        # replace schemas for default properties
        cols["_key"] = {"type": "string", "required": "true"}
        cols["_rev"] = {"type": "string", "required": "true"}

        column_schemas = {
            c: SingerSchema(type=cols[c].get("type"), format=cols[c].get("format"))
            for c in cols.keys()
        }
        schema = SingerSchema(type='object', properties=column_schemas)
        entry = CatalogEntry(
            table=s.get("name"),
            stream=s.get("name"),
            tap_stream_id=s.get("name"),
            schema=schema,
            key_properties=["_key"]
        )
        entries.append(entry)

    catalog = Catalog(entries)
    dump_catalog(catalog)
    return catalog


def dump_catalog(catalog: Catalog):
    catalog.dump()


def do_sync(conn_config, catalog, default_replication_method):
    client = C8CollectionClient(conn_config)
    client.sync(catalog.streams[0])


def main_impl():
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)
    conn_config = {'api_key': args.config['api_key'],
                   'region': args.config['region'],
                   'fabric': args.config['fabric'],
                   'source_collection': args.config['source_collection']}

    if args.discover:
        do_discovery(args.config.get("schemas"))

    elif args.catalog:
        do_sync(conn_config, args.catalog, args.config.get('default_replication_method'))
    else:
        LOGGER.info("No properties were selected")
    return


def main():
    try:
        main_impl()
    except Exception as exc:
        LOGGER.critical(exc)
