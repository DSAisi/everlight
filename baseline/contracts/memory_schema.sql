-- Target structural fragment only. Not an automatic migration or full application implementation.
PRAGMA foreign_keys=ON;
CREATE TABLE memory_objects(
 id TEXT PRIMARY KEY, kind TEXT NOT NULL CHECK(kind IN ('working','episodic','semantic','procedural','relational','emotional','identity','metamemory','reflective','atlas')),
 namespace TEXT NOT NULL, agent_id TEXT NOT NULL, session_id TEXT NOT NULL, channel_id TEXT NOT NULL,
 revision INTEGER NOT NULL CHECK(revision>=1), schema_version TEXT NOT NULL,
 review_status TEXT NOT NULL, deleted INTEGER NOT NULL DEFAULT 0 CHECK(deleted IN (0,1)),
 created_at TEXT NOT NULL, created_by TEXT NOT NULL, record_digest TEXT NOT NULL,
 UNIQUE(id,kind)
);
CREATE INDEX memory_kind_scope ON memory_objects(namespace,agent_id,kind,deleted,review_status);
CREATE TABLE memory_versions(
 object_id TEXT NOT NULL REFERENCES memory_objects(id), revision INTEGER NOT NULL CHECK(revision>=1),
 record_json TEXT NOT NULL CHECK(json_valid(record_json)), digest TEXT NOT NULL,
 commit_ref TEXT NOT NULL, PRIMARY KEY(object_id,revision)
);
CREATE TABLE source_registry(
 source_id TEXT NOT NULL, source_revision TEXT NOT NULL, namespace TEXT NOT NULL,
 source_type TEXT NOT NULL, source_hash TEXT NOT NULL, length_bytes INTEGER CHECK(length_bytes IS NULL OR length_bytes>=0),
 acl_ref TEXT NOT NULL, deleted INTEGER NOT NULL DEFAULT 0 CHECK(deleted IN(0,1)),
 PRIMARY KEY(source_id,source_revision)
);
CREATE TABLE source_refs(
 object_id TEXT NOT NULL, object_revision INTEGER NOT NULL,
 source_id TEXT NOT NULL, source_revision TEXT NOT NULL, source_hash TEXT NOT NULL,
 start_byte INTEGER, end_byte INTEGER, relation TEXT NOT NULL CHECK(relation IN('supports','contradicts','derived_from','continuation','associated_with')),
 FOREIGN KEY(object_id,object_revision) REFERENCES memory_versions(object_id,revision),
 FOREIGN KEY(source_id,source_revision) REFERENCES source_registry(source_id,source_revision),
 CHECK((start_byte IS NULL AND end_byte IS NULL) OR (start_byte IS NOT NULL AND end_byte IS NOT NULL AND start_byte>=0 AND end_byte>start_byte))
);
CREATE INDEX reverse_source_refs ON source_refs(source_id,source_revision,object_id);
CREATE TABLE dependencies(
 source_id TEXT NOT NULL, source_revision TEXT NOT NULL, derived_id TEXT NOT NULL REFERENCES memory_objects(id),
 derived_revision INTEGER NOT NULL, relation TEXT NOT NULL, processor_version TEXT NOT NULL,
 PRIMARY KEY(source_id,source_revision,derived_id,derived_revision,relation)
);
CREATE TABLE schema_meta(key TEXT PRIMARY KEY,value TEXT NOT NULL);
INSERT INTO schema_meta VALUES('design_schema','everlight-memory/6');

CREATE TABLE working_memory(object_id TEXT PRIMARY KEY,kind TEXT NOT NULL DEFAULT 'working' CHECK(kind='working'),goal TEXT NOT NULL, project_id TEXT, task_id TEXT, state TEXT NOT NULL CHECK(state IN ('planned','active','blocked','paused','completed','cancelled')), next_step TEXT, acceptance_json TEXT CHECK(acceptance_json IS NULL OR json_valid(acceptance_json)),FOREIGN KEY(object_id,kind) REFERENCES memory_objects(id,kind));

CREATE TABLE episodic_memory(object_id TEXT PRIMARY KEY,kind TEXT NOT NULL DEFAULT 'episodic' CHECK(kind='episodic'),event_refs_json TEXT NOT NULL CHECK(json_valid(event_refs_json)), participants_json TEXT NOT NULL CHECK(json_valid(participants_json)), valid_from TEXT, valid_to TEXT, completeness_json TEXT NOT NULL CHECK(json_valid(completeness_json)),FOREIGN KEY(object_id,kind) REFERENCES memory_objects(id,kind));

