"""The notebook's referral checks and assumed costs, with explicit inputs.

'Verified' is the notebook's screening label, not a guarantee of correctness.
"""

from scipy.stats import beta

from sec_analyst.concepts import CONCEPTS
from sec_analyst.service import RUNGS


def passes_filing_filter(connection, parsed, candidate, flags):
    """Require the issuer's own income statement to support a revenue candidate."""
    if not flags["answered"] or flags["via_mapper"] or not flags["single_candidate"]:
        return False
    if parsed.get("concept") != "Revenue":
        return True
    provenance = candidate.get("provenance")
    if not provenance:
        return False
    filing, tag, date, quarters = provenance[:4]
    # A broad heading such as "Net sales" can support total revenue.
    # A narrower heading such as "Product sales" cannot establish the total.
    lines = connection.execute("""
        SELECT DISTINCT p.tag, n.value
        FROM pre p
        LEFT JOIN num n ON n.adsh = p.adsh AND n.tag = p.tag AND n.version = p.version
            AND n.ddate = ? AND n.qtrs = ? AND n.coreg IS NULL AND n.uom = 'USD'
        WHERE p.adsh = ? AND p.stmt = 'IS' AND p.inpth = 0
          AND regexp_full_match(lower(trim(p.plabel)),
              '(total )?(net )?(operating )?(revenue|revenues|sales)(,? net)?')
    """, [date, quarters, filing]).fetchall()
    return lines == [(tag, candidate["value"])]


def signals(service, question):
    """Look for warning signs without using the reference answer."""
    parsed = service.parser.parse(question)
    answer = service.answer(question, len(RUNGS) - 1)
    flags = {
        "answered": answer["status"] == "answered",
        "via_mapper": False,
        "single_candidate": True,
        "restated": False,
    }
    if not flags["answered"] or parsed["intent"] not in ("point", "fiscal", "quarter"):
        return flags

    accession, tag, date, quarters = answer["provenance"][:4]
    # Remove the final selection so we can inspect the other candidate numbers.
    rows = service.run_sql(answer["sql"].replace(" LIMIT 1", ""))
    different_values = service.run_sql(f"""
        SELECT count(DISTINCT n.value)
        FROM num n JOIN sub s USING (adsh)
        WHERE n.tag = '{tag}' AND s.cik = {parsed['ciks'][0]}
          AND n.ddate = DATE '{date}' AND n.qtrs = {quarters}
          AND n.coreg IS NULL AND n.uom = 'USD'
    """)[0][0]
    flags.update(
        via_mapper=tag not in CONCEPTS[parsed["concept"]][1],
        single_candidate=len({row[0] for row in rows if row[1] == accession}) <= 1,
        restated=different_values > 1,
    )
    return flags


def policy(results, show, questions_per_week, analyst_eur, wrong_number_cost_eur):
    """Calculate the notebook's policy costs from an evaluated answer set."""
    shown_count = int(show.sum())
    wrong_count = int((show & ~results.correct).sum())
    referred_share = (~show).mean()
    wrong_rate = wrong_count / shown_count if shown_count else 0.0
    upper = (
        beta.ppf(0.95, wrong_count + 1, shown_count - wrong_count)
        if shown_count else 0.0
    )

    def weekly_cost(error_rate):
        return questions_per_week * (
            show.mean() * error_rate * wrong_number_cost_eur
            + referred_share * analyst_eur
        )

    return {
        "shown": show.mean(),
        "referred": referred_share,
        "wrong / shown": f"{wrong_count} / {shown_count}",
        "wrong rate": wrong_rate,
        "95% upper": upper,
        "€ per week": weekly_cost(wrong_rate),
        "€ per week at the upper bound": weekly_cost(upper),
    }
