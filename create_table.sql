REPLACE INTO mysql.user (Host, User, Password) VALUES('localhost', 'cyber', password('cyber') );
FLUSH PRIVILEGES;
CREATE DATABASE IF NOT EXISTS cyber;
GRANT ALL PRIVILEGES ON cyber.* TO cyber@localhost IDENTIFIED BY 'cyber';
FLUSH PRIVILEGES;

USE cyber;

CREATE TABLE IF NOT EXISTS `contact_message` (
 `_id` char(32) NOT NULL COMMENT 'uuid',
 `email` varchar(255) DEFAULT NULL,
 `content` varchar(2000) DEFAULT NULL,
 `ctime` bigint(19) NOT NULL DEFAULT '0',
 PRIMARY KEY (`_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
