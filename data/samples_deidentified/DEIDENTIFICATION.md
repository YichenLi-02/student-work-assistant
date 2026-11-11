# De-identification and Publication Notes

This directory was derived from the data owner's private source package. The original folder/MBOX was not changed and is not included here.

Replaced with fictional content:

- Universities, schools, campus addresses and domains, including Northbridge University, Harbor School of Global Management and Eastfield University. Fictional organisation domains use `*.example`; replacement mail addresses use `example.invalid`.
- Course identifiers and institution-specific term notation, including CS 4310/CS 3120 and changing the original '2025 Fall C' to '2025 Fall'.
- City/state references in time zones. Descriptions use Mountain Standard Time or UTC-7; the original city-based IANA zone became `Etc/GMT+7`, the same fixed UTC-7 offset without daylight saving. Date calculations are unchanged.
- Personal names in placeholders, body text, initials and team/project names, including role placeholders that retained real surnames.

Existing minimised email/link/phone placeholders, product/company names, dates, times, mail structure and annotation meanings were preserved. `date_candidates.jsonl` offsets were recalculated against the changed bodies and checked individually.

Private replacement mappings are not stored here. **De-identification is not anonymity:** content/date combinations can indirectly identify someone. These samples are published with this public repository for demonstration/testing. Review residual risk before republishing or combining datasets. Public availability does not authorise reconstructing identities, contacting people or uploading the original mailbox.

Documentation is English. Source bodies, exact quotes, original reviewer notes and Chinese test inputs retain their original language to preserve evidence and evaluation meaning.
