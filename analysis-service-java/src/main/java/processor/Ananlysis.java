package processor;

import java.util.Arrays;
import java.util.Properties;

import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.common.serialization.Serde;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.Topology;
import org.apache.kafka.streams.kstream.Consumed;
import org.apache.kafka.streams.kstream.KStream;
import org.deeplearning4j.nn.modelimport.keras.KerasModelImport;
import org.deeplearning4j.nn.multilayer.MultiLayerNetwork;
import org.nd4j.common.io.ClassPathResource;
import org.nd4j.linalg.api.ndarray.INDArray;
import org.nd4j.linalg.factory.Nd4j;

public class Ananlysis {
    public static String HEART_DISEASE_RAW_TOPIC = "heart-disease-raw";

	private static String prediction = "unknown";
	private static INDArray output = null;

	private static Serde<String> keySerde = Serdes.String();
	private static Serde<String> valSerde = Serdes.String();

	public static Properties createProperties() {
		Properties props = new Properties();
		props.put(StreamsConfig.APPLICATION_ID_CONFIG, "heart-disease-prediction");
		props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:29092");
		props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
		return props;
	}

	public static Topology createTopology() {
		final StreamsBuilder builder = new StreamsBuilder();
		KStream<String, String> inputEvents = builder.stream(HEART_DISEASE_RAW_TOPIC, Consumed.with(keySerde, valSerde));
		
        inputEvents.foreach((key, value) -> {
            System.out.println("key: " + key);
            System.out.println("value: " + value);
        });

		return builder.build();
	}
	
	public MultiLayerNetwork loadModel() throws Exception {
		// ########################################################
		// Step 1: Load Keras Model using DeepLearning4J API
		// ########################################################
		String simpleMlp = new ClassPathResource("generatedmodels/trained_model_wo_normalize.h5").getFile().getPath();
		System.out.println(simpleMlp.toString());

		MultiLayerNetwork model = KerasModelImport.importKerasSequentialModelAndWeights(simpleMlp);

		float[] vectorFloat = new float[]{65, 1, 4, 155, 0, 154, 0};
        INDArray rowVector = Nd4j.create(vectorFloat, 1, 7);
        System.out.println("rowVector:              " + rowVector);
        System.out.println("rowVector.shape():      " + Arrays.toString(rowVector.shape()));

		// Apply the analytic model:
		output = model.output(rowVector);
		prediction = output.toString();
		
		System.out.println("Prediction => " + prediction);

		return model;
	}
}
