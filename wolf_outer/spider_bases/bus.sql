CREATE TABLE IF NOT EXISTS `tb_goods` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `uuid` VARCHAR(40) NOT NULL,
    `brandId` VARCHAR(64) NULL DEFAULT NULL COMMENT '频道id',
    `productId` VARCHAR(64) NULL DEFAULT NULL COMMENT '产品id',
    `good_id` VARCHAR(64) NULL DEFAULT NULL COMMENT '物品id(详情中的)',
    `title` VARCHAR(64) NULL DEFAULT NULL COMMENT '标题',
    `pic` VARCHAR(256) NULL DEFAULT NULL COMMENT '图片url',
    `detail` VARCHAR(256) NULL DEFAULT NULL COMMENT '链接',
    `saleDiscount` VARCHAR(40) NULL DEFAULT NULL COMMENT 'discount',
    `discount` float NULL DEFAULT NULL COMMENT 'discount',
    `price` float NULL DEFAULT NULL COMMENT 'price',
    `marketPrice` float NULL DEFAULT NULL COMMENT 'marketPrice',
    `source_extern` VARCHAR(256) NULL DEFAULT NULL COMMENT 'source的其他',
    `source` VARCHAR(64) NULL DEFAULT NULL COMMENT '来源(如vip)',
    `du_price` float NULL DEFAULT NULL COMMENT 'du price',
    `du_count` INT(11) NULL DEFAULT NULL COMMENT 'du count',
    `extern` JSON NULL DEFAULT NULL COMMENT 'extern',
    `sold_items` JSON NULL DEFAULT NULL COMMENT '当前详情',
    `updated_ts` BIGINT(20) NULL DEFAULT NULL,
    `updated_date` DATETIME NULL DEFAULT NULL,
    `updated_day` VARCHAR(16) NULL DEFAULT NULL,
    PRIMARY KEY (`id`),
    UNIQUE INDEX `tb_goods_uuid_price_source_updated_day_IDX` (`uuid`, `price`, `source`, `updated_day`) USING BTREE,
    INDEX `tb_goods_uuid_IDX` (`uuid`) USING BTREE,
    INDEX `tb_goods_discount_IDX` (`discount`) USING BTREE,
    INDEX `tb_goods_updated_ts_IDX` (`updated_ts`) USING BTREE
)
COLLATE='utf8mb4_general_ci' ENGINE=InnoDB;


alter table tb_goods add column sold_items JSON NULL DEFAULT NULL comment '当前详情' after extern;


CREATE TABLE IF NOT EXISTS `tb_guanwang` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `uuid` VARCHAR(40) NOT NULL,
    `productId` VARCHAR(64) NULL DEFAULT NULL COMMENT '产品id',
    `good_id` VARCHAR(64) NULL DEFAULT NULL COMMENT '物品id(详情中的)',
    `title` VARCHAR(64) NULL DEFAULT NULL COMMENT '标题',
    `pic` VARCHAR(256) NULL DEFAULT NULL COMMENT '图片url',
    `detail` VARCHAR(256) NULL DEFAULT NULL COMMENT '链接',
    `discount` float NULL DEFAULT NULL COMMENT 'discount',
    `price` float NULL DEFAULT NULL COMMENT 'price',
    `fullPrice` float NULL DEFAULT NULL COMMENT 'fullPrice',
    `salesChannel` JSON NULL DEFAULT NULL COMMENT 'sale channels',
    `source` VARCHAR(64) NULL DEFAULT NULL COMMENT '来源',
    `du_price` float NULL DEFAULT NULL COMMENT 'du price',
    `du_count` INT(11) NULL DEFAULT NULL COMMENT 'du count',
    `extern` JSON NULL DEFAULT NULL COMMENT 'extern',
    `sold_items` JSON NULL DEFAULT NULL COMMENT '当前详情',
    `updated_ts` BIGINT(20) NULL DEFAULT NULL,
    `updated_date` DATETIME NULL DEFAULT NULL,
    `updated_day` VARCHAR(16) NULL DEFAULT NULL,
    PRIMARY KEY (`id`),
    UNIQUE INDEX `tb_guanwang_uuid_price_source_updated_day_IDX` (`uuid`, `price`, `source`, `updated_day`) USING BTREE,
    INDEX `tb_guanwang_uuid_IDX` (`uuid`) USING BTREE,
    INDEX `tb_guanwang_discount_IDX` (`discount`) USING BTREE,
    INDEX `tb_guanwang_updated_ts_IDX` (`updated_ts`) USING BTREE
)
COLLATE='utf8mb4_general_ci' ENGINE=InnoDB;












