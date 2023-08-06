# agunua command-line client 

`agunua` is a simple [Gemini](https://gemini.circumlunar.space/) command-line client, a bit like
curl or wget.

## Usage 

You can just call:

```
agunua YOUR-URL
```

And you will get the URL content. 

## Options

* `--maximum-time`: maximum time in seconds before giving in if the
  server does not respond
* `--secure`: checks the certificate
* `--no-tofu`: do not perform TOFU (Trust On First Use) validation
* `--accept-expired-certificate`: expired certificates are not
  accepted unless you use also this option
* `--ignore-missing-tls-close`: by default, servers which "forget" to send a TLS close before shutting down the connection are rejected
* `--no-sni`: do not send TLS Server Name Indication
* `--not-follow-redirect`: by default, the tool follows Gemini
  redirections but you can use this option to avoid it
* `--verbose`: more talkative
* `--display-links`: instead of displaying the content, display the
  links it contains
* `--maxlines`: maximum number of lines to retrieve (for text
  files). Set to 0 for "no limit"
* `--maxsize`: maximum amount of bytes to retrieve. Set to 0 for "no limit"
* `--connect-to`: connect to this specific host (name or IP address)
  not to the one mentioned in the URL
* `--socks`: connect through this SOCKS proxy, expressed as host:port
* `--certificate`: loads a client certificate which will be sent to
  the server
* `--key`: loads the private key for the above certificate
* `--binary`: even if this is a text file, download as binary
* `--force-ipv4`: use only the IPv4 protocol
* `--force-ipv6`: use only the IPv6 protocol

## Licence, author, etc

See [the general README of Agunua](README.md).
