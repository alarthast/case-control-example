from ehrql import create_dataset
from ehrql.tables.core import patients
from variables import (
    first_diagnosis,
    first_programme_attendance,
    programme_attendances,
    is_diabetic,
    resolved_events,
)

dataset = create_dataset()
dataset.define_population(is_diabetic & programme_attendances.exists_for_patient())
dataset.diagnosis_date = first_diagnosis.date.to_first_of_month()
dataset.age = patients.age_on(first_diagnosis.date)
dataset.sex = patients.sex
dataset.case_index_date = first_programme_attendance.date

dataset.resolved_date = (
    resolved_events.sort_by(resolved_events.date).first_for_patient().date
)
dataset.has_resolution_event = resolved_events.where(  # Parallels has_event_in_codelist
    resolved_events.date.is_on_or_after(first_programme_attendance.date)
).exists_for_patient()
