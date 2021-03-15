package org.hyperledger.bpa.impl.aries;

import org.hyperledger.bpa.api.PartnerAPI;

import java.util.Objects;

public class PartnerAddedEvent {
    private final PartnerAPI partner;

    public PartnerAddedEvent(PartnerAPI partner) {
        Objects.requireNonNull(partner, "Partner must not be null");
        this.partner = partner;
    }

    public PartnerAPI getSchema() {
        return partner;
    }

}
