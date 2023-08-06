# komle_witslm_client/bindings/v1410/api/witsml.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:682de33c77a81378cca97595ef81458c92565c4b
# Generated 2022-10-17 05:20:35.013716 by PyXB version 1.2.6 using Python 3.10.4.final.0
# Namespace http://www.witsml.org/api/140

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
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:55aeea1c-af06-4818-b84e-d2e8924e1232')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.6'

# A holder for module-level binding classes so we can access them from
# inside class definitions where property names may conflict.
_module_typeBindings = pyxb.utils.utility.Object()

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://www.witsml.org/api/140', create_if_missing=True)
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


# Atomic simple type: {http://www.witsml.org/api/140}timestamp
class timestamp (pyxb.binding.datatypes.dateTime):

    """A date with the time of day and a mandatory time zone.
			This type disallows an "empty" dateTime value."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'timestamp')
    _XSDLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/cs_dataTypes.xsd', 45, 1)
    _Documentation = 'A date with the time of day and a mandatory time zone.\n\t\t\tThis type disallows an "empty" dateTime value.'
timestamp._CF_pattern = pyxb.binding.facets.CF_pattern()
timestamp._CF_pattern.addPattern(pattern='.+T.+[Z+-].*')
timestamp._InitializeFacetMap(timestamp._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'timestamp', timestamp)
_module_typeBindings.timestamp = timestamp

# Atomic simple type: {http://www.witsml.org/api/140}logicalBoolean
class logicalBoolean (pyxb.binding.datatypes.boolean):

    """Values of "true" (or "1") and "false" (or "0")."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'logicalBoolean')
    _XSDLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/cs_dataTypes.xsd', 54, 1)
    _Documentation = 'Values of "true" (or "1") and "false" (or "0").'
logicalBoolean._CF_pattern = pyxb.binding.facets.CF_pattern()
logicalBoolean._CF_pattern.addPattern(pattern='.+')
logicalBoolean._InitializeFacetMap(logicalBoolean._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'logicalBoolean', logicalBoolean)
_module_typeBindings.logicalBoolean = logicalBoolean

# Atomic simple type: {http://www.witsml.org/api/140}integerCount
class integerCount (pyxb.binding.datatypes.short):

    """A integer that cannot be empty."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'integerCount')
    _XSDLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/cs_dataTypes.xsd', 66, 1)
    _Documentation = 'A integer that cannot be empty.'
integerCount._CF_pattern = pyxb.binding.facets.CF_pattern()
integerCount._CF_pattern.addPattern(pattern='.+')
integerCount._InitializeFacetMap(integerCount._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'integerCount', integerCount)
_module_typeBindings.integerCount = integerCount

# Atomic simple type: {http://www.witsml.org/api/140}abstractString
class abstractString (pyxb.binding.datatypes.string):

    """The intended abstract supertype of all strings.
			This abstract type allows the control over whitespace for all strings to be defined at a high level. 
			This type should not be used directly except to derive another type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'abstractString')
    _XSDLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/cs_dataTypes.xsd', 81, 1)
    _Documentation = 'The intended abstract supertype of all strings.\n\t\t\tThis abstract type allows the control over whitespace for all strings to be defined at a high level. \n\t\t\tThis type should not be used directly except to derive another type.'
abstractString._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
abstractString._CF_whiteSpace = pyxb.binding.facets.CF_whiteSpace(value=pyxb.binding.facets._WhiteSpace_enum.collapse)
abstractString._InitializeFacetMap(abstractString._CF_minLength,
   abstractString._CF_whiteSpace)
Namespace.addCategoryObject('typeBinding', 'abstractString', abstractString)
_module_typeBindings.abstractString = abstractString

# Atomic simple type: {http://www.witsml.org/api/140}str16
class str16 (abstractString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'str16')
    _XSDLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/cs_dataTypes.xsd', 21, 1)
    _Documentation = None
str16._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(16))
str16._InitializeFacetMap(str16._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'str16', str16)
_module_typeBindings.str16 = str16

# Atomic simple type: {http://www.witsml.org/api/140}str64
class str64 (abstractString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'str64')
    _XSDLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/cs_dataTypes.xsd', 27, 1)
    _Documentation = None
str64._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(64))
str64._InitializeFacetMap(str64._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'str64', str64)
_module_typeBindings.str64 = str64

# Atomic simple type: {http://www.witsml.org/api/140}str256
class str256 (abstractString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'str256')
    _XSDLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/cs_dataTypes.xsd', 33, 1)
    _Documentation = None
str256._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(256))
str256._InitializeFacetMap(str256._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'str256', str256)
_module_typeBindings.str256 = str256

# Atomic simple type: {http://www.witsml.org/api/140}str4096
class str4096 (abstractString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'str4096')
    _XSDLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/cs_dataTypes.xsd', 39, 1)
    _Documentation = None
str4096._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(4096))
str4096._InitializeFacetMap(str4096._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'str4096', str4096)
_module_typeBindings.str4096 = str4096

