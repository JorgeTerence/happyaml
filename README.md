# HappYAML

[![license](https://img.shields.io/github/license/JorgeTerence/happyaml?color=f7f7f7)](LICENSE)

[![made with care](https://img.shields.io/badge/a%20branch%20of%20-BuscaVest%20-9173e5)](https://github.com/BuscaVest)

It is pronounced like ハッヒºャマル

A pure Python implementation for YAML, converting to `dict` objects.

## About

This was originally part of the [ztau](https://github.com/JorgeTerence/ztau) repo, but I soon realized this should get an approriate place of it's own.

Though the package is still not published, you can use it by copying the `happyaml.py` file into your project and importing it. Yes, it only relies on the standard library.

```py
import happyaml

config = happyaml.parse("~/.config/myapp/myapp.yaml")
print(config["token"])
```

## Roadmap

- [ ] Dict arrays
- [ ] Inline arrays
