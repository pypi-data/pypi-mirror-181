--
-- migrator schema creation
--
CREATE SCHEMA migrator;
COMMENT ON SCHEMA migrator IS 'Schema containing the table used by the migrator for the process of migrating the ROC database';

-- roc_identifier table creation
CREATE TABLE migrator.revisions (
  id_revisions serial PRIMARY KEY,
  revisions_software text NOT NULL,
  revisions_revision text,
  UNIQUE(revisions_software)
);
COMMENT ON TABLE migrator.revisions IS 'Informations on revisions for ROC database';

COMMIT;
