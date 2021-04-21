package models;

import org.nd4j.linalg.api.ndarray.INDArray;
import org.nd4j.linalg.factory.Nd4j;

public class HeartDiseaseModel {
    private int age;
    private int sex;
    private int chest_pain_type;
    private int resting_blood_pressure;
    private int fasting_blood_sugar;
    private int max_heart_rate_achieved;
    private int exercise_induced_angina;
    private INDArray vectorIND; 

    public HeartDiseaseModel(Builder builder) {
        age = builder.age;
        sex = builder.sex;
        chest_pain_type = builder.chest_pain_type;
        resting_blood_pressure = builder.resting_blood_pressure;
        fasting_blood_sugar = builder.fasting_blood_sugar;
        max_heart_rate_achieved = builder.max_heart_rate_achieved;
        exercise_induced_angina = builder.exercise_induced_angina;
        vectorIND = builder.vectorIND;
    }

    public INDArray getVectorINDArray() {
        return this.vectorIND;
    }

    public static Builder builder(HeartDiseaseModel cp) {
        Builder builder = new Builder();

        builder.age = cp.age;
        builder.sex = cp.sex;
        builder.chest_pain_type = cp.chest_pain_type;
        builder.resting_blood_pressure = cp.resting_blood_pressure;
        builder.fasting_blood_sugar = cp.fasting_blood_sugar;
        builder.max_heart_rate_achieved =  cp.max_heart_rate_achieved;
        builder.exercise_induced_angina = cp.exercise_induced_angina;

        return builder;
    }

    @Override
    public String toString() {
        return "HeartDiseaseModel {" +
                "age=" + age +
                ", sex=" + sex +
                ", chest_pain_type=" + chest_pain_type +
                ", resting_blood_pressure=" + resting_blood_pressure +
                ", fasting_blood_sugar=" + fasting_blood_sugar +
                ", max_heart_rate_achieved=" + max_heart_rate_achieved +
                ", exercise_induced_angina=" + exercise_induced_angina +
                ", vectorIND=" + vectorIND +
                "}";
    }

    public static final class Builder {
        private int age;
        private int sex;
        private int chest_pain_type;
        private int resting_blood_pressure;
        private int fasting_blood_sugar;
        private int max_heart_rate_achieved;
        private int exercise_induced_angina;
        private INDArray vectorIND;

        private int vectorXDim = 1;
        private int vectorYDim = 7;

        private Builder() {
        }

        public Builder converToINDArray(){
            float[] vectorInt = new float[]{this.age, this.sex, this.chest_pain_type, 
                                        this.resting_blood_pressure, this.fasting_blood_sugar, 
                                        this.max_heart_rate_achieved, this.exercise_induced_angina};

            this.vectorIND = Nd4j.create(vectorInt, this.vectorXDim, this.vectorYDim);
            return this;
        }        

        public HeartDiseaseModel build() {
            return new HeartDiseaseModel(this);
        }
    }
}
