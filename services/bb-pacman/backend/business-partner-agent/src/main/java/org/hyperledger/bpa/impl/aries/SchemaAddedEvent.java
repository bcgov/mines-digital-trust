package org.hyperledger.bpa.impl.aries;

import org.hyperledger.bpa.api.aries.SchemaAPI;

import java.util.Objects;

public class SchemaAddedEvent {
    private final SchemaAPI schema;

    public SchemaAddedEvent(SchemaAPI schema) {
        Objects.requireNonNull(schema, "Schema must not be null");
        this.schema = schema;
    }

    public SchemaAPI getSchema() {
        return schema;
    }
}
