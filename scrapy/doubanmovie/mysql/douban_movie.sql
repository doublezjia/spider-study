# Host: localhost  (Version: 5.5.53)
# Date: 2017-10-09 18:49:10
# Generator: MySQL-Front 5.3  (Build 4.234)

/*!40101 SET NAMES utf8 */;

#
# Structure for table "douban_movie"
#

DROP TABLE IF EXISTS `douban_movie`;
CREATE TABLE `douban_movie` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL COMMENT '名称',
  `cast` varchar(255) DEFAULT NULL COMMENT '主演',
  `reldate` varchar(255) DEFAULT NULL COMMENT '上映日期',
  `ratingnum` varchar(255) DEFAULT NULL COMMENT '评分',
  `quote` varchar(255) DEFAULT NULL COMMENT '引用',
  `addtime` varchar(255) DEFAULT NULL COMMENT '添加时间',
  PRIMARY KEY (`Id`)
) ENGINE=MyISAM AUTO_INCREMENT=26 DEFAULT CHARSET=utf8;
