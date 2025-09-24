# junior.guru (aka coop) 🐣

The junior.guru website, Discord bot, and synchronization scripts.

## Status of the README

This README is missing a lot of information. Honza didn't have time yet to add a proper, nice README. The file currently only includes documentation of the hard parts of the development process, which would be easy to forget and difficult to learn again.

## Contributions

Contributions are welcome, but Honza didn't have much time yet to make the repo very friendly to contributors.

## Installation on macOS M1

This is needed for decrypting backups:

```
$ brew install gpg
```

## Screenshotting

```
$ playwright install
```

## Logging

Use `export LOG_LEVEL='debug'` to see DEBUG logging, by default logging is set to INFO and for some selected 'muted' loggers it's set to WARNING only. The setup is in `loggers.py`.

Sensitive information should always go to DEBUG. The CI is set to log only INFO. If shit hits the fan and the error in hand isn't reproducible locally, for a few builds even CI could be set to DEBUG, so don't put anything _actually sensitive_ to the logs!

## Setting up email address

1.  Add the following to the DNS:

    ```
    junior.guru '@' MX mx1.improvmx.com 10
    junior.guru '@' MX mx2.improvmx.com 20
    junior.guru '@' TXT 'v=spf1 include:spf.improvmx.com include:_spf.google.com ~all'
    ```

1.  Fill the form at [ImprovMX](https://improvmx.com/)

## Setting up Google Drive credentials

1.  Follow the steps in the [gspread guide](https://gspread.readthedocs.io/en/latest/oauth2.html). Instead of Google Drive API, enable Google Sheets API.
1.  Save the obtained JSON file to the project directory as `google_service_account.json`
1.  Make sure it is ignored by Git
1.  Run `cat google_service_account.json | pbcopy` to copy the JSON into your clipboard (macOS)
1.  Go to CircleCI project settings, page Environment Variables
1.  Add `GOOGLE_SERVICE_ACCOUNT` variable and paste the JSON from your clipboard as a value

The service account's email address needs to be manually invited wherever it should have access. If it should be able to access Google Analytics, go there and invite it as if it was a user.

## Setting up logo.junior.guru and podcast.junior.guru

The [logo.junior.guru](https://logo.junior.guru/) and [podcast.junior.guru](https://podcast.junior.guru/) have their own repos and run on GitHub Pages. Set it up in DNS:

```
logo.junior.guru '@' CNAME 'juniorguru.github.io'
podcast.junior.guru '@' CNAME 'juniorguru.github.io'
```

## Verify Google Search Console

In [Google Search Console](https://support.google.com/webmasters/answer/9008080?hl=en) click verify and set a TXT DNS record.
