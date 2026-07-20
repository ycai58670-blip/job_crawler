from __future__ import annotations

import random
import time

import config
from excel_export import save_records
from job_parser import extract_job_record, reached_last_page
from liepin_api import build_session, fetch_page


def main() -> None:
    if not config.XSRF_TOKEN:
        print(
            "警告：未设置 LIEPIN_XSRF_TOKEN。"
            "若接口验证失败，请从浏览器 Network 请求中复制 Token。"
        )

    session = build_session()
    pass_through = {
        "scene": "input",
        "skId": config.INITIAL_SK_ID,
        "fkId": config.INITIAL_FK_ID,
        "ckId": config.INITIAL_CK_ID,
    }
    all_records: list[dict[str, str]] = []
    seen_job_ids: set[str] = set()

    for page in range(config.MAX_PAGES):
        try:
            job_list, pagination, pass_through = fetch_page(
                session=session,
                keyword=config.KEYWORD,
                page=page,
                pass_through=pass_through,
            )
        except RuntimeError as exc:
            print(f"请求终止：{exc}")
            break

        if not job_list:
            print(f"第 {page} 页没有职位数据，停止翻页。")
            break

        added_count = 0
        for item in job_list:
            record = extract_job_record(item)
            job_id = record["职位ID"].strip()
            if job_id and job_id in seen_job_ids:
                continue
            if job_id:
                seen_job_ids.add(job_id)
            all_records.append(record)
            added_count += 1

        print(
            f"第 {page} 页返回 {len(job_list)} 条，"
            f"新增 {added_count} 条，累计 {len(all_records)} 条"
        )
        if reached_last_page(
            pagination=pagination,
            requested_page=page,
            job_count=len(job_list),
        ):
            print("已到最后一页。")
            break
        wait_seconds = random.uniform(
            config.MIN_SLEEP,
            config.MAX_SLEEP,
        )
        time.sleep(wait_seconds)

    saved_count = save_records(all_records)
    print(f"抓取结束，共保存 {saved_count} 条职位。")
    print(f"Excel 文件：{config.OUTPUT_FILE}")


if __name__ == "__main__":
    main()
