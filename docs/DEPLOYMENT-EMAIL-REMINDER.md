# Email setup reminder before FTP deployment

Do not treat the current static preview or GitHub Pages site as the final email setup.

## Contact form

- Keep the contact form as a prefilled email draft addressed to `sales@nartech.com.tr`.
- Include the visitor's name, phone number, description, and selected product when present.
- The visitor presses Send in their own email application. The website must not send this message automatically.

## API 2000 calculation report

- The calculation flow should automatically email the generated report to the email address entered by the visitor.
- The sender should be the NarTech mailbox, `sales@nartech.com.tr`.
- The `/api/api2000-report` backend already exists in `server.js`, but the static GitHub Pages/preview host cannot run it. The FTP deployment must include a Node-capable backend or an equivalent server-side endpoint.
- Configure the mail provider's SMTP host, port, TLS setting, authenticated username, app password, and permitted sender address as server-side environment secrets (`SMTP_HOST`, `SMTP_PORT`, `SMTP_SECURE`, `SMTP_USER`, `SMTP_PASS`, `SMTP_FROM`). Set `SMTP_FROM` to the NarTech mailbox if the provider permits it.
- Never put mailbox passwords or FTP credentials in source files, browser code, or this note.
- Before launch, verify the backend can deliver a test calculation report to a controlled recipient and confirm the sender and report content.
