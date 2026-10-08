"""Build index.html, the WordPress-safe embed, from source.html.

Page builders such as Divi's Code module rewrite pasted code: they add <br> and <p>
at line breaks, and can turn && or quote marks into HTML entities. Any of that breaks
an inline script. So index.html is a single line whose only visible code is a tiny
loader that uses no line breaks, quotes, &, < or >. The app's markup, styles and
script travel base64-encoded in data attributes, which builders leave alone.

Usage: python3 build.py
"""
import base64
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent
src = (ROOT / "source.html").read_text(encoding="utf-8")

src = re.sub(r"<!--.*?-->", "", src, flags=re.S)
scripts = re.findall(r"<script>(.*?)</script>", src, flags=re.S)
assert len(scripts) == 1, "source.html must contain exactly one <script>"
markup = re.sub(r"<script>.*?</script>", "", src, flags=re.S).strip()
js = scripts[0].strip()


def b64(text):
    return base64.b64encode(text.encode("utf-8")).decode("ascii")


loader = (
    "(function(){var m=document.getElementById(`asz-mount`);"
    "if(!m||m.getAttribute(`data-asz-ready`))return;"
    "m.setAttribute(`data-asz-ready`,`1`);"
    "function d(b){return new TextDecoder().decode(Uint8Array.from(atob(b),function(c){return c.charCodeAt(0)}))}"
    "m.innerHTML=d(m.getAttribute(`data-asz-html`));"
    "var s=document.createElement(`script`);s.textContent=d(m.getAttribute(`data-asz-js`));"
    "m.removeAttribute(`data-asz-html`);m.removeAttribute(`data-asz-js`);"
    "m.appendChild(s)})();"
)
for ch in "\n\"'&<>":
    assert ch not in loader, f"loader must not contain {ch!r}"

out = (
    '<div id="asz-mount" data-asz-html="' + b64(markup) + '" data-asz-js="' + b64(js) + '"></div>'
    "<script>" + loader + "</script>\n"
)
(ROOT / "index.html").write_text(out, encoding="utf-8")
print(f"index.html written: {len(out) // 1024} KB")
