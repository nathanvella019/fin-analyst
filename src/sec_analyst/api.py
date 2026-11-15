"""Local review API around the unchanged notebook answer model."""

from contextlib import asynccontextmanager
from importlib.metadata import version
import logging
import os
from pathlib import Path
from threading import Lock
import time
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, ConfigDict, Field
import yaml

from sec_analyst.custom_map import prepare_custom_map
from sec_analyst.mapper import TagMapper
from sec_analyst.mapper_data import prepare_line_items
from sec_analyst.monitoring import DASHBOARD, RequestMonitor
from sec_analyst.policy import signals
from sec_analyst.provenance import model_identity
from sec_analyst.service import QuestionService
from sec_analyst.warehouse import connect_warehouse


class Question(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    question: str = Field(min_length=1, max_length=2000, strict=True)


class AnalystRuntime:
    """One connection, one mapper, and serialized access to mutable SQL state."""

    def __init__(self, config_path):
        self.identity = model_identity(config_path)
        settings = yaml.safe_load(Path(config_path).read_text())
        processed = Path(settings["processed_dir"])
        self.connection = connect_warehouse(processed, settings["quarters"])
        self.lock = Lock()
        try:
            prepare_line_items(self.connection, processed)
            self.mapper = TagMapper(self.connection)
            prepare_custom_map(self.connection, [], self.mapper)
            self.service = QuestionService(self.connection)
        except Exception:
            self.connection.close()
            raise

    def ask(self, question):
        with self.lock:
            try:
                parsed = self.service.parser.parse(question)
            except (ValueError, OverflowError):
                raise HTTPException(422, "The question contains an invalid date")
            companies = parsed.get("ciks", []) if parsed["status"] == "ok" else []
            prepare_custom_map(self.connection, companies, self.mapper)
            # The map changes between requests; old SQL results must not survive.
            self.service.run_sql.cache_clear()
            candidate = self.service.answer(question, 4)
            flags = signals(self.service, question)
            screened = flags["answered"] and not flags["via_mapper"] and flags["single_candidate"]
            verification = (
                self.service.verify(candidate["sql"], candidate["value"])
                if flags["answered"] else None
            )
            return {
                "decision": "refer",
                "reason": "Baseline release criterion fails: a wrong answer passes its filter. Human review is required.",
                "answer": None,
                "candidate": candidate,
                "signals": flags,
                "passes_notebook_filter": screened,
                "verification": verification,
                "version": version("fin-analyst"),
                "mode": "review_only",
                "model_identity": self.identity,
            }

    def close(self):
        self.service.run_sql.cache_clear()
        self.connection.close()


def create_app(runtime_factory=None, log_dir=None):
    @asynccontextmanager
    async def lifespan(app):
        factory = runtime_factory or (
            lambda: AnalystRuntime(os.environ.get("FIN_ANALYST_CONFIG", "config/config.yaml"))
        )
        app.state.runtime = factory()
        try:
            app.state.monitor = RequestMonitor(
                log_dir or os.environ.get("FIN_ANALYST_LOG_DIR", "data/logs"),
                getattr(app.state.runtime, "identity", None),
            )
            yield
        finally:
            app.state.runtime.close()

    application = FastAPI(title="Financial Analyst — review API", lifespan=lifespan)

    @application.middleware("http")
    async def record_request(request: Request, call_next):
        if request.method != "POST" or request.url.path != "/ask":
            return await call_next(request)
        started = time.perf_counter()
        request_id = str(uuid4())
        status = 500
        try:
            response = await call_next(request)
            status = response.status_code
            response.headers["X-Request-ID"] = request_id
            return response
        finally:
            application.state.monitor.record(
                status, time.perf_counter() - started,
                getattr(request.state, "question_chars", None),
                getattr(request.state, "answer_result", None),
                request_id,
            )

    @application.get("/metrics")
    def metrics():
        return application.state.monitor.snapshot()

    @application.get("/monitor", response_class=HTMLResponse)
    def monitor():
        return DASHBOARD

    @application.get("/health")
    def health():
        return {"status": "ready", "mode": "review_only", "version": version("fin-analyst")}

    @application.post("/ask")
    def ask(body: Question, request: Request):
        request.state.question_chars = len(body.question)
        started = time.perf_counter()
        result = application.state.runtime.ask(body.question)
        request.state.answer_result = result
        logging.getLogger("uvicorn.error").info(
            "ask version=%s status=%s decision=%s question_chars=%d seconds=%.4f",
            result["version"], result["candidate"]["status"], result["decision"],
            len(body.question), time.perf_counter() - started,
        )
        return result

    return application


app = create_app()
