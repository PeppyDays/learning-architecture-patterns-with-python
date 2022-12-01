use allocation;

create table batches (
    id bigint unsigned auto_increment primary key,
    batch_id varchar(50) not null,
    sku varchar(50) not null,
    total_quantity smallint unsigned not null,
    eta date,
    allocated_order_lines text,
    unique key (batch_id)
);
