# Pandoc Kroki Filter

This is a pandoc filter that converts code blocks into diagrams using
[kroki.io](https://kroki.io/)!

````md
```blockdiag
blockdiag {
  Kroki -> generates -> "Block diagrams";
  Kroki -> is -> "very easy!";

  Kroki [color = "greenyellow"];
  "Block diagrams" [color = "pink"];
  "very easy!" [color = "orange"];
}
```

```mermaid
graph TD
  A[ Anyone ] -->|Can help | B( Go to github.com/yuzutech/kroki )
  B --> C{ How to contribute? }
  C --> D[ Reporting bugs ]
  C --> E[ Sharing ideas ]
  C --> F[ Advocating ]
```
````

## Usage

Install it with pip:

```sh
pip install git+https://gitlab.com/myriacore/pandoc-kroki-filter.git
```

And use it like any other pandoc filter:

```sh
pandoc example/sample.md -o example/sample.pdf --filter pandoc-kroki
```

See the provided [example markdown](example/sample.md) and the [example
pdf](example/sample.pdf) for a better understanding of what types of diagrams
are supported via kroki, and how to use them. 

## Configuration

By default, this filter will use `https://kroki.io/` as the endpoint for the
kroki server. If you want to use http, or are self-hosting and want to use
*your own* kroki server, you can use the `KROKI_SERVER` environment variable:

```sh
KROKI_SERVER='https://kroki.my.domain/' pandoc example/sample.md -o example/sample.pdf --filter pandoc-kroki
```

## Caveats

Currently, the mermaid support is kinda flaky, as you'll be able to see from the
Mermaid section in [the example pdf](example/sample.pdf). The bubble for the
graph appears, but the text apparently doesn't, for whatever reason.
