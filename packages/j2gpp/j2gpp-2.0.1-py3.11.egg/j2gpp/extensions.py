# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ Project:     j2gpp - Jinja2-based General Purpose Preprocessor            ║
# ║ Author:      Louis Duret-Robert - louisduret@gmail.com                    ║
# ║ Website:     louis-dr.github.io                                           ║
# ║ License:     MIT License                                                  ║
# ║ File:        extensions.py                                                ║
# ╟───────────────────────────────────────────────────────────────────────────╢
# ║ Description: Additional useful extensions.                                ║
# ║                                                                           ║
# ╚═══════════════════════════════════════════════════════════════════════════╝



from jinja2.ext import Extension



class WriteFile(Extension):
  # Set of tags triggering the extension
  tags = set(['write'])

  def __init__(self, environment):
    super().__init__(environment)

    # add the defaults to the environment
    environment.extend(filename="")

  def parse(self, parser):
    # the first token is the token that started the tag.  In our case
    # we only listen to ``'cache'`` so this will be a name token with
    # `cache` as value.  We get the line number so that we can give
    # that line number to the nodes we create by hand.
    lineno = next(parser.stream).lineno

    # now we parse a single expression that is used as cache key.
    args = [parser.parse_expression()]

    # if there is a comma, the user provided a timeout.  If not use
    # None as second parameter.
    if parser.stream.skip_if("comma"):
      args.append(parser.parse_expression())
    else:
      args.append(nodes.Const(None))

    # now we parse the body of the cache block up to `endcache` and
    # drop the needle (which would always be `endcache` in that case)
    body = parser.parse_statements(["name:endwrite"], drop_needle=True)

    # now return a `CallBlock` node that calls our _cache_support
    # helper method on this extension.
    return nodes.CallBlock(
      self.call_method("_cache_support", args), [], [], body
    ).set_lineno(lineno)