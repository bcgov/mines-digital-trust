package org.hyperledger.bpa.controller.api.admin;

import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@NoArgsConstructor
public class CreateCredDefRequest {
    private String schemaId;

    private String tag;

    private int revocationRegistrySize;

    private boolean supportRevocation;
}
