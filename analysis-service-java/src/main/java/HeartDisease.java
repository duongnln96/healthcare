import java.util.Properties;
import java.util.concurrent.CountDownLatch;

import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.Topology;

import processor.Ananlysis;

public class HeartDisease {
	public static void main(String[] args) {
		Properties props = Ananlysis.createProperties();

		final Topology topology = Ananlysis.createTopology();
		final KafkaStreams streams = new KafkaStreams(topology, props);
		final CountDownLatch latch = new CountDownLatch(1);

		Runtime.getRuntime().addShutdownHook(new Thread("kafka-streams-shutdown-hook") {
			@Override
			public void run() {
				System.out.println("Interrupt service ... ");
				streams.close();
				latch.countDown();
				System.exit(1);
			}
		});

		try {
			streams.start();
			latch.await();
		} catch (Throwable e) {
			System.exit(1);
		}
		System.exit(0);
	}
}
