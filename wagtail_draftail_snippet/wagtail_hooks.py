from django.urls import include, path
from django.urls import reverse_lazy
from django.utils.translation import gettext

from wagtail.admin.rich_text.editors.draftail import features as draftail_features
from wagtail import hooks

from . import urls
from .richtext import (
    ContentstateSnippetLinkConversionRule,
    ContentstateSnippetEmbedConversionRule,
    SnippetLinkHandler,
    SnippetEmbedHandler,
)


@hooks.register("register_rich_text_features")
def register_snippet_link_feature(features):
    feature_name = "snippet-link"
    type_ = "SNIPPET"

    features.register_link_type(SnippetLinkHandler)

    # wagtailadmin/js/chooser-modal.js is needed for window.ChooserModalOnloadHandlerFactory
    js_include = [
        "wagtailadmin/js/chooser-modal.js",
        "wagtail_draftail_snippet/js/snippet-chooser-modal.js", # onload handlers
        "wagtail_draftail_snippet/js/snippet-model-chooser-modal.js", # onload handlers
        "wagtail_draftail_snippet/js/wagtail-draftail-snippet.js",
    ]

    features.register_editor_plugin(
        "draftail",
        feature_name,
        draftail_features.EntityFeature(
            {
                "type": type_,
                "icon": "snippet",
                "description": gettext("Snippet Link"),
                "chooserUrls": {
                    "snippetModelChooser": reverse_lazy("wagtaildraftailsnippet:choose-snippet-link-model"),
                    "snippetChooser": reverse_lazy('wagtaildraftailsnippet:choose_generic'),
                },
            },
            js=js_include,
        ),
    )

    features.register_converter_rule(
        "contentstate", feature_name, ContentstateSnippetLinkConversionRule
    )


@hooks.register("register_rich_text_features")
def register_snippet_embed_feature(features):
    feature_name = "snippet-embed"
    type_ = "SNIPPET-EMBED"

    # Defines a handler for converting db saved content,
    # e.g. <embed app-name="xyz" content-type-name="abcd" embedtype="snippet" id="2"/>
    # into frontend HTML
    features.register_embed_type(SnippetEmbedHandler)

    # todo prob need to add this...
    # # define how to convert between editorhtml's representation of embeds and
    # # the database representation
    # features.register_converter_rule(
    #     "editorhtml", "embed", EditorHTMLEmbedConversionRule
    # )

    js_include = [
        "wagtailadmin/js/chooser-modal.js",  # is needed for window.ChooserModalOnloadHandlerFactory
        "wagtail_draftail_snippet/js/snippet-chooser-modal.js", # onload handlers
        "wagtail_draftail_snippet/js/snippet-model-chooser-modal.js", # onload handlers
        "wagtail_draftail_snippet/js/wagtail-draftail-snippet.js", # draftail choosers, Interfaces with Wagtail's ModalWorkflow
    ]

    features.register_editor_plugin(
        "draftail",
        feature_name,
        draftail_features.EntityFeature(
            {
                "type": type_,
                "icon": "code",
                "description": gettext("Snippet Embed"),
                "chooserUrls": {
                    "snippetChooser": reverse_lazy('wagtaildraftailsnippet:choose_generic'),
                    "snippetEmbedModelChooser": reverse_lazy("wagtaildraftailsnippet:choose-snippet-embed-model"),
                },
            },
            js=js_include,
        ),
    )

    # Define how to convert between contentstate's representation of embeds and
    # the database representation
    features.register_converter_rule(
        "contentstate", feature_name, ContentstateSnippetEmbedConversionRule
    )


@hooks.register("register_admin_urls")
def register_admin_urls():
    return [path("snippets/", include(urls, namespace="wagtaildraftailsnippet"))]
