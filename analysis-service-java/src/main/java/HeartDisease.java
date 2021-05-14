import java.util.Properties;
import java.util.concurrent.CountDownLatch;

import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.Topology;
import org.deeplearning4j.nn.multilayer.MultiLayerNetwork;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import processor.Ananlysis;

public class HeartDisease {

	private static final Logger LOG = LoggerFactory.getLogger(HeartDisease.class);
	public static void main(String[] args) throws Exception {
		Properties props = Ananlysis.createProperties();

		MultiLayerNetwork model = Ananlysis.loadModel();

		final Topology topology = Ananlysis.createTopology(model);
		final KafkaStreams kstreams = new KafkaStreams(topology, props);
		final CountDownLatch stopSignal = new CountDownLatch(1);

		Runtime.getRuntime().addShutdownHook(new Thread("kafka-streams-shutdown-hook") {
			@Override
			public void run() {
				LOG.info("Shutting down the Kafka Streams Application now");
				kstreams.close();
				stopSignal.countDown();
			}
		});

		try {
			kstreams.start();
			stopSignal.await();
		} catch (Throwable e) {
			LOG.info("Exception: {}", e);
		}
	}
}
