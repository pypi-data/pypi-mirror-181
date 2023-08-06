# MkDocs encriptMail Plugin

This [MkDocs](https://www.mkdocs.org) plugin converts markdown encoded email addresses like

```
[Email-Link](mailto:test@test.test)
```

into 

```html
<a href="javascript:linkTo_UnCryptMailto(%27ocknvq,vguvBvguv0vguv%27)">
    Email-Link
</a>
```

or

```
[test@test.test](mailto:test@test.test)
```

into 

```html
<a href="javascript:linkTo_UnCryptMailto(%27ocknvq,vguvBvguv0vguv%27)">
    test(Q)test(P)test
</a>
```

This allows to hide email address from spam bots and allows user to link email addresses.

## Requirements

This package requires Python >=3.5 and MkDocs version 1.0 or higher.  

## Installation

Install the package with pip:

```cmd
pip install mkdocs-encriptmail-plugin
```

Enable the plugin in your `mkdocs.yml`:

```yaml
plugins:
    - search
    - encriptmail:
       placeholderAt: (Q)
       placeholderDot: (P)
```

**Note:** If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set, but now you have to enable it explicitly.

More information about plugins in the [MkDocs documentation](https://www.mkdocs.org/user-guide/plugins/)
