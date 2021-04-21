package config;

import java.util.Properties;

import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.StreamsConfig;

public class AppConfig {
    // private String configPathFiles;
    // // private KafkaConfig kafaConfig;

    // AppConfig(String configPath) {
    //     this.configPathFiles = configPath;
    // }

    // private void loadConfig() {

    // }



	public Properties createProperties() {
		Properties props = new Properties();
		props.put(StreamsConfig.APPLICATION_ID_CONFIG, "heart-disease-application");
		props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "192.168.1.3:9092");
		// props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.Integer().getClass());
		props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass());
		return props;
	}

    @Override
    public String toString(){
        return "AppConfig [KafkaConfig=";
    }
}
