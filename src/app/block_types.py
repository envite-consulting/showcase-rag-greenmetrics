ALLOWED_BLOCK_TYPES: set[str] = {
    # ===== Standard block types (# - ######) =====
    "title",    # Block after the document title (#)
    "heading",  # Block after a heading (## - #####)
    "text",     # Base block type
    "special",  # Catch-all for undefined block types

    # ===== Special block types (######) =====
    # Standard paper sections
    "definition",
    "theorem",
    "lemma",
    "corollary",
    "proposition",
    "proof",
    "remark",
    "claim",
    "observation",
    "example",
    "algorithm",
    "axiom",
    "assumption",
    "conjecture",
    "question",
    "counterexample",
    "statement",
    "problem",
    "note",
    "notation",
    "convention",
    "result",
    "case",
    "figure",
    "table",

    # Paper sections that are usually less relevant for retrieval
    "abstract",
    "keywords",
    "pacs",
    "msc",
    "doi",
    "contents",
    "index",
    "acknowledgments",

    # Misc
    "outline",
    "addendum",
    "prerequisites",
    "disclaimer",
    "conclusion",
    "discussion",
}

# Dataset-specific aliases for block types with spelling variants,
# abbreviations, translations, or similar forms.
# Format: [alias, canonical block type].
BLOCK_TYPES_ALIASES: dict[str, str] = {
    # keywords
    "key": "keywords",
    "keyword": "keywords",

    # Plurals
    "remarks": "remark",
    "examples": "example",
    "assumptions": "assumption",
    "hypothesis": "assumption",
    "hypotheses": "assumption",

    # acknowledgments
    "acknowledgement": "acknowledgments",
    "acknowledgements": "acknowledgments",
    "acknowledgment": "acknowledgments",
    "acknowledgments": "acknowledgments",
    "acknowledgments\u200b": "acknowledgments",

    # abstract / contents
    "?abstractname?": "abstract",
    "abstractname": "abstract",
    "?contentsname?": "contents",
    "contentsname": "contents",

    # sub-*
    "sublemma": "lemma",
    "subfact": "statement",
    "fact": "statement",
    "facts": "statement",

    # proposition
    "prop": "proposition",

    # corollary
    "corolary": "corollary",
    "corrolary": "corollary",
    "corallary": "corollary",
    "corolary.": "corollary",
    "corrolary.": "corollary",

    # theorem / definition
    "theorem-definition": "theorem",
    "theorem–definition": "theorem",
    "definition-lemma": "definition",
    "theoreme": "theorem",
    "theorem(kamienny": "theorem",

    # Other languages: French / Spanish / Portuguese / Italian / Japanese
    "définition": "definition",
    "théorème": "theorem",
    "theorème": "theorem",
    "lemme": "lemma",
    "corollaire": "corollary",
    "remarque": "remark",
    "preuve": "proof",
    "exemple": "example",
    "problème": "problem",
    "remerciements": "acknowledgments",
    "definición": "definition",
    "definição": "definition",
    "definizione": "definition",
    "proposición": "proposition",
    "proposizione": "proposition",
    "proposição": "proposition",
    "lema": "lemma",
    "corolario": "corollary",
    "corolário": "corollary",
    "observación": "observation",
    "observação": "observation",
    "osservazione": "observation",
    "ejemplo": "example",
    "exemplo": "example",
    "teorema": "theorem",
    "概要": "abstract",
    "証明": "proof",
}
