from osmatching import match

match(
    case_csv="dataset_cases",
    match_csv="dataset_potential_controls",
    matches_per_case=3,
    match_variables={
        "sex": "category",
        "age": 5,
        "diagnosis_date": "category",
    },
    index_date_variable="case_index_date",
    replace_match_index_date_with_case="no_offset",
)
