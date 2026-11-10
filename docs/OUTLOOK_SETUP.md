# Connecting a Real Outlook Mailbox

This guide connects a real Outlook / Microsoft 365 mailbox to the app: read-only mail sync, calendar free/busy, real sending after review and, optionally, writing study blocks to a dedicated study calendar that the app creates in Outlook. It takes about 15 minutes.

> The offline version works fully without any of this. Keep the secrets below only in `.env` on your own computer: do not commit them, screenshot them or post them in a group chat.

## 0. Choose the demo account

| Account | Usable? | Notes |
|---|---|---|
| Personal Outlook.com / Hotmail / Live | **Recommended** | You consent to the permissions yourself when you sign in |
| School account (NUS / Microsoft 365) | Depends on school policy | School tenants usually do not let students authorise third-party apps to read mail and show "admin approval required" (AADSTS90094 / 65001). Do not rely on it for a presentation without IT approval |

Reading Teams chats works only with work or school accounts; personal accounts get mail and calendar only.

## 1. Register the app in Microsoft Entra

1. Open <https://entra.microsoft.com> (or Azure portal → Microsoft Entra ID) and go to **App registrations → New registration**.
   - Registering an app needs an Entra directory. If a personal account cannot get in, a teammate with an existing Azure directory can register it (after that any personal Outlook account can sign in), or you can activate free Azure with a personal account, which creates a "Default Directory".
2. Fill in:
   - **Name**: anything, for example `Student Work Assistant`.
   - **Supported account types**: **"Accounts in any organizational directory and personal Microsoft accounts"**, which matches `MICROSOFT_TENANT_ID=common` in `.env`.
   - **Redirect URI**: platform **Web**, value `http://localhost:8000/api/connections/microsoft/callback`.
     The portal does not accept addresses starting with `http://127.0.0.1`, so `localhost` is used here. After authorisation the app sends you back to `http://127.0.0.1:8000` automatically.
3. On the **Overview** page copy the **Application (client) ID** into `MICROSOFT_CLIENT_ID`.
4. Go to **Certificates & secrets → New client secret** and copy its **Value** right after creating it into `MICROSOFT_CLIENT_SECRET`.
   The value is shown only once. Do not copy the "Secret ID" next to it: that is a GUID and gives AADSTS7000215.
5. Recommended: under **API permissions → Add a permission → Microsoft Graph → Delegated permissions** add `offline_access`, `User.Read`, `Mail.Read` and `Calendars.Read`; add `Mail.Send` only for real sending and `Calendars.ReadWrite` only for writing study blocks to Outlook. Personal accounts do not need "Grant admin consent".

## 2. Fill in `.env` (project root)

```ini
MICROSOFT_CLIENT_ID=<Application (client) ID>
MICROSOFT_TENANT_ID=common
MICROSOFT_CLIENT_SECRET=<client secret value>
MICROSOFT_REDIRECT_URI=http://localhost:8000/api/connections/microsoft/callback
APP_ORIGIN=http://127.0.0.1:8000
```

If your `.env` was copied from an old template, replace the old `MICROSOFT_TENANT_ID=organizations` and the `127.0.0.1` redirect address with the values above.
Restart the server afterwards: double-click `Stop-Local.cmd`, then `Start-Local.cmd`.

## 3. Check the configuration

```powershell
src\backend\.venv\Scripts\python scripts\check-outlook.py
```

The script checks the client ID format, the tenant, whether the secret was mistaken for the Secret ID, the redirect address, and whether the Microsoft sign-in service is reachable. It never prints a secret.

## 4. Connect in the app

1. Open <http://127.0.0.1:8000>, go to **Sources & connections → Account connections** and click **Read mail** on the Microsoft card.
2. Choose the account on the Microsoft sign-in page and consent to the permissions. You return to the app, which shows "Connected · your address".
3. Under **Sync mail (read-only)** choose the time range (last 7 / 14 / 30 days) and the maximum number of mails, then click **Sync now**. Real mail appears on the Mail page and the demo samples are hidden automatically.
4. Optional: click **Read calendar free/busy times**; the Study plan page can then use "Outlook Calendar".
5. Optional, real sending: grant **Send mail** under **Extra write permissions**. Real sending also needs `APP_MODE=live`, `ENABLE_EXTERNAL_WRITES=true` and the real-writes switch in Settings, and every mail must be confirmed on its own in the review screen.
6. Optional, writing to an Outlook study calendar: grant **Dedicated study calendar** under **Extra write permissions** (Microsoft asks for `Calendars.ReadWrite`), click **Create dedicated study calendar** and confirm it in the review screen. Plans made from Outlook free/busy then say "Write to: the app's study calendar in Outlook" in the review screen, and after confirmation the study blocks appear in that calendar.
   - Microsoft has no permission that is limited to "calendars this app created", so this permission can change every calendar. The code only writes to the calendar it created: new events go only to that calendar, and when a block is moved the old one is deleted only from that calendar. Your main calendar and other calendars are never touched. If you would rather not grant it, study blocks can still be written to the Google study calendar.
   - Study blocks are written to the study calendar of the account whose free/busy produced the plan; if that account has no study calendar yet, they go to the other account that has one.

