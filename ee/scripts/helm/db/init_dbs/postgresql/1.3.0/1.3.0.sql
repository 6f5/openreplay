BEGIN;
CREATE INDEX sessions_session_id_project_id_start_ts_durationNN_idx ON sessions (session_id, project_id, start_ts) WHERE duration IS NOT NULL;
CREATE INDEX clicks_label_session_id_timestamp_idx ON events.clicks (label,session_id,timestamp);
CREATE INDEX pages_base_path_session_id_timestamp_idx ON events.pages (base_path,session_id,timestamp);
CREATE INDEX ON unstarted_sessions(project_id);
CREATE INDEX ON assigned_sessions(session_id);
CREATE INDEX ON technical_info(session_id);
CREATE INDEX inputs_label_session_id_timestamp_idx ON events.inputs (label,session_id,timestamp);

CREATE INDEX clicks_url_idx ON events.clicks (url);
CREATE INDEX clicks_url_gin_idx ON events.clicks USING GIN (url gin_trgm_ops);
CREATE INDEX clicks_url_session_id_timestamp_selector_idx ON events.clicks (url, session_id, timestamp,selector);

COMMIT ;