{
	"info": {
		"_postman_id": "fdc9ba6b-bab7-4efc-97af-d2d6ef5bb84f",
		"name": "MDT Issuer/Controller",
		"schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
	},
	"item": [
		{
			"name": "get_livesness",
			"event": [
				{
					"listen": "test",
					"script": {
						"id": "1d5994b0-f6ab-4cc7-9e3c-13cf27f59a61",
						"exec": [
							"pm.test(\"success=true\", function () {",
							"    var jsonData = pm.response.json();",
							"    pm.expect(jsonData.success).to.eql(true);",
							"});",
							""
						],
						"type": "text/javascript"
					}
				}
			],
			"request": {
				"method": "GET",
				"header": [],
				"url": {
					"raw": "http://localhost:5000/liveness",
					"protocol": "http",
					"host": [
						"localhost"
					],
					"port": "5000",
					"path": [
						"liveness"
					]
				}
			},
			"response": []
		},
		{
			"name": "issue_credential",
			"event": [
				{
					"listen": "test",
					"script": {
						"id": "d2ea6c82-9bde-425b-8deb-98f7ac34d5b5",
						"exec": [
							"pm.test(\"register and issue credential\", function () {",
							"    var jsonData = pm.response.json();",
							"    pm.expect(jsonData.length).to.eql(2);   ",
							"    pm.globals.set(\"cred_id_0\", jsonData[0].result);",
							"    pm.globals.set(\"cred_id_1\", jsonData[1].result);",
							"});"
						],
						"type": "text/javascript"
					}
				}
			],
			"request": {
				"method": "POST",
				"header": [],
				"body": {
					"mode": "raw",
					"raw": "[\n    {\n        \"schema\": \"my-registration.empr\",\n        \"version\": \"1.0.0\",\n        \"attributes\": {\n            \"corp_num\": \"ABC12345\",\n            \"registration_date\": \"2018-01-01\", \n            \"entity_name\": \"Ima Permit\",\n            \"entity_name_effective\": \"2018-01-01\", \n            \"entity_status\": \"ACT\", \n            \"entity_status_effective\": \"2019-01-01\",\n            \"entity_type\": \"ABC\", \n            \"registered_jurisdiction\": \"BC\", \n            \"addressee\": \"A Person\",\n            \"address_line_1\": \"123 Some Street\",\n            \"city\": \"Victoria\",\n            \"country\": \"Canada\",\n            \"postal_code\": \"V1V1V1\",\n            \"province\": \"BC\",\n            \"effective_date\": \"2019-01-01\",\n            \"expiry_date\": \"\"\n        }\n    },\n    {\n        \"schema\": \"bcgov-mines-act-permit.empr\",\n        \"version\": \"1.0.0\",\n        \"attributes\": {\n            \"permit_id\": \"MYPERMIT12345\",\n            \"entity_name\": \"Ima Permit\",\n            \"corp_num\": \"ABC12345\",\n            \"permit_issued_date\": \"2018-01-01\", \n            \"permit_type\": \"ABC\", \n            \"permit_status\": \"OK\", \n            \"effective_date\": \"2019-01-01\"\n        }\n    }\n]",
					"options": {
						"raw": {
							"language": "json"
						}
					}
				},
				"url": {
					"raw": "http://localhost:5000/issue-credential",
					"protocol": "http",
					"host": [
						"localhost"
					],
					"port": "5000",
					"path": [
						"issue-credential"
					]
				}
			},
			"response": []
		},
		{
			"name": "get_credential",
			"event": [
				{
					"listen": "test",
					"script": {
						"id": "d036439a-c3e0-4f44-bc98-fec0a5621d15",
						"exec": [
							"cred_id_0 = pm.globals.get(\"cred_id_0\");",
							"cred_id_1 = pm.globals.get(\"cred_id_1\");",
							"",
							"creds = [cred_id_1, cred_id_0]",
							"",
							"pm.test(\"get_cred_ids_from_creation\", function () {",
							"    var jsonData = pm.response.json();",
							"    pm.expect(jsonData.objects.results[0].credential_id).to.be.oneOf(creds);",
							"    pm.expect(jsonData.objects.results[1].credential_id).to.be.oneOf(creds);",
							"});",
							"",
							""
						],
						"type": "text/javascript"
					}
				}
			],
			"request": {
				"method": "GET",
				"header": [],
				"url": {
					"raw": "http://localhost:8080/api/search/credential/topic/facets?credential_type_id=&issuer_id=&topic_id=1&inactive=false&revoked=",
					"protocol": "http",
					"host": [
						"localhost"
					],
					"port": "8080",
					"path": [
						"api",
						"search",
						"credential",
						"topic",
						"facets"
					],
					"query": [
						{
							"key": "credential_type_id",
							"value": ""
						},
						{
							"key": "issuer_id",
							"value": ""
						},
						{
							"key": "topic_id",
							"value": "1"
						},
						{
							"key": "inactive",
							"value": "false"
						},
						{
							"key": "revoked",
							"value": ""
						}
					]
				}
			},
			"response": []
		}
	],
	"protocolProfileBehavior": {}
}