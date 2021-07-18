import random
# random.seed(11)

from dataclasses import dataclass

@dataclass
class HeartDiseaseModel(object):
    '''
    1. (Numeric) Age: Patients Age in years

    2. (Nominal) Sex: Gender of patient (Male - 1, Female - 0)

    3. (Nominal) Chest Pain Type: Type of chest pain experienced by patient categorized into
                1 typical, 2 typical angina, 3 non-anginal pain, 4 asymptomatic

    4. (Numeric) Resting bps: Level of blood pressure at resting mode in mm/HG

    5. (Nominal) Fasting blood sugar: Blood sugar levels on fasting > 120 mg/dl
        represents as 1 in case of true and 0 as false

    6. (Numeric) Max heart rate: Maximum heart rate achieved

    7. (Nominal) Exercise angina: Angina induced by exercise 0 depicting NO 1 depicting Yes

    '''
    age: int
    sex: int
    resting_blood_pressure: int
    fasting_blood_sugar: int
    max_heart_rate_achieved: int
    exercise_induced_angina: int
    chest_pain_type: str


class HeartDiseaseDataGenerator:
    def __init__(self) -> None:
        self._chest_pain_type = ['typical_angina',
                                'atypical_angina',
                                'non_anginal_pain',
                                'asymptomatic']

    def _radom_age(self) -> int:
        return random.randint(25, 75)

    def _random_sex(self) -> int:
        return random.randint(0, 1)

    def _random_chest_pain_type(self) -> str:
        return self._chest_pain_type[random.randint(0, 3)]

    def _random_resting_blood_pressure(self) -> int:
        return random.randint(80, 200)

    def _random_fasting_blood_sugar(self) -> int:
        return random.randint(0, 1)

    def _random_max_heart_rate_achieved(self) -> int:
        return random.randint(50, 220)

    def _random_exercise_induced_angina(self) -> int:
        return random.randint(0, 1)

    def generate(self, number_record: int):
        data_list = []

        for _ in range(number_record):
            data_list.append(HeartDiseaseModel(age=self._radom_age(),
                                            sex=self._random_sex(),
                                            resting_blood_pressure=self._random_resting_blood_pressure(),
                                            fasting_blood_sugar=self._random_fasting_blood_sugar(),
                                            max_heart_rate_achieved=self._random_max_heart_rate_achieved(),
                                            exercise_induced_angina=self._random_exercise_induced_angina(),
                                            chest_pain_type=self._random_chest_pain_type()).__dict__)

        return data_list
