package processor;

import java.util.Properties;

import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.Topology;
import org.apache.kafka.streams.kstream.KStream;
import org.deeplearning4j.nn.modelimport.keras.KerasModelImport;
import org.deeplearning4j.nn.multilayer.MultiLayerNetwork;
import org.nd4j.common.io.ClassPathResource;

public class Processor {
    public static String HEART_DISEASE_RAW_TOPIC = "heart-disease-raw";
    // public void startApplication() {
        
    // }

	public static Properties createProperties() {
		Properties props = new Properties();
		props.put(StreamsConfig.APPLICATION_ID_CONFIG, "heart-disease-prediction");
		props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "192.168.1.7:9092");
		props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass());
		props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass());
		return props;
	}

	public static Topology createTopology() throws Exception {
		final StreamsBuilder builder = new StreamsBuilder();
		KStream<String, String> inputEvents = builder.stream(HEART_DISEASE_RAW_TOPIC);
		
        inputEvents.foreach((key, value) -> {
            System.out.println("key: " + key);
            System.out.println("value: " + value);
        });

		// ########################################################
		// Step 1: Load Keras Model using DeepLearning4J API
		// ########################################################
		String simpleMlp = new ClassPathResource("generatedmodels/best_trained_model.h5").getFile().getPath();
		System.out.println(simpleMlp.toString());

		MultiLayerNetwork model = KerasModelImport.importKerasSequentialModelAndWeights(simpleMlp);
		System.out.println(model.toString());

		return builder.build();
	}  
}
