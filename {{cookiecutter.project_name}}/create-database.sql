-- execute these lines one at a time, being connected as the "main" user of the database
create database "{{cookiecutter.project_name}}";
create user "{{cookiecutter.project_name}}-user" with encrypted password '{{ random_ascii_string(12) }}';
grant all privileges on database "{{cookiecutter.project_name}}" to "{{cookiecutter.project_name}}-user";
-- change database connection
\c {{cookiecutter.project_name}}
GRANT ALL ON SCHEMA public TO "{{cookiecutter.project_name}}-user";
GRANT USAGE ON SCHEMA public TO "{{cookiecutter.project_name}}-user";