# Atomic simple type: {http://www.witsml.org/api/140}abstractTypeEnum
class abstractTypeEnum (abstractString):

    """The intended abstract supertype of all enumerated "types".
			This abstract type allows the maximum length of a type enumeration to be centrally defined.
			This type should not be used directly except to derive another type.
			It should be used for uncontrolled strings which are candidates to become enumerations at a future date."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'abstractTypeEnum')
    _XSDLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/cs_dataTypes.xsd', 107, 1)
    _Documentation = 'The intended abstract supertype of all enumerated "types".\n\t\t\tThis abstract type allows the maximum length of a type enumeration to be centrally defined.\n\t\t\tThis type should not be used directly except to derive another type.\n\t\t\tIt should be used for uncontrolled strings which are candidates to become enumerations at a future date.'
abstractTypeEnum._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(40))
abstractTypeEnum._InitializeFacetMap(abstractTypeEnum._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'abstractTypeEnum', abstractTypeEnum)
_module_typeBindings.abstractTypeEnum = abstractTypeEnum

# Atomic simple type: {http://www.witsml.org/api/140}EventType
class EventType (abstractTypeEnum, pyxb.binding.basis.enumeration_mixin):

    """These values represent the type of an event notification. """

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'EventType')
    _XSDLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/cs_catalog.xsd', 19, 1)
    _Documentation = 'These values represent the type of an event notification. '
EventType._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=EventType)
EventType.update = EventType._CF_enumeration.addEnumeration(unicode_value='update', tag='update')
EventType.add = EventType._CF_enumeration.addEnumeration(unicode_value='add', tag='add')
EventType.delete = EventType._CF_enumeration.addEnumeration(unicode_value='delete', tag='delete')
EventType._InitializeFacetMap(EventType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'EventType', EventType)
_module_typeBindings.EventType = EventType

# Atomic simple type: {http://www.witsml.org/api/140}SubscriptionAction
class SubscriptionAction (abstractTypeEnum, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'SubscriptionAction')
    _XSDLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/cs_catalog.xsd', 42, 1)
    _Documentation = None
SubscriptionAction._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=SubscriptionAction)
SubscriptionAction.add = SubscriptionAction._CF_enumeration.addEnumeration(unicode_value='add', tag='add')
SubscriptionAction.modify = SubscriptionAction._CF_enumeration.addEnumeration(unicode_value='modify', tag='modify')
SubscriptionAction.cancel = SubscriptionAction._CF_enumeration.addEnumeration(unicode_value='cancel', tag='cancel')
SubscriptionAction.verify = SubscriptionAction._CF_enumeration.addEnumeration(unicode_value='verify', tag='verify')
SubscriptionAction._InitializeFacetMap(SubscriptionAction._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'SubscriptionAction', SubscriptionAction)
_module_typeBindings.SubscriptionAction = SubscriptionAction

# Complex type {http://www.witsml.org/api/140}cs_contact with content type ELEMENT_ONLY
class cs_contact (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.witsml.org/api/140}cs_contact with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'cs_contact')
    _XSDLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/cs_contact.xsd', 26, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.witsml.org/api/140}name uses Python identifier name
    __name = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'name'), 'name', '__httpwww_witsml_orgapi140_cs_contact_httpwww_witsml_orgapi140name', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/cs_contact.xsd', 28, 3), )

    
    name = property(__name.value, __name.set, None, 'Name of contact. ')

    
    # Element {http://www.witsml.org/api/140}email uses Python identifier email
    __email = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'email'), 'email', '__httpwww_witsml_orgapi140_cs_contact_httpwww_witsml_orgapi140email', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/cs_contact.xsd', 33, 3), )

    
    email = property(__email.value, __email.set, None, 'Email address of contact. ')

    
    # Element {http://www.witsml.org/api/140}phone uses Python identifier phone
    __phone = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'phone'), 'phone', '__httpwww_witsml_orgapi140_cs_contact_httpwww_witsml_orgapi140phone', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/cs_contact.xsd', 38, 3), )

    
    phone = property(__phone.value, __phone.set, None, 'Phone number of contact. ')

    _ElementMap.update({
        __name.name() : __name,
        __email.name() : __email,
        __phone.name() : __phone
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.cs_contact = cs_contact
Namespace.addCategoryObject('typeBinding', 'cs_contact', cs_contact)


# Complex type {http://www.witsml.org/api/140}cs_function with content type ELEMENT_ONLY
class cs_function (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.witsml.org/api/140}cs_function with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'cs_function')
    _XSDLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/cs_function.xsd', 26, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.witsml.org/api/140}dataObject uses Python identifier dataObject
    __dataObject = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'dataObject'), 'dataObject', '__httpwww_witsml_orgapi140_cs_function_httpwww_witsml_orgapi140dataObject', True, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/cs_function.xsd', 28, 3), )

    
    dataObject = property(__dataObject.value, __dataObject.set, None, 'A WITSML data object (well, wellbore, etc) \n\t\t\t\t\twhich is supported by this Server/Publisher for this function. \n\t\t\t\t\t')

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__httpwww_witsml_orgapi140_cs_function_name', _module_typeBindings.str64, required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/cs_function.xsd', 36, 2)
    __name._UseLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/cs_function.xsd', 36, 2)
    
    name = property(__name.value, __name.set, None, 'Name of function, (WMLS_GetFromStore, etc)\n\t\t\t\t')

    _ElementMap.update({
        __dataObject.name() : __dataObject
    })
    _AttributeMap.update({
        __name.name() : __name
    })
_module_typeBindings.cs_function = cs_function
Namespace.addCategoryObject('typeBinding', 'cs_function', cs_function)


# Complex type {http://www.witsml.org/api/140}obj_capClients with content type ELEMENT_ONLY
class obj_capClients (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.witsml.org/api/140}obj_capClients with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'obj_capClients')
    _XSDLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capClient.xsd', 39, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.witsml.org/api/140}capClient uses Python identifier capClient
    __capClient = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'capClient'), 'capClient', '__httpwww_witsml_orgapi140_obj_capClients_httpwww_witsml_orgapi140capClient', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capClient.xsd', 41, 3), )

    
    capClient = property(__capClient.value, __capClient.set, None, 'Defines the singular Client Capabilities (capClient) element; only one can be specified. \n\t\t\t\t\t')

    
    # Attribute version uses Python identifier version
    __version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'version'), 'version', '__httpwww_witsml_orgapi140_obj_capClients_version', _module_typeBindings.str16, fixed=True, unicode_default='1.4.0')
    __version._DeclarationLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capClient.xsd', 48, 2)
    __version._UseLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capClient.xsd', 48, 2)
    
    version = property(__version.value, __version.set, None, "API schema version.  It is optional.\n\t\t\t\tIf the version is specified, its value must be set equal to the value specified by the \n\t\t\t\tversion's fixed attribute. Note that this is different from the data schema version.\n\t\t\t\t")

    _ElementMap.update({
        __capClient.name() : __capClient
    })
    _AttributeMap.update({
        __version.name() : __version
    })
_module_typeBindings.obj_capClients = obj_capClients
Namespace.addCategoryObject('typeBinding', 'obj_capClients', obj_capClients)


# Complex type {http://www.witsml.org/api/140}obj_capClient with content type ELEMENT_ONLY
class obj_capClient (pyxb.binding.basis.complexTypeDefinition):
    """Defines the singular Client Capabilities data type (obj_capClient).
			"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'obj_capClient')
    _XSDLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capClient.xsd', 58, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.witsml.org/api/140}contact uses Python identifier contact
    __contact = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'contact'), 'contact', '__httpwww_witsml_orgapi140_obj_capClient_httpwww_witsml_orgapi140contact', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capClient.xsd', 64, 3), )

    
    contact = property(__contact.value, __contact.set, None, 'Contact information for Client.\n\t\t\t\t\t')

    
    # Element {http://www.witsml.org/api/140}description uses Python identifier description
    __description = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'description'), 'description', '__httpwww_witsml_orgapi140_obj_capClient_httpwww_witsml_orgapi140description', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capClient.xsd', 70, 3), )

    
    description = property(__description.value, __description.set, None, 'Description of Client.\n\t\t\t\t\t')

    
    # Element {http://www.witsml.org/api/140}name uses Python identifier name
    __name = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'name'), 'name', '__httpwww_witsml_orgapi140_obj_capClient_httpwww_witsml_orgapi140name', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capClient.xsd', 76, 3), )

    
    name = property(__name.value, __name.set, None, 'Name of the Client.\n\t\t\t\t\t')

    
    # Element {http://www.witsml.org/api/140}vendor uses Python identifier vendor
    __vendor = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'vendor'), 'vendor', '__httpwww_witsml_orgapi140_obj_capClient_httpwww_witsml_orgapi140vendor', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capClient.xsd', 82, 3), )

    
    vendor = property(__vendor.value, __vendor.set, None, 'Vendor of the Client software.\n\t\t\t\t\t')

    
    # Element {http://www.witsml.org/api/140}version uses Python identifier version
    __version = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'version'), 'version', '__httpwww_witsml_orgapi140_obj_capClient_httpwww_witsml_orgapi140version', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capClient.xsd', 88, 3), )

    
    version = property(__version.value, __version.set, None, "Client software Executable Program version (identification only; use apiVers to determine Client's API Capability).\n\t\t\t\t\t")

    
    # Element {http://www.witsml.org/api/140}schemaVersion uses Python identifier schemaVersion
    __schemaVersion = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'schemaVersion'), 'schemaVersion', '__httpwww_witsml_orgapi140_obj_capClient_httpwww_witsml_orgapi140schemaVersion', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capClient.xsd', 94, 3), )

    
    schemaVersion = property(__schemaVersion.value, __schemaVersion.set, None, 'A comma separated list of schema versions (without spaces) that are supported \n\t\t\t\t\tby the cllient. The oldest version should be listed first, followed by the next \n\t\t\t\t\toldest, etc. ')

    
    # Attribute apiVers uses Python identifier apiVers
    __apiVers = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'apiVers'), 'apiVers', '__httpwww_witsml_orgapi140_obj_capClient_apiVers', _module_typeBindings.str16, required=True)
    __apiVers._DeclarationLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capClient.xsd', 102, 2)
    __apiVers._UseLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capClient.xsd', 102, 2)
    
    apiVers = property(__apiVers.value, __apiVers.set, None, 'Version of the API specification to which this Publisher conforms. \n\t\t\t\t')

    _ElementMap.update({
        __contact.name() : __contact,
        __description.name() : __description,
        __name.name() : __name,
        __vendor.name() : __vendor,
        __version.name() : __version,
        __schemaVersion.name() : __schemaVersion
    })
    _AttributeMap.update({
        __apiVers.name() : __apiVers
    })
