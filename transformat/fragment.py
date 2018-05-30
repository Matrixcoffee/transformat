import re

def safe_concat(*args):
	for n, a in enumerate(args):
		if a is None: continue
		return a.append(*args[n+1:])
	return None

class FormattedFragment:
	def __init__(self, content=None):
		self.content = content
		self.next_fragment = None

	def append(self, *fragments):
		last = self
		for fragment in fragments:
			if fragment is None: continue
			while last.next_fragment is not None: last = last.next_fragment
			last.next_fragment = fragment
			last = fragment
		return self

	def _as_html(self, content):
		return content

	def as_html(self):
		if isinstance(self.content, FormattedFragment):
			c = self.content.as_html()
		else:
			c = self.content

		r = self._as_html(c)

		if self.next_fragment is None: return r
		return r + self.next_fragment.as_html()

	def _as_text(self, content, context):
		return content

	def as_text(self, context=None, toplevel=True):
		if context is None: context = []
		if isinstance(self.content, FormattedFragment):
			c = self.content.as_text(context, toplevel=False)
		else:
			c = self.content

		r = self._as_text(c, context)

		if self.next_fragment is None: return r
		r += self.next_fragment.as_text(context, toplevel=False)

		if toplevel and context:
			r += "\n"
			for i, url in enumerate(context):
				r = "{}\n[{}]: {}".format(r, i + 1, url)

		return r

	def _repr(self):
		return "{}({!r})".format(self.__class__.__name__, self.content)

	def __repr__(self):
		r = self._repr()
		if self.next_fragment is None: return r
		return "{} -> {!r}".format(r, self.next_fragment)


class LinkFragment(FormattedFragment):
	def __init__(self, uri, *args, **kwargs):
		#print("args:", repr(args))
		#print("kwargs:", repr(kwargs))
		self.uri = uri
		FormattedFragment.__init__(self, *args, **kwargs)

	def _as_html(self, content):
		if content is None: content = self.uri
		return "<a href=\"{}\">{}</a>".format(self.uri, content)

	def _as_text(self, content, context):
		if content is None:
			content = self.uri
		else:
			if self.uri not in context: context.append(self.uri)
			content = "{}[{}]".format(content, context.index(self.uri) + 1)

		return content

	def _repr(self):
		return "{}({!r}, {!r})".format(self.__class__.__name__, self.uri, self.content)


class MarkupFragment(FormattedFragment):
	TYPES=('bold',   'verbatim', 'italic', 'strikethrough', 'underline', 'code')
	HTML =("strong", "pre",      "em",     "del",           "u",         "code")
	TEXT =("*",      "",         "/",      "+",             "_",         "`"   )

	HTML_MAP = dict(zip(TYPES, HTML))
	TEXT_MAP = dict(zip(TYPES, TEXT))

	def __init__(self, mtype, *args, **kwargs):
		if mtype not in self.TYPES:
			raise KeyError("{!r} is not a valid type of MarkupFragment".format(mtype))
		self.mtype = mtype
		FormattedFragment.__init__(self, *args, **kwargs)

	def _as_html(self, content):
		return "<{0}>{1}</{0}>".format(self.HTML_MAP[self.mtype], content)

	def _as_text(self, content, context):
		return "{0}{1}{0}".format(self.TEXT_MAP[self.mtype], content)

	def _repr(self):
		return "{}({!r}, {!r})".format(self.__class__.__name__, self.mtype, self.content)


class TextFragment(FormattedFragment):
	pass

