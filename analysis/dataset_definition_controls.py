import datetime

from ehrql import create_dataset
from ehrql.tables.core import patients
from ehrql.query_language import PatientFrame, Series, table_from_file
from variables import (
    first_diagnosis,
    resolved_events,
)

CONTROLS = "output/matched_matches.csv"


@table_from_file(CONTROLS)
class matched_patients(PatientFrame):
    age = Series(int)
    sex = Series(str)
    case_index_date = Series(datetime.date)


dataset = create_dataset()
dataset.define_population(matched_patients.exists_for_patient())
dataset.diagnosis_date = first_diagnosis.date.to_first_of_month()
dataset.age = patients.age_on(first_diagnosis.date)
dataset.sex = patients.sex
dataset.case_index_date = matched_patients.case_index_date

dataset.resolved_date = (
    resolved_events.sort_by(resolved_events.date).first_for_patient().date
)
dataset.has_resolution_event = resolved_events.where(
    resolved_events.date.is_on_or_after(matched_patients.case_index_date)
).exists_for_patient()
