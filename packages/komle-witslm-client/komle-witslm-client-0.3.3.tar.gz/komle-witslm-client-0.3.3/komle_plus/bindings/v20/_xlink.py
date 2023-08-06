# komle_plus/bindings/v20/_xlink.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:b43cd366527ddb6a0e58594876e07421e0148f30
# Generated 2022-10-17 04:03:28.030193 by PyXB version 1.2.6 using Python 3.10.4.final.0
# Namespace http://www.w3.org/1999/xlink [xmlns:xlink]

from __future__ import unicode_literals
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import io
import pyxb.utils.utility
import pyxb.utils.domutils
import sys
import pyxb.utils.six as _six
# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:aeabab8e-5c30-477e-bdd6-5e8ed893ecb8')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.6'

# A holder for module-level binding classes so we can access them from
# inside class definitions where property names may conflict.
_module_typeBindings = pyxb.utils.utility.Object()

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://www.w3.org/1999/xlink', create_if_missing=True)
Namespace.configureCategories(['typeBinding', 'elementBinding'])

def CreateFromDocument (xml_text, fallback_namespace=None, location_base=None, default_namespace=None):
    """Parse the given XML and use the document element to create a
    Python instance.

    @param xml_text An XML document.  This should be data (Python 2
    str or Python 3 bytes), or a text (Python 2 unicode or Python 3
    str) in the L{pyxb._InputEncoding} encoding.

    @keyword fallback_namespace An absent L{pyxb.Namespace} instance
    to use for unqualified names when there is no default namespace in
    scope.  If unspecified or C{None}, the namespace of the module
    containing this function will be used, if it is an absent
    namespace.

    @keyword location_base: An object to be recorded as the base of all
    L{pyxb.utils.utility.Location} instances associated with events and
    objects handled by the parser.  You might pass the URI from which
    the document was obtained.

    @keyword default_namespace An alias for @c fallback_namespace used
    in PyXB 1.1.4 through 1.2.6.  It behaved like a default namespace
    only for absent namespaces.
    """

    if pyxb.XMLStyle_saxer != pyxb._XMLStyle:
        dom = pyxb.utils.domutils.StringToDOM(xml_text)
        return CreateFromDOM(dom.documentElement)
    if fallback_namespace is None:
        fallback_namespace = default_namespace
    if fallback_namespace is None:
        fallback_namespace = Namespace.fallbackNamespace()
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=fallback_namespace, location_base=location_base)
    handler = saxer.getContentHandler()
    xmld = xml_text
    if isinstance(xmld, _six.text_type):
        xmld = xmld.encode(pyxb._InputEncoding)
    saxer.parse(io.BytesIO(xmld))
    instance = handler.rootObject()
    return instance

def CreateFromDOM (node, fallback_namespace=None, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if fallback_namespace is None:
        fallback_namespace = default_namespace
    if fallback_namespace is None:
        fallback_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, fallback_namespace)


# Atomic simple type: [anonymous]
class STD_ANON (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v2.0_Data_Schema/energyml/data/common/v2.1/xsd_schemas/xlink/1.0.0/xlinks.xsd', 58, 6)
    _Documentation = None
STD_ANON._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=STD_ANON)
STD_ANON.new = STD_ANON._CF_enumeration.addEnumeration(unicode_value='new', tag='new')
STD_ANON.replace = STD_ANON._CF_enumeration.addEnumeration(unicode_value='replace', tag='replace')
STD_ANON.embed = STD_ANON._CF_enumeration.addEnumeration(unicode_value='embed', tag='embed')
STD_ANON.other = STD_ANON._CF_enumeration.addEnumeration(unicode_value='other', tag='other')
STD_ANON.none = STD_ANON._CF_enumeration.addEnumeration(unicode_value='none', tag='none')
STD_ANON._InitializeFacetMap(STD_ANON._CF_enumeration)
_module_typeBindings.STD_ANON = STD_ANON

# Atomic simple type: [anonymous]
class STD_ANON_ (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v2.0_Data_Schema/energyml/data/common/v2.1/xsd_schemas/xlink/1.0.0/xlinks.xsd', 85, 6)
    _Documentation = None
STD_ANON_._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=STD_ANON_)
STD_ANON_.onLoad = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='onLoad', tag='onLoad')
STD_ANON_.onRequest = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='onRequest', tag='onRequest')
STD_ANON_.other = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='other', tag='other')
STD_ANON_.none = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='none', tag='none')
STD_ANON_._InitializeFacetMap(STD_ANON_._CF_enumeration)
_module_typeBindings.STD_ANON_ = STD_ANON_