_module_typeBindings.obj_capClient = obj_capClient
Namespace.addCategoryObject('typeBinding', 'obj_capClient', obj_capClient)


# Complex type {http://www.witsml.org/api/140}obj_capPublishers with content type ELEMENT_ONLY
class obj_capPublishers (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.witsml.org/api/140}obj_capPublishers with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'obj_capPublishers')
    _XSDLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capPublisher.xsd', 39, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.witsml.org/api/140}capPublisher uses Python identifier capPublisher
    __capPublisher = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'capPublisher'), 'capPublisher', '__httpwww_witsml_orgapi140_obj_capPublishers_httpwww_witsml_orgapi140capPublisher', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capPublisher.xsd', 41, 3), )

    
    capPublisher = property(__capPublisher.value, __capPublisher.set, None, None)

    
    # Attribute version uses Python identifier version
    __version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'version'), 'version', '__httpwww_witsml_orgapi140_obj_capPublishers_version', _module_typeBindings.str16, fixed=True, unicode_default='1.4.0')
    __version._DeclarationLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capPublisher.xsd', 43, 2)
    __version._UseLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capPublisher.xsd', 43, 2)
    
    version = property(__version.value, __version.set, None, "API schema version.  It is optional.\n\t\t\t\tIf the version is specified, its value must be set equal to the value specified by the \n\t\t\t\tversion's fixed attribute. Note that this is different from the data schema version.\n\t\t\t\t")

    _ElementMap.update({
        __capPublisher.name() : __capPublisher
    })
    _AttributeMap.update({
        __version.name() : __version
    })
_module_typeBindings.obj_capPublishers = obj_capPublishers
Namespace.addCategoryObject('typeBinding', 'obj_capPublishers', obj_capPublishers)


