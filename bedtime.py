#!/usr/bin/env python
"""Define XML trees declaratively as functional-style data structures friendly
to programming with functions and recursion.

>>> e = E(u"html", [E(u"head"), E(u"body")])
>>> e
<E: html>
>>> unicode(e)
u'<html><head/><body/></html>'

>>> e2 = E(u"html", {u"xml:lang": "en", u"xmlns": u"http://www.w3.org/1999/xhtml"}, [E(u"head"), E(u"body")])
>>> e2.attrs["xmlns"]
u'http://www.w3.org/1999/xhtml'
>>> unicode(e2)
u'<html xml:lang="en" xmlns="http://www.w3.org/1999/xhtml"><head/><body/></html>'

>>> e3 = E(u"html", [E(u"head", E(u"title", "My home page")), E(u"body", [E(u"h1", u"My home page"), E(u"p", u"Welcome to my home page.")])])
>>> unicode(e3)
u'<html><head><title>My home page</title></head><body><h1>My home page</h1><p>Welcome to my home page.</p></body></html>'

>>> e4 = E("entities", {u"attr": u"\"\" & \"\""}, "<A&B>")
>>> unicode(e4)
u'<entities attr=" &amp; ">&lt;A&amp;B&gt;</entities>'
"""
from xml.etree.cElementTree import fromstring
from xml.sax.saxutils import escape, quoteattr


def dict_from_element(el):
    """Convert a tree of Elements to a Python dictionary. Expects the XML to be
    in literal style and for there to be no duplicate key names.
    
    """
    if isinstance(el, basestring):
        return dict_from_element(fromstring(el))
    elif hasattr(el, "getroot"):
        return dict_from_element(el.getroot())
    elif hasattr(el, "getchildren") and len(el.getchildren()):
        result = {}
        for child in el:
            key = child.tag.split("}")[-1]

            # if the key already exists, place values into a list
            value = dict_from_element(child)
            if key in result:
                if type(result[key]) in (tuple, list):
                    result[key].append(value)
                else:
                    result[key] = [result[key], value]
            else:
                result[key] = value

        return result
    else:
        if hasattr(el, "text"):
            return el.text
        else:
            return u""


class E(object):
    """An XML element."""
    def __init__(self, name, attrs=None, children=None):
        node_types = (E, list, tuple, basestring)

        self.attrs = {}
        self.children = []
        self.name = name
        
        children_in_first_arg = isinstance(attrs, node_types) and \
                attrs is not None and children is None

        if children_in_first_arg:
            self.children = attrs
        else:
            if attrs is not None:
                self.attrs = attrs
            if children is not None:
                self.children = children

        if not isinstance(self.attrs, dict):
            if children is None:
                raise ValueError("Child must be instance of E, basestring, list or tuple")
            else:
                raise ValueError("Attributes must be dictionary")
        if not isinstance(self.children, node_types):
            raise ValueError("Children must be sequence or string")

    def __repr__(self):
        return "<E: %s>" % self.name

    def __unicode__(self):
        if self.children:
            return u"""<%s%s>%s</%s>""" % (self.name, self._attr_str(),
                    self._children_str(), self.name)
        else:
            return u"""<%s%s/>""" % (self.name, self._attr_str())

    def _attr_str(self):
        if self.attrs:
            attr_pairs = (u"%s=%s" % (k, quoteattr(v)) for k, v in
                    self.attrs.iteritems())
            return u" " + u" ".join(attr_pairs)
        else:
            return u""

    def _children_str(self):
        if self.children:
            if isinstance(self.children, (list, tuple)):
                return u"".join((self._encode_child(c) for c in self.children))
            else:
                return self._encode_child(self.children)
        else:
            return u""

    def _encode_child(self, c):
        if isinstance(c, basestring):
            return escape(c)
        else:
            return unicode(c)


if __name__ == "__main__":
    from doctest import testmod
    testmod()
