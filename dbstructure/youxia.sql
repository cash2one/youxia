/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50527
 Source Host           : localhost
 Source Database       : jtm.im

 Target Server Type    : MySQL
 Target Server Version : 50527
 File Encoding         : utf-8

 Date: 01/02/2014 18:26:36 PM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `user`
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `username` text,
  `password` text,
  `nickname` text,
  `name` text,
  `gender` text,
  `email` text,
  `mobile` text,
  `sign` text,
  `avatar` text,
  `intro` text,
  `followees` int(11) DEFAULT 0,
  `followers` int(11) DEFAULT 0,
  `questions` int(11) DEFAULT 0,
  `answers` int(11) DEFAULT 0,
  `posts` int(11) DEFAULT 0,
  `comments` int(11) DEFAULT 0,
  `up_num` int(11) DEFAULT 0,
  `down_num` int(11) DEFAULT 0,
  `thank_num` int(11) DEFAULT 0,
  `report_num` int(11) DEFAULT 0,
  `reputation` int(11) DEFAULT 0,
  `income` int(11) DEFAULT 2000,
  `expend` int(11) DEFAULT 0,
  `permission` int(11) DEFAULT 0,
  `created` datetime DEFAULT NULL,
  `updated` datetime DEFAULT NULL,
  `last_login` datetime DEFAULT NULL,
  `view_follow` datetime DEFAULT NULL,
  `admin` text,
  PRIMARY KEY (`uid`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `post`
-- ----------------------------
DROP TABLE IF EXISTS `post`;
CREATE TABLE `post` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` text,
  `subtitle` text,
  `thumb` text,
  `link` text,
  `dlink` text,
  `post_type` text,
  `source` text,
  `price` text,
  `vendor` text,
  `author_name` text,
  `up_num` text,
  `down_num` text,
  `reply_num` text,
  `follow_num` text,
  `content` longtext,
  `processed_content` longtext,
  `author_id` text,
  `updated` datetime DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `nowfeed`
-- ----------------------------
DROP TABLE IF EXISTS `nowfeed`;
CREATE TABLE `nowfeed` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `avatar` text,
  `name` text,
  `subname` text,
  `content` text,
  `image` text,
  `source` text,
  `link` text,
  `nowfeed_type` text,
  `video_time` text,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