# Complex type {http://www.witsml.org/api/140}obj_capPublisher with content type ELEMENT_ONLY
class obj_capPublisher (pyxb.binding.basis.complexTypeDefinition):
    """Defines the singular Publisher Capabilities data type (obj_capPublisher).
			"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'obj_capPublisher')
    _XSDLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capPublisher.xsd', 53, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.witsml.org/api/140}contact uses Python identifier contact
    __contact = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'contact'), 'contact', '__httpwww_witsml_orgapi140_obj_capPublisher_httpwww_witsml_orgapi140contact', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capPublisher.xsd', 59, 3), )

    
    contact = property(__contact.value, __contact.set, None, 'Contact information for Publisher.\n\t\t\t\t\t')

    
    # Element {http://www.witsml.org/api/140}description uses Python identifier description
    __description = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'description'), 'description', '__httpwww_witsml_orgapi140_obj_capPublisher_httpwww_witsml_orgapi140description', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capPublisher.xsd', 65, 3), )

    
    description = property(__description.value, __description.set, None, 'Description of Publisher.\n\t\t\t\t\t')

    
    # Element {http://www.witsml.org/api/140}name uses Python identifier name
    __name = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'name'), 'name', '__httpwww_witsml_orgapi140_obj_capPublisher_httpwww_witsml_orgapi140name', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capPublisher.xsd', 71, 3), )

    
    name = property(__name.value, __name.set, None, 'Name of the Publisher.\n\t\t\t\t\t')

    
    # Element {http://www.witsml.org/api/140}vendor uses Python identifier vendor
    __vendor = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'vendor'), 'vendor', '__httpwww_witsml_orgapi140_obj_capPublisher_httpwww_witsml_orgapi140vendor', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capPublisher.xsd', 77, 3), )

    
    vendor = property(__vendor.value, __vendor.set, None, 'Vendor of the Publisher software.\n\t\t\t\t\t')

    
    # Element {http://www.witsml.org/api/140}version uses Python identifier version
    __version = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'version'), 'version', '__httpwww_witsml_orgapi140_obj_capPublisher_httpwww_witsml_orgapi140version', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capPublisher.xsd', 83, 3), )

    
    version = property(__version.value, __version.set, None, "Publisher software Executable Program version (identification only; use apiVers to determine Publisher's API Capability).\n\t\t\t\t\t")

    
    # Element {http://www.witsml.org/api/140}schemaVersion uses Python identifier schemaVersion
    __schemaVersion = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'schemaVersion'), 'schemaVersion', '__httpwww_witsml_orgapi140_obj_capPublisher_httpwww_witsml_orgapi140schemaVersion', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capPublisher.xsd', 89, 3), )

    
    schemaVersion = property(__schemaVersion.value, __schemaVersion.set, None, 'The data schema version that is represented by each object in "function".')

    
    # Element {http://www.witsml.org/api/140}function uses Python identifier function
    __function = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'function'), 'function', '__httpwww_witsml_orgapi140_obj_capPublisher_httpwww_witsml_orgapi140function', True, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capPublisher.xsd', 94, 3), )

    
    function = property(__function.value, __function.set, None, 'A WITSML data object (well, wellbore, etc) which this Publisher can publish.\n\t\t\t\t\t')

    
    # Attribute apiVers uses Python identifier apiVers
    __apiVers = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'apiVers'), 'apiVers', '__httpwww_witsml_orgapi140_obj_capPublisher_apiVers', _module_typeBindings.str16, required=True)
    __apiVers._DeclarationLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capPublisher.xsd', 101, 2)
    __apiVers._UseLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capPublisher.xsd', 101, 2)
    
    apiVers = property(__apiVers.value, __apiVers.set, None, 'Version of the API specification to which this Publisher conforms. \n\t\t\t\t')

    _ElementMap.update({
        __contact.name() : __contact,
        __description.name() : __description,
        __name.name() : __name,
        __vendor.name() : __vendor,
        __version.name() : __version,
        __schemaVersion.name() : __schemaVersion,
        __function.name() : __function
    })
    _AttributeMap.update({
        __apiVers.name() : __apiVers
    })
_module_typeBindings.obj_capPublisher = obj_capPublisher
Namespace.addCategoryObject('typeBinding', 'obj_capPublisher', obj_capPublisher)


# Complex type {http://www.witsml.org/api/140}obj_capServers with content type ELEMENT_ONLY
class obj_capServers (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.witsml.org/api/140}obj_capServers with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'obj_capServers')
    _XSDLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 39, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.witsml.org/api/140}capServer uses Python identifier capServer
    __capServer = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'capServer'), 'capServer', '__httpwww_witsml_orgapi140_obj_capServers_httpwww_witsml_orgapi140capServer', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 46, 3), )

    
    capServer = property(__capServer.value, __capServer.set, None, None)

    
    # Attribute version uses Python identifier version
    __version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'version'), 'version', '__httpwww_witsml_orgapi140_obj_capServers_version', _module_typeBindings.str16, fixed=True, unicode_default='1.4.0')
    __version._DeclarationLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 48, 2)
    __version._UseLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 48, 2)
    
    version = property(__version.value, __version.set, None, "API schema version.  It is optional.\n\t\t\t\tIf the version is specified, its value must be set equal to the value specified by the \n\t\t\t\tversion's fixed attribute. Note that this is different from the data schema version.\n\t\t\t\t")

    _ElementMap.update({
        __capServer.name() : __capServer
    })
    _AttributeMap.update({
        __version.name() : __version
    })
_module_typeBindings.obj_capServers = obj_capServers
Namespace.addCategoryObject('typeBinding', 'obj_capServers', obj_capServers)


# Complex type {http://www.witsml.org/api/140}obj_capServer with content type ELEMENT_ONLY
class obj_capServer (pyxb.binding.basis.complexTypeDefinition):
    """Defines the singular Server Capabilities data type (obj_capServer).
			"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'obj_capServer')
    _XSDLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 58, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.witsml.org/api/140}contact uses Python identifier contact
    __contact = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'contact'), 'contact', '__httpwww_witsml_orgapi140_obj_capServer_httpwww_witsml_orgapi140contact', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 64, 3), )

    
    contact = property(__contact.value, __contact.set, None, 'Contact information for Server.\n\t\t\t\t\t')

    
    # Element {http://www.witsml.org/api/140}description uses Python identifier description
    __description = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'description'), 'description', '__httpwww_witsml_orgapi140_obj_capServer_httpwww_witsml_orgapi140description', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 70, 3), )

    
    description = property(__description.value, __description.set, None, 'Description of Server.\n\t\t\t\t\t')

    
    # Element {http://www.witsml.org/api/140}name uses Python identifier name
    __name = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'name'), 'name', '__httpwww_witsml_orgapi140_obj_capServer_httpwww_witsml_orgapi140name', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 76, 3), )

    
    name = property(__name.value, __name.set, None, 'Name of the Server.\n\t\t\t\t\t')

    
    # Element {http://www.witsml.org/api/140}vendor uses Python identifier vendor
    __vendor = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'vendor'), 'vendor', '__httpwww_witsml_orgapi140_obj_capServer_httpwww_witsml_orgapi140vendor', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 82, 3), )

    
    vendor = property(__vendor.value, __vendor.set, None, 'Vendor of the Server software.\n\t\t\t\t\t')

    
    # Element {http://www.witsml.org/api/140}version uses Python identifier version
    __version = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'version'), 'version', '__httpwww_witsml_orgapi140_obj_capServer_httpwww_witsml_orgapi140version', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 88, 3), )

    
    version = property(__version.value, __version.set, None, "Server software Executable Program version (identification only; \n\t\t\t\t\tuse apiVers to determine Server's API Capability).\n\t\t\t\t\t")

    
    # Element {http://www.witsml.org/api/140}schemaVersion uses Python identifier schemaVersion
    __schemaVersion = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'schemaVersion'), 'schemaVersion', '__httpwww_witsml_orgapi140_obj_capServer_httpwww_witsml_orgapi140schemaVersion', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 95, 3), )

    
    schemaVersion = property(__schemaVersion.value, __schemaVersion.set, None, 'The data schema version that is represented by each object in "function".')

    
    # Element {http://www.witsml.org/api/140}compressionMethod uses Python identifier compressionMethod
    __compressionMethod = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'compressionMethod'), 'compressionMethod', '__httpwww_witsml_orgapi140_obj_capServer_httpwww_witsml_orgapi140compressionMethod', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 100, 3), )

    
    compressionMethod = property(__compressionMethod.value, __compressionMethod.set, None, 'The comma delimited list of compression methods supported by the server.')

    
    # Element {http://www.witsml.org/api/140}profileName uses Python identifier profileName
    __profileName = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'profileName'), 'profileName', '__httpwww_witsml_orgapi140_obj_capServer_httpwww_witsml_orgapi140profileName', True, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 105, 3), )

    
    profileName = property(__profileName.value, __profileName.set, None, 'The name of a profile supported by the server.')

    
    # Element {http://www.witsml.org/api/140}function uses Python identifier function
    __function = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'function'), 'function', '__httpwww_witsml_orgapi140_obj_capServer_httpwww_witsml_orgapi140function', True, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 110, 3), )

    
    function = property(__function.value, __function.set, None, 'Specifies server function capabilities.  ')

    
    # Attribute apiVers uses Python identifier apiVers
    __apiVers = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'apiVers'), 'apiVers', '__httpwww_witsml_orgapi140_obj_capServer_apiVers', _module_typeBindings.str16, required=True)
    __apiVers._DeclarationLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 116, 2)
    __apiVers._UseLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 116, 2)
    
    apiVers = property(__apiVers.value, __apiVers.set, None, 'Version of the API specification to which this Publisher conforms. \n\t\t\t\t')

    _ElementMap.update({
        __contact.name() : __contact,
        __description.name() : __description,
        __name.name() : __name,
        __vendor.name() : __vendor,
        __version.name() : __version,
        __schemaVersion.name() : __schemaVersion,
        __compressionMethod.name() : __compressionMethod,
        __profileName.name() : __profileName,
        __function.name() : __function
    })
    _AttributeMap.update({
        __apiVers.name() : __apiVers
    })
_module_typeBindings.obj_capServer = obj_capServer
Namespace.addCategoryObject('typeBinding', 'obj_capServer', obj_capServer)


