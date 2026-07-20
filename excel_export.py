import pandas as pd

import config


def save_records(records: list[dict[str, str]]) -> int:
    dataframe = pd.DataFrame(records, columns=config.OUTPUT_COLUMNS)

    if not dataframe.empty:
        dataframe = dataframe.drop_duplicates(
            subset=["职位ID"],
            keep="first",
        )

    dataframe.to_excel(
        config.OUTPUT_FILE,
        index=False,
        engine="openpyxl",
    )

    return len(dataframe)
