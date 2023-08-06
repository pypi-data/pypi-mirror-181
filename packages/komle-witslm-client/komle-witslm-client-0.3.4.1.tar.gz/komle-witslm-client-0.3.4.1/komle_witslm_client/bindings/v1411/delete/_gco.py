# komle_witslm_client/bindings/v1411/delete/_gco.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:2bd68004d120daf987d63b2efda66ae3eda8eaea
# Generated 2022-10-17 03:39:40.738067 by PyXB version 1.2.6 using Python 3.10.4.final.0
# Namespace http://www.isotc211.org/2005/gco [xmlns:gco]

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
import komle_witslm_client.bindings.v1411.delete._nsgroup as _ImportedBinding_bindingsv1411delete__nsgroup

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://www.isotc211.org/2005/gco', create_if_missing=True)
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

from komle_witslm_client.bindings.v1411.delete._nsgroup import CharacterString # {http://www.isotc211.org/2005/gco}CharacterString
from komle_witslm_client.bindings.v1411.delete._nsgroup import Boolean # {http://www.isotc211.org/2005/gco}Boolean
from komle_witslm_client.bindings.v1411.delete._nsgroup import DateTime # {http://www.isotc211.org/2005/gco}DateTime
from komle_witslm_client.bindings.v1411.delete._nsgroup import Decimal # {http://www.isotc211.org/2005/gco}Decimal
from komle_witslm_client.bindings.v1411.delete._nsgroup import Real # {http://www.isotc211.org/2005/gco}Real
from komle_witslm_client.bindings.v1411.delete._nsgroup import Integer # {http://www.isotc211.org/2005/gco}Integer
from komle_witslm_client.bindings.v1411.delete._nsgroup import Record # {http://www.isotc211.org/2005/gco}Record
from komle_witslm_client.bindings.v1411.delete._nsgroup import AbstractGenericName # {http://www.isotc211.org/2005/gco}AbstractGenericName
from komle_witslm_client.bindings.v1411.delete._nsgroup import LocalName # {http://www.isotc211.org/2005/gco}LocalName
from komle_witslm_client.bindings.v1411.delete._nsgroup import ScopedName # {http://www.isotc211.org/2005/gco}ScopedName
from komle_witslm_client.bindings.v1411.delete._nsgroup import Date # {http://www.isotc211.org/2005/gco}Date
from komle_witslm_client.bindings.v1411.delete._nsgroup import UnlimitedInteger # {http://www.isotc211.org/2005/gco}UnlimitedInteger
from komle_witslm_client.bindings.v1411.delete._nsgroup import Binary # {http://www.isotc211.org/2005/gco}Binary
from komle_witslm_client.bindings.v1411.delete._nsgroup import AbstractObject_ as AbstractObject # {http://www.isotc211.org/2005/gco}AbstractObject
from komle_witslm_client.bindings.v1411.delete._nsgroup import TypeName # {http://www.isotc211.org/2005/gco}TypeName
from komle_witslm_client.bindings.v1411.delete._nsgroup import MemberName # {http://www.isotc211.org/2005/gco}MemberName
from komle_witslm_client.bindings.v1411.delete._nsgroup import Multiplicity # {http://www.isotc211.org/2005/gco}Multiplicity
from komle_witslm_client.bindings.v1411.delete._nsgroup import MultiplicityRange # {http://www.isotc211.org/2005/gco}MultiplicityRange
from komle_witslm_client.bindings.v1411.delete._nsgroup import RecordType # {http://www.isotc211.org/2005/gco}RecordType
from komle_witslm_client.bindings.v1411.delete._nsgroup import Measure # {http://www.isotc211.org/2005/gco}Measure
from komle_witslm_client.bindings.v1411.delete._nsgroup import Length # {http://www.isotc211.org/2005/gco}Length
from komle_witslm_client.bindings.v1411.delete._nsgroup import Angle # {http://www.isotc211.org/2005/gco}Angle
from komle_witslm_client.bindings.v1411.delete._nsgroup import Scale # {http://www.isotc211.org/2005/gco}Scale
from komle_witslm_client.bindings.v1411.delete._nsgroup import Distance # {http://www.isotc211.org/2005/gco}Distance
from komle_witslm_client.bindings.v1411.delete._nsgroup import Date_Type # {http://www.isotc211.org/2005/gco}Date_Type
from komle_witslm_client.bindings.v1411.delete._nsgroup import UnlimitedInteger_Type # {http://www.isotc211.org/2005/gco}UnlimitedInteger_Type
from komle_witslm_client.bindings.v1411.delete._nsgroup import Binary_Type # {http://www.isotc211.org/2005/gco}Binary_Type
from komle_witslm_client.bindings.v1411.delete._nsgroup import AbstractObject_Type # {http://www.isotc211.org/2005/gco}AbstractObject_Type
from komle_witslm_client.bindings.v1411.delete._nsgroup import CodeListValue_Type # {http://www.isotc211.org/2005/gco}CodeListValue_Type
from komle_witslm_client.bindings.v1411.delete._nsgroup import TypeName_Type # {http://www.isotc211.org/2005/gco}TypeName_Type
from komle_witslm_client.bindings.v1411.delete._nsgroup import MemberName_Type # {http://www.isotc211.org/2005/gco}MemberName_Type
from komle_witslm_client.bindings.v1411.delete._nsgroup import Multiplicity_Type # {http://www.isotc211.org/2005/gco}Multiplicity_Type
from komle_witslm_client.bindings.v1411.delete._nsgroup import MultiplicityRange_Type # {http://www.isotc211.org/2005/gco}MultiplicityRange_Type
from komle_witslm_client.bindings.v1411.delete._nsgroup import RecordType_Type # {http://www.isotc211.org/2005/gco}RecordType_Type
from komle_witslm_client.bindings.v1411.delete._nsgroup import TypeName_PropertyType # {http://www.isotc211.org/2005/gco}TypeName_PropertyType
from komle_witslm_client.bindings.v1411.delete._nsgroup import MemberName_PropertyType # {http://www.isotc211.org/2005/gco}MemberName_PropertyType
from komle_witslm_client.bindings.v1411.delete._nsgroup import Multiplicity_PropertyType # {http://www.isotc211.org/2005/gco}Multiplicity_PropertyType
from komle_witslm_client.bindings.v1411.delete._nsgroup import MultiplicityRange_PropertyType # {http://www.isotc211.org/2005/gco}MultiplicityRange_PropertyType
from komle_witslm_client.bindings.v1411.delete._nsgroup import Measure_PropertyType # {http://www.isotc211.org/2005/gco}Measure_PropertyType
from komle_witslm_client.bindings.v1411.delete._nsgroup import Length_PropertyType # {http://www.isotc211.org/2005/gco}Length_PropertyType
from komle_witslm_client.bindings.v1411.delete._nsgroup import Angle_PropertyType # {http://www.isotc211.org/2005/gco}Angle_PropertyType
from komle_witslm_client.bindings.v1411.delete._nsgroup import Scale_PropertyType # {http://www.isotc211.org/2005/gco}Scale_PropertyType
from komle_witslm_client.bindings.v1411.delete._nsgroup import Distance_PropertyType # {http://www.isotc211.org/2005/gco}Distance_PropertyType
from komle_witslm_client.bindings.v1411.delete._nsgroup import CharacterString_PropertyType # {http://www.isotc211.org/2005/gco}CharacterString_PropertyType
from komle_witslm_client.bindings.v1411.delete._nsgroup import Boolean_PropertyType # {http://www.isotc211.org/2005/gco}Boolean_PropertyType
from komle_witslm_client.bindings.v1411.delete._nsgroup import GenericName_PropertyType # {http://www.isotc211.org/2005/gco}GenericName_PropertyType
from komle_witslm_client.bindings.v1411.delete._nsgroup import LocalName_PropertyType # {http://www.isotc211.org/2005/gco}LocalName_PropertyType
from komle_witslm_client.bindings.v1411.delete._nsgroup import ScopedName_PropertyType # {http://www.isotc211.org/2005/gco}ScopedName_PropertyType
from komle_witslm_client.bindings.v1411.delete._nsgroup import UomAngle_PropertyType # {http://www.isotc211.org/2005/gco}UomAngle_PropertyType
from komle_witslm_client.bindings.v1411.delete._nsgroup import UomLength_PropertyType # {http://www.isotc211.org/2005/gco}UomLength_PropertyType
from komle_witslm_client.bindings.v1411.delete._nsgroup import UomScale_PropertyType # {http://www.isotc211.org/2005/gco}UomScale_PropertyType
from komle_witslm_client.bindings.v1411.delete._nsgroup import UnitOfMeasure_PropertyType # {http://www.isotc211.org/2005/gco}UnitOfMeasure_PropertyType
from komle_witslm_client.bindings.v1411.delete._nsgroup import UomArea_PropertyType # {http://www.isotc211.org/2005/gco}UomArea_PropertyType
from komle_witslm_client.bindings.v1411.delete._nsgroup import UomVelocity_PropertyType # {http://www.isotc211.org/2005/gco}UomVelocity_PropertyType
from komle_witslm_client.bindings.v1411.delete._nsgroup import UomTime_PropertyType # {http://www.isotc211.org/2005/gco}UomTime_PropertyType
from komle_witslm_client.bindings.v1411.delete._nsgroup import UomVolume_PropertyType # {http://www.isotc211.org/2005/gco}UomVolume_PropertyType
from komle_witslm_client.bindings.v1411.delete._nsgroup import DateTime_PropertyType # {http://www.isotc211.org/2005/gco}DateTime_PropertyType
from komle_witslm_client.bindings.v1411.delete._nsgroup import Date_PropertyType # {http://www.isotc211.org/2005/gco}Date_PropertyType
from komle_witslm_client.bindings.v1411.delete._nsgroup import Number_PropertyType # {http://www.isotc211.org/2005/gco}Number_PropertyType
from komle_witslm_client.bindings.v1411.delete._nsgroup import Decimal_PropertyType # {http://www.isotc211.org/2005/gco}Decimal_PropertyType
from komle_witslm_client.bindings.v1411.delete._nsgroup import Real_PropertyType # {http://www.isotc211.org/2005/gco}Real_PropertyType
from komle_witslm_client.bindings.v1411.delete._nsgroup import Integer_PropertyType # {http://www.isotc211.org/2005/gco}Integer_PropertyType
from komle_witslm_client.bindings.v1411.delete._nsgroup import UnlimitedInteger_PropertyType # {http://www.isotc211.org/2005/gco}UnlimitedInteger_PropertyType
from komle_witslm_client.bindings.v1411.delete._nsgroup import Record_PropertyType # {http://www.isotc211.org/2005/gco}Record_PropertyType
from komle_witslm_client.bindings.v1411.delete._nsgroup import RecordType_PropertyType # {http://www.isotc211.org/2005/gco}RecordType_PropertyType
from komle_witslm_client.bindings.v1411.delete._nsgroup import Binary_PropertyType # {http://www.isotc211.org/2005/gco}Binary_PropertyType
from komle_witslm_client.bindings.v1411.delete._nsgroup import ObjectReference_PropertyType # {http://www.isotc211.org/2005/gco}ObjectReference_PropertyType
