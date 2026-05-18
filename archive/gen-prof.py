# from linkml_runtime.utils.schemaview import SchemaView
# sv = SchemaView("target/linkml/diagram-layout.linkml.yml")
# print(sv.schema.extensions)

from functools import partial
import yaml
from pyoxigraph import Dataset, Quad, NamedNode, Literal, serialize, RdfFormat

ROLES = ["constraints", "vocabulary", "schema", "profile"]


def is_curie(element):
    return ":" in element and not (element.startswith("http://") or element.startswith("https://"))


def is_uri(element):
    return element.startswith("http")


def to_uri(element, schema):
    if is_curie(element):
        name = curie_to_uri(element, schema)
    elif not is_uri(element):
        name = name_to_uri(element, schema)
    else:
        name = element

    return NamedNode(name)


def curie_to_uri(curie, schema):
    prefix, name = curie.split(":")

    return f"{schema["prefixes"][prefix]}{name}"


def name_to_uri(name, schema):
    return curie_to_uri(f"{schema['default_prefix']}:{name}", schema)


def media_type(format):
    return {
        "turtle": "https://www.iana.org/assignments/media-types/text/turtle",
    }[format]


def to_prof_resource(schema, dataset):
    q = partial(Quad, graph_name=None)
    val = Literal
    uri = partial(to_uri, schema=schema)

    for role, lang in schema["extensions"].items():
        if role in ROLES and role != "profile" and lang:
            l, format = lang.split("/")
            res = uri(f"{schema['id']}#{role}")
            dataset.add(q(res, uri("prof:hasRole"), uri(f"role:{role}")))
            dataset.add(q(res, uri("rdf:type"), uri("prof:ResourceDescriptor")))
            dataset.add(q(res, uri("rdfs:label"), val(f"{schema['aliases'][0]} {role.title()}")))
            dataset.add(q(res, uri("dcterms:title"), val(f"{schema['title']} {role.title()}")))
            dataset.add(q(res, uri("dcterms:format"), uri(media_type(format))))
            dataset.add(
                q(
                    res,
                    uri("dcterms:description"),
                    val(f"{role.title()} for {schema['title']} profile described in RDFS+."),
                )
            )
            dataset.add(q(res, uri("adms:representationTechnique"), uri(f"{schema['id']}/lang/{l}")))


def to_profile(schema, dataset):
    q = partial(Quad, graph_name=None)
    val = Literal  # TODO: Use `default_range` mapped to XSD
    uri = partial(to_uri, schema=schema)

    dataset.add(q(uri(schema["instantiates"]), uri("rdf:type"), uri("prof:Profile")))

    s = uri(schema["id"])
    for _q in [
        q(s, uri("rdf:type"), uri("prof:Profile")),
        q(s, uri("dcat:version"), val(schema["version"])),
        q(s, uri("dcat:isVersionOf"), uri(schema["instantiates"])),
        q(s, uri("dcterms:issued"), val(schema["extensions"]["issued"], datatype=uri("xsd:dateTime"))),
        q(s, uri("dcterms:rightsHolder"), val(schema["extensions"]["rights_holder"])),
        q(s, uri("dcterms:rights"), val(schema["extensions"]["rights"])),
        q(s, uri("dcterms:conformsTo"), uri(schema["conforms_to"])),
        *[q(s, uri("dcterms:contributor"), uri(o)) for o in schema["contributors"]],
        q(s, uri("dcterms:creator"), uri(schema["created_by"])),
        q(s, uri("dcterms:publisher"), uri(schema["extensions"]["publisher"])),
        q(s, uri("dcterms:description"), val(schema["description"])),
        q(s, uri("dcterms:title"), val(schema["title"])),
        *[q(s, uri("rdfs:comment"), val(o)) for o in schema["comments"]],
        *[q(s, uri("rdfs:label"), val(o)) for o in schema["aliases"]],  # TODO: What about `name` from LinkML?
        q(s, uri("dcterms:language"), val(schema["in_language"], datatype=uri("xsd:language"))),
        q(s, uri("dcterms:license"), uri(schema["license"])),
    ]:
        dataset.add(_q)

    for role, lang in schema["extensions"].items():
        if role in ROLES and role != "profile" and lang:
            dataset.add(q(s, uri("prof:hasResource"), uri(f"{schema['id']}#{role}")))


if __name__ == "__main__":
    schema_file = "target/linkml/diagram-layout.linkml.yml"
    prof_dataset = Dataset()

    with open(schema_file) as f:
        schema_dict = yaml.safe_load(f)

    to_profile(schema_dict, prof_dataset)
    to_prof_resource(schema_dict, prof_dataset)
    serialize(
        prof_dataset,
        "prof.ttl",
        RdfFormat.TURTLE,  # TODO: HTTPS URIs get rendered improperly, this seems to be a bug with the serialization. With `JSON_LD` it works fine.
        prefixes=schema_dict["prefixes"],
        base_iri=curie_to_uri(schema_dict["default_prefix"] + ":", schema_dict),
    )

    # for class_name, class_ in schema_dict["classes"].items():
    #     vocab_dataset.add(Quad(NamedNode()))
