# ADR 0002: Preserve and evaluate the notebook referral policy

Status: accepted for baseline reproduction; not approved for operational release.

## Decision and reason

Keep the supplied answer model and Section 6 referral rules unchanged. Move the signals and cost calculation into `sec_analyst.policy`, passing the service and operating assumptions explicitly. Evaluate both phrasings of the fixed 151-question benchmark through `python3 -m sec_analyst.evaluate_policy`.

The notebook's `verified` filter means answered, no custom-tag mapping, and no differing candidate values within the selected filing. Restatement is reported but is not a referral condition. Aggregate questions retain the notebook's default flags; they do not receive the same individual-filing checks. Re-running SQL and passing this filter are different checks, and neither establishes that a selected tag has the intended meaning.

## Results and consequences

Development: 126 shown, one wrong. Held-out wording: 115 shown, one wrong. Both wrong verified rows are the same FutureFuel fact under different phrasings, not two independent financial cases. Expected value USD 66,893,000; selected value USD 69,306,000. The C4 requirement of no wrong verified answer currently fails. The evaluation reports this; an automated release gate remains to be built.

Notebook assumptions: 150 questions/week, 20 analyst minutes/question, EUR 70/hour, EUR 2,000/wrong number. The analyst-only baseline costs EUR 3,500/week. Filtered answers cost EUR 2,566/week on development and EUR 2,821/week on held-out wording at observed rates, but EUR 9,865 and EUR 10,107 at the respective one-sided 95% error-rate upper bounds. These are modeled costs excluding infrastructure, assuming analyst responses are correct.

Break-even wrong rate: 1.17%. With zero errors, at least 256 shown answers are needed for the notebook's one-sided bound to reach this threshold. This is not 256 arbitrary questions, and the two phrasings must not be pooled as independent evidence. Current filtered samples contain errors. Cost sensitivity, larger independently reviewed questions, an operational decision and the required head-of-research approval remain C3 work. No approval is claimed.
