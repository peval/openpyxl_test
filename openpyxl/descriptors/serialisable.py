from __future__ import absolute_import
# copyright openpyxl 2010-2015

from keyword import kwlist
KEYWORDS = frozenset(kwlist)

from . import _Serialiasable, Sequence
from .namespace import namespaced

from openpyxl.compat import safe_string
from openpyxl.xml.functions import (
    Element,
    localname,
)

seq_types = (list, tuple)

class Serialisable(_Serialiasable):
    """
    Objects can serialise to XML their attributes and child objects.
    The following class attributes are created by the metaclass at runtime:
    __attrs__ = attributes
    __nested__ = single-valued child treated as an attribute
    __elements__ = child elements
    """

    __attrs__ = None
    __nested__ = None
    __elements__ = None
    __namespaced__ = None

    idx_base = 0

    @property
    def tagname(self):
        raise(NotImplementedError)

    namespace = None

    @classmethod
    def from_tree(cls, node):
        """
        Create object from XML
        """
        attrib = dict(node.attrib)
        for key, ns in cls.__namespaced__:
            if ns in attrib:
                attrib[key] = attrib[ns]
                del attrib[ns]
        for el in node:
            tag = localname(el)
            if tag in KEYWORDS:
                tag = "_" + tag
            desc = getattr(cls, tag, None)
            if desc is None:
                continue
            if tag in cls.__nested__:
                if hasattr(desc, 'from_tree'):
                    if isinstance(desc, Sequence):
                        attrib.setdefault(tag, [])
                        attrib[tag].append(desc.from_tree(el))
                    else:
                        attrib[tag] = desc.from_tree(el)
            else:
                if isinstance(desc, property):
                    continue
                elif hasattr(desc.expected_type, "from_tree"):
                    obj = desc.expected_type.from_tree(el)
                else:
                    obj = el.text
                if isinstance(desc, Sequence):
                    if tag not in attrib:
                        attrib[tag] = []
                    attrib[tag].append(obj)
                else:
                    attrib[tag] = obj
        return cls(**attrib)


    def to_tree(self, tagname=None, idx=None, namespace=None):

        if tagname is None:
            tagname = self.tagname

        # keywords have to be masked
        if tagname.startswith("_"):
            tagname = tagname[1:]

        namespace = getattr(self, "namespace", namespace)
        if namespace is not None:
            tagname = "{%s}%s" % (namespace, tagname)

        attrs = dict(self)
        for key, ns in self.__namespaced__:
            if key in attrs:
                attrs[ns] = attrs[key]
                del attrs[key]

        el = Element(tagname, attrs)

        for child in self.__elements__:
            desc = getattr(self.__class__, child, None)
            obj = getattr(self, child)

            if isinstance(obj, seq_types):
                if isinstance(desc, Sequence):
                    desc.idx_base = self.idx_base
                    nodes = (desc.to_tree(child, obj, namespace))
                else:
                    nodes = (v.to_tree(child, namespace) for v in obj)
                for node in nodes:
                    el.append(node)
            else:
                if child in self.__nested__:
                    node = desc.to_tree(child, obj, namespace)
                elif obj is None:
                    continue
                else:
                    node = obj.to_tree(child)
                if node is not None:
                    el.append(node)
        return el


    def __iter__(self):
        for attr in self.__attrs__:
            value = getattr(self, attr)
            if value is not None:
                yield attr, safe_string(value)


    def __eq__(self, other):
        if not dict(self) == dict(other):
            return False
        for el in self.__elements__:
            if getattr(self, el) != getattr(other, el):
                return False
        return True


    def __ne__(self, other):
        return not self == other
