# Geminitrack, to retrieve an entire Gemini capsule

`geminitrack` is a command-line client to retrieve an entire [Gemini](https://gemini.circumlunar.space/) capsule, for instance to take a backup. It is part of the [Agunua](https://framagit.org/bortzmeyer/agunua/) library.

## Usage

```
geminitrack URL
```

And the files will be downloaded to the current directory, in a subdirectory named from the capsule name. The files will be named from the Gemini URL with some caveats (see later). The program limits itself to URLs which start with the original URL. So, it will never go to another capsule, for instance. By default,`geminitrack` does not modify the files at all, so some internal links may break (for instance links to directories, links with queries, etc) but you know that you get a pristine copy. Use the option `--patch-links` if you prefer to modify the links.

By default, it limits the number of files downloaded and the time spent, mostly to preserve the remote server. *Don't change this behaviour unless you know the remote capsule authorizes it.*

Download is unconditional: whether or not there already exist a file in the destination directory, it will be written over.

Warning: characters in the URL path must be letters, digits and a few others. Everything else will be replaced with underscores.

## Options 

* `--verbose`: makes the download more talkative (default is false)
* `--maximum-files N`: maximum number of files to download (default 20)
* `--directory S`: directory to put the files on (default is current directory)
* `--exclude S`: files to exclude from downloading (a regular expression) (default is none)
* `--maximum-time N`:  maximum number of seconds for the download (default 30)
* `--sleep N`: number of seconds to sleep between two resources (default 1)
* `--patch-links`: adjust the links in the gemtext files so that local reading of stored files will work (default is to leave the files and their links as they are)
* `--gempub`: produces a Gempub (for ebooks) file
* `--raw-directory`: do not add the capsule name (and possibly path) after the storage directory (default is to add them)
* `--secure`: accepts only certificates signed a known Certificate Authority (default is to accept anything)
* `--no-tofu`: do not perform TOFU (Trust On First Use) key checking
* `--accept-expired-certificate`:  expired certificates are not accepted unless you use also this option

## Licence, author, etc

See [the general README of Agunua](README.md).
