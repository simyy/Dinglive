# TV
CREATE TABLE `tv` (
      `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
      `anchor` varchar(32) NOT NULL COMMENT '主播姓名',
      `avatar` varchar(1024) NOT NULL COMMENT '主播头像',
      `room_id` varchar(128) NOT NULL COMMENT '房间ID',
      `room_name` varchar(128) NOT NULL COMMENT '房间名称',
      `room_site` varchar(1024) NOT NULL COMMENT '房间地址',
      `update_time` datetime NOT NULL COMMENT '最近更新时间',
      `is_online` int(2) NOT NULL COMMENT '是否上线 0为离线，1为在线',
      `fans_count` int(11) NOT NULL COMMENT '粉丝数量',
      `audience_count` int(11) NOT NULL COMMENT '观众数量',
      `category_id` int(3) NOT NULL COMMENT '直播类型id',
      `source_id` int(3) NOT NULL COMMENT '直播来源id 0斗鱼，1战旗，2熊猫，3龙珠，4虎牙',
      PRIMARY KEY (`id`),
      UNIQUE KEY `idx_room_id_srouce_id` (`room_id`, `source_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

# 来源
CREATE TABLE `tv_source` (
      `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
      `name` varchar(32) NOT NULL COMMENT '来源名称',
      `pic` varchar(256) NULL COMMENT '图片',
      `url` varchar(1024) NULL COMMENT '地址',
      `count` int(11) NOT NULL DEFAULT 0 COMMENT '来源总数',
      PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

# 分类
CREATE TABLE `tv_category` (
      `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
      `name` varchar(32) NOT NULL COMMENT '分类名称',
      `pic` varchar(256) NULL COMMENT '图片位置',
      `count` int(11) NULL DEFAULT 0 COMMENT '总数',
      PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
