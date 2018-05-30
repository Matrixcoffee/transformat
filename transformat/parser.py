# https://orgmode.org/worg/dev/org-syntax.html

import re

import transformat.fragment as fragment

class OrgElementParser:
	RE_LINK = None
	RE_MARKUP = None
	MAP_MARKER = {	"*": 'bold',
			"=": 'verbatim',
			"/": 'italic',
			"+": 'strikethrough',
			"_": 'underline',
			"~": 'code'}

	@classmethod
	def setup_class(klass):
		PRE = "^|\\s|[({'\"]"
		MARKER = "[*=/+_~]"
		BORDER = "[^\\s,'\"]"
		POST = "[-\\s.,:!?'\")}]|$"
		BODY = "[^\\n]*?(?:\\n[^\\n]*?){0,3}"
		CONTENTS = "(?:" + BORDER + BODY + ")?" + BORDER

		klass.RE_LINK = re.compile("(^[^[]*)\\[\\[([^]]+)(?:\\]\\[([^]]+))?\\]\\](.*$)")
		klass.RE_MARKUP = re.compile("(^.*?(?:" + PRE + "))(" + MARKER + ")(" + CONTENTS + ")\\2((?:" + POST + ").*$)")

	@classmethod
	def parse(klass, text):
		m = klass.RE_LINK.search(text)
		if not m: return klass.parse_nolink(text)
		print("parse:", repr(m.groups()))

		f = klass.parse_nolink(m.group(1))
		c = klass.parse_nolink(m.group(3))
		n = klass.parse(m.group(4))
		l = fragment.LinkFragment(m.group(2), c)

		return fragment.safe_concat(f, l, n)

	@classmethod
	def parse_nolink(klass, text):
		if text is None: return None
		if text == "": return None
		m = klass.RE_MARKUP.search(text)
		if m is None: return fragment.TextFragment(text)
		print("parse_nolink:", repr(m.groups()))

		f = klass.parse_nolink(m.group(1))
		c = klass.parse_nolink(m.group(3))
		n = klass.parse_nolink(m.group(4))
		m = fragment.MarkupFragment(klass.MAP_MARKER[m.group(2)], c)

		return fragment.safe_concat(f, m, n)

OrgElementParser.setup_class()


def main():
	tst = [	"Text with [[https://undecorated/link]] for testing.",
		"Text *with _underline_ and* bold.",
		"Have /a/ [[https://link][Link *with /italics/ and* bold]] and _maybe some =other=_ stuff.",
		"=update users set admin = 1 where name = '<matrix ID here>';="
	]

	while True:
		if tst:
			l = tst.pop(0)
		else:
			print("Enter string: ", end='')
			l = input()

		s = l.strip()
		if s == "": break

		f = OrgElementParser.parse(s)
		print(repr(f))
		print(f.as_html())
		print(f.as_text())

if __name__ == '__main__':
	main()
