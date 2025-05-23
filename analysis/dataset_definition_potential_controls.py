from ehrql import create_dataset
from ehrql.tables.core import patients
from variables import (
    first_diagnosis,
    programme_attendances,
    is_diabetic,
)

dataset = create_dataset()
dataset.define_population(is_diabetic & ~programme_attendances.exists_for_patient())
dataset.diagnosis_date = first_diagnosis.date.to_first_of_month()
dataset.age = patients.age_on(first_diagnosis.date)
dataset.sex = patients.sex
