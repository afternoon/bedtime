Define XML trees declaratively as functional-style data structures friendly
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
