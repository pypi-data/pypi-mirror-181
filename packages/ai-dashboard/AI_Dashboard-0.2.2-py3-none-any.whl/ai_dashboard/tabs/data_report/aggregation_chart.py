from typing import Optional, List, Dict, Any


def aggregation_chart(
    groupby: List[Dict[str, Any]],
    metric: List[Dict[str, Any]],
    chart_type: str = "column",
    title: Optional[str] = None,
    page_size: int = 20,
    show_frequencies: bool = False,
    sentiment_field: str = "",
    sort_direction: str = "desc",
):
    """
    Example for aggregates
    [
        {
            "agg": "category",
            "field": "_cluster_.desc_all-mpnet-base-v2_vector_.kmeans-8",
            "name": "category _cluster_.desc_all-mpnet-base-v2_vector_.kmeans-8",
            "aggType": "groupby",
        },
        {
            "agg": "avg",
            "field": "_sentiment_.desc.cardiffnlp-twitter-roberta-base-sentiment.overall_sentiment_score",
            "name": "avg desc (Sentiment Score)",
            "aggType": "metric",
        },
    ]
    """
    assert sort_direction in {"desc", "asc"}

    for query in groupby:
        query["aggType"] = "groupby"

    for query in metric:
        query["aggType"] = "metric"

    return [
        {
            "type": "appBlock",
            "content": [
                {
                    "type": "datasetAggregation",
                    "attrs": {
                        "uid": "",
                        "title": title,
                        "chartType": chart_type,
                        "filters": [],
                        "xAxis": {
                            "fields": [],
                            "numResults": page_size,
                            "resortAlphanumerically": False,
                        },
                        "yAxis": {
                            "fields": [],
                            "showFrequency": show_frequencies,
                            "sortBy": "",
                            "sortDirection": sort_direction,
                        },
                        "timeseries": {
                            "field": "insert_date_",
                            "interval": "monthly",
                        },
                        "sentiment": {
                            "field": sentiment_field,
                            "mode": "overview",
                            "interval": "monthly",
                        },
                        "wordCloud": {"mode": "cloud"},
                    },
                }
            ],
        },
    ]
