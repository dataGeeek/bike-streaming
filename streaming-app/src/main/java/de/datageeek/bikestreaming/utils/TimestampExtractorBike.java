package de.datageeek.bikestreaming.utils;

import de.datageeek.bikestreaming.model.NycBikeData;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.streams.processor.TimestampExtractor;

// Extracts the embedded timestamp of a record (giving you "event-time" semantics).
public class TimestampExtractorBike implements TimestampExtractor {

    @Override
    public long extract(final ConsumerRecord<Object, Object> record, final long previousTimestamp) {
        long timestamp = -1;
        final NycBikeData bikeRecord = (NycBikeData) record.value();
        if (bikeRecord != null) {
            timestamp = bikeRecord.getTimestampInMillis();
        }
        if (timestamp < 0) {
            if (previousTimestamp >= 0) {
                return previousTimestamp;
            } else {
                return System.currentTimeMillis();
            }
        }
        return timestamp;
    }

}
