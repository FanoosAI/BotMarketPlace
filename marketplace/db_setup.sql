create table if not exists bots (
    username varchar primary key check (username like 'bot_%'),
    name text not null,
    registered_at datetime default current_timestamp,
    registered_by varchar primary key
);

