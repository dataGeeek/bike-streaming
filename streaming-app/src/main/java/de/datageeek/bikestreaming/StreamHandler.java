package de.datageeek.bikestreaming;

import de.datageeek.bikestreaming.model.NycBikeData;
import de.datageeek.bikestreaming.model.NycBikeDataAggregated;
import de.datageeek.bikestreaming.serializer.JsonDeserializer;
import de.datageeek.bikestreaming.serializer.JsonSerializer;
import de.datageeek.bikestreaming.utils.TimestampExtractorBike;
import org.apache.kafka.common.serialization.*;
import org.apache.kafka.streams.Consumed;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.KeyValue;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.kstream.*;

import java.util.Properties;

class StreamHandler {
    static void process(Properties config){
        System.out.println("Configuration:");
        config.forEach((key, value) -> System.out.println(key + ": " + value));

        final String INPUT_TOPIC = config.getProperty("INPUT_TOPIC").trim();
        final String MAPPED_TOPIC = config.getProperty("MAPPED_TOPIC").trim();
        final String ENRICHED_TOPIC = config.getProperty("ENRICHED_TOPIC").trim();

        final Serde<String> stringSerde = Serdes.String();

        final JsonSerializer<NycBikeData> jsonSerializerInput = new JsonSerializer<>();
        final JsonDeserializer<NycBikeData> jsonDeserializerInput = new JsonDeserializer<>(NycBikeData.class);
        final Serde<NycBikeData> jsonSerdeInput = Serdes.serdeFrom(jsonSerializerInput, jsonDeserializerInput);

        final JsonSerializer<NycBikeDataAggregated> jsonSerializerAvg = new JsonSerializer<>();
        final JsonDeserializer<NycBikeDataAggregated> jsonDeserializerAvg = new JsonDeserializer<>(NycBikeDataAggregated.class);
        final Serde<NycBikeDataAggregated> jsonSerdeAvg = Serdes.serdeFrom(jsonSerializerAvg, jsonDeserializerAvg);


        StreamsBuilder builder = new StreamsBuilder();

        // Mappingfrom empty key to station id as key and writing to mapped topic
        KStream<String, NycBikeData> input = builder.stream(
                INPUT_TOPIC,
                Consumed.with(stringSerde, jsonSerdeInput)
                        .withTimestampExtractor(new TimestampExtractorBike())
        );

        input
                .map((key, value) -> new KeyValue<>(value.getIdAsString(), value))
                .peek((key, value) -> System.out.println("Key_input: " + key + " Value: "+ value))
                .to(MAPPED_TOPIC, Produced.with(stringSerde, jsonSerdeInput));

        //calculate avg number of available bikes for 1 hour windows, add timestamp for window star & end and add enriched time fields
        KStream<String, NycBikeData> avg = builder.stream(
                MAPPED_TOPIC,
                Consumed.with(stringSerde, jsonSerdeInput)
                        .withTimestampExtractor(new TimestampExtractorBike())
        );
        avg
                .groupByKey(Serialized.with(stringSerde, jsonSerdeInput))
                .windowedBy(TimeWindows.of(60L * 60L * 1000L))
                .aggregate(NycBikeDataAggregated::new,
                        (key, value, NycBikeDataAggregated) -> NycBikeDataAggregated.add(value),
                        Materialized.with(stringSerde, jsonSerdeAvg))
                .mapValues(NycBikeDataAggregated::computeAvgBikes)
                .toStream()
                .map((key, value) -> new KeyValue<>(key.key(), value.setWindowStartAndEnd(key.window().start(), key.window().end())))
                .mapValues(NycBikeDataAggregated::setDateFields)
                .peek(((key, value) -> System.out.println("Key_avg: " + key + " Value: "+ value)))
                .to(ENRICHED_TOPIC, Produced.with(stringSerde, jsonSerdeAvg));

        final KafkaStreams streams = new KafkaStreams(builder.build(), config);
        streams.setUncaughtExceptionHandler((Thread thread, Throwable throwable) -> {
            // Handle the exception
            System.err.println("An error occured:");
            System.err.println(throwable.getLocalizedMessage());
        });
        streams.cleanUp();
        streams.start();

        // Add shutdown hook to respond to SIGTERM and gracefully close Kafka Streams
        Runtime.getRuntime().addShutdownHook(new Thread(streams::close));
    }
}
