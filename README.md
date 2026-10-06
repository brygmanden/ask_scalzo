# Scalzo Chatter Box

A small course companion featuring a caricature of John Scalzo and passages from his interview with Matt Perger.

- Tap John’s shoulder for a quote.
- Ask a question to find a relevant interview passage and timestamp.
- Browse the full source transcript.

## Try it

Open `dist/index.html` in a browser. The prototype runs locally without dependencies or an API key. Alternatively, serve `dist/` with any static web server.

## How it works

`dist/app.js` matches questions against interview topics and returns source passages. It does not generate AI answers. The supplied auto-generated captions may contain transcription errors. Lesson-specific answers require adding the lesson text.

The character illustration was generated from the supplied reference photo. `dist/transcript.json` contains the supplied interview captions; `dist/wisdom.json` contains the extracted topics and quotes. The same wisdom data is embedded in `index.html` so it works when opened locally.

## Course integration

This is a standalone prototype. Integration into the course platform remains to be implemented.
