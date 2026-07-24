#!/usr/bin/env python

import base64
import os
import zlib

from pandocfilters import Image, Para, get_caption, toJSONFilter

# Diagram types that will be supported.
DIAGRAM_TYPES = [
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
DIAGRAM_SYNONYMNS = {
    "dot": "graphviz",
    "c4": "c4plantuml",
    "vega-lite": "vegalite",
}
AVAILABLE_DIAGRAMS = DIAGRAM_TYPES + list(DIAGRAM_SYNONYMNS.keys())

# List of diagrams types the user chooses not to process
DIAGRAM_BLACKLIST = list(
    filter(
        lambda d: d in AVAILABLE_DIAGRAMS,
        os.environ.get("KROKI_DIAGRAM_BLACKLIST", "").split(","),
    )
)

# kroki server to point to
KROKI_SERVER = os.environ.get("KROKI_SERVER", "https://kroki.io/")
KROKI_SERVER = KROKI_SERVER[:-1] if KROKI_SERVER[-1] == "/" else KROKI_SERVER


def kroki(key, value, format_, _):
    if key == "CodeBlock":
        [[ident, classes, keyvals], content] = value
        diagram_classes = list(set(AVAILABLE_DIAGRAMS) & set(classes))
        if len(diagram_classes) == 1 and diagram_classes[0] not in DIAGRAM_BLACKLIST:
            caption, typef, keyvals = get_caption(keyvals)

            # Divine the correct diagram type to use with kroki
            if diagram_classes[0] in DIAGRAM_SYNONYMNS.keys():
                diagram_type = DIAGRAM_SYNONYMNS[diagram_classes[0]]
            else:
                diagram_type = diagram_classes[0]

            # create the url to the kroki diagram and link as an image
            encoded = base64.urlsafe_b64encode(
                zlib.compress(content.encode("utf-8"), 9)
            ).decode()
            url = KROKI_SERVER + "/" + diagram_type + "/svg/" + encoded
            if diagram_type == "mermaid":
                url += "?html-labels=false"

            return Para([Image([ident, [], keyvals], caption, [url, typef])])


def main():
    toJSONFilter(kroki)


if __name__ == "__main__":
    main()
