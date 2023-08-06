# komle_plus/bindings/uom.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:de5669d245f178776916647737ebc73cda75213c
# Generated 2022-10-17 08:47:44.064764 by PyXB version 1.2.6 using Python 3.10.4.final.0
# Namespace http://www.posc.org/schemas

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
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:4a9a6097-219a-41bd-baf9-cfe1b80f1840')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.6'

# A holder for module-level binding classes so we can access them from
# inside class definitions where property names may conflict.
_module_typeBindings = pyxb.utils.utility.Object()

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://www.posc.org/schemas', create_if_missing=True)
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


# Union simple type: {http://www.posc.org/schemas}expandedDateTime
# superclasses pyxb.binding.datatypes.anySimpleType
class expandedDateTime (pyxb.binding.basis.STD_union):

    """Expand possibilities of dateTime format to include date, dateTime, gYearMonth, and gYear"""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'expandedDateTime')
    _XSDLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 337, 0)
    _Documentation = 'Expand possibilities of dateTime format to include date, dateTime, gYearMonth, and gYear'

    _MemberTypes = ( pyxb.binding.datatypes.dateTime, pyxb.binding.datatypes.date, pyxb.binding.datatypes.gYearMonth, pyxb.binding.datatypes.gYear, )
expandedDateTime._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=expandedDateTime)
expandedDateTime._CF_pattern = pyxb.binding.facets.CF_pattern()
expandedDateTime._InitializeFacetMap(expandedDateTime._CF_enumeration,
   expandedDateTime._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'expandedDateTime', expandedDateTime)
_module_typeBindings.expandedDateTime = expandedDateTime

