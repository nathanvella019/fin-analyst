# RD1: EU AI Act working classification

Checked 15 November 2026 against official EU sources. This is a reasoned assignment assessment for Nathan to review, not a regulator's determination. No code or tests change.

## Short classification line

**Working tier: non-high-risk company-filings lookup, with transparency requirements where applicable; basis: Article 6 and Annex III 5(b); prospective provider: Nathan if he supplies it under his own name; prospective deployer: the research/credit organisation using it.** [Classification rules](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-6), [Annex III](https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3), [roles](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-3).

## Why this fits our stated use

Our service retrieves company filing figures and shows a source for human review. It does not currently assess an individual's loan eligibility or credit score, or act as a regulated product's safety component. On those stated facts, my working interpretation is that neither Article 6 high-risk route is triggered. This is about intended purpose, not whether a financial error could be costly. [Article 6](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-6).

Annex III 5(b) covers assessment of natural persons' creditworthiness. An individual is a natural person; a company is a different legal subject. A future use involving a sole trader or personal guarantor needs a new assessment. Human review or a disclaimer alone does not settle the Article 6 classification. [Annex III](https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3), [Article 6(3)](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-6).

**Question for counsel before expanding use:** could our lookup become part of assessing a sole trader's or guarantor's creditworthiness, and would Annex III 5(b) apply? If it is only preparatory, do Article 6(3)'s conditions actually hold?

## Who is responsible?

| Role | Meaning for this project |
| --- | --- |
| Provider | The party supplying/putting the system into service under its own name. Nathan would fill this role if he did that; an organisation commissioning and supplying it under its name could instead be the provider. |
| Deployer | The organisation using it under its authority, such as the research firm. It can also be the provider. |
| Today | Nathan is developing and testing the local prototype; there is no claimed live research-desk deployment. The SEC supplies data and Docker supplies runtime technology. Neither becomes this application's provider merely for that reason. |

These role definitions come from [Article 3(3)–(4)](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-3). Article 2(8) excludes pre-market/pre-service development and testing, except real-world testing; it is not a blanket exemption for every student project. [Article 2](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-2).

## Two boundaries to keep clear

- **Does the Act's AI definition apply?** Plain database filtering can fall outside it. Our combined service also fits a TF-IDF mapper; its inference capability needs assessment. The working classification above assumes that the combined service qualifies as AI. We should not claim certainty merely because it uses scikit-learn. [Article 3(1)](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-3), [Commission definition guidance](https://digital-strategy.ec.europa.eu/en/library/commission-publishes-guidelines-ai-system-definition-facilitate-first-ai-acts-rules-application).
- **Non-high-risk does not mean no duties or no danger.** For direct interaction, Article 50(1) requires informing users that they are interacting with AI unless that is obvious in context. For intended external use, make that clear alongside the filing source and review requirement. This note does not claim a complete compliance audit. [Article 50](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-50).

The official Service Desk identifies its text as based on EUR-Lex's consolidated version dated 27 July 2026. [Consolidated legislation](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02024R1689-20260727). This assessment avoids assuming that the original 2024 implementation timetable is still current.

### Wording for the diary

For a prospective company-filings lookup, “minimal risk” is a descriptive working label for the use outside the prohibited and high-risk categories. The application can still involve direct interaction with a person. Article 50(1) requires informing that person of the AI interaction unless it is obvious in context. Article 3(3) and (4) define provider and deployer. Under Article 25(1)(c), if a deployer changes the intended purpose of a system already on the market or in service so that it becomes high-risk, that deployer becomes a provider for that system. Assessing natural persons’ creditworthiness is the relevant boundary in Annex III 5(b). [Article 5](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-5), [Article 6](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-6), [Article 25](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-25), [Article 50](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-50), [Annex III](https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3).