# Complex type {http://www.witsml.org/api/140}obj_capSubscribers with content type ELEMENT_ONLY
class obj_capSubscribers (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.witsml.org/api/140}obj_capSubscribers with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'obj_capSubscribers')
    _XSDLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capSubscriber.xsd', 39, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.witsml.org/api/140}capSubscriber uses Python identifier capSubscriber
    __capSubscriber = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'capSubscriber'), 'capSubscriber', '__httpwww_witsml_orgapi140_obj_capSubscribers_httpwww_witsml_orgapi140capSubscriber', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capSubscriber.xsd', 41, 3), )

    
    capSubscriber = property(__capSubscriber.value, __capSubscriber.set, None, 'Defines the singular Subscriber Capabilities \n\t\t\t\t\t(capSubscriber) element; only one can be specified. \n\t\t\t\t\t')

    
    # Attribute version uses Python identifier version
    __version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'version'), 'version', '__httpwww_witsml_orgapi140_obj_capSubscribers_version', _module_typeBindings.str16, fixed=True, unicode_default='1.4.0')
    __version._DeclarationLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capSubscriber.xsd', 49, 2)
    __version._UseLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capSubscriber.xsd', 49, 2)
    
    version = property(__version.value, __version.set, None, "API schema version.  It is optional.\n\t\t\t\tIf the version is specified, its value must be set equal to the value specified by the \n\t\t\t\tversion's fixed attribute. Note that this is different from the data schema version.\n\t\t\t\t")

    _ElementMap.update({
        __capSubscriber.name() : __capSubscriber
    })
    _AttributeMap.update({
        __version.name() : __version
    })
_module_typeBindings.obj_capSubscribers = obj_capSubscribers
Namespace.addCategoryObject('typeBinding', 'obj_capSubscribers', obj_capSubscribers)