# Complex type {http://www.posc.org/schemas}documentInfoType with content type ELEMENT_ONLY
class documentInfoType (pyxb.binding.basis.complexTypeDefinition):
    """
A convenience schema to capture a set of data that is relevant for many 
exchange documents. It includes information about the file that was created, 
and high-level information about the data that is being exchanged within the
file.
                  """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'documentInfoType')
    _XSDLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 46, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.posc.org/schemas}_DocClasses uses Python identifier DocClasses
    __DocClasses = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, '_DocClasses'), 'DocClasses', '__httpwww_posc_orgschemas_documentInfoType_httpwww_posc_orgschemas_DocClasses', True, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 35, 0), )

    
    DocClasses = property(__DocClasses.value, __DocClasses.set, None, '\nAn abstract element, to serve as a head for a substitution group. The \n_DocClasses is intended to handle any classification systems that a group\nwould model. It may be a simple substitution, or a container with many\nclasses contained in it.\n                ')

    
    # Element {http://www.posc.org/schemas}DocumentName uses Python identifier DocumentName
    __DocumentName = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DocumentName'), 'DocumentName', '__httpwww_posc_orgschemas_documentInfoType_httpwww_posc_orgschemasDocumentName', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 56, 2), )

    
    DocumentName = property(__DocumentName.value, __DocumentName.set, None, '\nAn identifier for the document. This is intended to be unique within the \ncontext of the NamingSystem.\n                ')

    
    # Element {http://www.posc.org/schemas}DocumentAlias uses Python identifier DocumentAlias
    __DocumentAlias = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DocumentAlias'), 'DocumentAlias', '__httpwww_posc_orgschemas_documentInfoType_httpwww_posc_orgschemasDocumentAlias', True, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 64, 2), )

    
    DocumentAlias = property(__DocumentAlias.value, __DocumentAlias.set, None, '\nZero or more alternate names for the document. These names do not need to be\nunique within the naming system.\n                ')

    
    # Element {http://www.posc.org/schemas}DocumentDate uses Python identifier DocumentDate
    __DocumentDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DocumentDate'), 'DocumentDate', '__httpwww_posc_orgschemas_documentInfoType_httpwww_posc_orgschemasDocumentDate', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 72, 2), )

    
    DocumentDate = property(__DocumentDate.value, __DocumentDate.set, None, '\nThe date of the creation of the document. This is not the same as the date\nthat the file was created. For this date, the document is considered to be\nthe set of information associated with this document information.\nFor example, the document may be a seismic binset. This represents the date\nthat the binset was created. The FileCreation information would capture the\ndate that the XML file was created to send or exchange the binset.\n                ')

    
    # Element {http://www.posc.org/schemas}FileCreationInformation uses Python identifier FileCreationInformation
    __FileCreationInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FileCreationInformation'), 'FileCreationInformation', '__httpwww_posc_orgschemas_documentInfoType_httpwww_posc_orgschemasFileCreationInformation', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 93, 2), )

    
    FileCreationInformation = property(__FileCreationInformation.value, __FileCreationInformation.set, None, '\nThe information about the creation of the exchange file. This is not about\nthe creation of the data within the file, but the creation of the file itself.\n                ')

    
    # Element {http://www.posc.org/schemas}SecurityInformation uses Python identifier SecurityInformation
    __SecurityInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SecurityInformation'), 'SecurityInformation', '__httpwww_posc_orgschemas_documentInfoType_httpwww_posc_orgschemasSecurityInformation', True, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 101, 2), )

    
    SecurityInformation = property(__SecurityInformation.value, __SecurityInformation.set, None, '\nInformation about the security to be applied to this file. More than one\nclassification can be given.\n                ')

    
    # Element {http://www.posc.org/schemas}Disclaimer uses Python identifier Disclaimer
    __Disclaimer = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Disclaimer'), 'Disclaimer', '__httpwww_posc_orgschemas_documentInfoType_httpwww_posc_orgschemasDisclaimer', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 109, 2), )

    
    Disclaimer = property(__Disclaimer.value, __Disclaimer.set, None, '\nA free-form string that allows a disclaimer to accompany the information.\n                ')

    
    # Element {http://www.posc.org/schemas}AuditTrail uses Python identifier AuditTrail
    __AuditTrail = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'AuditTrail'), 'AuditTrail', '__httpwww_posc_orgschemas_documentInfoType_httpwww_posc_orgschemasAuditTrail', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 116, 2), )

    
    AuditTrail = property(__AuditTrail.value, __AuditTrail.set, None, '\nA collection of events that can document the history of the data.\n                ')

    
    # Element {http://www.posc.org/schemas}DataOwnerRef uses Python identifier DataOwnerRef
    __DataOwnerRef = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DataOwnerRef'), 'DataOwnerRef', '__httpwww_posc_orgschemas_documentInfoType_httpwww_posc_orgschemasDataOwnerRef', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 131, 4), )

    
    DataOwnerRef = property(__DataOwnerRef.value, __DataOwnerRef.set, None, None)

    
    # Element {http://www.posc.org/schemas}DataOwnerID uses Python identifier DataOwnerID
    __DataOwnerID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DataOwnerID'), 'DataOwnerID', '__httpwww_posc_orgschemas_documentInfoType_httpwww_posc_orgschemasDataOwnerID', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 132, 4), )

    
    DataOwnerID = property(__DataOwnerID.value, __DataOwnerID.set, None, None)

    
    # Element {http://www.posc.org/schemas}Comment uses Python identifier Comment
    __Comment = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Comment'), 'Comment', '__httpwww_posc_orgschemas_documentInfoType_httpwww_posc_orgschemasComment', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 134, 2), )

    
    Comment = property(__Comment.value, __Comment.set, None, '\nAn optional comment about the document.\n                ')

    
    # Attribute modver uses Python identifier modver
    __modver = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'modver'), 'modver', '__httpwww_posc_orgschemas_documentInfoType_modver', pyxb.binding.datatypes.string, fixed=True, unicode_default='1.1')
    __modver._DeclarationLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 142, 1)
    __modver._UseLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 142, 1)
    
    modver = property(__modver.value, __modver.set, None, None)

    _ElementMap.update({
        __DocClasses.name() : __DocClasses,
        __DocumentName.name() : __DocumentName,
        __DocumentAlias.name() : __DocumentAlias,
        __DocumentDate.name() : __DocumentDate,
        __FileCreationInformation.name() : __FileCreationInformation,
        __SecurityInformation.name() : __SecurityInformation,
        __Disclaimer.name() : __Disclaimer,
        __AuditTrail.name() : __AuditTrail,
        __DataOwnerRef.name() : __DataOwnerRef,
        __DataOwnerID.name() : __DataOwnerID,
        __Comment.name() : __Comment
    })
    _AttributeMap.update({
        __modver.name() : __modver
    })
_module_typeBindings.documentInfoType = documentInfoType
Namespace.addCategoryObject('typeBinding', 'documentInfoType', documentInfoType)


