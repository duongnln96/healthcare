package config;

public class KafkaConfig {
    public String bootstrapServer;
    public Integer partition;
    public Long timeout;

    public KafkaConfig(String bootstrapServer, Integer partition, Long timeout) {
        this.bootstrapServer = bootstrapServer;
        this.partition = partition;
        this.timeout = timeout;
    }



    @Override
    public String toString() {
        return "KafkaConfig=[bootstrapServer=" + bootstrapServer + "partition=" + partition
                + "timeout=" + timeout;
    }
}
