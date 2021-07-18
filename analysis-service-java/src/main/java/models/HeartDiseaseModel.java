package models;

import java.util.Arrays;
import java.util.List;

import org.datavec.api.transform.TransformProcess;
import org.datavec.api.transform.schema.Schema;
import org.datavec.api.util.ndarray.RecordConverter;
import org.datavec.api.writable.Writable;
import org.deeplearning4j.nn.multilayer.MultiLayerNetwork;
import org.nd4j.linalg.api.ndarray.INDArray;

public class HeartDiseaseModel {
    private int age;
    private int sex;
    private int resting_blood_pressure;
    private int fasting_blood_sugar;
    private int max_heart_rate_achieved;
    private int exercise_induced_angina;
    private String chest_pain_type;
    private Double predictResult;

    public HeartDiseaseModel(Builder builder) {
        age = builder.age;
        sex = builder.sex;
        resting_blood_pressure = builder.resting_blood_pressure;
        fasting_blood_sugar = builder.fasting_blood_sugar;
        max_heart_rate_achieved = builder.max_heart_rate_achieved;
        exercise_induced_angina = builder.exercise_induced_angina;
        chest_pain_type = builder.chest_pain_type;
        predictResult = builder.predictResult.getDouble(0);
    }

    public static Builder builder(HeartDiseaseModel cp) {
        Builder builder = new Builder();

        builder.age = cp.age;
        builder.sex = cp.sex;
        builder.resting_blood_pressure = cp.resting_blood_pressure;
        builder.fasting_blood_sugar = cp.fasting_blood_sugar;
        builder.max_heart_rate_achieved =  cp.max_heart_rate_achieved;
        builder.exercise_induced_angina = cp.exercise_induced_angina;
        builder.chest_pain_type = cp.chest_pain_type;

        return builder;
    }

    @Override
    public String toString() {
        return "HeartDisease [{" +
                " age=" + age +
                ", sex=" + sex +
                ", resting_blood_pressure=" + resting_blood_pressure +
                ", fasting_blood_sugar=" + fasting_blood_sugar +
                ", max_heart_rate_achieved=" + max_heart_rate_achieved +
                ", exercise_induced_angina=" + exercise_induced_angina +
                ", chest_pain_type=" + chest_pain_type +
                ", predict_result=" + predictResult +
                " }]";
    }

    public static final class Builder {
        private int age;
        private int sex;
        private int resting_blood_pressure;
        private int fasting_blood_sugar;
        private int max_heart_rate_achieved;
        private int exercise_induced_angina;
        private String chest_pain_type;

        private INDArray predictResult;
        private final Schema schema;

        private Builder() {
            this.schema = new Schema.Builder()
                                .addColumnsInteger("age", "sex")
                                .addColumnsInteger("resting_blood_pressure", "fasting_blood_sugar", "max_heart_rate_achieved", "exercise_induced_angina")
                                .addColumnCategorical("chest_pain_type", "asymptomatic", "atypical_angina", "non_anginal_pain", "typical_angina")
                                .build();
        }

        private TransformProcess transformProcess(Schema schema) {
            TransformProcess transformProcess = new TransformProcess.Builder(schema)
                .categoricalToOneHot("chest_pain_type")
                .build();

            return transformProcess;
        }

        private INDArray preProcessing() {
            List<Writable> record = RecordConverter.toRecord(this.schema,
                                                    Arrays.asList(
                                                        this.age,
                                                        this.sex,
                                                        this.resting_blood_pressure,
                                                        this.fasting_blood_sugar,
                                                        this.max_heart_rate_achieved,
                                                        this.exercise_induced_angina,
                                                        this.chest_pain_type));

            List<Writable> transformed = this.transformProcess(this.schema).execute(record);

            INDArray data = RecordConverter.toArray(transformed);

            return data;
        }

        public Builder predict(MultiLayerNetwork model){
            INDArray vectorIND = this.preProcessing();
            this.predictResult = model.output(vectorIND);

            return this;
        }

        public HeartDiseaseModel build() {
            return new HeartDiseaseModel(this);
        }
    }
}
