# Emojito

There are many packages that provide shortnames for emojis. This package allows you to provide your own shortnames and with what to replace them.

## Features

- Find and replace shortnames. You provide the shortnames and the content with which to replace them. You can also provide a callable from which you can in stead generate the content.
- Compatible with HTML. In stead of indiscrimnately finding and replacing shortnames anywhere in the text, accidentally replacing content that overlaps with tags, the HTML will be parsed and only the plain text within tags will be affected.

## Example

```py
from emojito import Emojitos


# Define your shortnames and their replacements.
emojitos = Emojitos()
emojitos.add(['one'], '1️⃣')
emojitos.add(['two'], '2️⃣')
emojitos.add(['three'], '3️⃣')


# Provide a text containing your shortnames.
document = """
<h1>This is an example of Emojito</h1>

<ul>
    <li>:one: Number One</li>
    <li>:two: Number Two</li>
    <li>:three: Number Three</li>
</ul>
"""

# Replace all instances of your shortnames in the document.
result = emojitos.replace(document)
```