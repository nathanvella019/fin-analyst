"""The notebook's TF-IDF custom-tag mapper and evaluation."""

import re

import duckdb
import numpy as np
import pandas as pd
from scipy.stats import beta
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize


STMTS = ["BS", "IS", "CF", "EQ", "CI"]
VARIANTS = {
    "taxonomy names and labels only": ("taxonomy",),
    "other filers' line labels only": ("labels",),
    "both (the baseline mapper)": ("taxonomy", "labels"),
}


def split_camel(tag):
    """Split a tag such as NetIncomeLoss into lowercase words."""
    words = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", tag)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", words).lower()


class TagMapper:
    """Rank standard tags with the notebook's two similarity signals."""

    def __init__(self, connection: duckdb.DuckDBPyConnection, where="TRUE"):
        standard_labels = connection.execute("""
            SELECT tag, any_value(tlabel) AS tlabel
            FROM tag
            WHERE custom = 0
            GROUP BY tag
        """).df().set_index("tag").tlabel

        standard_pairs = connection.execute("""
            SELECT tag, label
            FROM li
            WHERE NOT custom
            GROUP BY tag, label
            ORDER BY tag, label
        """).df().reset_index(names="pid")
        connection.register("mapper_standard_pairs", standard_pairs)
        connection.execute("""
            CREATE OR REPLACE TABLE std_pairs AS
            SELECT * FROM mapper_standard_pairs
        """)
        connection.unregister("mapper_standard_pairs")

        all_tags = pd.Index(sorted(standard_pairs.tag.unique()))
        taxonomy_text = [
            split_camel(tag) + " "
            + str(standard_labels.get(tag, "") or "").lower()
            for tag in all_tags
        ]
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            sublinear_tf=True,
            dtype=np.float32,
        ).fit(list(standard_pairs.label) + taxonomy_text)
        all_label_vectors = normalize(
            self.vectorizer.transform(standard_pairs.label)
        )
        all_taxonomy_vectors = normalize(
            self.vectorizer.transform(taxonomy_text)
        )

        pair_ids = connection.execute(f"""
            SELECT DISTINCT p.pid
            FROM li
            JOIN std_pairs p USING (tag, label)
            WHERE NOT li.custom AND {where}
            ORDER BY 1
        """).df().pid.values
        statement_tags = connection.execute(f"""
            SELECT DISTINCT tag, stmt
            FROM li
            WHERE NOT custom AND {where}
        """).df()

        selected_tags = standard_pairs.tag.values[pair_ids]
        self.classes = pd.Index(sorted(set(selected_tags)))
        class_ids = {tag: index for index, tag in enumerate(self.classes)}
        statement_tags = statement_tags[statement_tags.tag.isin(class_ids)]
        self.on_stmt = np.zeros((len(STMTS), len(self.classes)), bool)
        self.on_stmt[
            statement_tags.stmt.map(STMTS.index).values,
            statement_tags.tag.map(class_ids).values,
        ] = True

        self.label_vectors = all_label_vectors[pair_ids]
        self.taxonomy_vectors = all_taxonomy_vectors[
            all_tags.get_indexer(self.classes)
        ]
        self.pair_cls = pd.Series(selected_tags).map(class_ids).values
        self.n_pairs = len(pair_ids)

    def components(self, ctag, label, stmt):
        custom_text = pd.Series(ctag).map(split_camel) + " " + pd.Series(label)
        taxonomy_scores = (
            normalize(self.vectorizer.transform(custom_text))
            @ self.taxonomy_vectors.T
        ).toarray()
        label_scores = np.zeros_like(taxonomy_scores)
        queries = normalize(self.vectorizer.transform(label))

        for start in range(0, len(label), 100):
            similarities = (
                queries[start:start + 100] @ self.label_vectors.T
            ).tocsr()
            rows = np.repeat(
                np.arange(similarities.shape[0]),
                np.diff(similarities.indptr),
            )
            np.maximum.at(
                label_scores[start:start + 100],
                (rows, self.pair_cls[similarities.indices]),
                similarities.data,
            )

        statement_mask = self.on_stmt[pd.Series(stmt).map(STMTS.index).values]
        return taxonomy_scores, label_scores, statement_mask

    def suggest(self, df, k=5, use=("taxonomy", "labels"), chunk=1000):
        suggestions = []
        score_chunks = []
        for start in range(0, len(df), chunk):
            batch = df.iloc[start:start + chunk]
            taxonomy_scores, label_scores, mask = self.components(
                batch.ctag.values, batch.label.values, batch.stmt.values
            )
            scores = np.where(
                mask,
                ("taxonomy" in use) * taxonomy_scores
                + ("labels" in use) * label_scores,
                -1,
            )
            top = np.argsort(-scores, axis=1)[:, :k]
            suggestions.extend(list(self.classes[row]) for row in top)
            score_chunks.append(np.take_along_axis(scores, top, axis=1))

        return suggestions, np.vstack(score_chunks)


def evaluate(mapper, test, variants=VARIANTS):
    taxonomy_scores, label_scores, mask = mapper.components(
        test.ctag.values, test.label.values, test.stmt.values
    )
    class_ids = {tag: index for index, tag in enumerate(mapper.classes)}
    targets = test.stag.map(class_ids).fillna(-1).values[:, None]
    results = {}
    for name, use in variants.items():
        scores = np.where(
            mask,
            ("taxonomy" in use) * taxonomy_scores
            + ("labels" in use) * label_scores,
            -1,
        )
        top = np.argsort(-scores, axis=1)[:, :5]
        results[name] = {
            "top-1": (top[:, :1] == targets).any(1).mean(),
            "top-5": (top == targets).any(1).mean(),
            "test tags": len(test),
        }
    return pd.DataFrame(results).T


def ci95(successes, total):
    """Return the notebook's 95% Clopper–Pearson interval."""
    lower = beta.ppf(0.025, successes, total - successes + 1) if successes > 0 else 0.0
    upper = beta.ppf(0.975, successes + 1, total - successes) if successes < total else 1.0
    return lower, upper
