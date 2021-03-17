package org.hyperledger.bpa.impl.aries;

import java.util.Objects;

public class CredentialDefinitionAddedEvent {
    private final String credDefId;

    public CredentialDefinitionAddedEvent(String credDefId) {
        Objects.requireNonNull(credDefId, "Credential Definition ID must not be null");
        this.credDefId = credDefId;
    }

    public String getCredentialDefinitionId() {
        return credDefId;
    }
}
