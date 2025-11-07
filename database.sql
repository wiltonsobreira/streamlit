create table tm_form (
nm_escope_product varchar(50),
nm_product varchar(50),
nm_pm	varchar(50),
fl_iuds char(1),
dt_created datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
dt_updated datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
dt_deleted datetime DEFAULT NULL
);


create table tc_escope_product (
nm_escope_product varchar(50),
dt_created datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
dt_updated datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
dt_deleted datetime DEFAULT NULL
);

create table tc_product (
nm_escope_product varchar(50),
nm_product varchar(50),
dt_created datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
dt_updated datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
dt_deleted datetime DEFAULT NULL
);

insert into tc_escope_product
(
nm_escope_product
)
select 
'data_transform'
UNION 
select 
'data_quality'

insert into tc_product
(
nm_escope_product,
nm_product
)
select 
'data_transform',
'data_process'
UNION 
select 
'data_quality',
'data_process'
UNION 
select 
'data_quality',
'product_4'
UNION 
select 
'data_transform',
'product_2'
UNION 
select 
'data_transform',
'product_3'


select * from tc_escope_product
select * from tc_product
select * from tm_form


