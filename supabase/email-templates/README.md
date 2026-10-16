# E-mail templates (Supabase → Authentication → Emails → Templates)

| Template in Supabase | Subject | Body (paste the HTML) |
|---|---|---|
| Confirm signup | `Confirm your e-mail – Islamic Learning Games` | `confirm-signup.html` (game sign-ups and a parent's first login) |
| Magic Link | `Your login code – Islamic Learning Games` | `magic-link.html` (parents' login code, `parents/`) |
| Reset password | `Choose a new password – Islamic Learning Games` | `reset-password.html` |

`{{ .ConfirmationURL }}` is filled in by Supabase with the personal link, `{{ .Token }}` with the 6-digit code.