# Complex type {http://www.witsml.org/api/140}obj_capSubscriber with content type ELEMENT_ONLY
class obj_capSubscriber (pyxb.binding.basis.complexTypeDefinition):
    """Defines the singular Subscriber Capabilities data 
			type (obj_capSubscriber).
			"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'obj_capSubscriber')
    _XSDLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capSubscriber.xsd', 59, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.witsml.org/api/140}contact uses Python identifier contact
    __contact = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'contact'), 'contact', '__httpwww_witsml_orgapi140_obj_capSubscriber_httpwww_witsml_orgapi140contact', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capSubscriber.xsd', 66, 3), )

    
    contact = property(__contact.value, __contact.set, None, 'Contact information for Subscriber.\n\t\t\t\t\t')

    
    # Element {http://www.witsml.org/api/140}description uses Python identifier description
    __description = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'description'), 'description', '__httpwww_witsml_orgapi140_obj_capSubscriber_httpwww_witsml_orgapi140description', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capSubscriber.xsd', 72, 3), )

    
    description = property(__description.value, __description.set, None, 'Description of Subscriber.\n\t\t\t\t\t')

    
    # Element {http://www.witsml.org/api/140}name uses Python identifier name
    __name = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'name'), 'name', '__httpwww_witsml_orgapi140_obj_capSubscriber_httpwww_witsml_orgapi140name', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capSubscriber.xsd', 78, 3), )

    
    name = property(__name.value, __name.set, None, 'Name of the Subscriber.\n\t\t\t\t\t')

    
    # Element {http://www.witsml.org/api/140}vendor uses Python identifier vendor
    __vendor = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'vendor'), 'vendor', '__httpwww_witsml_orgapi140_obj_capSubscriber_httpwww_witsml_orgapi140vendor', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capSubscriber.xsd', 84, 3), )

    
    vendor = property(__vendor.value, __vendor.set, None, 'Vendor of the Subscriber software.\n\t\t\t\t\t')

    
    # Element {http://www.witsml.org/api/140}version uses Python identifier version
    __version = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'version'), 'version', '__httpwww_witsml_orgapi140_obj_capSubscriber_httpwww_witsml_orgapi140version', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capSubscriber.xsd', 90, 3), )

    
    version = property(__version.value, __version.set, None, "Subscriber software Executable Program version (identification only; use apiVers to determine Subscriber's API Capability).\n\t\t\t\t\t")

    
    # Element {http://www.witsml.org/api/140}schemaVersion uses Python identifier schemaVersion
    __schemaVersion = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'schemaVersion'), 'schemaVersion', '__httpwww_witsml_orgapi140_obj_capSubscriber_httpwww_witsml_orgapi140schemaVersion', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capSubscriber.xsd', 96, 3), )

    
    schemaVersion = property(__schemaVersion.value, __schemaVersion.set, None, 'A comma separated list of schema versions (without spaces) that are supported \n\t\t\t\t\tby the subscriber. The oldest version should be listed first, followed by the next \n\t\t\t\t\toldest, etc. ')

    
    # Attribute apiVers uses Python identifier apiVers
    __apiVers = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'apiVers'), 'apiVers', '__httpwww_witsml_orgapi140_obj_capSubscriber_apiVers', _module_typeBindings.str16, required=True)
    __apiVers._DeclarationLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capSubscriber.xsd', 104, 2)
    __apiVers._UseLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capSubscriber.xsd', 104, 2)
    
    apiVers = property(__apiVers.value, __apiVers.set, None, 'Version of the API specification to which this Publisher conforms. \n\t\t\t\t')

    _ElementMap.update({
        __contact.name() : __contact,
        __description.name() : __description,
        __name.name() : __name,
        __vendor.name() : __vendor,
        __version.name() : __version,
        __schemaVersion.name() : __schemaVersion
    })
    _AttributeMap.update({
        __apiVers.name() : __apiVers
    })
_module_typeBindings.obj_capSubscriber = obj_capSubscriber
Namespace.addCategoryObject('typeBinding', 'obj_capSubscriber', obj_capSubscriber)


# Complex type {http://www.witsml.org/api/140}obj_subscriptions with content type ELEMENT_ONLY
class obj_subscriptions (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.witsml.org/api/140}obj_subscriptions with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'obj_subscriptions')
    _XSDLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_subscription.xsd', 34, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.witsml.org/api/140}subscription uses Python identifier subscription
    __subscription = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'subscription'), 'subscription', '__httpwww_witsml_orgapi140_obj_subscriptions_httpwww_witsml_orgapi140subscription', True, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_subscription.xsd', 36, 3), )

    
    subscription = property(__subscription.value, __subscription.set, None, 'Defines the singular subscription object.  \n\t\t\t\t\t')

    
    # Attribute version uses Python identifier version
    __version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'version'), 'version', '__httpwww_witsml_orgapi140_obj_subscriptions_version', _module_typeBindings.str16, fixed=True, unicode_default='1.4.0')
    __version._DeclarationLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_subscription.xsd', 43, 2)
    __version._UseLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_subscription.xsd', 43, 2)
    
    version = property(__version.value, __version.set, None, "Data object schema version.  It is optional.\n\t\t\t\tIf the version is specified, its value must be set equal to the value specified by the \n\t\t\t\tversion's fixed attribute.\n\t\t\t\t")

    _ElementMap.update({
        __subscription.name() : __subscription
    })
    _AttributeMap.update({
        __version.name() : __version
    })
_module_typeBindings.obj_subscriptions = obj_subscriptions
Namespace.addCategoryObject('typeBinding', 'obj_subscriptions', obj_subscriptions)


# Complex type {http://www.witsml.org/api/140}obj_subscription with content type ELEMENT_ONLY
class obj_subscription (pyxb.binding.basis.complexTypeDefinition):
    """Defines the singular subscription data type (obj_subscription).
			"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'obj_subscription')
    _XSDLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_subscription.xsd', 53, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute host uses Python identifier host
    __host = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'host'), 'host', '__httpwww_witsml_orgapi140_obj_subscription_host', _module_typeBindings.str256, required=True)
    __host._DeclarationLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_subscription.xsd', 67, 2)
    __host._UseLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_subscription.xsd', 67, 2)
    
    host = property(__host.value, __host.set, None, 'Host name of Subscriber to receive published data over HTTP/S POST. ')

    
    # Attribute process uses Python identifier process
    __process = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'process'), 'process', '__httpwww_witsml_orgapi140_obj_subscription_process', _module_typeBindings.str256, required=True)
    __process._DeclarationLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_subscription.xsd', 72, 2)
    __process._UseLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_subscription.xsd', 72, 2)
    
    process = property(__process.value, __process.set, None, 'Process name on Subscriber that will process published data received over HTTP/S POST. ')

    
    # Attribute encrypt uses Python identifier encrypt
    __encrypt = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'encrypt'), 'encrypt', '__httpwww_witsml_orgapi140_obj_subscription_encrypt', _module_typeBindings.logicalBoolean)
    __encrypt._DeclarationLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_subscription.xsd', 77, 2)
    __encrypt._UseLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_subscription.xsd', 77, 2)
    
    encrypt = property(__encrypt.value, __encrypt.set, None, 'Specifies whether encryption (HTTPS) is to be used when publishing (POSTing) the data.  \n\t\t\t\tValues are "true" (or "1") and "false" ( or "0").')

    
    # Attribute port uses Python identifier port
    __port = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'port'), 'port', '__httpwww_witsml_orgapi140_obj_subscription_port', _module_typeBindings.str16)
    __port._DeclarationLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_subscription.xsd', 83, 2)
    __port._UseLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_subscription.xsd', 83, 2)
    
    port = property(__port.value, __port.set, None, 'The TCP port on which the Subscriber wishes to receive the data over HTTP/S POST. ')

    
    # Attribute retry uses Python identifier retry
    __retry = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'retry'), 'retry', '__httpwww_witsml_orgapi140_obj_subscription_retry', _module_typeBindings.integerCount)
    __retry._DeclarationLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_subscription.xsd', 88, 2)
    __retry._UseLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_subscription.xsd', 88, 2)
    
    retry = property(__retry.value, __retry.set, None, 'Number of times the Publisher will retry a failed POST to the Subscriber before discarding the data as undeliverable.\n\t\t\t\t')

    
    # Attribute idPub uses Python identifier idPub
    __idPub = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'idPub'), 'idPub', '__httpwww_witsml_orgapi140_obj_subscription_idPub', _module_typeBindings.str256)
    __idPub._DeclarationLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_subscription.xsd', 94, 2)
    __idPub._UseLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_subscription.xsd', 94, 2)
    
    idPub = property(__idPub.value, __idPub.set, None, 'The identifier of the Publisher, as clear, un-encoded text in the format: userid:password Assigned by the Subscriber and sent by the Publisher as BASIC authentication when POSTing data to the Subscriber.\n\t\t\t\t')

    
    # Attribute idSub uses Python identifier idSub
    __idSub = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'idSub'), 'idSub', '__httpwww_witsml_orgapi140_obj_subscription_idSub', _module_typeBindings.str256)
    __idSub._DeclarationLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_subscription.xsd', 100, 2)
    __idSub._UseLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_subscription.xsd', 100, 2)
    
    idSub = property(__idSub.value, __idSub.set, None, 'The unique identifier of the accepted subscription within the context of this Publisher. This identifier is used by the Subscriber when subsequently modifies or cancels the subscription.')

    
    # Attribute retCode uses Python identifier retCode
    __retCode = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'retCode'), 'retCode', '__httpwww_witsml_orgapi140_obj_subscription_retCode', _module_typeBindings.integerCount)
    __retCode._DeclarationLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_subscription.xsd', 105, 2)
    __retCode._UseLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_subscription.xsd', 105, 2)
    
    retCode = property(__retCode.value, __retCode.set, None, 'A return code returned by the Publisher indicating the disposition of the subscription request. A value of 1 indicates the request was accepted. ')

    
    # Attribute action uses Python identifier action
    __action = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'action'), 'action', '__httpwww_witsml_orgapi140_obj_subscription_action', _module_typeBindings.SubscriptionAction, required=True)
    __action._DeclarationLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_subscription.xsd', 110, 2)
    __action._UseLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_subscription.xsd', 110, 2)
    
    action = property(__action.value, __action.set, None, 'Specifies the action to be performed on the subscription request: add, modify, cancel or verify. ')

    
    # Attribute test uses Python identifier test
    __test = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'test'), 'test', '__httpwww_witsml_orgapi140_obj_subscription_test', _module_typeBindings.logicalBoolean)
    __test._DeclarationLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_subscription.xsd', 115, 2)
    __test._UseLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_subscription.xsd', 115, 2)
    
    test = property(__test.value, __test.set, None, 'Specifies that a network test will first be performed by the Publisher to make sure the Subscriber system can be contacted. Default is "true"; specify test="false" to bypass the test. \n\t\t\t\tValues are "true" (or "1") and "false" ( or "0").')

    
    # Attribute updateInterval uses Python identifier updateInterval
    __updateInterval = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'updateInterval'), 'updateInterval', '__httpwww_witsml_orgapi140_obj_subscription_updateInterval', _module_typeBindings.integerCount)
    __updateInterval._DeclarationLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_subscription.xsd', 121, 2)
    __updateInterval._UseLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_subscription.xsd', 121, 2)
    
    updateInterval = property(__updateInterval.value, __updateInterval.set, None, 'The minimum interval between publication of changed data objects matching this subscription request. Changes occurring more frequently than the specified value will not be published. If not specified, the Publisher will publish data objects as frequently as they become available')

    _HasWildcardElement = True
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __host.name() : __host,
        __process.name() : __process,
        __encrypt.name() : __encrypt,
        __port.name() : __port,
        __retry.name() : __retry,
        __idPub.name() : __idPub,
        __idSub.name() : __idSub,
        __retCode.name() : __retCode,
        __action.name() : __action,
        __test.name() : __test,
        __updateInterval.name() : __updateInterval
    })
_module_typeBindings.obj_subscription = obj_subscription
Namespace.addCategoryObject('typeBinding', 'obj_subscription', obj_subscription)


