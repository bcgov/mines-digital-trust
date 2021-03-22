
CREATE TABLE issued_credential (
   id uuid PRIMARY KEY,
   issued_at timestamp without time zone,
   type character varying(255),
   connection_id character varying(255) NOT NULL,
   state character varying(255) NOT NULL,
   thread_id character varying(255) NOT NULL,
   credential_exchange_id character varying(255) NOT NULL,
   schema_id character varying(255),
   label character varying(255),
   credential_definition_id character varying(255),
   credential jsonb,
   credential_preview jsonb
);