## 5. Verify with the real account

```powershell
src\backend\.venv\Scripts\python scripts\check-outlook.py --live
```

This step is read-only: the script reports the account, the number of inbox mails in the last 30 days, the time of the newest one and the number of events in the next 7 days, and writes them to `local-data/outlook-check.json`. It prints no mail content, sends nothing and writes nothing to the calendar.

## How data is handled

- **What is read**: the inbox only. "Junk Email" and "Deleted Items" are read only when "Include spam/trash" is ticked. Mail is filtered by the chosen time range, and mail already stored is not downloaded again.
- **Minimised before storage**: only the plain-text body is kept (remote images are never loaded); addresses, phone numbers, codes, links and long numbers are replaced with placeholders. Attachments are recorded by name and size only; their content is not downloaded.
- **Tokens**: stored in the Windows Credential Manager; the database only keeps a reference. "Disconnect" deletes the local token. To revoke access on the Microsoft side, use <https://account.live.com/consent/Manage> for personal accounts and <https://myapps.microsoft.com> for school accounts.
- **Sending**: one Graph `sendMail` call sends exactly the recipients, body and attachments that were reviewed, with attachments up to 3 MB in total. A 202 response only means Microsoft accepted the request, not that the mail was delivered.

## Common errors

When a connection fails, the account card shows the error code Microsoft returned and how to fix it.

| Error code | Cause | Fix |
|---|---|---|
| AADSTS50011 | Redirect address does not match | The redirect URI in Entra must be exactly `MICROSOFT_REDIRECT_URI` (including `localhost`, port and path) |
| AADSTS50020 / AADSTS500200 | The app does not accept this kind of account | Change the supported account types to include personal accounts and set `MICROSOFT_TENANT_ID=common` |
| AADSTS50194 | A single-tenant app used `common` | Set `MICROSOFT_TENANT_ID` to the Directory (tenant) ID, or make the app multi-tenant |
| AADSTS700016 | App not found | Wrong client ID, or the app is not in the given tenant |
| AADSTS7000215 | Invalid secret | Use the secret's Value, not the Secret ID; it may also have expired and need replacing |
| AADSTS7000218 | Web app without a secret | Fill in `MICROSOFT_CLIENT_SECRET` in `.env` |
| AADSTS700025 | A public client cannot send a secret | Clear `MICROSOFT_CLIENT_SECRET`, or register the redirect address on the Web platform |
| AADSTS9002327 | Redirect address registered on the SPA platform | Remove it and register it on the **Web** platform |
| AADSTS65001 / 90094 / 90095 | Admin consent required | School tenant restriction; use a personal Outlook account |
| Creating the study calendar fails: a calendar with that name exists | Outlook already has a calendar with the same name (for example one made by hand) | Rename or delete it in Outlook, then click **Create dedicated study calendar** in the app |
| Calendar `calendarView http 403:ErrorAccessDenied` | Older versions asked for `Calendars.ReadBasic`, which Microsoft rejects for reading the calendar of personal Outlook.com accounts | After updating the code, click **Read calendar free/busy times** again on the account card, consent to `Calendars.Read` (still read-only), then run `scripts/check-outlook.py --live` to confirm |

## Known limitations

- Writing to the Outlook study calendar needs `Calendars.ReadWrite`, which is broader than what the app uses (see step 4, point 6); writing only to the app's own calendar is enforced in code.
- If the study calendar is deleted in Outlook, it has to be created again in the app; `scripts/check-outlook.py --live` points this out.
- A sent reply is a new mail with the subject "Re: …"; it is not merged into the original conversation.
- The automated tests (`tests/test_connectors_outlook.py`) use a simulated Graph API, so they only show that the requests and error handling are correct. Whether a real account works is shown by step 5 and by trying it in the app.
