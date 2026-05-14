# from linkml_runtime.utils.schemaview import SchemaView
# sv = SchemaView("target/linkml/diagram-layout.linkml.yml")
# print(sv.schema.extensions)

import yaml
from pyoxigraph import Dataset, Quad, NamedNode


def is_curie(element):
    return not element.startswith("http") and ":" in element


def is_uri(element):
    return element.startswith("http")


def val(element, schema):
    if is_curie(element):
        name = curie_to_uri(element, schema)
    elif not is_uri(element):
        name = name_to_uri(element, schema)
    else:
        name = element
    
    return name


def curie_to_uri(curie, schema):
    prefix, name = curie.split(":")

    return f"{schema["prefixes"][prefix]}{name}"


def name_to_uri(name, schema):
    return curie_to_uri(f"{schema['default_prefix']}:{name}", schema)


def metadata(schema, dataset):
    dataset.add(Quad(NamedNode(val(schema["id"], schema)), NamedNode(val("rdf:type", schema)), NamedNode(val(schema["instantiates"], schema))))

    # id: https://cim.ucaiug.io/grid/DiagramLayout/2.1
    # instantiates: https://cim.ucaiug.io/grid/DiagramLayout
    # version: '2.1'  # NOTE: PAV version, not OWL version IRI
    # name: diagram-layout  # NOTE: rdfs:label, but must conform to NCName pattern. Weird.
    # aliases: Diagram Layout Application Profile 2.1  # Derive rdfs:label from this as well
    # title: Diagram Layout 2.1
    # description: Diagram Layout application profile specific the expected data to be exchanges to describe a Common Information Model (CIM) Diagram Layout.
    # prefixes:
    # linkml: https://w3id.org/linkml/
    # cim: https://cim.ucaiug.io/ns#
    # dl: http://iec.ch/TC57/ns/CIM/DiagramLayout-EU#
    # dctype: http://purl.org/dc/dcmitype/
    # rdf: http://www.w3.org/1999/02/22-rdf-syntax-ns#
    # rdfs: http://www.w3.org/2000/01/rdf-schema#
    # xsd: http://www.w3.org/2001/XMLSchema#
    # dcat: http://www.w3.org/ns/dcat#
    # dcterms: http://purl.org/dc/terms/
    # dc: http://purl.org/dc/elements/1.1/
    # owl: http://www.w3.org/2002/07/owl#
    # skos: http://www.w3.org/2004/02/skos/core#
    # vann: http://purl.org/vocab/vann/
    # dom: https://cim.ucaiug.io/ns/domain#
    # qk: http://qudt.org/vocab/quantitykind/
    # unit: https://qudt.org/vocab/unit/
    # orcid: https://orcid.org/
    # default_prefix: cim
    # default_range: string
    # imports:
    # - linkml:types
    # #   - ./extra-types
    # default_curi_maps:
    # - semweb_context
    # source: iec61970cim17v40_iec61968cim13v13a_iec62325cim03v17a.eap
    # conforms_to: https://cim.ucaiug.io/prof/Profile/1.0  # Profile schema
    # created_by: orcid:0009-0009-8211-926X
    # contributors:
    # - orcid:0000-0002-7167-7321
    # - orcid:0000-0001-7508-7428
    # extensions:  # TODO: Feature request for LinkML to add these DCTerms terms
    # issued: '2025-03-06T17:59:40+01:00'
    # rightsHolder: UCA International User Group
    # rights: Copyright
    # publisher: https://www.ucaiug.org  # NOTE: Supposed to be native, but somehow doesn't work.
    # # Profile resources
    # # syntax:
    # # <role>: <language>/<serialization>
    # constraints: shacl/ttl
    # vocabulary: rdfs+/ttl
    # profile: prof/jsonld
    # schema:  # empty means "none"
    # license: http://www.apache.org/licenses/LICENSE-2.0
    # last_updated_on: "2025-03-06"  # dcterms:modified "2025-03-06"^^xsd:date ;
    # comments: Diagram Layout application profile defined by DX-PROF
    # in_language: en-GB



if __name__ == "__main__":
    schema_file = "target/linkml/diagram-layout.linkml.yml"
    vocab_dataset = Dataset()

    with open(schema_file) as f:
        schema_dict = yaml.safe_load(f)
    
    metadata(schema_dict, vocab_dataset)
    print(vocab_dataset)

    # for class_name, class_ in schema_dict["classes"].items():
    #     vocab_dataset.add(Quad(NamedNode()))