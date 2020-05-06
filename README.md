# junior.guru

## Status of the README

This README is missing a lot of information. Honza didn't have time yet to add a proper, nice README. The file currently only includes documentation of the hard parts of the development process, which would be easy to forget and difficult to learn again.

## Setting up email address

According to [spectrum.chat/zeit](https://spectrum.chat/zeit/now/redirection-email-domain~b5e1b613-ae92-42f9-bc49-e8c824a8a7f2?m=MTUzNDE5OTg3MzMwMw==):

1.  Run following:

    ```
    $ now dns add junior.guru '@' MX mx1.improvmx.com 10
    $ now dns add junior.guru '@' MX mx2.improvmx.com 20
    ```
1.  Fill the form at [ImprovMX](https://improvmx.com/)
1.  Setup and verify the address in [MailChimp](https://mailchimp.com/)

## Setting up Google Drive credentials

1.  Follow the steps in the [gspread guide](https://gspread.readthedocs.io/en/latest/oauth2.html). Instead of Google Drive API, enable Google Sheets API.
1.  Save the obtained JSON file into the `juniorguru/fetch` directory as `google_service_account.json`
1.  Make sure it is ignored by Git
1.  Run `cat juniorguru/fetch/google_service_account.json | pbcopy` to copy the JSON into your clipboard (macOS)
1.  Go to CircleCI project settings, page Environment Variables
1.  Add `GOOGLE_SERVICE_ACCOUNT` variable and paste the JSON from your clipboard as a value

## Git hooks

- [isort](https://github.com/timothycrosley/isort/#git-hook)
