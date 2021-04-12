Drop Database if exists BOOL_QUERY;
Create Database if not exists BOOL_QUERY;

Use BOOL_QUERY;

Create Table if not exists document (
    id bigint Primary Key AUTO_INCREMENT,
    url varchar(200) NOT NULL Unique,
    size int,
    description varchar(2000),
    status boolean NOT NULL default 1,
    type ENUM('txt', 'html', 'pdf') NOT NULL default ('txt'),
    language ENUM('zh', 'en') NOT NULL default ('zh')
) AUTO_INCREMENT = 1;

Create Table if not exists dictionary (
    word varchar(200),
    document_id bigint,
    count int NOT NULL default 0 check (count >= 0),
    language ENUM('zh', 'en') NOT NULL default ('zh'),
    foreign key (document_id) references document(id) on update Cascade on delete Cascade,
    Primary Key(word, document_id)
);
