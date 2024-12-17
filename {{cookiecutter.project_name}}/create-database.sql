-- execute these lines one at a time, being connected as the "main" user of the database
create database "{{project_name}}";
create user "{{project_name}}-user" with encrypted password '{{ random_ascii_string(12) }}';
grant all privileges on database "{{project_name}}" to "{{project_name}}-user";
-- change database connection
\c {{project_name}}
GRANT ALL ON SCHEMA public TO "{{project_name}}-user";
GRANT USAGE ON SCHEMA public TO "{{project_name}}-user";
