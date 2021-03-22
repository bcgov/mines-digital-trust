package org.hyperledger.bpa.api;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hyperledger.aries.api.creddef.CredentialDefinition;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class CredDefAPI {
    private String id;

    private String schemaId;

    private String tag;

    public static CredDefAPI from(CredentialDefinition o) {
        return CredDefAPI
                .builder()
                .id(o.getId())
                .schemaId(o.getSchemaId())
                .tag(o.getTag())
                .build();
    }
}
