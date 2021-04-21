package utils.serde;

import java.util.Map;

import org.apache.kafka.common.serialization.Deserializer;
import org.apache.kafka.common.serialization.Serde;
import org.apache.kafka.common.serialization.Serializer;

import models.HeartDiseaseModel;
import utils.serializer.JsonDeserializer;
import utils.serializer.JsonSerializer;

public class StreamsSerdes {

    public static Serde<HeartDiseaseModel> HeartDiseaseSerde() {
        return new HeartDiseaseSerde();
    }    

    public static final class HeartDiseaseSerde extends WrapperSerde<HeartDiseaseModel> {
        public HeartDiseaseSerde(){
            super(new JsonSerializer<>(), new JsonDeserializer<>(HeartDiseaseModel.class));
        }
    }    

    private static class WrapperSerde<T> implements Serde<T> {

        private JsonSerializer<T> serializer;
        private JsonDeserializer<T> deserializer;

        public WrapperSerde(JsonSerializer<T> serializer, JsonDeserializer<T> deserializer) {
            this.serializer = serializer;
            this.deserializer = deserializer;
        }

        @Override
        public void configure(Map<String, ?> map, boolean b) {

        }

        @Override
        public void close() {

        }

        @Override
        public Serializer<T> serializer() {
           return serializer;
        }

        @Override
        public Deserializer<T> deserializer() {
           return deserializer;
        }
    }    
    
}
