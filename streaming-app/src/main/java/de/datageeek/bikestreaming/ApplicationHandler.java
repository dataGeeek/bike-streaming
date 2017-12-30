package de.datageeek.bikestreaming;

import org.apache.kafka.streams.StreamsConfig;
import java.util.Properties;
import java.io.IOException;

public class ApplicationHandler {
    public static void main(String[] args) {
        Properties config = loadConfig();
        StreamHandler.process(config);
    }

    private static Properties loadConfig() {
        Properties configFile = new Properties();
        try {
            configFile.load(
                    ApplicationHandler.class.getClassLoader().getResourceAsStream("streaming.properties")
            );
        }
        catch (IOException exc){
            System.err.println("--- Could not load properties file ---");
            return configFile;
        }
        Properties streamsConfig = new Properties();
        streamsConfig.put(StreamsConfig.APPLICATION_ID_CONFIG, configFile.get("APPLICATION_ID_CONFIG"));
        streamsConfig.put(StreamsConfig.CLIENT_ID_CONFIG, configFile.get("CLIENT_ID_CONFIG"));
        streamsConfig.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, configFile.get("BOOTSTRAP_SERVERS_CONFIG"));
        streamsConfig.put(StreamsConfig.COMMIT_INTERVAL_MS_CONFIG, configFile.get("COMMIT_INTERVAL_MS_CONFIG"));
        streamsConfig.put(StreamsConfig.CACHE_MAX_BYTES_BUFFERING_CONFIG, configFile.get("CACHE_MAX_BYTES_BUFFERING_CONFIG"));
        streamsConfig.put("KEY", configFile.get("KEY"));
        streamsConfig.put("INPUT_TOPIC", configFile.get("INPUT_TOPIC"));
        streamsConfig.put("MAPPED_TOPIC", configFile.get("MAPPED_TOPIC"));
        streamsConfig.put("ENRICHED_TOPIC", configFile.get("ENRICHED_TOPIC"));
        streamsConfig.put("OUTPUT_TOPIC", configFile.get("OUTPUT_TOPIC"));
        return streamsConfig;
    }
}
