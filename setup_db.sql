-- Crea el usuario y la base de datos de DataPath (solo si no existen).
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'datapath') THEN
    CREATE ROLE datapath LOGIN PASSWORD 'datapath' CREATEROLE;
  END IF;
END
$$;

SELECT 'CREATE DATABASE datapath OWNER datapath'
WHERE NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'datapath')\gexec
