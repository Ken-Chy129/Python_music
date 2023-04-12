/*
SQLyog Community v13.1.7 (64 bit)
MySQL - 8.0.26 : Database - pyhomework
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`pyhomework` /*!40100 DEFAULT CHARACTER SET utf8 */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `pyhomework`;

/*Table structure for table `collects` */

DROP TABLE IF EXISTS `collects`;

CREATE TABLE `collects` (
  `user` varchar(50) NOT NULL,
  `singer_name` varchar(50) DEFAULT NULL,
  `song_name` varchar(50) DEFAULT NULL,
  `song_url` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

/*Data for the table `collects` */

insert  into `collects`(`user`,`singer_name`,`song_name`,`song_url`) values 
('129496','陈奕迅','2001太空漫游','https://mp3.haoge500.com/hot/2004/07-13/26373.mp3'),
('129496','陈奕迅','冤家','https://mp3.haoge500.com/hot/2004/07-13/140.mp3'),
('129496','陈奕迅','防不胜防','https://mp3.haoge500.com/mp3/20/19819.mp3'),
('129496','陈奕迅','2001太空漫游','https://mp3.haoge500.com/hot/2004/07-13/26373.mp3'),
('129496','陈奕迅','防不胜防','https://mp3.haoge500.com/mp3/20/19819.mp3');

/*Table structure for table `downloads` */

DROP TABLE IF EXISTS `downloads`;

CREATE TABLE `downloads` (
  `user` varchar(50) NOT NULL,
  `singer_name` varchar(50) DEFAULT NULL,
  `song_name` varchar(50) DEFAULT NULL,
  `song_url` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

/*Data for the table `downloads` */

insert  into `downloads`(`user`,`singer_name`,`song_name`,`song_url`) values 
('129496','陈奕迅','防不胜防','https://mp3.haoge500.com/mp3/20/19819.mp3');

/*Table structure for table `users` */

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `username` varchar(50) COLLATE utf8_bin NOT NULL,
  `password` varchar(100) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8_bin;

/*Data for the table `users` */

insert  into `users`(`username`,`password`) values 
('123456789','123456789'),
('129496','123456'),
('Linno','123456'),
('xxx','129496');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
