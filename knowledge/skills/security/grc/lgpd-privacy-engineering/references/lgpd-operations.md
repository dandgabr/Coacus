# LGPD assessment and operational handoffs

Resolve the controlling text in the [Brazilian LGPD source register](brazilian-lgpd-sources.md).
For each conclusion, record the jurisdiction, activity ID, rule, supporting
evidence, outstanding facts, decision owner and review date.

## Map, decide and document

For each purpose, trace entry points, fields and inferences to stores, proxies,
SDKs, processors and deletion paths. Distinguish client activity from server
forwarding and contract statements from observed settings. Compare proposed
purposes against the actual flow. Determine controller or processor roles per
activity, including when the same company acts in different roles for separate
purposes. Verify controller designation of a data protection officer, any
applicable exemption, and the contact channel. Check the small-agent definition,
group and revenue exclusions, high-risk criteria and any specific ANPD decision
before relying on flexible treatment. Record evidence for each condition.

For ordinary data and sensitive data, check LGPD Articles 7 and 11 separately.
Use legitimate interest only for eligible ordinary data under Article 7. Document
the concrete interest, reasonable expectations, less intrusive alternatives,
impact on people and safeguards. If the balance is unsupported, change the
processing or evaluate another applicable basis. When children or adolescents
are involved, document the prevailing best interests and applicable Article 14
safeguards before proceeding.

Determine the reason for an impact assessment. Record an ANPD request, another
applicable legal requirement, high-risk treatment analysis or a preventive
assessment as appropriate. Under Resolution 2/2022 Article 4, the test combines
one general factor (large scale or significant effects on fundamental interests
or rights) with one specific factor (emerging technology, public-area
monitoring, solely automated decisions, or the specified sensitive or
age-related data). Evaluate scale on the facts. Record reasonably foreseeable
harms, controls, proof of effectiveness and residual risk. For AI, consider
inference, unfair decisions, vendor reuse of inputs, inaccurate personal data
and cross-tenant exposure where relevant.

### Canonical templates

Use these paths from the Coacus checkout. A standalone skill install includes
this procedure. Open the corresponding files from the Coacus repository when
the checkout is unavailable.

