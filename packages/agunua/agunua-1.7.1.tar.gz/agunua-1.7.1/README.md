# Agunua

Agunua is a Python library for the development of Gemini clients.

## Installation

You need Python 3, [netaddr](https://github.com/netaddr/netaddr),
[PySocks](https://github.com/Anorov/PySocks) and [PyOpenSSL](https://www.pyopenssl.org/).  You
can install the dependencies with pip `pip3 install agunua`. 

## Usage

```
import Agunua
...
u = Agunua.GeminiUri(url)
print(u)
```

Parameters in the `GeminiUri()` constructor (you can find their
default values at the beginning of the file `Agunua/__init__.py`):

* `url`: the URL to load
* `insecure`: accept invalid certificates (signed by unknown CA, for
  instance)
* `tofu`: performs TOFU (Trust On First Use) validation. It is a
  string, not a boolean. If empty, we disable TOFU. Otherwise, it is
  the directory of TOFU data.
* `accept_expired`: accept expired certificates (`insecure = True` is
  not sufficient for that)
* `get_content`: retrieve the actual resource (default is to get
  metadata only)
* `parse_content`: if it is gemtext (text/gemini), parse and extract
  links
* `maxlines`: if it is text, maximum number of lines retrieved. Set to
  None if you don't want a limit
* `maxsize`: maximum size in bytes to retrieve. Set to
  None if you don't want a limit
* `binary`: (automatic if the content is text). Retrieve as binary
  content, don't play with end-of-lines
* `follow_redirect`: automatically follow Gemini redirections
* `redirect_depth`: maximum number of redirections followed
* `ignore_missing_tls_close`: ignore the lack of a proper TLS close (may lead to truncation attacks but many Gemini servers don't send it)
* `iri`: handle IRI (URI in Unicode)
* `force_ipv4`: use the IPv4 protocol only
* `force_ipv6`: use the IPv6 protocol only
* `send_sni`: send the TLS Server Name Indication 
* `connect_to`: use the host name in the URI for the Gemini request but
  connect only to this host (name or address). Useful when the host is
  multihomed.
* `clientcert`: the filename of a client certificate that will be sent
  to the server.
* `clientkey`: the filename of the private key of the above
  certificate.
* `use_socks`: use a SOCKS5 proxy (for instance for `.onion`
  capsules). The value must be a tuple (socks proxy name, socks proxy port).

If the URL is invalid (wrong syntax), you won't get a `GeminiUri`
object. If you get one, it does not mean the resource has been
retrieved successfully. See the attribute `network_success` for that,
and then the attribute `status_code` (that you have to interpret
yourself, in most cases).

Attributes of `GeminiUri` objects (not all of them will always be
present; for instance, if you did not ask to get content, you won't
have an attribute `size`; if the status code is not 20 - OK - you
won't get a mediatype; etc):

* `network_success`: resource was retrieved successfully
* `status_code`: if retrieved successfully, the Gemini two-digit
  status code
* `error`: if `network_success` is false, this is the reason
* `ip_address`: IP address used for the retrieval (except is SOCKS was used)
* `meta`: the `meta` field of the Gemini protocol. It depends on the
 status code. Read the Gemini specification for detail.
* `binary`: if you asked for binary access, it will be True. If you
  asked for text access (binary=False in the constructor) and asked to
  ge the content (get_content=True), it will be set to False if
  decoding went well and True if the decoding failed, for instance
  because the file did not match the announced "charset".
* `links`: an array of the links found in the document (if you've set
  `parse_content`)
* `payload`: the content
* `size`: the size of the payload. Since Gemini does not have a way to
  indicate at the beginning the payload size, this will be obtained
  only if `get_content`is true, and it will be limited by the
  parameter `maxsize`
* `mediatype`: the media type (MIME type) of the resource, such as
`text/gemini` or `image/jpeg`
* `lang`: the human language of the resource, as standardized in [BCP 47](https://www.rfc-editor.org/info/bcp47)
* `charset`: actually the encoding of the resource such as UTF-8 or US-ASCII
* `tls_version`: the TLS version, for instance, "TLSv1.3"
* `no_shutdown`: [DEPRECATED See https://framagit.org/bortzmeyer/agunua/-/issues/50] set to True if the server did not properly close the TLS session. It may mean that the content was truncated. Meaningful only with `get_content=True` and if you asked for the whole file.
* `possible_truncation_issue`: set to True if we got a TLS error which may indicate that the data were truncated.
* The rest is related to certificates:
* `issuer`: the CA (Certificate Authority)
* `subject`: the name in the certificate (X.509 calls it "subject")
* `expired`: the certificate has expired
* `cert_not_after`: expiration date
* `cert_not_before`: inception date
* `cert_algo`: algorithm used by the CA
* `cert_key_type`: algorithm of the public key
* `keystring`: the public key
* `cert_key_size`: size of the public key

For an example, see `sample-client.py`. (In the source code, the test suite under `tests/` is also a good way to learn about how to use the library.) Agunua is used in the [Manisha monitoring tool](https://framagit.org/bortzmeyer/manisha/) and in the [Lupa crawler](https://framagit.org/bortzmeyer/lupa/).

### Command-line client

`agunua` is a simple Gemini command-line client, a bit like curl. See
[its documentation](agunua.md). Most parameters of the library
`GeminiUri()` constructor can be set via options. Important: the
default value is not always the same with the command-line tool. For
instance, it defaults to actually retrieving the content.

### Download an entire capsule

Another command-line client, `geminitrack`, allows you to retrieve an entire capsule, for instance for backups. See [its documentation](geminitrack.md).

## Name

Agunua is a melanesian serpent god. Caduceus would have been better
for a Python + Gemini project since there are two snakes on a caduceus
but it was already used.

## License

GPL. See LICENSE.

## Recent changes

See the file CHANGES.

## Authors

Stéphane Bortzmeyer <stephane+framagit@bortzmeyer.org>.

## Reference site

https://framagit.org/bortzmeyer/agunua/ Use the Gitlab issue tracker to
report bugs or wishes. But you can of course also access it with
gemini at gemini://gemini.bortzmeyer.org/software/agunua/

## Other Gemini clients in Python 

* https://tildegit.org/solderpunk/gemini-demo-1 Very simple but working client
* https://github.com/cbrews/ignition Modelled on the `requests` library so very convenient for programmers
* https://git.carcosa.net/jmcbray/gusmobile/ Good code
* https://git.sr.ht/~fkfd/picross 
* https://github.com/apellis/pygemini No longer maintained


