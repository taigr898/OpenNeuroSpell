# coding: utf8
from __future__ import unicode_literals

import hug
from hug_middleware_cors import CORSMiddleware
import spacy
import sys

spacy.prefer_gpu()

#MODELS = {
#    "en_core_web_sm": spacy.load("en_core_web_sm"),
#    "en_core_web_md": spacy.load("en_core_web_md"),
#    "en_core_web_lg": spacy.load("en_core_web_lg"),
#    "de_core_news_sm": spacy.load("de_core_news_sm"),
#    "es_core_news_sm": spacy.load("es_core_news_sm"),
#    "pt_core_news_sm": spacy.load("pt_core_news_sm"),
#    "fr_core_news_sm": spacy.load("fr_core_news_sm"),
#    "fr_core_news_md": spacy.load("fr_core_news_md"),
#    "it_core_news_sm": spacy.load("it_core_news_sm"),
#    "nl_core_news_sm": spacy.load("nl_core_news_sm"),
#}

MODELS = {
    "en_core_web_sm": spacy.load("en_core_web_sm")
    ,"fr_core_news_sm": spacy.load("fr_core_news_sm")
}

def get_model_desc(nlp, model_name):
    """Get human-readable model name, language name and version."""
    lang_cls = spacy.util.get_lang_class(nlp.lang)
    lang_name = lang_cls.__name__
    model_version = nlp.meta["version"]
    return "{} - {} (v{})".format(lang_name, model_name, model_version)


@hug.get("/models")
def models():
    return {name: get_model_desc(nlp, name) for name, nlp in MODELS.items()}


@hug.post("/dep")
def dep(
    text: str,
    model: str,
    collapse_punctuation: bool = False,
    collapse_phrases: bool = False,
):
    """Get dependencies for displaCy visualizer."""
    nlp = MODELS[model]
    doc = nlp(text)
    if collapse_phrases:
        for np in list(doc.noun_chunks):
            np.merge(tag=np.root.tag_, lemma=np.root.lemma_, ent_type=np.root.ent_type_)
    options = {"collapse_punct": collapse_punctuation}
    return spacy.displacy.parse_deps(doc, options)

@hug.post("/tag")
def tag(
    text: str,
    model: str,
):
    print("TAG=====")
    print("TEXT="+text)
    print("MODEL="+model)
    nlp = MODELS[model]
    doc = nlp(text)
    return [[token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
            token.shape_, token.is_alpha, token.is_stop]
            for token in doc
    ]

@hug.post("/ent")
def ent(text: str, model: str):
    """Get entities for displaCy ENT visualizer."""
    print("ENT=====")
    print("TEXT="+text)
    print("MODEL="+model)
    nlp = MODELS[model]
    doc = nlp(text)
    return [
        {"start": ent.start_char, "end": ent.end_char, "label": ent.label_}
        for ent in doc.ents
    ]


if __name__ == "__main__":
    import waitress

    app = hug.API(__name__)
    app.http.add_middleware(CORSMiddleware(app))
    if len(sys.argv) == 1 :
        waitress.serve(__hug_wsgi__, port=8091)
    else :
        waitress.serve(__hug_wsgi__, port=(8091+int(sys.argv[1])))
    