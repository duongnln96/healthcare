package processor;

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

import models.HeartDiseaseModel;
import utils.serde.StreamsSerdes;

public class Ananlysis {
    public static String HEART_DISEASE_RAW_TOPIC = "heart-disease-raw";

	private static String prediction = "unknown";
	private static INDArray output = null;

	private static Serde<String> keySerde = Serdes.String();
	private static Serde<HeartDiseaseModel> HeartDiseaseSerde = StreamsSerdes.HeartDiseaseSerde();

	public static Properties createProperties() {
		Properties props = new Properties();
		props.put(StreamsConfig.APPLICATION_ID_CONFIG, "heart-disease-prediction");
		props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:29092");
		props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
		return props;
	}

	public static Topology createTopology(MultiLayerNetwork model) {
		final StreamsBuilder builder = new StreamsBuilder();
		KStream<String, HeartDiseaseModel> inputEvents = builder.stream(HEART_DISEASE_RAW_TOPIC, 
																		Consumed.with(keySerde, HeartDiseaseSerde))
				.mapValues(hd -> HeartDiseaseModel.builder(hd).converToINDArray().build());

		// inputEvents.print(Printed.<String, HeartDiseaseModel>toSysOut().withLabel("HeartDiseaseModel"));
		
        inputEvents.foreach((key, value) -> {
			// Apply the analytic model:
			output = model.output(value.getVectorINDArray());
			prediction = output.toString();
		
			System.out.println("Prediction => " + prediction);
        });

		return builder.build();
	}
	
	public static MultiLayerNetwork loadModel() throws Exception {
		String simpleMlp = new ClassPathResource("generatedmodels/trained_model_wo_normalize.h5").getFile().getPath();

		MultiLayerNetwork model = KerasModelImport.importKerasSequentialModelAndWeights(simpleMlp);

		return model;
	}
}
