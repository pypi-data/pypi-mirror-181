# komle_witslm_client/bindings/v1411/delete/_abs.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:8303e32165e8ecb1e71ee1daf2c80a31c9900992
# Generated 2022-10-17 03:39:40.737672 by PyXB version 1.2.6 using Python 3.10.4.final.0
# Namespace http://www.energistics.org/schemas/abstract [xmlns:abs]

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
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:d61e4130-834f-41dd-9235-d512510b552e')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.6'

# A holder for module-level binding classes so we can access them from
# inside class definitions where property names may conflict.
_module_typeBindings = pyxb.utils.utility.Object()

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://www.energistics.org/schemas/abstract', create_if_missing=True)
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


# Complex type {http://www.energistics.org/schemas/abstract}abstractObject with content type EMPTY
class abstractObject (pyxb.binding.basis.complexTypeDefinition):
    """The intended abstract supertype of all schema roots 
			that may be a member of a substitution group (whether contextual or data).
			The type of root global elements should be extended from this type and the 
			root global element should be declared to be a member of one of the above substitution groups."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'abstractObject')
    _XSDLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.1.1_Data_Schema/abstract_v1.0/xsd_schemas/sub_abstractSubstitutionGroup.xsd', 30, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.abstractObject = abstractObject
Namespace.addCategoryObject('typeBinding', 'abstractObject', abstractObject)


abstractDataObject = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'abstractDataObject'), abstractObject, abstract=pyxb.binding.datatypes.boolean(1), documentation='Substitution group for normative data objects.', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.1.1_Data_Schema/abstract_v1.0/xsd_schemas/sub_abstractSubstitutionGroup.xsd', 18, 1))
Namespace.addCategoryObject('elementBinding', abstractDataObject.name().localName(), abstractDataObject)

abstractContextualObject = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'abstractContextualObject'), abstractObject, abstract=pyxb.binding.datatypes.boolean(1), documentation='Substitution group for contextual objects.', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.1.1_Data_Schema/abstract_v1.0/xsd_schemas/sub_abstractSubstitutionGroup.xsd', 24, 1))
Namespace.addCategoryObject('elementBinding', abstractContextualObject.name().localName(), abstractContextualObject)
