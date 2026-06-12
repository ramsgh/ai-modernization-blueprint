from pyflink.common import WatermarkStrategy
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaOffsetsInitializer, KafkaRecordSerializationSchema, KafkaSink, KafkaSource
import json
import uuid


def to_embedding_request(raw_event: str) -> str:
    event = json.loads(raw_event)
    payload = event.get("payload", event)
    document = {
        "embedding_request_id": str(uuid.uuid4()),
        "source_event_id": payload.get("event_id"),
        "source_system": payload.get("source_system", "erp"),
        "entity_type": "purchase_order",
        "entity_id": payload.get("purchase_order_id"),
        "text": (
            f"Purchase order {payload.get('purchase_order_id')} for supplier "
            f"{payload.get('supplier_id')} is {payload.get('status')} with amount "
            f"{payload.get('amount')} {payload.get('currency')}."
        ),
        "metadata": {
            "domain": "procurement",
            "classification": "internal",
            "event_time": payload.get("event_time")
        }
    }
    return json.dumps(document)


def main() -> None:
    env = StreamExecutionEnvironment.get_execution_environment()
    env.enable_checkpointing(60000)

    source = KafkaSource.builder() \
        .set_bootstrap_servers("kafka:9092") \
        .set_topics("erp.purchase_order.changed.v1") \
        .set_group_id("ai-enrichment-job") \
        .set_starting_offsets(KafkaOffsetsInitializer.earliest()) \
        .set_value_only_deserializer(SimpleStringSchema()) \
        .build()

    sink = KafkaSink.builder() \
        .set_bootstrap_servers("kafka:9092") \
        .set_record_serializer(
            KafkaRecordSerializationSchema.builder()
            .set_topic("ai.embedding.requested.v1")
            .set_value_serialization_schema(SimpleStringSchema())
            .build()
        ) \
        .build()

    env.from_source(source, WatermarkStrategy.no_watermarks(), "purchase-order-source") \
        .map(to_embedding_request) \
        .sink_to(sink)

    env.execute("ai-modernization-enrichment")


if __name__ == "__main__":
    main()
