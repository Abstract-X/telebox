from typing import Optional
import re

from httpx import Client
import lxml.html  # noqa
from lxml.html import HtmlElement  # noqa

from apicodegen.documentation.types import Type, Method, Field, Parameter


field_value_patterns = (
    re.compile(r', always “([A-Za-z0-9_]+)”$'),
    re.compile(r", must be ([A-Za-z0-9_]+)$")
)
type_pattern = r"[A-Z][a-zA-Z0-9]+(?:[A-Z][a-zA-Z0-9]+)*"
method_result_type_patterns = (
    re.compile(rf"On success, .*?([Aa]rray of {type_pattern}) .*?is returned" ),
    re.compile(rf"On success, .*?({type_pattern}) (?:object )?is returned" ),
    re.compile(rf"On success, returns .*?({type_pattern}) object" ),
    re.compile(rf"Returns .*?({type_pattern}) of .*?on success" ),
    re.compile(rf"Returns .*?([Aa]rray of {type_pattern}) objects" ),
    re.compile(rf"Returns .*?of .*?({type_pattern}) object" ),
    re.compile(rf"Returns .*?({type_pattern}) object" ),
    re.compile(rf"Returns .*?(?:as )?({type_pattern}) on success" )
)


class Documentation:
    def __init__(self, types: list[Type], methods: list[Method]):
        self.types: list[Type] = types
        self.type_names: set[str] = {i.name for i in types}
        self.methods: list[Method] = methods


def get_documentation() -> Documentation:
    content = _get_content()
    types, methods = _get_entities(content)

    return Documentation(
        types=types,
        methods=methods
    )


def _get_content() -> str:
    with Client() as client:
        response = client.get(
            url="https://core.telegram.org/bots/api",
            headers={
                "accept": "text/html",
                "accept-encoding": "gzip",
                "accept-language": "en",
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
            }
        )
        response.raise_for_status()

        return response.text


def _get_entities(content: str) -> tuple[list[Type], list[Method]]:
    type_elements = {}
    method_elements = {}

    for name, elements in _get_structured_elements(content).items():
        if _check_type_element(name, elements):
            type_elements[name] = elements
        elif _check_method_element(name, elements):
            method_elements[name] = elements

    types = [
        _get_type(
            name=name,
            elements=elements
        )
        for name, elements in type_elements.items()
    ]
    methods = [
        _get_method(
            name=name,
            elements=elements
        )
        for name, elements in method_elements.items()
    ]

    return types, methods


def _get_structured_elements(content: str) -> dict[str, list[HtmlElement]]:
    document = lxml.html.fromstring(content)
    elements = {}
    name = None

    for br in document.xpath("//br"):
        br.tail = "\n" + (br.tail or "")
        br.drop_tag()

    for i in document.xpath('//*[@id="dev_page_content"]')[0]:
        if not isinstance(i, HtmlElement):
            continue

        if i.tag == "h3":
            name = None
        elif i.tag == "h4":
            name = i.text_content()
            elements[name] = []
        elif name is not None:
            elements[name].append(i)

    return elements


def _check_type_element(name: str, elements: list[HtmlElement]) -> bool:
    if not (name[0].isupper() and (" " not in name)):
        return False

    for element in elements:
        if element.tag == "table":
            names = {
                i.text_content()
                for i in element.find("thead").find("tr").findall("th")
            }

            if names != {"Field", "Type", "Description"}:
                return False

    return True


def _check_method_element(name: str, elements: list[HtmlElement]) -> bool:
    if not (name[0].islower() and (" " not in name)):
        return False

    for element in elements:
        if element.tag == "table":
            names = {
                i.text_content()
                for i in element.find("thead").find("tr").findall("th")
            }

            if names != {"Parameter", "Type", "Required", "Description"}:
                return False

    return True


def _get_type(name: str, elements: list[HtmlElement]) -> Type:
    fields = []
    types = []
    description = None

    for element in elements:
        if (element.tag == "p") and (not description):
            description = element.text_content()
        elif element.tag == "table":
            for tr in element.find("tbody").findall("tr"):
                fields.append(
                    _get_type_field(tr)
                )
        elif element.tag == "ul":
            for li in element.findall("li"):
                a = li.find("a")

                if a is not None:
                    types.append(
                        a.text_content()
                    )

    if (
        (not fields)
        and (not types)
        and ("currently holds no information" not in description.lower())
        and (name != "InputFile")
    ):
        raise ValueError(f"{name!r} has no fields or types!")
    elif fields and types:
        raise ValueError(f"{name!r} has both fields and types!")

    fields.sort(key=lambda field_: (1 if field_.value else 0, field_.is_optional))

    return Type(
        name=name,
        description=description,
        fields=fields,
        types=types,
        is_union=types and not fields
    )


def _get_method(name: str, elements: list[HtmlElement]) -> Method:
    parameters = []
    description = None

    for element in elements:
        if (element.tag == "p") and (not description):
            description = element.text_content()
        elif element.tag == "table":
            for tr in element.find("tbody").findall("tr"):
                parameters.append(
                    _get_method_parameter(tr)
                )

    if (
        (not parameters)
        and ("requires no parameters" not in description.lower())
    ):
        raise ValueError(f"{name!r} has no parameters!")

    raw_result_type = _get_method_raw_result_type(description)
    result_types, result_array_nesting = _get_types_and_array_nesting(raw_result_type)

    parameters.sort(key=lambda parameter_: parameter_.is_optional)

    return Method(
        name=name,
        result_types=result_types,
        result_array_nesting=result_array_nesting,
        description=description,
        parameters=parameters
    )


def _get_type_field(element: HtmlElement) -> Field:
    name, raw_type, description = [i.text_content() for i in element.findall("td")]
    types, array_nesting = _get_types_and_array_nesting(raw_type)

    return Field(
        name=name,
        types=types,
        array_nesting=array_nesting,
        description=description,
        is_optional=description.startswith("Optional. "),
        value=_get_type_field_value(description)
    )


def _get_method_parameter(element: HtmlElement) -> Parameter:
    name, raw_type, is_required, description = [i.text_content() for i in element.findall("td")]
    types, array_nesting = _get_types_and_array_nesting(raw_type)

    return Parameter(
        name=name,
        types=types,
        array_nesting=array_nesting,
        description=description,
        is_optional=is_required == "Optional"
    )


def _get_method_raw_result_type(description: str) -> str:
    for i in method_result_type_patterns:
        match = i.search(description)

        if match is not None:
            type_ = match.group(1).strip()

            if "otherwise True is returned" in description:
                type_ += " or True"

            return type_

    raise ValueError(f"Unknown result type! (description={description!r})")


def _get_type_field_value(description: str) -> Optional[str]:
    for i in field_value_patterns:
        match = i.search(description)

        if match is not None:
            return match.group(1).strip()


def _get_types_and_array_nesting(raw_type: str) -> tuple[list[str], int]:
    raw_type = raw_type.replace(" and ", ",").replace(" or ", ",")
    array_nesting = 0

    while raw_type.lower().startswith("array of "):
        array_nesting += 1
        raw_type = raw_type[9:]

    types = []

    for i in raw_type.split(","):
        i = i.strip()

        if i.lower() == "int":
            types.append("Integer")
        else:
            types.append(i)

    return types, array_nesting
