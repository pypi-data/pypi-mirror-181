# komle_witslm_client/bindings/v20/_gml.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:c4f74fce23a2f49d6da683416eb2980bfced7e33
# Generated 2022-10-17 04:03:28.030791 by PyXB version 1.2.6 using Python 3.10.4.final.0
# Namespace http://www.opengis.net/gml/3.2 [xmlns:gml]

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
import komle_witslm_client.bindings.v20._nsgroup as _ImportedBinding_bindingsv20__nsgroup

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://www.opengis.net/gml/3.2', create_if_missing=True)
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

from komle_witslm_client.bindings.v20._nsgroup import AbstractObject # {http://www.opengis.net/gml/3.2}AbstractObject
from komle_witslm_client.bindings.v20._nsgroup import remarks # {http://www.opengis.net/gml/3.2}remarks
from komle_witslm_client.bindings.v20._nsgroup import scope # {http://www.opengis.net/gml/3.2}scope
from komle_witslm_client.bindings.v20._nsgroup import minimumValue # {http://www.opengis.net/gml/3.2}minimumValue
from komle_witslm_client.bindings.v20._nsgroup import maximumValue # {http://www.opengis.net/gml/3.2}maximumValue
from komle_witslm_client.bindings.v20._nsgroup import realizationEpoch # {http://www.opengis.net/gml/3.2}realizationEpoch
from komle_witslm_client.bindings.v20._nsgroup import operationVersion # {http://www.opengis.net/gml/3.2}operationVersion
from komle_witslm_client.bindings.v20._nsgroup import name # {http://www.opengis.net/gml/3.2}name
from komle_witslm_client.bindings.v20._nsgroup import AbstractGML # {http://www.opengis.net/gml/3.2}AbstractGML
from komle_witslm_client.bindings.v20._nsgroup import axisAbbrev # {http://www.opengis.net/gml/3.2}axisAbbrev
from komle_witslm_client.bindings.v20._nsgroup import anchorDefinition # {http://www.opengis.net/gml/3.2}anchorDefinition
from komle_witslm_client.bindings.v20._nsgroup import semiMajorAxis # {http://www.opengis.net/gml/3.2}semiMajorAxis
from komle_witslm_client.bindings.v20._nsgroup import secondDefiningParameter # {http://www.opengis.net/gml/3.2}secondDefiningParameter
from komle_witslm_client.bindings.v20._nsgroup import SecondDefiningParameter # {http://www.opengis.net/gml/3.2}SecondDefiningParameter
from komle_witslm_client.bindings.v20._nsgroup import identifier # {http://www.opengis.net/gml/3.2}identifier
from komle_witslm_client.bindings.v20._nsgroup import AbstractTimeObject # {http://www.opengis.net/gml/3.2}AbstractTimeObject
from komle_witslm_client.bindings.v20._nsgroup import axisDirection # {http://www.opengis.net/gml/3.2}axisDirection
from komle_witslm_client.bindings.v20._nsgroup import rangeMeaning # {http://www.opengis.net/gml/3.2}rangeMeaning
from komle_witslm_client.bindings.v20._nsgroup import greenwichLongitude # {http://www.opengis.net/gml/3.2}greenwichLongitude
from komle_witslm_client.bindings.v20._nsgroup import description # {http://www.opengis.net/gml/3.2}description
from komle_witslm_client.bindings.v20._nsgroup import descriptionReference # {http://www.opengis.net/gml/3.2}descriptionReference
from komle_witslm_client.bindings.v20._nsgroup import domainOfValidity # {http://www.opengis.net/gml/3.2}domainOfValidity
from komle_witslm_client.bindings.v20._nsgroup import AbstractTimePrimitive # {http://www.opengis.net/gml/3.2}AbstractTimePrimitive
from komle_witslm_client.bindings.v20._nsgroup import Definition # {http://www.opengis.net/gml/3.2}Definition
from komle_witslm_client.bindings.v20._nsgroup import ellipsoidalCS # {http://www.opengis.net/gml/3.2}ellipsoidalCS
from komle_witslm_client.bindings.v20._nsgroup import axis # {http://www.opengis.net/gml/3.2}axis
from komle_witslm_client.bindings.v20._nsgroup import cartesianCS # {http://www.opengis.net/gml/3.2}cartesianCS
from komle_witslm_client.bindings.v20._nsgroup import sphericalCS # {http://www.opengis.net/gml/3.2}sphericalCS
from komle_witslm_client.bindings.v20._nsgroup import geodeticDatum # {http://www.opengis.net/gml/3.2}geodeticDatum
from komle_witslm_client.bindings.v20._nsgroup import primeMeridian # {http://www.opengis.net/gml/3.2}primeMeridian
from komle_witslm_client.bindings.v20._nsgroup import ellipsoid # {http://www.opengis.net/gml/3.2}ellipsoid
from komle_witslm_client.bindings.v20._nsgroup import conversion # {http://www.opengis.net/gml/3.2}conversion
from komle_witslm_client.bindings.v20._nsgroup import coordinateOperationAccuracy # {http://www.opengis.net/gml/3.2}coordinateOperationAccuracy
from komle_witslm_client.bindings.v20._nsgroup import sourceCRS # {http://www.opengis.net/gml/3.2}sourceCRS
from komle_witslm_client.bindings.v20._nsgroup import targetCRS # {http://www.opengis.net/gml/3.2}targetCRS
from komle_witslm_client.bindings.v20._nsgroup import baseGeodeticCRS # {http://www.opengis.net/gml/3.2}baseGeodeticCRS
from komle_witslm_client.bindings.v20._nsgroup import verticalCS # {http://www.opengis.net/gml/3.2}verticalCS
from komle_witslm_client.bindings.v20._nsgroup import verticalDatum # {http://www.opengis.net/gml/3.2}verticalDatum
from komle_witslm_client.bindings.v20._nsgroup import AbstractCRS # {http://www.opengis.net/gml/3.2}AbstractCRS
from komle_witslm_client.bindings.v20._nsgroup import CoordinateSystemAxis # {http://www.opengis.net/gml/3.2}CoordinateSystemAxis
from komle_witslm_client.bindings.v20._nsgroup import AbstractCoordinateSystem # {http://www.opengis.net/gml/3.2}AbstractCoordinateSystem
from komle_witslm_client.bindings.v20._nsgroup import PrimeMeridian # {http://www.opengis.net/gml/3.2}PrimeMeridian
from komle_witslm_client.bindings.v20._nsgroup import Ellipsoid # {http://www.opengis.net/gml/3.2}Ellipsoid
from komle_witslm_client.bindings.v20._nsgroup import AbstractDatum # {http://www.opengis.net/gml/3.2}AbstractDatum
from komle_witslm_client.bindings.v20._nsgroup import AbstractSingleCRS # {http://www.opengis.net/gml/3.2}AbstractSingleCRS
from komle_witslm_client.bindings.v20._nsgroup import AbstractOperation # {http://www.opengis.net/gml/3.2}AbstractOperation
from komle_witslm_client.bindings.v20._nsgroup import AbstractSingleOperation # {http://www.opengis.net/gml/3.2}AbstractSingleOperation
from komle_witslm_client.bindings.v20._nsgroup import AbstractCoordinateOperation # {http://www.opengis.net/gml/3.2}AbstractCoordinateOperation
from komle_witslm_client.bindings.v20._nsgroup import GeodeticCRS # {http://www.opengis.net/gml/3.2}GeodeticCRS
from komle_witslm_client.bindings.v20._nsgroup import EllipsoidalCS # {http://www.opengis.net/gml/3.2}EllipsoidalCS
from komle_witslm_client.bindings.v20._nsgroup import CartesianCS # {http://www.opengis.net/gml/3.2}CartesianCS
from komle_witslm_client.bindings.v20._nsgroup import SphericalCS # {http://www.opengis.net/gml/3.2}SphericalCS
from komle_witslm_client.bindings.v20._nsgroup import GeodeticDatum # {http://www.opengis.net/gml/3.2}GeodeticDatum
from komle_witslm_client.bindings.v20._nsgroup import AbstractGeneralConversion # {http://www.opengis.net/gml/3.2}AbstractGeneralConversion
from komle_witslm_client.bindings.v20._nsgroup import AbstractGeneralDerivedCRS # {http://www.opengis.net/gml/3.2}AbstractGeneralDerivedCRS
from komle_witslm_client.bindings.v20._nsgroup import VerticalCRS # {http://www.opengis.net/gml/3.2}VerticalCRS
from komle_witslm_client.bindings.v20._nsgroup import VerticalCS # {http://www.opengis.net/gml/3.2}VerticalCS
from komle_witslm_client.bindings.v20._nsgroup import VerticalDatum # {http://www.opengis.net/gml/3.2}VerticalDatum
from komle_witslm_client.bindings.v20._nsgroup import ProjectedCRS # {http://www.opengis.net/gml/3.2}ProjectedCRS
from komle_witslm_client.bindings.v20._nsgroup import AbstractGMLType # {http://www.opengis.net/gml/3.2}AbstractGMLType
from komle_witslm_client.bindings.v20._nsgroup import STD_ANON # None
from komle_witslm_client.bindings.v20._nsgroup import STD_ANON_ # None
from komle_witslm_client.bindings.v20._nsgroup import STD_ANON_2 # None
from komle_witslm_client.bindings.v20._nsgroup import CodeType # {http://www.opengis.net/gml/3.2}CodeType
from komle_witslm_client.bindings.v20._nsgroup import STD_ANON_3 # None
from komle_witslm_client.bindings.v20._nsgroup import UomSymbol # {http://www.opengis.net/gml/3.2}UomSymbol
from komle_witslm_client.bindings.v20._nsgroup import UomURI # {http://www.opengis.net/gml/3.2}UomURI
from komle_witslm_client.bindings.v20._nsgroup import AggregationType # {http://www.opengis.net/gml/3.2}AggregationType
from komle_witslm_client.bindings.v20._nsgroup import MeasureType # {http://www.opengis.net/gml/3.2}MeasureType
from komle_witslm_client.bindings.v20._nsgroup import CTD_ANON # None
from komle_witslm_client.bindings.v20._nsgroup import CTD_ANON_ # None
from komle_witslm_client.bindings.v20._nsgroup import DefinitionBaseType # {http://www.opengis.net/gml/3.2}DefinitionBaseType
from komle_witslm_client.bindings.v20._nsgroup import NilReasonType # {http://www.opengis.net/gml/3.2}NilReasonType
from komle_witslm_client.bindings.v20._nsgroup import NilReasonEnumeration # {http://www.opengis.net/gml/3.2}NilReasonEnumeration
from komle_witslm_client.bindings.v20._nsgroup import CodeWithAuthorityType # {http://www.opengis.net/gml/3.2}CodeWithAuthorityType
from komle_witslm_client.bindings.v20._nsgroup import AbstractTimeObjectType # {http://www.opengis.net/gml/3.2}AbstractTimeObjectType
from komle_witslm_client.bindings.v20._nsgroup import UomIdentifier # {http://www.opengis.net/gml/3.2}UomIdentifier
from komle_witslm_client.bindings.v20._nsgroup import AngleType # {http://www.opengis.net/gml/3.2}AngleType
from komle_witslm_client.bindings.v20._nsgroup import LengthType # {http://www.opengis.net/gml/3.2}LengthType
from komle_witslm_client.bindings.v20._nsgroup import DefinitionType # {http://www.opengis.net/gml/3.2}DefinitionType
from komle_witslm_client.bindings.v20._nsgroup import StringOrRefType # {http://www.opengis.net/gml/3.2}StringOrRefType
from komle_witslm_client.bindings.v20._nsgroup import ReferenceType # {http://www.opengis.net/gml/3.2}ReferenceType
from komle_witslm_client.bindings.v20._nsgroup import CTD_ANON_2 # None
from komle_witslm_client.bindings.v20._nsgroup import AbstractTimePrimitiveType # {http://www.opengis.net/gml/3.2}AbstractTimePrimitiveType
from komle_witslm_client.bindings.v20._nsgroup import TimePrimitivePropertyType # {http://www.opengis.net/gml/3.2}TimePrimitivePropertyType
from komle_witslm_client.bindings.v20._nsgroup import EllipsoidalCSPropertyType # {http://www.opengis.net/gml/3.2}EllipsoidalCSPropertyType
from komle_witslm_client.bindings.v20._nsgroup import CoordinateSystemAxisPropertyType # {http://www.opengis.net/gml/3.2}CoordinateSystemAxisPropertyType
from komle_witslm_client.bindings.v20._nsgroup import CartesianCSPropertyType # {http://www.opengis.net/gml/3.2}CartesianCSPropertyType
from komle_witslm_client.bindings.v20._nsgroup import SphericalCSPropertyType # {http://www.opengis.net/gml/3.2}SphericalCSPropertyType
from komle_witslm_client.bindings.v20._nsgroup import GeodeticDatumPropertyType # {http://www.opengis.net/gml/3.2}GeodeticDatumPropertyType
from komle_witslm_client.bindings.v20._nsgroup import PrimeMeridianPropertyType # {http://www.opengis.net/gml/3.2}PrimeMeridianPropertyType
from komle_witslm_client.bindings.v20._nsgroup import EllipsoidPropertyType # {http://www.opengis.net/gml/3.2}EllipsoidPropertyType
from komle_witslm_client.bindings.v20._nsgroup import GeneralConversionPropertyType # {http://www.opengis.net/gml/3.2}GeneralConversionPropertyType
from komle_witslm_client.bindings.v20._nsgroup import CTD_ANON_3 # None
from komle_witslm_client.bindings.v20._nsgroup import CRSPropertyType # {http://www.opengis.net/gml/3.2}CRSPropertyType
from komle_witslm_client.bindings.v20._nsgroup import GeodeticCRSPropertyType # {http://www.opengis.net/gml/3.2}GeodeticCRSPropertyType
from komle_witslm_client.bindings.v20._nsgroup import VerticalCSPropertyType # {http://www.opengis.net/gml/3.2}VerticalCSPropertyType
from komle_witslm_client.bindings.v20._nsgroup import VerticalDatumPropertyType # {http://www.opengis.net/gml/3.2}VerticalDatumPropertyType
from komle_witslm_client.bindings.v20._nsgroup import IdentifiedObjectType # {http://www.opengis.net/gml/3.2}IdentifiedObjectType
from komle_witslm_client.bindings.v20._nsgroup import RelatedTimeType # {http://www.opengis.net/gml/3.2}RelatedTimeType
from komle_witslm_client.bindings.v20._nsgroup import AbstractCRSType # {http://www.opengis.net/gml/3.2}AbstractCRSType
from komle_witslm_client.bindings.v20._nsgroup import AbstractCoordinateSystemType # {http://www.opengis.net/gml/3.2}AbstractCoordinateSystemType
from komle_witslm_client.bindings.v20._nsgroup import CoordinateSystemAxisType # {http://www.opengis.net/gml/3.2}CoordinateSystemAxisType
from komle_witslm_client.bindings.v20._nsgroup import AbstractDatumType # {http://www.opengis.net/gml/3.2}AbstractDatumType
from komle_witslm_client.bindings.v20._nsgroup import PrimeMeridianType # {http://www.opengis.net/gml/3.2}PrimeMeridianType
from komle_witslm_client.bindings.v20._nsgroup import EllipsoidType # {http://www.opengis.net/gml/3.2}EllipsoidType
from komle_witslm_client.bindings.v20._nsgroup import AbstractCoordinateOperationType # {http://www.opengis.net/gml/3.2}AbstractCoordinateOperationType
from komle_witslm_client.bindings.v20._nsgroup import GeodeticCRSType # {http://www.opengis.net/gml/3.2}GeodeticCRSType
from komle_witslm_client.bindings.v20._nsgroup import EllipsoidalCSType # {http://www.opengis.net/gml/3.2}EllipsoidalCSType
from komle_witslm_client.bindings.v20._nsgroup import CartesianCSType # {http://www.opengis.net/gml/3.2}CartesianCSType
from komle_witslm_client.bindings.v20._nsgroup import SphericalCSType # {http://www.opengis.net/gml/3.2}SphericalCSType
from komle_witslm_client.bindings.v20._nsgroup import GeodeticDatumType # {http://www.opengis.net/gml/3.2}GeodeticDatumType
from komle_witslm_client.bindings.v20._nsgroup import AbstractGeneralDerivedCRSType # {http://www.opengis.net/gml/3.2}AbstractGeneralDerivedCRSType
from komle_witslm_client.bindings.v20._nsgroup import AbstractGeneralConversionType # {http://www.opengis.net/gml/3.2}AbstractGeneralConversionType
from komle_witslm_client.bindings.v20._nsgroup import VerticalCRSType # {http://www.opengis.net/gml/3.2}VerticalCRSType
from komle_witslm_client.bindings.v20._nsgroup import VerticalCSType # {http://www.opengis.net/gml/3.2}VerticalCSType
from komle_witslm_client.bindings.v20._nsgroup import VerticalDatumType # {http://www.opengis.net/gml/3.2}VerticalDatumType
from komle_witslm_client.bindings.v20._nsgroup import ProjectedCRSType # {http://www.opengis.net/gml/3.2}ProjectedCRSType
