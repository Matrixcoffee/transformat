# Transformat
[Transformat](https://github.com/Matrixcoffee/transformat) is a general purpose
formatted text storage and transformation library.

## Why does it exist?
Transformat was written to give FAQBot rich text capabilities. From FAQBot
there was a need to perform org-mode -> html conversion, and at the second
level (FAQBot's extractors) markdown -> org-mode. However, it is designed to be
re-useable by myself and others.

## What does it do?
Transformat is for everybody who needs to do one or more of the following:
* Parse one or more of the supported formatting languages
* Generate and/or store formatted text in a universal internal representation
* Output formatted text in one or more of the supported formatting languages

This includes safe sanitization (converting from and to the same format), as
none of the origial markup will survive. The input will be fully consumed,
converted to the internal representation, and completely regenerated from
there. (In theory. This is not guaranteed so long as Transformat is still alpha.)

## Supported formats
Transformat understands only a subset of any of these languages, namely the
subset that directly deals with basic formatting. More specifically, it handles
blocks of formatted text, possibly consisting of several paragraphs, and
excluding any document structural elements.

 Anything else will be rejected, mangled or discarded.

### In
* HTML (planned)
* [markdown](https://github.github.com/gfm/) (GFM) (planned)
* [org-mode](https://orgmode.org/)

### Out
* HTML
* text/plain
* org-mode (planned)

### Markup Features
* <font color="red">Co</font><font color="blue">lor</font> (planned)
* **Bold**
* <u>Underline</u>
* _Italics_
* `Code`
* Links
* Paragraphs (planned)
* Ordered lists (planned)
* Unordered lists (planned)

## Status
**Early alpha**. The bare minimum necessary to get FAQBot to output some decent
formatted text.

## Recommended Installation
Just clone the repository somewhere (probably inside or alongside your main
project directory) and add it to your `PYTHONPATH`.

Good Luck!

## License
Copyright 2018 @Coffee:matrix.org

   > Licensed under the Apache License, Version 2.0 (the "License");
   > you may not use this file except in compliance with the License.

   > The full text of the License can be obtained from the file called [LICENSE](LICENSE).

   > Unless required by applicable law or agreed to in writing, software
   > distributed under the License is distributed on an "AS IS" BASIS,
   > WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   > See the License for the specific language governing permissions and
   > limitations under the License.
