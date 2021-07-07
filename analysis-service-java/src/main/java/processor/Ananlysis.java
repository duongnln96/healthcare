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
import org.apache.kafka.streams.kstream.Printed;
import org.apache.kafka.streams.kstream.Produced;
import org.deeplearning4j.nn.modelimport.keras.KerasModelImport;
import org.deeplearning4j.nn.multilayer.MultiLayerNetwork;
import org.nd4j.common.io.ClassPathResource;

import models.HeartDiseaseModel;
import utils.serde.StreamsSerdes;

public class Ananlysis {
    public static final String HEART_DISEASE_IN_TOPIC = "heart-disease-raw";
	public static final String HEART_DISEASE_OUT_TOPIC = "heart-disease-out";

	private static Serde<String> keySerde = Serdes.String();
	private static Serde<HeartDiseaseModel> HeartDiseaseSerde = StreamsSerdes.HeartDiseaseSerde();

	public static Properties createProperties() {
		Properties props = new Properties();
		props.put(StreamsConfig.APPLICATION_ID_CONFIG, "heart-disease-app-id");
		props.put(StreamsConfig.CLIENT_ID_CONFIG, "heart-disease-client-id");
		props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
		props.put(StreamsConfig.METRICS_RECORDING_LEVEL_CONFIG, "DEBUG");
		props.put(StreamsConfig.NUM_STREAM_THREADS_CONFIG, "1");
		// props.put(StreamsConfig.BUFFERED_RECORDS_PER_PARTITION_CONFIG, "1500");
		props.put(ConsumerConfig.GROUP_ID_CONFIG, "heart-disease-group-id");
		props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");

		return props;
	}

	public static Topology createTopology(MultiLayerNetwork model) {
		final StreamsBuilder builder = new StreamsBuilder();
		KStream<String, HeartDiseaseModel> heartdiseaseStream = builder.stream(HEART_DISEASE_IN_TOPIC,
																		Consumed.with(keySerde, HeartDiseaseSerde))
				.mapValues(hd -> HeartDiseaseModel.builder(hd).predict(model).build());

		heartdiseaseStream.print(Printed.<String, HeartDiseaseModel>toSysOut().withLabel("HeartDiseasePredict"));
		heartdiseaseStream.to(HEART_DISEASE_OUT_TOPIC, Produced.with(keySerde, HeartDiseaseSerde));

		return builder.build();
	}

	public static MultiLayerNetwork loadModel() throws Exception {
		String simpleMlp = new ClassPathResource("generatedmodels/best_trained_model_3.h5").getFile().getPath();

		MultiLayerNetwork model = KerasModelImport.importKerasSequentialModelAndWeights(simpleMlp);

		return model;
	}
}