capClients = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'capClients'), obj_capClients, documentation='The WITSML API mandated plural root element which allows \n\t\t\tmultiple singular objects to be sent. The plural name is formed by adding\n\t\t\tan "s" to the singular name.\n\t\t\tPresent only for consistency with other WITSML data objects (multiple \n\t\t\tcapClient elements are not allowed). \n\t\t\t', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capClient.xsd', 28, 1))
Namespace.addCategoryObject('elementBinding', capClients.name().localName(), capClients)

capPublishers = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'capPublishers'), obj_capPublishers, location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capPublisher.xsd', 29, 1))
Namespace.addCategoryObject('elementBinding', capPublishers.name().localName(), capPublishers)

capServers = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'capServers'), obj_capServers, location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 29, 1))
Namespace.addCategoryObject('elementBinding', capServers.name().localName(), capServers)

capSubscribers = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'capSubscribers'), obj_capSubscribers, documentation='The WITSML API mandated plural root element which allows \n\t\t\tmultiple singular objects to be sent. The plural name is formed by adding\n\t\t\tan "s" to the singular name.\n\t\t\tPresent only for consistency with other WITSML data objects (multiple \n\t\t\tcapSubscriber elements are not allowed). \n\t\t\t', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capSubscriber.xsd', 28, 1))
Namespace.addCategoryObject('elementBinding', capSubscribers.name().localName(), capSubscribers)

subscriptions = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'subscriptions'), obj_subscriptions, location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_subscription.xsd', 27, 1))
Namespace.addCategoryObject('elementBinding', subscriptions.name().localName(), subscriptions)



cs_contact._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'name'), str64, scope=cs_contact, documentation='Name of contact. ', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/cs_contact.xsd', 28, 3)))

cs_contact._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'email'), str256, scope=cs_contact, documentation='Email address of contact. ', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/cs_contact.xsd', 33, 3)))

cs_contact._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'phone'), str64, scope=cs_contact, documentation='Phone number of contact. ', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/cs_contact.xsd', 38, 3)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/cs_contact.xsd', 28, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/cs_contact.xsd', 33, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/cs_contact.xsd', 38, 3))
    counters.add(cc_2)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(cs_contact._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'name')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/cs_contact.xsd', 28, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(cs_contact._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'email')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/cs_contact.xsd', 33, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(cs_contact._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'phone')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/cs_contact.xsd', 38, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
cs_contact._Automaton = _BuildAutomaton()




cs_function._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'dataObject'), str64, scope=cs_function, documentation='A WITSML data object (well, wellbore, etc) \n\t\t\t\t\twhich is supported by this Server/Publisher for this function. \n\t\t\t\t\t', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/cs_function.xsd', 28, 3)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/cs_function.xsd', 28, 3))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(cs_function._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'dataObject')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/cs_function.xsd', 28, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
cs_function._Automaton = _BuildAutomaton_()




obj_capClients._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'capClient'), obj_capClient, scope=obj_capClients, documentation='Defines the singular Client Capabilities (capClient) element; only one can be specified. \n\t\t\t\t\t', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capClient.xsd', 41, 3)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capClient.xsd', 41, 3))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(obj_capClients._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'capClient')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capClient.xsd', 41, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
obj_capClients._Automaton = _BuildAutomaton_2()




obj_capClient._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'contact'), cs_contact, scope=obj_capClient, documentation='Contact information for Client.\n\t\t\t\t\t', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capClient.xsd', 64, 3)))

obj_capClient._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'description'), str4096, scope=obj_capClient, documentation='Description of Client.\n\t\t\t\t\t', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capClient.xsd', 70, 3)))

obj_capClient._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'name'), str64, scope=obj_capClient, documentation='Name of the Client.\n\t\t\t\t\t', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capClient.xsd', 76, 3)))

obj_capClient._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'vendor'), str64, scope=obj_capClient, documentation='Vendor of the Client software.\n\t\t\t\t\t', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capClient.xsd', 82, 3)))

obj_capClient._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'version'), str64, scope=obj_capClient, documentation="Client software Executable Program version (identification only; use apiVers to determine Client's API Capability).\n\t\t\t\t\t", location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capClient.xsd', 88, 3)))

obj_capClient._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'schemaVersion'), str64, scope=obj_capClient, documentation='A comma separated list of schema versions (without spaces) that are supported \n\t\t\t\t\tby the cllient. The oldest version should be listed first, followed by the next \n\t\t\t\t\toldest, etc. ', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capClient.xsd', 94, 3)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capClient.xsd', 64, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capClient.xsd', 70, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capClient.xsd', 76, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capClient.xsd', 82, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capClient.xsd', 88, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capClient.xsd', 94, 3))
    counters.add(cc_5)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(obj_capClient._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'contact')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capClient.xsd', 64, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(obj_capClient._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'description')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capClient.xsd', 70, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(obj_capClient._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'name')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capClient.xsd', 76, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(obj_capClient._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'vendor')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capClient.xsd', 82, 3))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(obj_capClient._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'version')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capClient.xsd', 88, 3))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(obj_capClient._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'schemaVersion')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capClient.xsd', 94, 3))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_5, True) ]))
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
obj_capClient._Automaton = _BuildAutomaton_3()




obj_capPublishers._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'capPublisher'), obj_capPublisher, scope=obj_capPublishers, location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capPublisher.xsd', 41, 3)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capPublisher.xsd', 41, 3))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(obj_capPublishers._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'capPublisher')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capPublisher.xsd', 41, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
obj_capPublishers._Automaton = _BuildAutomaton_4()




obj_capPublisher._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'contact'), cs_contact, scope=obj_capPublisher, documentation='Contact information for Publisher.\n\t\t\t\t\t', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capPublisher.xsd', 59, 3)))

obj_capPublisher._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'description'), str4096, scope=obj_capPublisher, documentation='Description of Publisher.\n\t\t\t\t\t', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capPublisher.xsd', 65, 3)))

obj_capPublisher._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'name'), str64, scope=obj_capPublisher, documentation='Name of the Publisher.\n\t\t\t\t\t', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capPublisher.xsd', 71, 3)))

obj_capPublisher._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'vendor'), str64, scope=obj_capPublisher, documentation='Vendor of the Publisher software.\n\t\t\t\t\t', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capPublisher.xsd', 77, 3)))

obj_capPublisher._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'version'), str64, scope=obj_capPublisher, documentation="Publisher software Executable Program version (identification only; use apiVers to determine Publisher's API Capability).\n\t\t\t\t\t", location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capPublisher.xsd', 83, 3)))

obj_capPublisher._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'schemaVersion'), str64, scope=obj_capPublisher, documentation='The data schema version that is represented by each object in "function".', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capPublisher.xsd', 89, 3)))