# Complex type {http://www.posc.org/schemas}fileCrType with content type ELEMENT_ONLY
class fileCrType (pyxb.binding.basis.complexTypeDefinition):
    """
A block of information about the creation of the XML file. This is different
than the creation of the data that is included within the file.
                """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'fileCrType')
    _XSDLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 145, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.posc.org/schemas}FileCreationDate uses Python identifier FileCreationDate
    __FileCreationDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FileCreationDate'), 'FileCreationDate', '__httpwww_posc_orgschemas_fileCrType_httpwww_posc_orgschemasFileCreationDate', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 153, 2), )

    
    FileCreationDate = property(__FileCreationDate.value, __FileCreationDate.set, None, '\nThe date and/or time that the file was created.\n                ')

    
    # Element {http://www.posc.org/schemas}SoftwareName uses Python identifier SoftwareName
    __SoftwareName = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SoftwareName'), 'SoftwareName', '__httpwww_posc_orgschemas_fileCrType_httpwww_posc_orgschemasSoftwareName', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 160, 2), )

    
    SoftwareName = property(__SoftwareName.value, __SoftwareName.set, None, '\nIf appropriate, the software that created the file. This is a free form\nstring, and may include whatever information is deemed relevant.\n                ')

    
    # Element {http://www.posc.org/schemas}FileCreator uses Python identifier FileCreator
    __FileCreator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FileCreator'), 'FileCreator', '__httpwww_posc_orgschemas_fileCrType_httpwww_posc_orgschemasFileCreator', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 168, 2), )

    
    FileCreator = property(__FileCreator.value, __FileCreator.set, None, '\nThe person or business associate that created the file. This is a free\nform string.\n                ')

    
    # Element {http://www.posc.org/schemas}Comment uses Python identifier Comment
    __Comment = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Comment'), 'Comment', '__httpwww_posc_orgschemas_fileCrType_httpwww_posc_orgschemasComment', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 176, 2), )

    
    Comment = property(__Comment.value, __Comment.set, None, '\nAny comment that would be useful to further explain the creation of this\ninstance document.\n                ')

    _ElementMap.update({
        __FileCreationDate.name() : __FileCreationDate,
        __SoftwareName.name() : __SoftwareName,
        __FileCreator.name() : __FileCreator,
        __Comment.name() : __Comment
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.fileCrType = fileCrType
Namespace.addCategoryObject('typeBinding', 'fileCrType', fileCrType)


# Complex type {http://www.posc.org/schemas}securityInfoType with content type ELEMENT_ONLY
class securityInfoType (pyxb.binding.basis.complexTypeDefinition):
    """
Information about the security classification of the document. This is
intended as a documentation of the security so that the file will not 
inadvertently be sent to someone who is not allowed access to the data. 
This block also carries a date that the security classification expires.
For example, a well log is confidential for a period of time, and then
becomes open.
All security classes are characterized by their classification systems.
                """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'securityInfoType')
    _XSDLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 187, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.posc.org/schemas}Class uses Python identifier Class
    __Class = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Class'), 'Class', '__httpwww_posc_orgschemas_securityInfoType_httpwww_posc_orgschemasClass', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 200, 2), )

    
    Class = property(__Class.value, __Class.set, None, '\nThe security class in which this document is classified. Examples would \nbe confidential, partner confidential, tight. The meaning of the class is\ndetermined by the System in which it is defined.\n                ')

    
    # Element {http://www.posc.org/schemas}System uses Python identifier System
    __System = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'System'), 'System', '__httpwww_posc_orgschemas_securityInfoType_httpwww_posc_orgschemasSystem', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 209, 2), )

    
    System = property(__System.value, __System.set, None, '\nThe security classification system. This gives context to the meaning of the\nClass value.\n                ')

    
    # Element {http://www.posc.org/schemas}EndDate uses Python identifier EndDate
    __EndDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'EndDate'), 'EndDate', '__httpwww_posc_orgschemas_securityInfoType_httpwww_posc_orgschemasEndDate', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 217, 2), )

    
    EndDate = property(__EndDate.value, __EndDate.set, None, '\nThe date on which this security class is no longer applicable.\n                ')

    
    # Element {http://www.posc.org/schemas}Comment uses Python identifier Comment
    __Comment = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Comment'), 'Comment', '__httpwww_posc_orgschemas_securityInfoType_httpwww_posc_orgschemasComment', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 224, 2), )

    
    Comment = property(__Comment.value, __Comment.set, None, '\nA general comment to further define the security class.\n                ')

    _ElementMap.update({
        __Class.name() : __Class,
        __System.name() : __System,
        __EndDate.name() : __EndDate,
        __Comment.name() : __Comment
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.securityInfoType = securityInfoType
Namespace.addCategoryObject('typeBinding', 'securityInfoType', securityInfoType)


# Complex type {http://www.posc.org/schemas}auditType with content type ELEMENT_ONLY
class auditType (pyxb.binding.basis.complexTypeDefinition):
    """
The audit records what happened to the data, to produce the data that is in
this file. It consists of one or more events.
                """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'auditType')
    _XSDLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 234, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.posc.org/schemas}Event uses Python identifier Event
    __Event = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Event'), 'Event', '__httpwww_posc_orgschemas_auditType_httpwww_posc_orgschemasEvent', True, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 242, 2), )

    
    Event = property(__Event.value, __Event.set, None, None)

    _ElementMap.update({
        __Event.name() : __Event
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.auditType = auditType
Namespace.addCategoryObject('typeBinding', 'auditType', auditType)


# Complex type {http://www.posc.org/schemas}eventType with content type ELEMENT_ONLY
class eventType (pyxb.binding.basis.complexTypeDefinition):
    """
An event type captures the basic information about an event that has 
affected the data.
                """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'eventType')
    _XSDLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 246, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.posc.org/schemas}EventDate uses Python identifier EventDate
    __EventDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'EventDate'), 'EventDate', '__httpwww_posc_orgschemas_eventType_httpwww_posc_orgschemasEventDate', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 254, 2), )

    
    EventDate = property(__EventDate.value, __EventDate.set, None, '\nThe date on which the event took place.\n                ')

    
    # Element {http://www.posc.org/schemas}ResponsiblePartyRef uses Python identifier ResponsiblePartyRef
    __ResponsiblePartyRef = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ResponsiblePartyRef'), 'ResponsiblePartyRef', '__httpwww_posc_orgschemas_eventType_httpwww_posc_orgschemasResponsiblePartyRef', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 269, 3), )

    
    ResponsiblePartyRef = property(__ResponsiblePartyRef.value, __ResponsiblePartyRef.set, None, None)

    
    # Element {http://www.posc.org/schemas}ResponsiblePartyID uses Python identifier ResponsiblePartyID
    __ResponsiblePartyID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ResponsiblePartyID'), 'ResponsiblePartyID', '__httpwww_posc_orgschemas_eventType_httpwww_posc_orgschemasResponsiblePartyID', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 270, 3), )

    
    ResponsiblePartyID = property(__ResponsiblePartyID.value, __ResponsiblePartyID.set, None, None)

    
    # Element {http://www.posc.org/schemas}Comment uses Python identifier Comment
    __Comment = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Comment'), 'Comment', '__httpwww_posc_orgschemas_eventType_httpwww_posc_orgschemasComment', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 272, 2), )

    
    Comment = property(__Comment.value, __Comment.set, None, '\nA free form comment that can further define the event that occurred.\n                ')

    _ElementMap.update({
        __EventDate.name() : __EventDate,
        __ResponsiblePartyRef.name() : __ResponsiblePartyRef,
        __ResponsiblePartyID.name() : __ResponsiblePartyID,
        __Comment.name() : __Comment
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.eventType = eventType
Namespace.addCategoryObject('typeBinding', 'eventType', eventType)


# Complex type {http://www.posc.org/schemas}abstractFeatureType with content type ELEMENT_ONLY
class abstractFeatureType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.posc.org/schemas}abstractFeatureType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'abstractFeatureType')
    _XSDLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 282, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.posc.org/schemas}Text uses Python identifier Text
    __Text = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Text'), 'Text', '__httpwww_posc_orgschemas_abstractFeatureType_httpwww_posc_orgschemasText', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 284, 4), )

    
    Text = property(__Text.value, __Text.set, None, None)

    _ElementMap.update({
        __Text.name() : __Text
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.abstractFeatureType = abstractFeatureType
Namespace.addCategoryObject('typeBinding', 'abstractFeatureType', abstractFeatureType)


# Complex type {http://www.posc.org/schemas}identifierType with content type ELEMENT_ONLY
class identifierType (pyxb.binding.basis.complexTypeDefinition):
    """
A common way for handling names of objects. An identifier type must include a Name. It
may also include a NamingSystem, which gives meaning to the name. Since Names and 
NamingSystems may change with time, it may also include a Version, to further refine the
meaning of the name.
Note that this three-part structure is based on the ISO Identifier type.
    """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'identifierType')
    _XSDLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 288, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.posc.org/schemas}Name uses Python identifier Name
    __Name = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Name'), 'Name', '__httpwww_posc_orgschemas_identifierType_httpwww_posc_orgschemasName', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 299, 4), )

    
    Name = property(__Name.value, __Name.set, None, '\nThe name of the object being identified. It may or may not be a unique name, depending on the use of this type. When used as an "identifier," it should be a unique name, within the naming system. When used as an "alias," the name is not required to be unique.\n    ')

    
    # Element {http://www.posc.org/schemas}NamingSystem uses Python identifier NamingSystem
    __NamingSystem = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'NamingSystem'), 'NamingSystem', '__httpwww_posc_orgschemas_identifierType_httpwww_posc_orgschemasNamingSystem', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 307, 6), )

    
    NamingSystem = property(__NamingSystem.value, __NamingSystem.set, None, "\nThe naming system under which the name is defined. For example, if the name is a person's social security number, the naming system would be SSN, or some equivalent code which represents that the name is a social security number. Since naming system may be a code, there are two attributes (nameRef and systemList), which may be used to lead an application to a registry, where meaning can be obtained for the code. \n    ")

    
    # Element {http://www.posc.org/schemas}Version uses Python identifier Version
    __Version = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Version'), 'Version', '__httpwww_posc_orgschemas_identifierType_httpwww_posc_orgschemasVersion', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 314, 6), )

    
    Version = property(__Version.value, __Version.set, None, '\nWhen a naming system is declared, it may be further qualified by giving a version of the\nnaming system. This is needed only when a group puts out a new set of names that are not\nbackward compatible with a previous list.\n    ')

    
    # Element {http://www.posc.org/schemas}Comment uses Python identifier Comment
    __Comment = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Comment'), 'Comment', '__httpwww_posc_orgschemas_identifierType_httpwww_posc_orgschemasComment', False, pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 324, 4), )

    
    Comment = property(__Comment.value, __Comment.set, None, None)

    _ElementMap.update({
        __Name.name() : __Name,
        __NamingSystem.name() : __NamingSystem,
        __Version.name() : __Version,
        __Comment.name() : __Comment
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.identifierType = identifierType
Namespace.addCategoryObject('typeBinding', 'identifierType', identifierType)


# Complex type {http://www.posc.org/schemas}referenceToType with content type EMPTY
class referenceToType (pyxb.binding.basis.complexTypeDefinition):
    """
A reference, with no content. The only attribute is href, which is a reference to another instance.
    """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'referenceToType')
    _XSDLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 328, 0)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'href'), 'href', '__httpwww_posc_orgschemas_referenceToType_href', pyxb.binding.datatypes.string, required=True)
    __href._DeclarationLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 334, 1)
    __href._UseLocation = pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 334, 1)
    
    href = property(__href.value, __href.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __href.name() : __href
    })
