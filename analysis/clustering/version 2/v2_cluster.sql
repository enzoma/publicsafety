-- INITIAL HEADER TO DROP OLD SHEMA AND CREATE Clustering SCHEMA -- 
--DROP SCHEMA clustering CASCADE;
--CREATE SCHEMA clustering;
DROP TABLE clustering.assignments_v2 CASCADE;
SET search_path TO clustering,public;

-- CREATE CLUSTERING V2 TABLE ---
CREATE TABLE clustering.assignments_v2(
  tractno FLOAT NOT NULL,
  clusternum INTEGER NOT NULL
);

-- ALTER TABLE ONLY clustering.assignments
--   ADD CONSTRAINT clustering_pkey PRIMARY KEY (id);
-- ALTER TABLE ONLY clustering.assignments
--   ADD CONSTRAINT clustering_unique UNIQUE(id);

\copy clustering.assignments_v2 (tractno, clusternum) FROM '/mnt/data1/CPD/V2_normalized_cluster_assignments.csv' CSV HEADER