obj_capPublisher._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'function'), cs_function, scope=obj_capPublisher, documentation='A WITSML data object (well, wellbore, etc) which this Publisher can publish.\n\t\t\t\t\t', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capPublisher.xsd', 94, 3)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capPublisher.xsd', 59, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capPublisher.xsd', 65, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capPublisher.xsd', 71, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capPublisher.xsd', 77, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capPublisher.xsd', 83, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capPublisher.xsd', 89, 3))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capPublisher.xsd', 94, 3))
    counters.add(cc_6)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(obj_capPublisher._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'contact')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capPublisher.xsd', 59, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(obj_capPublisher._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'description')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capPublisher.xsd', 65, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(obj_capPublisher._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'name')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capPublisher.xsd', 71, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(obj_capPublisher._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'vendor')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capPublisher.xsd', 77, 3))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(obj_capPublisher._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'version')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capPublisher.xsd', 83, 3))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(obj_capPublisher._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'schemaVersion')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capPublisher.xsd', 89, 3))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(obj_capPublisher._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'function')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capPublisher.xsd', 94, 3))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_6, True) ]))
    st_6._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
obj_capPublisher._Automaton = _BuildAutomaton_5()




obj_capServers._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'capServer'), obj_capServer, scope=obj_capServers, location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 46, 3)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 46, 3))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(obj_capServers._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'capServer')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 46, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
obj_capServers._Automaton = _BuildAutomaton_6()




obj_capServer._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'contact'), cs_contact, scope=obj_capServer, documentation='Contact information for Server.\n\t\t\t\t\t', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 64, 3)))

obj_capServer._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'description'), str4096, scope=obj_capServer, documentation='Description of Server.\n\t\t\t\t\t', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 70, 3)))

obj_capServer._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'name'), str64, scope=obj_capServer, documentation='Name of the Server.\n\t\t\t\t\t', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 76, 3)))

obj_capServer._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'vendor'), str64, scope=obj_capServer, documentation='Vendor of the Server software.\n\t\t\t\t\t', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 82, 3)))

obj_capServer._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'version'), str64, scope=obj_capServer, documentation="Server software Executable Program version (identification only; \n\t\t\t\t\tuse apiVers to determine Server's API Capability).\n\t\t\t\t\t", location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 88, 3)))

obj_capServer._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'schemaVersion'), str64, scope=obj_capServer, documentation='The data schema version that is represented by each object in "function".', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 95, 3)))

obj_capServer._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'compressionMethod'), str64, scope=obj_capServer, documentation='The comma delimited list of compression methods supported by the server.', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 100, 3)))

obj_capServer._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'profileName'), str64, scope=obj_capServer, documentation='The name of a profile supported by the server.', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 105, 3)))

obj_capServer._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'function'), cs_function, scope=obj_capServer, documentation='Specifies server function capabilities.  ', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 110, 3)))

def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 64, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 70, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 76, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 82, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 88, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 95, 3))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 100, 3))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 105, 3))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 110, 3))
    counters.add(cc_8)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(obj_capServer._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'contact')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 64, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(obj_capServer._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'description')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 70, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(obj_capServer._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'name')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 76, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(obj_capServer._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'vendor')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 82, 3))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(obj_capServer._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'version')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 88, 3))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(obj_capServer._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'schemaVersion')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 95, 3))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(obj_capServer._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'compressionMethod')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 100, 3))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(obj_capServer._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'profileName')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 105, 3))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(obj_capServer._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'function')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capServer.xsd', 110, 3))
    st_8 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_7, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_8, True) ]))
    st_8._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
obj_capServer._Automaton = _BuildAutomaton_7()




obj_capSubscribers._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'capSubscriber'), obj_capSubscriber, scope=obj_capSubscribers, documentation='Defines the singular Subscriber Capabilities \n\t\t\t\t\t(capSubscriber) element; only one can be specified. \n\t\t\t\t\t', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capSubscriber.xsd', 41, 3)))

def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capSubscriber.xsd', 41, 3))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(obj_capSubscribers._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'capSubscriber')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capSubscriber.xsd', 41, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
obj_capSubscribers._Automaton = _BuildAutomaton_8()




obj_capSubscriber._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'contact'), cs_contact, scope=obj_capSubscriber, documentation='Contact information for Subscriber.\n\t\t\t\t\t', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capSubscriber.xsd', 66, 3)))

obj_capSubscriber._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'description'), str4096, scope=obj_capSubscriber, documentation='Description of Subscriber.\n\t\t\t\t\t', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capSubscriber.xsd', 72, 3)))

obj_capSubscriber._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'name'), str64, scope=obj_capSubscriber, documentation='Name of the Subscriber.\n\t\t\t\t\t', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capSubscriber.xsd', 78, 3)))

obj_capSubscriber._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'vendor'), str64, scope=obj_capSubscriber, documentation='Vendor of the Subscriber software.\n\t\t\t\t\t', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capSubscriber.xsd', 84, 3)))

obj_capSubscriber._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'version'), str64, scope=obj_capSubscriber, documentation="Subscriber software Executable Program version (identification only; use apiVers to determine Subscriber's API Capability).\n\t\t\t\t\t", location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capSubscriber.xsd', 90, 3)))

obj_capSubscriber._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'schemaVersion'), str64, scope=obj_capSubscriber, documentation='A comma separated list of schema versions (without spaces) that are supported \n\t\t\t\t\tby the subscriber. The oldest version should be listed first, followed by the next \n\t\t\t\t\toldest, etc. ', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capSubscriber.xsd', 96, 3)))

def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capSubscriber.xsd', 66, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capSubscriber.xsd', 72, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capSubscriber.xsd', 78, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capSubscriber.xsd', 84, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capSubscriber.xsd', 90, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capSubscriber.xsd', 96, 3))
    counters.add(cc_5)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(obj_capSubscriber._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'contact')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capSubscriber.xsd', 66, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(obj_capSubscriber._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'description')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capSubscriber.xsd', 72, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(obj_capSubscriber._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'name')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capSubscriber.xsd', 78, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(obj_capSubscriber._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'vendor')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capSubscriber.xsd', 84, 3))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(obj_capSubscriber._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'version')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capSubscriber.xsd', 90, 3))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(obj_capSubscriber._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'schemaVersion')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_capSubscriber.xsd', 96, 3))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_5, True) ]))
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
obj_capSubscriber._Automaton = _BuildAutomaton_9()




obj_subscriptions._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'subscription'), obj_subscription, scope=obj_subscriptions, documentation='Defines the singular subscription object.  \n\t\t\t\t\t', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_subscription.xsd', 36, 3)))

def _BuildAutomaton_10 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_10
    del _BuildAutomaton_10
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_subscription.xsd', 36, 3))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(obj_subscriptions._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'subscription')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_subscription.xsd', 36, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
obj_subscriptions._Automaton = _BuildAutomaton_10()




def _BuildAutomaton_11 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_11
    del _BuildAutomaton_11
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_subscription.xsd', 59, 3))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.WildcardUse(pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_skip, namespace_constraint=pyxb.binding.content.Wildcard.NC_any), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/WITSML_v1.4.0_API_schema/obj_subscription.xsd', 59, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
obj_subscription._Automaton = _BuildAutomaton_11()

__version__ = "1.4.0"
