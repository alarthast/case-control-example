from ehrql import codelist_from_csv
from ehrql.tables.core import (
    patients,
    clinical_events,
)

start_date = "2022-01-01"
end_date = "2024-12-31"

diabetes_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-dm_cod.csv", column="code"
)
resolved_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-dmres_cod.csv", column="code"
)
programme_attendance_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-ndasepatt_cod.csv",
    column="code",
)

study_period_events = clinical_events.where(
    clinical_events.date.is_on_or_between(start_date, end_date)
)
diagnosis_events = study_period_events.where(
    study_period_events.snomedct_code.is_in(diabetes_codes)
)
programme_attendances = study_period_events.where(
    study_period_events.snomedct_code.is_in(programme_attendance_codes)
)
resolved_events = clinical_events.where(  # Parallels events_in_codelist
    clinical_events.snomedct_code.is_in(resolved_codes)
)

was_alive = patients.date_of_death.is_null() | (patients.date_of_death < start_date)
is_diabetic = was_alive & diagnosis_events.exists_for_patient()

first_diagnosis = diagnosis_events.sort_by(study_period_events.date).first_for_patient()
first_programme_attendance = programme_attendances.sort_by(
    study_period_events.date
).first_for_patient()