_module_typeBindings.referenceToType = referenceToType
Namespace.addCategoryObject('typeBinding', 'referenceToType', referenceToType)


DocumentInformation = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DocumentInformation'), documentInfoType, documentation='\nA standard name for an element of type documentInfoType. Other names may be \nused at the discretion of the developer.\n                  ', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 24, 0))
Namespace.addCategoryObject('elementBinding', DocumentInformation.name().localName(), DocumentInformation)

DocClasses = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, '_DocClasses'), abstractFeatureType, abstract=pyxb.binding.datatypes.boolean(1), documentation='\nAn abstract element, to serve as a head for a substitution group. The \n_DocClasses is intended to handle any classification systems that a group\nwould model. It may be a simple substitution, or a container with many\nclasses contained in it.\n                ', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 35, 0))
Namespace.addCategoryObject('elementBinding', DocClasses.name().localName(), DocClasses)



documentInfoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, '_DocClasses'), abstractFeatureType, abstract=pyxb.binding.datatypes.boolean(1), scope=documentInfoType, documentation='\nAn abstract element, to serve as a head for a substitution group. The \n_DocClasses is intended to handle any classification systems that a group\nwould model. It may be a simple substitution, or a container with many\nclasses contained in it.\n                ', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 35, 0)))

documentInfoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DocumentName'), identifierType, scope=documentInfoType, documentation='\nAn identifier for the document. This is intended to be unique within the \ncontext of the NamingSystem.\n                ', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 56, 2)))

documentInfoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DocumentAlias'), identifierType, scope=documentInfoType, documentation='\nZero or more alternate names for the document. These names do not need to be\nunique within the naming system.\n                ', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 64, 2)))

documentInfoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DocumentDate'), pyxb.binding.datatypes.date, scope=documentInfoType, documentation='\nThe date of the creation of the document. This is not the same as the date\nthat the file was created. For this date, the document is considered to be\nthe set of information associated with this document information.\nFor example, the document may be a seismic binset. This represents the date\nthat the binset was created. The FileCreation information would capture the\ndate that the XML file was created to send or exchange the binset.\n                ', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 72, 2)))

documentInfoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FileCreationInformation'), fileCrType, scope=documentInfoType, documentation='\nThe information about the creation of the exchange file. This is not about\nthe creation of the data within the file, but the creation of the file itself.\n                ', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 93, 2)))

documentInfoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SecurityInformation'), securityInfoType, scope=documentInfoType, documentation='\nInformation about the security to be applied to this file. More than one\nclassification can be given.\n                ', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 101, 2)))

documentInfoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Disclaimer'), pyxb.binding.datatypes.string, scope=documentInfoType, documentation='\nA free-form string that allows a disclaimer to accompany the information.\n                ', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 109, 2)))

documentInfoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AuditTrail'), auditType, scope=documentInfoType, documentation='\nA collection of events that can document the history of the data.\n                ', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 116, 2)))

documentInfoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DataOwnerRef'), referenceToType, scope=documentInfoType, location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 131, 4)))

documentInfoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DataOwnerID'), pyxb.binding.datatypes.string, scope=documentInfoType, location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 132, 4)))

documentInfoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Comment'), pyxb.binding.datatypes.string, scope=documentInfoType, documentation='\nAn optional comment about the document.\n                ', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 134, 2)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 64, 2))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 72, 2))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 84, 2))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 93, 2))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=5, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 101, 2))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 109, 2))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 116, 2))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 123, 2))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 134, 2))
    counters.add(cc_8)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(documentInfoType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DocumentName')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 56, 2))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(documentInfoType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DocumentAlias')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 64, 2))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(documentInfoType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DocumentDate')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 72, 2))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(documentInfoType._UseForTag(pyxb.namespace.ExpandedName(Namespace, '_DocClasses')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 84, 2))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(documentInfoType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FileCreationInformation')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 93, 2))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(documentInfoType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SecurityInformation')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 101, 2))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(documentInfoType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Disclaimer')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 109, 2))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(documentInfoType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'AuditTrail')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 116, 2))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(documentInfoType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DataOwnerRef')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 131, 4))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(documentInfoType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DataOwnerID')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 132, 4))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(documentInfoType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Comment')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 134, 2))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    transitions.append(fac.Transition(st_7, [
         ]))
    transitions.append(fac.Transition(st_8, [
         ]))
    transitions.append(fac.Transition(st_9, [
         ]))
    transitions.append(fac.Transition(st_10, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
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
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
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
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True) ]))
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
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_7, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_7, False) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_8, True) ]))
    st_10._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
documentInfoType._Automaton = _BuildAutomaton()




fileCrType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FileCreationDate'), expandedDateTime, scope=fileCrType, documentation='\nThe date and/or time that the file was created.\n                ', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 153, 2)))

fileCrType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SoftwareName'), pyxb.binding.datatypes.string, scope=fileCrType, documentation='\nIf appropriate, the software that created the file. This is a free form\nstring, and may include whatever information is deemed relevant.\n                ', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 160, 2)))

fileCrType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FileCreator'), pyxb.binding.datatypes.string, scope=fileCrType, documentation='\nThe person or business associate that created the file. This is a free\nform string.\n                ', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 168, 2)))

