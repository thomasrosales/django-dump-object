# Dump-Object Command

This package is useful to get from database a set of objects using a simple filter, and save the results into a json file.

## Installation

Into of any app folder copy & paste the folder management/ int he root path.

## Usage
Notice that the --attr-filter and --attr-val are list of values, besides the --attr-filter is the building of the field model and the query filter. For Example: id__exac

```bash
python manage.py dump_object appName.ModelName --attr-filter "pk__lte" --attr-val 30 --no-follow  > result.json
```

## Examples

```bash
python manage.py dump_object appName.ModelName --no-follow --attr-filter "user_id__exact" --attr-val 6817 > result.json
```

```bash
python manage.py dump_object appName.ModelName --attr-filter "unit__slug__exact" --attr-val "value" --no-follow --limit 10 > result.json 
```

```bash
python manage.py dump_object appName.ModelName --no-follow --attr-filter "id__lte" "score__lte" --attr-val 4 70 --limit 2
```

## Results

```json
[
    {
        "model": "appName.ModelName",
        "pk": 1,
        "fields": {
            "created": "2014-12-09",
            "modified": "2014-12-09",
            "user": 18388,
            "rule": 14,
            "score": 49,
            "completed": true,
            "questions_score": 0,
            "rule_check_score": -1,
            "drag_sentences_score": 100,
            "total_time": 35,
            "score_details": {
                "rule_check": "0_of_0",
                "questions": "0_of_0",
                "sentences": "8_of_8"
            },
            "wpm": null,
            "notes": null
        }
    },
    {
        "model": "appName.ModelName",
        "pk": 2,
        "fields": {
            "created": "2014-12-09",
            "modified": "2014-12-09",
            "user": 18388,
            "rule": 3,
            "score": 74,
            "completed": true,
            "questions_score": 75,
            "rule_check_score": -1,
            "drag_sentences_score": -1,
            "total_time": 76,
            "score_details": {
                "rule_check": "0_of_0",
                "questions": "3_of_4",
                "sentences": "0_of_0"
            },
            "wpm": null,
            "notes": null
        }
    },
    {
        "model": "appName.ModelName",
        "pk": 3,
        "fields": {
            "created": "2014-12-08",
            "modified": "2014-12-08",
            "user": 9437,
            "rule": 15,
            "score": 99,
            "completed": true,
            "questions_score": 100,
            "rule_check_score": -1,
            "drag_sentences_score": -1,
            "total_time": 28,
            "score_details": {
                "rule_check": "0_of_0",
                "questions": "4_of_4",
                "sentences": "0_of_0"
            },
            "wpm": null,
            "notes": null
        }
    },
    {
        "model": "appName.ModelName",
        "pk": 4,
        "fields": {
            "created": "2014-12-08",
            "modified": "2014-12-08",
            "user": 9437,
            "rule": 10,
            "score": 99,
            "completed": true,
            "questions_score": 100,
            "rule_check_score": -1,
            "drag_sentences_score": -1,
            "total_time": 28,
            "score_details": {
                "rule_check": "0_of_0",
                "questions": "4_of_4",
                "sentences": "0_of_0"
            },
            "wpm": null,
            "notes": null
        }
    },
    {
        "model": "appName.ModelName",
        "pk": 5,
        "fields": {
            "created": "2014-12-04",
            "modified": "2014-12-04",
            "user": 11402,
            "rule": 9,
            "score": 50,
            "completed": true,
            "questions_score": 0,
            "rule_check_score": 100,
            "drag_sentences_score": -1,
            "total_time": 37,
            "score_details": {
                "rule_check": "10_of_10",
                "questions": "0_of_0",
                "sentences": "0_of_0"
            },
            "wpm": null,
            "notes": null
        }
    }
]
```
