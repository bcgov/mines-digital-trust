package org.hyperledger.bpa.impl.aries;

import io.micronaut.context.event.ApplicationEventPublisher;
import io.micronaut.scheduling.annotation.Async;
import io.micronaut.scheduling.annotation.Scheduled;
import lombok.AccessLevel;
import lombok.NonNull;
import lombok.Setter;
import lombok.extern.slf4j.Slf4j;
import org.hyperledger.aries.AriesClient;
import org.hyperledger.aries.api.creddef.CredentialDefinition;
import org.hyperledger.aries.api.creddef.CredentialDefinition.*;
import org.hyperledger.bpa.api.CredDefAPI;
import org.hyperledger.bpa.api.aries.SchemaAPI;
import org.hyperledger.bpa.model.BPASchema;
import org.hyperledger.bpa.repository.SchemaRepository;

import javax.inject.Inject;
import javax.inject.Singleton;
import java.io.IOException;
import java.util.*;

@Slf4j
@Singleton
public class CredentialDefinitionService {

    @Inject
    @Setter(AccessLevel.PACKAGE)
    SchemaRepository schemaRepo;

    @Inject
    AriesClient ac;

    private Map<String, CredDefAPI> mySchemaCredDefs = new HashMap<>();
    private List<CredDefAPI> myCredDefs = new ArrayList<>();

    public String createCredentialDefinition(@NonNull String schemaId, String tag, int revocationRegistrySize,
            boolean supportRevocation) {
        // do we need to force tag to be of a particular format (illegal chars etc)?
        // do we need to validate revocation size?
        String result = null;
        CredentialDefinitionRequest creddef = CredentialDefinitionRequest.builder()
                .revocationRegistrySize(revocationRegistrySize)
                .schemaId(schemaId)
                .supportRevocation(supportRevocation)
                .tag(tag)
                .build();
        try {
            Optional<CredentialDefinitionResponse> creddefResponse = ac.credentialDefinitionsCreate(creddef);
            if (creddefResponse.isPresent()) {
                result = creddefResponse.get().getCredentialDefinitionId();
                log.debug("Credential Definition created: {}", result);
                refreshSchemaCredDefsAsync();
            } else {
                log.error("Credential Definition not created.");
            }
        } catch (IOException e) {
            log.error("aca-py not reachable", e);
        }
        return result;
    }

    @Scheduled(fixedRate = "10m", initialDelay = "10m")
    public void refreshSchemaCredDefs() {
        myCredDefs = getMyCredentialDefinitions();
        mySchemaCredDefs = new HashMap<>();
        schemaRepo.findAll().forEach((s) -> myCredDefs.stream()
                .filter(x -> x.getSchemaId().contentEquals(s.getSeqNo().toString())).findFirst()
                .ifPresent(c -> mySchemaCredDefs.put(s.getSchemaId(), c)));
    }

    @Async
    public void refreshSchemaCredDefsAsync() {
        refreshSchemaCredDefs();
    }

    public Map<String, CredDefAPI> getSchemaCredDefs() {
        return mySchemaCredDefs;
    }

    public CredDefAPI getSchemaCredDef(String schemaId) {
        try {
            return mySchemaCredDefs.get(schemaId);
        } catch (NullPointerException e) {
            return null;
        }
    }

    public List<CredDefAPI> getCredDefs() {
        return myCredDefs;
    }

    public Optional<CredentialDefinition> getCredentialDefinition(@NonNull String id) {
        Optional<CredentialDefinition> result = null;
        try {
            result = ac.credentialDefinitionsGetById(id);
        } catch (IOException e) {
            log.error("aca-py not reachable", e);
        }
        return result;
    }

    private List<String> getCreatedCredentialDefinitionIds() {
        List<String> result = null;
        try {
            Optional<CredentialDefinition.CredentialDefinitionsCreated> created = ac.credentialDefinitionsCreated(null);
            if (created.isPresent()) {
                result = created.get().getCredentialDefinitionIds();
            }
        } catch (IOException e) {
            log.error("aca-py not reachable", e);
        }
        return result;
    }

    private List<CredDefAPI> getMyCredentialDefinitions() {
        List<CredDefAPI> result = new ArrayList<>();
        this.getCreatedCredentialDefinitionIds().stream()
                .forEach((id) -> this.getCredentialDefinition(id).ifPresent(c -> result.add(CredDefAPI.from(c))));
        return result;
    }

}
