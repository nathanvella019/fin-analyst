# 0013 — Check the income statement before marking a revenue figure verified

The given answer engine can select sales of goods when the analyst asked for total revenue. Repeating the SQL confirms the number on the selected line. It cannot tell us whether the company calls that line its total. C3 asks us to own the referral rules. C4 requires zero wrong verified answers.

Keep the supplied parser, SQL, mapper, benchmark and candidate numbers. Apply the notebook checks first. For revenue, require exactly one distinct tag and value under a recognised total-revenue or sales heading on the cited primary income statement. Match the candidate's filing, date, duration, USD unit and main reporting entity. Send missing, unsupported or ambiguous cases for review. The written headings deliberately cover common English labels. Other wording can send a correct answer to review.

CI scores the policy and reports the notebook result alongside it. The API exposes both filter decisions and keeps analyst approval for every figure. The check uses filing data available at request time. The scored questions helped motivate this policy, and the benchmark also uses statement labels to define total revenue. This is regression evidence. Independent review of new cases is still needed before automatic release.

The alternative of referring every revenue question caught the same known error but sent many more correct figures for review. Adjusting a mapper threshold would leave an incorrect selection between standard tags untouched. [Policy comparison](../evidence/rd2/task-3-measurement.md#what-if-an-analyst-reviewed-every-revenue-question) · [Mapper threshold decision](0012-forward-mapper-gate.md)
