# Interface Design Audit: Student Work Assistant

Basis: the open-source `refactoring-ui` design guidelines ([edisonmbli/refactoring-ui-skill](https://github.com/edisonmbli/refactoring-ui-skill) @ 4459662c, MIT licence). Rule numbers (§) refer to the references in that project.

**Stack**: React + Vite with plain CSS: **no Tailwind**, no component library, no dark mode. The CSS variables inherited from the prototype are the existing design system, so this pass only maps the rules onto those variables: the palette is unchanged, Tailwind is not introduced and no dependency is added.
**How it was checked**: screenshots rendered at widths of 1280 and 375 pixels. Contrast was measured for every text and background pair.

## Conclusion

No P0 issues: all 14 text and background pairs reach 4.5:1, every page has an empty state, and nothing overflows horizontally at a width of 375. The problems are the systemic ones below: spacing, font size, font weight, radius and colour had no scale, and every value was tuned by hand.

## Systemic issues (fixed)

| # | Dimension | Rule | Before | After |
|---|---|---|---|---|
| S1 | Font size | §4.1 | 10 sizes (10/11/12/13/14/17/19/20/22/23px), neighbours only about 8% apart | 5 steps: `--text-xs/sm/base/lg/xl` = 12/14/16/20/24 |
| S2 | Font weight | §2.2.b | 5 weights (400/500/600/650/750) | 2: `--weight-normal` 400 and `--weight-bold` 600 |
| S3 | Spacing | §3.2 §3.2.1 | 14 different gap values, including 7/9/13/15/17/21px | 7 steps `--space-1…7` = 4/8/12/16/24/32/48, each at least 25% from its neighbour |
| S4 | Radius | §1.4.3 | 8 values (4/5/6/7/8/10/12/99px) | Controls 6, containers 12, pills 999 |
| S5 | Colour | §1.5 §5.2.1 | 16 colour values hard-coded outside the variables | All moved into `tokens.css` and named, values unchanged; 2 nearly identical greys merged |
| S6 | Line height | §4.5 | 1.7–1.9 for all small text | Body 1.6, headings 1.25 |

## Local issues (fixed)

| # | Dimension | Level | Where | Rule | Before | After |
|---|---|---|---|---|---|---|
| 1 | Hierarchy | P1 | Mail page status bar | §2.8 | "Refresh mail" and "Smart classification" were both dark primary buttons | Only "Smart classification" stays primary; "Refresh mail" becomes a secondary button |
| 2 | Hierarchy | P1 | Mail cards | §2.4 §8.5.1 | Important mail had a red left border, a pink background and a solid red label at once; 8 cards turned the page red | Important: one dark left line and a dark label; red is kept for account-security notices and date conflicts |
| 3 | Hierarchy | P1 | Mail card and detail | §2.5 | Real mail showed a string of internal IDs, and times appeared in both ISO and local format | Internal IDs only on sample mail; one local time format, with the ISO original in a tooltip |
| 4 | Typography | P1 | Mail detail body | §4.2.3 §4.3 §4.5 | Monospace, unlimited line length, line height 1.85, and the export's "blank line after every line" shown as is | Body font, maximum line length 70ch, line height 1.6. `\r` removed and extra blank lines merged for display only; the stored original and evidence offsets are unchanged |

Files changed: `src/frontend/src/styles/{tokens,prototype,app}.css`, `pages/MailPage.tsx`, `components/MailDetail.tsx`, `api/types.ts`; the backend `providers/mail_readers.py` also normalises line endings during sync.

## Not changed, recorded for later decisions

| # | Dimension | Level | Where | Rule | Now | Suggestion |
|---|---|---|---|---|---|---|
| a | Hierarchy | P2 | Mail stat cards | §2.1 | Academic, career and events show 0 and look as prominent as non-zero cards | Use light grey for zero values, or hide them |
| b | Colour | P2 | "Important" stat card | §2.4 | The number uses danger red, while "important" on the cards is now neutral | Use `--ink` to match the cards |
| c | Hierarchy | P2 | Task rows | §2.4 | The "to check" and "no date" labels are both yellow | Keep the status yellow and make date labels neutral |
| d | Finishing | P2 | Account connections | §8.1 | Granted permissions show as disabled buttons with a ✓, which looks unavailable | Show a "granted" status label instead |

## Re-check

Screenshots retaken at widths of 1280 and 375: only one primary button remains, important and warning are distinct, the original text is readable, and nothing overflows horizontally at 375. All backend tests passed at the time (50), and the frontend type check and build passed.

## Later adjustments (2026-10-20)

- At the user's choice the background became a light blue-grey: `--bg` #EEF2F7, `--soft` #F6F8FB, `--line` #DDE3EC. The light steps share one blue-grey hue so that warm and cool greys are not mixed (§5.5.1); the dark text greys are unchanged.
- Contrast re-measured: grey text is 4.73:1 on the new background and 5.00:1 on the light grey surface, still above the 4.5:1 of §5.6.
- At the user's request every important mail has a red left line again (`.mail-card.important`), without the pink background; the pink background is still used only for account-security notices and date conflicts, so the page does not turn red (§2.4).
