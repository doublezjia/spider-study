# Host: localhost  (Version: 5.5.53)
# Date: 2017-09-30 14:55:58
# Generator: MySQL-Front 5.3  (Build 4.234)

/*!40101 SET NAMES utf8 */;

#
# Structure for table "qiubai"
#

DROP TABLE IF EXISTS `qiubai`;
CREATE TABLE `qiubai` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL COMMENT '用户',
  `follower` varchar(255) DEFAULT NULL COMMENT '粉丝',
  `follow` varchar(255) DEFAULT NULL COMMENT '关注',
  `discuss` varchar(255) DEFAULT NULL COMMENT '评论',
  `accelerated_again` varchar(255) DEFAULT NULL COMMENT '糗事',
  `choice` varchar(255) DEFAULT NULL COMMENT '精选',
  `smiling_face` varchar(255) DEFAULT NULL COMMENT '笑脸',
  `avatar` varchar(255) DEFAULT NULL COMMENT '头像',
  `curtime` varchar(255) DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`Id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

#
# Structure for table "weather"
#

DROP TABLE IF EXISTS `weather`;
CREATE TABLE `weather` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL COMMENT '地方名',
  `temperature` varchar(255) DEFAULT NULL COMMENT '温度',
  `date` date DEFAULT NULL COMMENT '日期',
  PRIMARY KEY (`Id`)
) ENGINE=MyISAM AUTO_INCREMENT=25 DEFAULT CHARSET=utf8;
