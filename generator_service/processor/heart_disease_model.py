import random
random.seed(11)
import uuid

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
    chest_pain_type: int
    resting_blood_pressure: int
    fasting_blood_sugar: int
    max_heart_rate_achieved: int    
    exercise_induced_angina: int


class HeartDiseaseDataGenerator:
    def __init__(self) -> None:
        self._id = None
        self._age = None
        self._sex = None
        self._chest_pain_type = None
        self._resting_blood_pressure = None
        self._fasting_blood_sugar = None
        self._max_heart_rate_achieved = None
        self._exercise_induced_angina = None

    def _radom_uuid(self):
        self._id = uuid.uuid4().__str__

    def _radom_age(self):
        self._age = random.randint(25, 70)

    def _random_sex(self):
        self._sex = random.randint(0, 1)
    
    def _random_chest_pain_type(self):
        self._chest_pain_type = random.randint(1, 4)

    def _random_resting_blood_pressure(self):
        self._resting_blood_pressure = random.randint(80, 200)

    def _random_fasting_blood_sugar(self):
        self._fasting_blood_sugar = random.randint(0, 1)

    def _random_max_heart_rate_achieved(self):
        self._max_heart_rate_achieved = random.randint(50, 220)

    def _random_exercise_induced_angina(self):
        self._exercise_induced_angina = random.randint(0, 1)

    def generate(self, number_record: int):
        data_list = []

        for _ in range(number_record):
            # self._radom_uuid()
            self._radom_age()
            self._random_sex()
            self._random_chest_pain_type()
            self._random_resting_blood_pressure()
            self._random_fasting_blood_sugar()
            self._random_max_heart_rate_achieved()
            self._random_exercise_induced_angina()
            
            data_list.append(HeartDiseaseModel(age=self._age,
                                                sex=self._sex,
                                                chest_pain_type=self._chest_pain_type,
                                                resting_blood_pressure=self._resting_blood_pressure,
                                                fasting_blood_sugar=self._fasting_blood_sugar,
                                                max_heart_rate_achieved=self._max_heart_rate_achieved,
                                                exercise_induced_angina=self._exercise_induced_angina).__dict__)

        return data_list
