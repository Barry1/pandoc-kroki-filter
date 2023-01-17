#!/usr/bin/env python

import base64
import os
import sys
import zlib

from pandocfilters import (
    Image,
    Para,
    get_caption,
    get_extension,
    get_filename4code,
    toJSONFilter,
)

# Diagram types that will be supported.
DIAGRAM_TYPES: list[str] = [
    "blockdiag",
    "bpmn",
    "bytefield",
    "seqdiag",
    "actdiag",
    "nwdiag",
    "packetdiag",
    "rackdiag",
    "c4plantuml",
    "ditaa",
    "erd",
    "excalidraw",
    "graphviz",
    "mermaid",
    "nomnoml",
    "plantuml",
    "svgbob",
    "umlet",
    "vega",
    "vegalite",
    "wavedrom",
]
DIAGRAM_SYNONYMNS: dict[str, str] = {
    "dot": "graphviz",
    "c4": "c4plantuml",
    "vega-lite": "vegalite",
}
AVAILABLE_DIAGRAMS: list[str] = DIAGRAM_TYPES + list(DIAGRAM_SYNONYMNS.keys())

# List of diagrams types the user chooses not to process
DIAGRAM_BLACKLIST: list[str] = list(
    filter(
        lambda d: d in AVAILABLE_DIAGRAMS,
        os.environ.get("KROKI_DIAGRAM_BLACKLIST", "").split(","),
    )
)

# kroki server to point to
KROKI_SERVER: str = os.environ.get("KROKI_SERVER", "https://kroki.io/")
KROKI_SERVER = KROKI_SERVER[:-1] if KROKI_SERVER[-1] == "/" else KROKI_SERVER


def kroki(key, value, format_, _):
    if key == "CodeBlock":
        [[ident, classes, keyvals], content] = value
        diagram_classes: list[str] = list(
            set(AVAILABLE_DIAGRAMS) & set(classes)
        )
        if (
            len(diagram_classes) == 1
            and diagram_classes[0] not in DIAGRAM_BLACKLIST
        ):
            caption, typef, keyvals = get_caption(keyvals)

            # Divine the correct diagram type to use with kroki
            if diagram_classes[0] in DIAGRAM_SYNONYMNS.keys():
                diagram_type: str = DIAGRAM_SYNONYMNS[diagram_classes[0]]
            else:
                diagram_type = diagram_classes[0]

            # create the url to the kroki diagram and link as an image
            encoded: str = base64.urlsafe_b64encode(
                zlib.compress(content.encode("utf-8"), 9)
            ).decode()
            url: str = f"{KROKI_SERVER}/{diagram_type}/svg/{encoded}"

            return Para([Image([ident, [], keyvals], caption, [url, typef])])


def main() -> None:
    toJSONFilter(kroki)


if __name__ == "__main__":
    main()