CREATE TABLE semantic_memory(object_id TEXT PRIMARY KEY,kind TEXT NOT NULL DEFAULT 'semantic' CHECK(kind='semantic'),subject_id TEXT NOT NULL, predicate TEXT NOT NULL, value_json TEXT NOT NULL CHECK(json_valid(value_json)), epistemic TEXT NOT NULL, valid_from TEXT, valid_to TEXT, condition_json TEXT CHECK(condition_json IS NULL OR json_valid(condition_json)),FOREIGN KEY(object_id,kind) REFERENCES memory_objects(id,kind));

CREATE TABLE procedural_memory(object_id TEXT PRIMARY KEY,kind TEXT NOT NULL DEFAULT 'procedural' CHECK(kind='procedural'),goal TEXT NOT NULL, environment_json TEXT NOT NULL CHECK(json_valid(environment_json)), preconditions_json TEXT NOT NULL CHECK(json_valid(preconditions_json)), steps_json TEXT NOT NULL CHECK(json_valid(steps_json)), results_json TEXT NOT NULL CHECK(json_valid(results_json)), failure_modes_json TEXT NOT NULL CHECK(json_valid(failure_modes_json)),FOREIGN KEY(object_id,kind) REFERENCES memory_objects(id,kind));

CREATE TABLE relational_memory(object_id TEXT PRIMARY KEY,kind TEXT NOT NULL DEFAULT 'relational' CHECK(kind='relational'),record_type TEXT NOT NULL CHECK(record_type IN ('entity','alias','relation','interaction','expectation')), from_id TEXT, to_id TEXT, holder_id TEXT, domain TEXT, valid_from TEXT, valid_to TEXT, details_json TEXT NOT NULL CHECK(json_valid(details_json)),FOREIGN KEY(object_id,kind) REFERENCES memory_objects(id,kind));

CREATE TABLE emotional_memory(object_id TEXT PRIMARY KEY,kind TEXT NOT NULL DEFAULT 'emotional' CHECK(kind='emotional'),owner_id TEXT NOT NULL, target_id TEXT, concern_id TEXT, episode_id TEXT, expression TEXT, interpretation_json TEXT CHECK(interpretation_json IS NULL OR json_valid(interpretation_json)), change_mode TEXT NOT NULL CHECK(change_mode IN ('retained','revised','coexisting','suspended','unknown')), details_json TEXT NOT NULL CHECK(json_valid(details_json)),FOREIGN KEY(object_id,kind) REFERENCES memory_objects(id,kind));

CREATE TABLE identity_memory(object_id TEXT PRIMARY KEY,kind TEXT NOT NULL DEFAULT 'identity' CHECK(kind='identity'),field_key TEXT NOT NULL, value_json TEXT NOT NULL CHECK(json_valid(value_json)), field_kind TEXT NOT NULL, policy_ref TEXT NOT NULL, valid_from TEXT, valid_to TEXT,FOREIGN KEY(object_id,kind) REFERENCES memory_objects(id,kind));

CREATE TABLE metamemory(object_id TEXT PRIMARY KEY,kind TEXT NOT NULL DEFAULT 'metamemory' CHECK(kind='metamemory'),run_id TEXT NOT NULL, query_id TEXT, route TEXT, coverage_json TEXT NOT NULL CHECK(json_valid(coverage_json)), gaps_json TEXT NOT NULL CHECK(json_valid(gaps_json)),FOREIGN KEY(object_id,kind) REFERENCES memory_objects(id,kind));

CREATE TABLE reflective_memory(object_id TEXT PRIMARY KEY,kind TEXT NOT NULL DEFAULT 'reflective' CHECK(kind='reflective'),axis TEXT NOT NULL CHECK(axis IN ('work','emotional','social')), holder_id TEXT NOT NULL, observation TEXT NOT NULL, interpretation_json TEXT CHECK(interpretation_json IS NULL OR json_valid(interpretation_json)), applies_json TEXT NOT NULL CHECK(json_valid(applies_json)), strategy_json TEXT NOT NULL CHECK(json_valid(strategy_json)), counter_json TEXT NOT NULL CHECK(json_valid(counter_json)),FOREIGN KEY(object_id,kind) REFERENCES memory_objects(id,kind));

CREATE TABLE atlas_memory(object_id TEXT PRIMARY KEY,kind TEXT NOT NULL DEFAULT 'atlas' CHECK(kind='atlas'),document_id TEXT NOT NULL, resource_kind TEXT NOT NULL, locator_ref TEXT NOT NULL, content_hash TEXT, source_revision TEXT NOT NULL, extraction_json TEXT NOT NULL CHECK(json_valid(extraction_json)), index_state TEXT NOT NULL CHECK(index_state IN ('available','stale','moved','missing','denied')),FOREIGN KEY(object_id,kind) REFERENCES memory_objects(id,kind));

-- All stores need application-level ACL, CAS, reference support and lifecycle checks.
-- These tables deliberately do not claim cross-database foreign keys or global atomicity.
