from __future__ import annotations

import json
import random
import time
import uuid
from typing import Any
from urllib.parse import quote

import requests

import config


def build_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(
        {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Content-Type": "application/json;charset=UTF-8",
            "Origin": "https://www.liepin.com",
            "Referer": "https://www.liepin.com/",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 Chrome/150.0.0.0 "
                "Safari/537.36 Edg/150.0.0.0"
            ),
            "X-Client-Type": "web",
            "X-Fscp-Std-Info": json.dumps(
                {"client_id": "40108"},
                separators=(",", ":"),
            ),
            "X-Fscp-Version": "1.1",
            "X-Requested-With": "XMLHttpRequest",
        }
    )

    if config.XSRF_TOKEN:
        session.headers["X-XSRF-TOKEN"] = config.XSRF_TOKEN

    if config.COOKIE:
        session.headers["Cookie"] = config.COOKIE

    return session


def build_payload(
    keyword: str,
    page: int,
    pass_through: dict[str, str],
) -> dict[str, Any]:
    condition = {
        "city": config.CITY_CODE,
        "dq": config.CITY_CODE,
        "pubTime": "",
        "currentPage": page,
        "pageSize": config.PAGE_SIZE,
        "key": keyword,
        "suggestTag": "",
        "workYearCode": "",
        "compId": "",
        "compName": "",
        "compTag": "",
        "industry": "",
        "salaryCode": "",
        "jobKind": "",
        "compScale": "",
        "compKind": "",
        "compStage": "",
        "eduLevel": "",
        "salaryLow": "",
        "salaryHigh": "",
    }

    return {
        "data": {
            "mainSearchPcConditionForm": condition,
            "passThroughForm": {
                "scene": pass_through.get(
                    "scene",
                    "input" if page == 0 else "condition",
                ),
                "skId": pass_through.get("skId", ""),
                "fkId": pass_through.get("fkId", ""),
                "ckId": pass_through.get("ckId", ""),
            },
        }
    }


def build_request_headers(keyword: str) -> dict[str, str]:
    page_location = (
        "https://www.liepin.com/zhaopin/"
        f"?city={config.CITY_CODE}&key={quote(keyword)}"
    )

    return {
        "X-Fscp-Trace-Id": str(uuid.uuid4()),
        "X-Fscp-Bi-Stat": json.dumps(
            {"location": page_location},
            ensure_ascii=False,
            separators=(",", ":"),
        ),
    }


def fetch_page(
    session: requests.Session,
    keyword: str,
    page: int,
    pass_through: dict[str, str],
) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, str]]:
    payload = build_payload(keyword, page, pass_through)

    for attempt in range(1, config.MAX_RETRY + 1):
        try:
            response = session.post(
                config.API_URL,
                headers=build_request_headers(keyword),
                json=payload,
                timeout=config.REQUEST_TIMEOUT,
            )
            print(
                f"页面={page} | HTTP={response.status_code} | "
                f"尝试={attempt}/{config.MAX_RETRY}"
            )
            response.raise_for_status()
            result = response.json()

            if result.get("flag") != 1:
                result_preview = json.dumps(result, ensure_ascii=False)[:500]
                raise RuntimeError(f"接口业务状态异常：{result_preview}")

            outer_data = result.get("data", {})
            if not isinstance(outer_data, dict):
                outer_data = {}

            business_data = outer_data.get("data", {})
            if not isinstance(business_data, dict):
                business_data = {}

            raw_jobs = business_data.get("jobCardList", [])
            if not isinstance(raw_jobs, list):
                raw_jobs = []
            jobs = [item for item in raw_jobs if isinstance(item, dict)]

            pagination = outer_data.get("pagination", {})
            if not isinstance(pagination, dict):
                pagination = {}

            returned = outer_data.get("passThroughData", {})
            if not isinstance(returned, dict):
                returned = {}

            next_pass_through = {
                key: str(returned.get(key, pass_through.get(key, "")) or "")
                for key in ("skId", "fkId", "ckId")
            }
            next_pass_through["scene"] = str(
                returned.get("scene", "condition") or "condition"
            )

            return jobs, pagination, next_pass_through

        except (requests.RequestException, ValueError, RuntimeError) as exc:
            if attempt >= config.MAX_RETRY:
                raise RuntimeError(
                    f"第 {page} 页请求最终失败：{exc}"
                ) from exc

            wait_seconds = random.uniform(
                config.MIN_SLEEP,
                config.MAX_SLEEP,
            )
            print(f"请求失败：{exc}，{wait_seconds:.1f} 秒后重试")
            time.sleep(wait_seconds)

    return [], {}, pass_through
