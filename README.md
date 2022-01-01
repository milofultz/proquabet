# Proquabet

Turn your prose into a constant stream of encrypted and meaningless-sounding five-letter words!

## What?

This will convert a string of text into UTF-8 codes, and then each of those characters into a [proquint][], and vice versa.

*I personally found the original paper kind of difficult to parse, so if that happens for you, try checking my [wiki page on proquints](https://www.tinybrain.fans/proquints.html) to see if that helps, as it is a more step-by-step process/how-to.*

## Usage

Pass in the text via stdin to encode it by default, or use the `-decode`/`--d` flag to decode. e.g.

```bash
echo "Hello World!" | python3 main.py
# hodoj kudos kusob jitoz lanos kibod babap
echo "hodoj kudos kusob jitoz lanos kibod babap" | python3 main.py --d
# Hello World!
```

You can also add the `-punctuation`/`--p` flag to make the encoded output a little more like human-readable text using punctuation and capitalization. This is accounted for automatically on decoding.

```bash
echo "Hello World!" | python3 main.py --punctuation
# Hodoj; kudos kusob jitoz lanos kibod babap?
echo "Hodoj; kudos kusob jitoz lanos kibod babap?" | python3 main.py --d
# Hello World!
```

### Flags

Flag | Effect
--- | ---
`-encode` / `--e` | Encode text into proquints
`-decode` / `--d` | Decode text from proquints
`--punctuation` / `--p` | Make output more human-like, with random punctuation and capitalization.

## Why? 

I was fascinated by [proquints][] when I first saw them in [icco's Go implementation](https://merveilles.town/web/statuses/107505257480989361). I've always been interested in codes and cryptography, so I once I understood how it worked, I figured to drill it further, I should do something silly with it. So here we are, back where we started but with MORE MATH.

[proquint]: https://arxiv.org/html/0901.4016
[proquints]: https://arxiv.org/html/0901.4016