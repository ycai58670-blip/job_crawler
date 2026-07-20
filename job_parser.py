from __future__ import annotations

from datetime import datetime
from typing import Any

import config


def normalize_labels(labels: Any) -> str:
    if not isinstance(labels, list):
        return ""

    values = [
        str(item).strip()
        for item in labels
        if str(item).strip()
    ]
    return "、".join(values)


def format_refresh_time(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        return ""

    try:
        parsed_time = datetime.strptime(text, "%Y%m%d%H%M%S")
    except ValueError:
        return text

    return parsed_time.strftime("%Y-%m-%d %H:%M:%S")


def extract_job_record(item: dict[str, Any]) -> dict[str, str]:
    job = item.get("job", {})
    comp = item.get("comp", {})
    recruiter = item.get("recruiter", {})

    if not isinstance(job, dict):
        job = {}
    if not isinstance(comp, dict):
        comp = {}
    if not isinstance(recruiter, dict):
        recruiter = {}

    return {
        "职位ID": str(job.get("jobId", "") or ""),
        "职位名称": str(job.get("title", "") or ""),
        "地点": str(job.get("dq", "") or ""),
        "薪资": str(job.get("salary", "") or ""),
        "学历": normalize_labels(job.get("labels", [])),
        "更新时间": format_refresh_time(job.get("refreshTime")),
        "职位链接": str(job.get("link", "") or ""),
        "公司名称": str(comp.get("compName", "") or ""),
        "公司规模": str(comp.get("compScale", "") or ""),
        "公司行业": str(comp.get("compIndustry", "") or ""),
        "融资阶段": str(comp.get("compStage", "") or ""),
        "招聘人": str(recruiter.get("recruiterName", "") or ""),
    }


def reached_last_page(
    pagination: dict[str, Any],
    requested_page: int,
    job_count: int,
) -> bool:
    try:
        current_page = int(
            pagination.get("currentPage", requested_page)
        )
    except (TypeError, ValueError):
        current_page = requested_page

    try:
        total_page = int(pagination.get("totalPage", 0))
    except (TypeError, ValueError):
        total_page = 0

    has_reached_reported_end = (
        total_page > 0
        and current_page >= total_page - 1
    )
    has_short_last_page = (
        total_page <= 0
        and job_count < config.PAGE_SIZE
    )

    return has_reached_reported_end or has_short_last_page