fileCrType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Comment'), pyxb.binding.datatypes.string, scope=fileCrType, documentation='\nAny comment that would be useful to further explain the creation of this\ninstance document.\n                ', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 176, 2)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 160, 2))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 168, 2))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 176, 2))
    counters.add(cc_2)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(fileCrType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FileCreationDate')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 153, 2))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(fileCrType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SoftwareName')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 160, 2))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(fileCrType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FileCreator')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 168, 2))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(fileCrType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Comment')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 176, 2))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
fileCrType._Automaton = _BuildAutomaton_()




securityInfoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Class'), pyxb.binding.datatypes.string, scope=securityInfoType, documentation='\nThe security class in which this document is classified. Examples would \nbe confidential, partner confidential, tight. The meaning of the class is\ndetermined by the System in which it is defined.\n                ', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 200, 2)))

securityInfoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'System'), pyxb.binding.datatypes.string, scope=securityInfoType, documentation='\nThe security classification system. This gives context to the meaning of the\nClass value.\n                ', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 209, 2)))

securityInfoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'EndDate'), expandedDateTime, scope=securityInfoType, documentation='\nThe date on which this security class is no longer applicable.\n                ', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 217, 2)))

securityInfoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Comment'), pyxb.binding.datatypes.string, scope=securityInfoType, documentation='\nA general comment to further define the security class.\n                ', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 224, 2)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 209, 2))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 217, 2))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 224, 2))
    counters.add(cc_2)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(securityInfoType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Class')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 200, 2))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(securityInfoType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'System')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 209, 2))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(securityInfoType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'EndDate')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 217, 2))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(securityInfoType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Comment')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 224, 2))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
securityInfoType._Automaton = _BuildAutomaton_2()




auditType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Event'), eventType, scope=auditType, location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 242, 2)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(auditType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Event')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 242, 2))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
auditType._Automaton = _BuildAutomaton_3()




eventType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'EventDate'), expandedDateTime, scope=eventType, documentation='\nThe date on which the event took place.\n                ', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 254, 2)))

eventType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ResponsiblePartyRef'), referenceToType, scope=eventType, location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 269, 3)))

eventType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ResponsiblePartyID'), pyxb.binding.datatypes.string, scope=eventType, location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 270, 3)))

eventType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Comment'), pyxb.binding.datatypes.string, scope=eventType, documentation='\nA free form comment that can further define the event that occurred.\n                ', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 272, 2)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 261, 2))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(eventType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'EventDate')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 254, 2))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(eventType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ResponsiblePartyRef')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 269, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(eventType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ResponsiblePartyID')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 270, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(eventType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Comment')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 272, 2))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
eventType._Automaton = _BuildAutomaton_4()




abstractFeatureType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Text'), pyxb.binding.datatypes.string, scope=abstractFeatureType, location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 284, 4)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 284, 4))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(abstractFeatureType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Text')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 284, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
abstractFeatureType._Automaton = _BuildAutomaton_5()




identifierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Name'), pyxb.binding.datatypes.string, scope=identifierType, documentation='\nThe name of the object being identified. It may or may not be a unique name, depending on the use of this type. When used as an "identifier," it should be a unique name, within the naming system. When used as an "alias," the name is not required to be unique.\n    ', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 299, 4)))

identifierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'NamingSystem'), pyxb.binding.datatypes.string, scope=identifierType, documentation="\nThe naming system under which the name is defined. For example, if the name is a person's social security number, the naming system would be SSN, or some equivalent code which represents that the name is a social security number. Since naming system may be a code, there are two attributes (nameRef and systemList), which may be used to lead an application to a registry, where meaning can be obtained for the code. \n    ", location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 307, 6)))

identifierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Version'), pyxb.binding.datatypes.string, scope=identifierType, documentation='\nWhen a naming system is declared, it may be further qualified by giving a version of the\nnaming system. This is needed only when a group puts out a new set of names that are not\nbackward compatible with a previous list.\n    ', location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 314, 6)))

identifierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Comment'), pyxb.binding.datatypes.string, scope=identifierType, location=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 324, 4)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 306, 4))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 314, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 324, 4))
    counters.add(cc_2)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(identifierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Name')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 299, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(identifierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'NamingSystem')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 307, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(identifierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Version')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 314, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(identifierType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Comment')), pyxb.utils.utility.Location('https://raw.githubusercontent.com/HemersonRafael/witsml_files/main/schemas/uom/units20/DocumentInfo.xsd', 324, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_1, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
identifierType._Automaton = _BuildAutomaton_6()

