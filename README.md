# NarTech

Static pages are generated from the Word documents in `docs/`.

## Local preview

```sh
npm install
npm start
```

Open `http://localhost:4318`.

## Regenerate pages

Install the Python package in `requirements-build.txt`, then run `npm run build`.

## Email settings

The API 2000 report is sent to the visitor's entered email address. Copy `.env.example` to `.env` and fill in the SMTP settings when the NarTech mailbox is available. `CONTACT_EMAIL` is the destination for contact form submissions. No recipient or mailbox is hardcoded.
