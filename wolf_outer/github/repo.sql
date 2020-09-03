CREATE TABLE IF NOT EXISTS `tb_basic_info` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `repo_id` VARCHAR(64) NULL DEFAULT NULL comment '唯一id',
    `repo_name` VARCHAR(256) NULL DEFAULT NULL comment '显示标题',
    `commit_count` INT(11) NULL DEFAULT NULL comment '',
    `branch_count` INT(11) NULL DEFAULT NULL comment '',
    `package_count` INT(11) NULL DEFAULT NULL comment '',
    `release_count` INT(11) NULL DEFAULT NULL comment '',
    `contributors_count` INT(11) NULL DEFAULT NULL comment '',
    `watch_count` INT(11) NULL DEFAULT NULL comment '',
    `star_count` INT(11) NULL DEFAULT NULL comment '',
    `fork_count` INT(11) NULL DEFAULT NULL comment '',
    `issue_count` INT(11) NULL DEFAULT NULL comment '',
    `pull_request_count` INT(11) NULL DEFAULT NULL comment '',
    `tags_count` INT(11) NULL DEFAULT NULL comment '',
    `license` text NULL DEFAULT NULL comment '',
    `topic` TEXT NULL DEFAULT NULL comment '',
    `languages` JSON NULL DEFAULT NULL comment '',
    `link` TEXT NULL DEFAULT NULL comment '',
    `get_ts` BIGINT(20) NULL DEFAULT '0' comment '获取时间',
    PRIMARY KEY (`id`) USING BTREE,
    unique index tb_basic_info_repo_name_idx (`repo_name`)
) COLLATE='utf8mb4_general_ci' ENGINE=InnoDB;


CREATE TABLE IF NOT EXISTS `tb_release_version` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `repo_id` VARCHAR(64) NULL DEFAULT NULL comment '',
    `repo_name` VARCHAR(256) NULL DEFAULT NULL comment '',
    `version_name` VARCHAR(256) NULL DEFAULT NULL comment '',
    `version_id` VARCHAR(64) NULL DEFAULT NULL comment '',
    `release_time` VARCHAR(64) NULL DEFAULT NULL comment '',
    `contributors` JSON NULL DEFAULT NULL comment '',
    `link` VARCHAR(1024) NULL DEFAULT NULL comment '',
    release_documents TEXT NULL DEFAULT NULL comment '',
    `source_link` VARCHAR(1024) NULL DEFAULT NULL comment '',
    `tag_id` VARCHAR(64) NULL DEFAULT NULL comment '',
    verified VARCHAR(64) NULL DEFAULT NULL comment '',
    `get_ts` BIGINT(20) NULL DEFAULT '0' comment '获取时间',
    PRIMARY KEY (`id`) USING BTREE,
    unique index tb_release_version_repo_name_version_name_idx (`repo_name`, `version_name`),
    INDEX `tb_release_version_repo_name_IDX` (`repo_name`) USING BTREE
) COLLATE='utf8mb4_general_ci' ENGINE=InnoDB;


CREATE TABLE IF NOT EXISTS `tb_commits` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `repo_id` VARCHAR(64) NULL DEFAULT NULL comment '',
    `repo_name` VARCHAR(256) NULL DEFAULT NULL comment '',
    tag_id VARCHAR(64) NULL DEFAULT NULL comment '',
    commit_id VARCHAR(64) NULL DEFAULT NULL comment '',
    commitor VARCHAR(64) NULL DEFAULT NULL comment '',
    author VARCHAR(64) NULL DEFAULT NULL comment '',
    commit_time VARCHAR(64) NULL DEFAULT NULL comment '',
    link VARCHAR(1024) NULL DEFAULT NULL comment '',
    checkstatus VARCHAR(64) NULL DEFAULT NULL comment '',
    verified VARCHAR(64) NULL DEFAULT NULL comment '',
    commit_text text NULL DEFAULT NULL comment '',
    `get_ts` BIGINT(20) NULL DEFAULT '0' comment '获取时间',
    PRIMARY KEY (`id`) USING BTREE,
    unique index tb_commits_repo_name_tag_id_commit_id_idx (`repo_name`, `tag_id`, `commit_id`),
    INDEX `tb_commits_repo_name_IDX` (`repo_name`) USING BTREE
) COLLATE='utf8mb4_general_ci' ENGINE=InnoDB;


CREATE TABLE IF NOT EXISTS `tb_issues` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `repo_id` VARCHAR(64) NULL DEFAULT NULL comment '',
    `repo_name` VARCHAR(256) NULL DEFAULT NULL comment '',
    issue_id INT(11) NULL DEFAULT NULL comment '',
    issue_link VARCHAR(1024) NULL DEFAULT NULL comment '',
    issue_title VARCHAR(1024) NULL DEFAULT NULL comment '',
    issue_label VARCHAR(1024) NULL DEFAULT NULL comment '',
    issue_project VARCHAR(1024) NULL DEFAULT NULL comment '',
    issue_milestones VARCHAR(1024) NULL DEFAULT NULL comment '',
    issue_linked_pull_request VARCHAR(1024) NULL DEFAULT NULL comment '',
    open_time VARCHAR(64) NULL DEFAULT NULL comment '',
    participants VARCHAR(1024) NULL DEFAULT NULL comment '',
    commitors VARCHAR(1024) NULL DEFAULT NULL comment '',
    assigners VARCHAR(1024) NULL DEFAULT NULL comment '',
    assignee VARCHAR(128) NULL DEFAULT NULL comment '',
    `issue_network_links` JSON NULL DEFAULT NULL comment '',
    issue_text text NULL DEFAULT NULL comment '',
    `get_ts` BIGINT(20) NULL DEFAULT '0' comment '获取时间',
    PRIMARY KEY (`id`) USING BTREE,
    unique index tb_issues_repo_name_issue_id_idx (`repo_name`, `issue_id`),
    INDEX `tb_issues_repo_name_IDX` (`repo_name`) USING BTREE
) COLLATE='utf8mb4_general_ci' ENGINE=InnoDB;


CREATE TABLE IF NOT EXISTS `tb_pull_requests` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `repo_id` VARCHAR(64) NULL DEFAULT NULL comment '',
    `repo_name` VARCHAR(256) NULL DEFAULT NULL comment '',
    pull_request_id INT(11) NULL DEFAULT NULL comment '',
    pull_request_link VARCHAR(1024) NULL DEFAULT NULL comment '',
    pull_request_title VARCHAR(1024) NULL DEFAULT NULL comment '',
    pull_request_label VARCHAR(1024) NULL DEFAULT NULL comment '',
    pull_request_project VARCHAR(1024) NULL DEFAULT NULL comment '',
    pull_request_milestones VARCHAR(1024) NULL DEFAULT NULL comment '',
    linked_issue VARCHAR(1024) NULL DEFAULT NULL comment '',
    open_time VARCHAR(64) NULL DEFAULT NULL comment '',
    participants VARCHAR(1024) NULL DEFAULT NULL comment '',
    commitors VARCHAR(1024) NULL DEFAULT NULL comment '',
    assigners VARCHAR(1024) NULL DEFAULT NULL comment '',
    assignee VARCHAR(128) NULL DEFAULT NULL comment '',
    `get_ts` BIGINT(20) NULL DEFAULT '0' comment '获取时间',
    PRIMARY KEY (`id`) USING BTREE,
    unique index tb_pull_requests_repo_name_pull_request_id_idx (`repo_name`, `pull_request_id`),
    INDEX `tb_pull_requests_repo_name_IDX` (`repo_name`) USING BTREE
) COLLATE='utf8mb4_general_ci' ENGINE=InnoDB;























