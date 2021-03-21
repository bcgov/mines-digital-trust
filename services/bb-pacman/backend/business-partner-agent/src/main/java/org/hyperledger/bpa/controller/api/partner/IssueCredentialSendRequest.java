package org.hyperledger.bpa.controller.api.partner;

import com.fasterxml.jackson.annotation.JsonRawValue;
import com.fasterxml.jackson.databind.JsonNode;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class IssueCredentialSendRequest {
    private String schemaId;
    private String credentialDefinitionId;
    @JsonRawValue
    @Schema(example = "{}")
    private JsonNode document;
}
