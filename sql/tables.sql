
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
CREATE INDEX tbl_limit_up_down_count on tbl_rise_fall_count(date);

