
CREATE TABLE IF NOT EXISTS `tbl_pcp_distribution`(
   `id` INT UNSIGNED AUTO_INCREMENT,
   `date` VARCHAR(10) NOT NULL,
   `total_count` int NOT NULL,
   `halt_count` int NOT NULL,
   `limit_down_count` int NOT null,
   `limit_up_count` int NOT NULL,
   `st_limit_down_count` int NOT null,
   `st_limit_up_count` int NOT NULL,
   `range_p0` int NOT NULL,
   `range_p1` int NOT NULL,
   `range_p2` int NOT NULL,
   `range_p3` int NOT NULL,
   `range_p4` int NOT NULL,
   `range_p5` int NOT NULL,
   `range_p6` int NOT NULL,
   `range_p7` int NOT NULL,
   `range_p8` int NOT NULL,
   `range_p9` int NOT NULL,
   `range_p10` int NOT NULL,
   `range_p20` int NOT NULL,
   `range_m1` int NOT NULL,
   `range_m2` int NOT NULL,
   `range_m3` int NOT NULL,
   `range_m4` int NOT NULL,
   `range_m5` int NOT NULL,
   `range_m6` int NOT NULL,
   `range_m7` int NOT NULL,
   `range_m8` int NOT NULL,
   `range_m9` int NOT NULL,
   `range_m10` int NOT NULL,
   `range_m20` int NOT NULL,
   `data_ts`  bigint not NUll,
   `create_time` DATETIME, 
    PRIMARY KEY ( `id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE IF NOT EXISTS `tbl_rise_fall_count`(
   `id` INT UNSIGNED AUTO_INCREMENT,
   `date` VARCHAR(10) NOT NULL,
   `rise_count` int NOT NULL,
   `fall_count` int NOT NULL,
   `data_ts`  bigint not NUll,
   `data_ts_format` varchar(50) not NULL,
   `create_time` DATETIME, 
    PRIMARY KEY ( `id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE INDEX index_tbl_rise_fall_count_date on tbl_rise_fall_count(date);

CREATE TABLE IF NOT EXISTS `tbl_limit_up_down_count`(
   `id` INT UNSIGNED AUTO_INCREMENT,
   `date` VARCHAR(10) NOT NULL,
   `limit_up_count` int NOT NULL,
   `limit_down_count` int NOT NULL,
   `data_ts`  bigint not NUll,
   `data_ts_format` varchar(50) not NULL,
   `create_time` DATETIME, 
    PRIMARY KEY ( `id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE INDEX index_tbl_limit_up_down_count on tbl_rise_fall_count(date);

CREATE TABLE IF NOT EXISTS `tbl_quotation_event_history` (
    `id` INT UNSIGNED AUTO_INCREMENT,
    `msg_id` int NOT NULL,
    `date` VARCHAR(10) NOT NULL,
    `target` varchar(50) NOT NULL,
    `event_type` int NOT NULL,
    `event_timestamp` bigint NOT NULL,
    `event_timestamp_format` varchar(50) NOT NULL,
    `good_or_bad` int NOT NULL,
    `stock_abnormal_event_data` longtext,
    `plate_abnormal_event_data` longtext,
    `create_time` DATETIME,
    PRIMARY KEY (`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE INDEX index_tbl_quotation_event_history on tbl_quotation_event_history(msg_id);

create TABLE if not EXISTS `tbl_msg` (
    `id` int UNSIGNED AUTO_INCREMENT,
    `date` VARCHAR(10) NOT NULL,
    `msg_id` int not null,
    `msg_ts` bigint not null,
    `msg_ts_format` varchar(50) not null,
    `msg_type` int not null,
    `msg_title` text not null,
    `msg_content` longtext,
    `create_time` datetime,
    PRIMARY key (`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE INDEX index_tbl_msg on tbl_msg(msg_id);

create table if not EXISTS `tbl_pool_limit_up_down` (
    `id` int UNSIGNED AUTO_INCREMENT,
    `date` varchar(10) not null,
    `type` varchar(20) not null,
    `stock_code` varchar(20) not null,
    `stock_name` varchar(100) ,
    `reason` text,
    `content` longtext,
    `create_time` datetime,
    PRIMARY key (`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
create index index_tbl_pool_limit_up_down on tbl_pool_limit_up_down (`date`);
