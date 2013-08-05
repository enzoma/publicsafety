-- INITIAL HEADER TO DROP OLD SHEMA AND CREATE Clustering SCHEMA -- 
DROP SCHEMA clustering CASCADE;

CREATE SCHEMA clustering;

SET search_path TO clustering,public;

-- CREATE CLUSTERING TABLE ---
CREATE TABLE clustering.assignments(
  tractno FLOAT NOT NULL,
  clusternum INTEGER NOT NULL
);

-- ALTER TABLE ONLY clustering.assignments
--   ADD CONSTRAINT clustering_pkey PRIMARY KEY (id);
-- ALTER TABLE ONLY clustering.assignments
--   ADD CONSTRAINT clustering_unique UNIQUE(id);

\copy clustering.assignments (tractno, clusternum) FROM '/mnt/data1/CPD/normalized_cluster_assignments.csv' CSV HEADER