| Output | Coacus repository path | Published source |
| --- | --- | --- |
| Personal data inventory | `templates/domains/architecture_si/personal-data-map.template.md` | [Personal data map](https://github.com/dandgabr/Coacus/blob/main/templates/domains/architecture_si/personal-data-map.template.md) |
| Processing record | `templates/domains/architecture_si/ropa.template.md` | [ROPA](https://github.com/dandgabr/Coacus/blob/main/templates/domains/architecture_si/ropa.template.md) |
| Legitimate interest assessment | `templates/domains/architecture_si/legitimate-interest-assessment.template.md` | [LIA](https://github.com/dandgabr/Coacus/blob/main/templates/domains/architecture_si/legitimate-interest-assessment.template.md) |
| Data protection impact assessment | `templates/domains/architecture_si/dpia-privacy.template.md` | [DPIA and RIPD](https://github.com/dandgabr/Coacus/blob/main/templates/domains/architecture_si/dpia-privacy.template.md) |

### Public privacy notice draft

Derive the notice from reviewed activity IDs. Cover specific purposes, form
and duration of processing, controller identity and contact, shared use and
its purpose, agent responsibilities, and the applicable rights with an
accessible request channel (Article 9). Add the data protection officer or
eligible privacy channel, relevant transfer disclosures, cookies and audience
safeguards where applicable. Mark unknowns for review. Keep internal evidence
and personal data out of the public draft. Record the authorized review and
the published version when the project owner supplies it.

## Data subject requests and retention

Record request channel, receipt, right requested, applicable regime and due
date. For confirmation or access under LGPD Article 19, the ordinary simplified
response is immediate and a complete statement is due within 15 days from the
request. For eligible small agents, Resolution 2/2022 Article 15 allows up to
15 days for the simplified statement and Article 14(III) doubles the complete
statement period to 30 days. Assess each other right under its applicable
rules. Internal service targets can be stricter.

Provide an intake for authorized representatives, people without an active
account, and requests received by support. Verify identity and authority in
proportion to the disclosure or action. Track related processors and the
Article 18(6) communication duty and exceptions. Record the disposition and
the information communicated where fulfillment is partial or unavailable.

Maintain a schedule with an activity ID, data class, trigger, retention period,
specific basis, stores, responsible team and deletion or restriction method.
Check applicable Article 16 grounds for exceptions after the end of processing.
For a restore, reapply pending erasure or restriction before previously erased
data is exposed. Validate outcomes in live stores, replicas, derived stores and
processors and document backup expiration and evidence. Apply Marco Civil log
retention only to qualifying providers and categories. Protect subject-linked
audit records as potentially personal data.

## Suppliers, contracts and transfers

For each flow, record the exporter and importer, roles, purpose, data class,
destination, remote support access, onward recipients, evidence source and
review date. Verify whether the operation is an international transfer. Collection directly from an individual by a foreign processing agent does not
in itself establish an exporter-to-importer transfer under Resolution 19/2024
Articles 5–6. Check LGPD scope on its
own. Confirm a valid processing basis and a separate transfer mechanism.
Check the current adequacy decision for the actual recipient and purpose.
Evaluate any onward transfer or foreign support access by the relevant actors,
even where the primary recipient is covered by an adequacy decision.

For the contract review, gather per-role instructions or purposes, data and
retention scope, subcontracting, security controls, notice timing, assistance
with rights, audit evidence, deletion or return, and change/escalation paths.
Treat this as a contractual checklist. Confirm the executed instrument and
dates with the owner. If Brazilian standard clauses are selected, use the
official Resolution 19/2024 Annex II terms, preserve the prescribed wording
and record the completed instrument.
Provide the applicable transfer transparency information in Portuguese under
the regulation.

## Security incident

Open an internal timeline and escalate immediately to the incident owner.
Record occurrence, discovery, when the controller knew that personal data
were affected, the source of that knowledge, and the timezone. Preserve
evidence through the approved incident process. A processor informs the
controller without undue delay and supplies relevant facts. Reassess missing
facts as they become available and record changes to the decision.

Apply Resolution 15/2024 Articles 4–5. Assess significant effects on fundamental
interests or rights together with at least one listed category: sensitive data,
children's, adolescents' or older people's data, financial data, authentication
data, legally protected confidential data, or large-scale data. Record the
controller's reason to communicate or its documented reasons for a different
decision. Check specific legislation and small-agent eligibility.

| Record | Default and evidence |
| --- | --- |
| ANPD notification | Three business days from controller knowledge that personal data were affected, subject to a specific legal deadline. Prepare the Article 6(2) facts, counts, timeline, measures, possible harm, mitigations, delay explanation when applicable, parties and representative evidence. Record the official form or filing receipt. |
| Supplemental ANPD notification | Document the reason for an incomplete initial filing. Article 6(3) allows 20 business days from the communication to supplement it. Record the protocol and missing information. |
| Affected-person communication | Three business days from the same knowledge trigger. Draft in plain language with the nature and category of data, protective measures, risks, mitigation, dates, delay reason if relevant and help contact. Use direct individual notice where possible. Where direct notice is unavailable, check Article 9(3) for the public fallback and its minimum three-month visibility. Under Article 9(4), record the declaration of the means used, due within three business days after the initial notice period ends. |
| Eligible small agent | Articles 6(8) and 9(6) double the stated initial communication periods, and Article 6(8) also doubles the ANPD supplement period. Record eligibility and check applicable specific legislation. |
| Controller's incident record | Keep communicated and uncommunicated incidents for at least five years from recording, subject to longer applicable obligations and the Article 10(2) public-sector archival exception. Keep this schedule separate from ordinary request logs. |

Use a shared incident ID to keep the two draft audiences and their receipts
aligned. Fill the current official form from the regulator draft.

- **Regulator draft** — [Incident ID and filing status], [controller, operator
  and representative], [occurrence and knowledge times], [data categories,
  affected and total activity counts], [security measures before and after],
  [impact and mitigation], [cause and scope], [missing facts and delay reason],
  [supplement owner and due date], [submission reference].
- **Affected-person draft** — [What happened and when we became aware], [your
  affected data and potential impact], [steps we took and what you can do],
  [reason for delay if applicable], [contact], [delivery channel and date].
  Record the proof declaration separately.

Keep communications at draft status until the authorized controller or
representative acts. For content-related reporting under the Digital ECA,
consult `brazil-eca-digital` for the distinct route and clocks.
