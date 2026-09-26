# E-mail templates (Supabase → Authentication → Emails → Templates)

| Template in Supabase | Subject | Body (paste the HTML) |
|---|---|---|
| Confirm signup | `Confirm your e-mail – Islamic Learning Games` | `confirm-signup.html` |
| Reset password | `Choose a new password – Islamic Learning Games` | `reset-password.html` |

`{{ .ConfirmationURL }}` is filled in by Supabase with the personal link.
