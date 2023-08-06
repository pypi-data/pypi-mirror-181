import json
import os
from typing import Any, Dict, Optional, cast

import opentracing  # type: ignore
from chaoslib.types import Configuration, Experiment, Journal, Secrets
from logzero import logger

from chaosreliably import RELIABLY_HOST, get_session

__all__ = ["after_experiment_control", "before_experiment_control"]


def before_experiment_control(
    context: Experiment,
    exp_id: str,
    org_id: str,
    state: Journal,
    configuration: Configuration = None,
    secrets: Secrets = None,
    **kwargs: Any,
) -> None:
    get_span(org_id, exp_id)
    set_plan_status(org_id, "running", None, configuration, secrets)


def after_experiment_control(
    context: Experiment,
    exp_id: str,
    org_id: str,
    state: Journal,
    configuration: Configuration = None,
    secrets: Secrets = None,
    **kwargs: Any,
) -> None:
    span = get_span(org_id, exp_id)

    try:
        result = complete_run(
            org_id, exp_id, context, state, configuration, secrets
        )

        if result:
            payload = result
            extension = get_reliably_extension_from_journal(state)

            exec_id = payload["id"]

            if span:
                span.set_baggage_item("reliably_execution_id", exec_id)

            host = secrets.get(
                "host", os.getenv("RELIABLY_HOST", RELIABLY_HOST)
            )

            url = f"https://{host}/executions/view/?id={exec_id}&exp={exp_id}"
            extension["execution_url"] = url

            add_runtime_extra(extension)
            set_plan_status(org_id, "completed", None, configuration, secrets)
    except Exception as ex:
        logger.debug(
            f"An error occurred: {ex}, while running the after-experiment "
            "control, the execution won't be affected.",
            exc_info=True,
        )
        if span:
            span.set_baggage_item("reliably_error", str(ex))
        set_plan_status(org_id, "error", str(ex), configuration, secrets)
    finally:
        if span:
            span.set_tag("reliably-control", "finished")


###############################################################################
# Private functions
###############################################################################
def complete_run(
    org_id: str,
    exp_id: str,
    experiment: Experiment,
    state: Journal,
    configuration: Configuration,
    secrets: Secrets,
) -> Optional[Dict[str, Any]]:
    with get_session(configuration, secrets) as session:
        resp = session.post(
            f"/{org_id}/experiments/{exp_id}/executions",
            json={"result": json.dumps(state)},
        )
        logger.debug(f"Response from {resp.url}: {resp.status_code}")
        if resp.status_code == 201:
            return cast(Dict[str, Any], resp.json())
    return None


def get_reliably_extension_from_journal(journal: Journal) -> Dict[str, Any]:
    experiment = journal.get("experiment")
    extensions = experiment.setdefault("extensions", [])
    for extension in extensions:
        if extension["name"] == "reliably":
            return cast(Dict[str, Any], extension)

    extension = {"name": "reliably"}
    extensions.append(extension)
    return cast(Dict[str, Any], extension)


def add_runtime_extra(extension: Dict[str, Any]) -> None:
    extra = os.getenv("RELIABLY_EXECUTION_EXTRA")
    if not extra:
        return

    try:
        extension["extra"] = json.loads(extra)
    except Exception:
        pass


def set_plan_status(
    org_id: str,
    status: str,
    message: Optional[str],
    configuration: Configuration,
    secrets: Secrets,
) -> None:
    plan_id = os.getenv("RELIABLY_PLAN_ID")
    if not plan_id:
        return None

    with get_session(configuration, secrets) as session:
        resp = session.put(
            f"/{org_id}/plans/{plan_id}/status",
            json={"status": status, "error": message},
        )
        logger.debug(f"Response from {resp.url}: {resp.status_code}")


def get_span(org_id: str, experiment_id: str) -> Optional[opentracing.Span]:
    tracer = opentracing.global_tracer()
    scope = tracer.scope_manager.active
    span = scope.span if scope else None
    if not span:
        return None

    span.set_baggage_item("reliably_org_id", org_id)
    span.set_baggage_item("reliably_experiment_id", experiment_id)

    plan_id = os.getenv("RELIABLY_PLAN_ID")
    if plan_id:
        span.set_baggage_item("reliably_plan_id", plan_id)

    return span
