# Stories Guidelines

Stories live as Markdown files in src/jg/coop/web/docs/stories, where each file is just another page within the MkDocs junior.guru website.

## Adding a new story

- The author of the stories, Adéla, typically creates a Google Docs document, and sends a photo of the person as an attachment.
- In Google Docs, go to _Download_, then _Markdown (.md)_.
- Save the file to src/jg/coop/web/docs/stories, filename being the name of the interviewee (all lowercase, without diacritics, and with dashes instead of whitespace).
- Put the photo inside src/jg/coop/images/avatars-participants, again with a filename reflecting the name of the interviewee (all lowercase, without diacritics, and with dashes instead of whitespace)
- Analyze the image and determine the most aesthetically pleasing (and largest) possible looking crop of the image to regular square. Convert the image to JPEG and make sure it has `.jpg` as an extension. Then run `uv run jg tidy` which optimizes all images.
- Look at other existing stories inside the src/jg/coop/web/docs/stories folder and rework the Markdown file so that it fits all the conventions: front matter with configuration, some added markup for navigation, article lead, correct markup of the interview text itself…
- Each question and answer should be separated by double new lines.
- If the interview contains standalone quotes, usually in form of `*„text”*`, use the `blockquote_avatar` to render it properly. See other existing interviews for guidance.
- Fix typos in markup, e.g. double whitespace `  ` after a regular sentence, which should be a single whitespace ` `. Replace `...` with `…`.
