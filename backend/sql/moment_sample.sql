CREATE TABLE IF NOT EXISTS `moment` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '说说ID',
  `content` TEXT NOT NULL COMMENT '说说内容',
  `access_password` VARCHAR(255) DEFAULT NULL COMMENT '说说密码，留空则无需密码查看',
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建日期',
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改日期',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='空间说说表';

INSERT INTO `moment` (`content`, `access_password`, `create_time`, `update_time`) VALUES
('今天把博客的空间页结构定下来了，接下来把后台管理和密码访问一起补齐。', NULL, '2026-03-15 21:30:00', '2026-03-15 21:30:00'),
('凌晨改样式时突然觉得，时间线特别适合放这种碎碎念，轻一点也更真实。', NULL, '2026-03-16 00:18:00', '2026-03-16 00:18:00'),
('这条是加密示例：只有知道密码的人才能看到完整内容。', '$2b$12$example_replace_with_bcrypt_hash', '2026-03-16 23:40:00', '2026-03-16 23:40:00');
