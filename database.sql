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

-- drop table tm_form_recommendation;

create table tm_form_recommendation (
ds_email_sender varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
cd_product varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
nm_product varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
nm_product_use_method varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
ds_other_product_use_method varchar(200) COLLATE utf8mb4_unicode_ci NULL,
nm_product_scope varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
ds_other_product_scope varchar(200) COLLATE utf8mb4_unicode_ci NULL,
nm_squad_owner varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
fl_squad_owner_financas char(1) COLLATE utf8mb4_unicode_ci NOT NULL,
ds_email_product_manager varchar(100) COLLATE utf8mb4_unicode_ci NULL,
ds_email_tech_lead varchar(100) COLLATE utf8mb4_unicode_ci NULL,
ds_sn_st_product varchar(100) COLLATE utf8mb4_unicode_ci NULL,
fl_support char(1) COLLATE utf8mb4_unicode_ci NOT NULL,
ds_support_tier	varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
fl_allow_inner_source char(1) COLLATE utf8mb4_unicode_ci NOT NULL,
url_git_repository varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
fl_user_documentation char(1) COLLATE utf8mb4_unicode_ci NOT NULL,
url_user_documentation varchar(200) COLLATE utf8mb4_unicode_ci NULL,
fl_inner_source_documentation char(1) COLLATE utf8mb4_unicode_ci NOT NULL,
url_inner_source_documentation varchar(200) COLLATE utf8mb4_unicode_ci NULL,
fl_iu_digital_store char(1) COLLATE utf8mb4_unicode_ci NOT NULL,
url_iu_digital_store varchar(200) COLLATE utf8mb4_unicode_ci NULL,
fl_video_user_product char(1) COLLATE utf8mb4_unicode_ci NOT NULL,
url_video_user_product varchar(200) COLLATE utf8mb4_unicode_ci NULL,
fl_video_inner_source char(1) COLLATE utf8mb4_unicode_ci NOT NULL,
url_video_inner_source varchar(200) COLLATE utf8mb4_unicode_ci NULL,
dt_release_product date NULL,
nr_user_squads smallint(5) unsigned NULL,
ds_name_user_squads varchar(200) COLLATE utf8mb4_unicode_ci NULL,
ts_created datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
ts_updated datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
ts_deleted datetime DEFAULT NULL
);

select * from tm_form_recommendation

-- drop table tc_product_use_method;

create table tc_product_use_method (
id_product_use_method tinyint(1) NOT NULL,
cd_product_use_method varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
nm_product_use_method varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
ts_created datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
ts_updated datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
ts_deleted datetime DEFAULT NULL
);

insert into tc_product_use_method
(
id_product_use_method,
cd_product_use_method,
nm_product_use_method
)
select 
1,
'application_with_user_interface',
'Application with User Interface'
UNION 
select 
2,
'api',
'API'
UNION 
select 
3,
'library',
'Library'
UNION 
select 
4,
-- 'other_product_use_method_describe',
-- 'Other Product Use Method - [Describe]';
'opcao_nao_localizada_incluir_novas_opcoes_no_campo_abaixo',
'Opção não localizada - Incluir novas opções no campo abaixo';

-- delete from tc_product_use_method where id_product_use_method = 4

/*
insert into tc_product_use_method
(
id_product_use_method,
cd_product_use_method,
nm_product_use_method
)
select 
4,
-- 'other_product_use_method_describe',
-- 'Other Product Use Method - [Describe]';
'opcao_nao_localizada_incluir_novas_opcoes_no_campo_abaixo',
'. Opção não localizada - Incluir novas opções no campo abaixo';*/

select * from tc_product_use_method

-- drop table tc_product_scope;

create table tc_product_scope (
id_product_scope smallint(5) NOT NULL,
cd_product_scope varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
nm_product_scope varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
ts_created datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
ts_updated datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
ts_deleted datetime DEFAULT NULL
);

insert into tc_product_scope
(
id_product_scope,
cd_product_scope,
nm_product_scope
)
select 
1,
'gerenciamento_de_regras_flexiveis',
'Gerenciamento de Regras Flexíveis'
UNION
select
2,
'transformacao_de_dados',
'Transformação de Dados'
UNION
select
3,
'qualidade_de_dados',
'Qualidade de Dados'
UNION
select
4,
'autenticacao_de_acessos',
'Autenticação de Acessos'
UNION
select
5,
'autorizacao_de_acessos',
'Autorização de Acessos'
UNION
select
6,
'provedor_de_identidade',
'Provedor de Identifidade'
UNION
select
7,
'gestao_de_acessos',
'Gestão de Acessos'
UNION
select
8,
'observabilidade',
'Observabilidade'
UNION
select
9,
'notificacao_da_plataforma_de_dados',
'Notificação da Plataforma de Dados'
UNION
select
10,
'ingestao_mainframe_private_link',
'Ingestão Mainframe - Private Link'
UNION 
select 
11,
-- 'other_product_scope_describe',
-- 'Other Product Scope - [Describe]';
'opcao_nao_localizada_incluir_novas_opcoes_no_campo_abaixo',
'. Opção não localizada - Incluir novas opções no campo abaixo';

-- delete from tc_product_scope where id_product_scope = 11

/*
insert into tc_product_scope
(
id_product_scope,
cd_product_scope,
nm_product_scope
)
select 
11,
-- 'other_product_scope_describe',
-- 'Other Product Scope - [Describe]';
'opcao_nao_localizada_incluir_novas_opcoes_no_campo_abaixo',
'. Opção não localizada - Incluir novas opções no campo abaixo';*/



select * from tc_product_scope

-- drop table tc_product_scope;

create table tc_support_tier (
id_support_tier tinyint(1) NOT NULL,
cd_support_tier varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
ds_support_tier	varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
ts_created datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
ts_updated datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
ts_deleted datetime DEFAULT NULL
);


insert into tc_support_tier
(
id_support_tier,
cd_support_tier,
ds_support_tier
)
select
1,
'tier_1',
'Tier 1'
UNION 
select
2,
'tier_2',
'Tier 2'
UNION 
select
3,
'tier_3',
'Tier 3'
UNION 
select
4,
'tier_4',
'Tier 4'
UNION 
select 
5,
-- 'not_applicable',
-- 'Not Applicable';
'nao_aplicavel',
'Não Aplicável';

-- delete from tc_support_tier where id_support_tier = 5

/*
insert into tc_support_tier
(
id_support_tier,
cd_support_tier,
ds_support_tier
)
select 
5,
-- 'not_applicable',
-- 'Not Applicable';
'nao_aplicavel',
'. Não Aplicável';*/



select * from tc_support_tier



tb_form_recommendation

ds_email_sender 
id_product 						-- sequence (n�o usado na tabela forms)
cd_product 						-- unique (gerado a partir do nome)
nm_product 
nm_method_use 					-- fk (+1 bridge table)
nm_scope						-- fk (+1 bridge table)
nm_squad_owner
fl_squad_owner_financas
ds_email_product_manager
ds_email_tech_lead
ds_sn_st_product
fl_support
nr_tier_support					-- fk (incluir n�o possui suporte) 
fl_allow_inner_source
url_git_repository
fl_user_documentation
url_user_documentation
fl_inner_source_documentation
url_inner_source_documentation
fl_iu_digital_store
url_iu_digital_store
fl_video_user_product
url_video_user_product
fl_video_inner_source
url_video_inner_source
dt_release_product
nr_user_squads
ds_name_user_squads
