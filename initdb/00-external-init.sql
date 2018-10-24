-- Set up authentication
CREATE USER 'external'@'%' IDENTIFIED BY 'external' ;
CREATE DATABASE IF NOT EXISTS `external`;
GRANT ALL ON `external`.* TO 'external'@'%' ;
USE external;

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Dumping structure for table feinstaub.auth_user
CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;

-- Dumping data for table feinstaub.auth_user: ~14 rows (approximately)
DELETE FROM `auth_user`;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
	(1, '...', '2017-04-25 17:37:19', 1, 'admin', '', '', 'test1@codefor.de', 1, 1, '2015-03-31 20:50:35'),
	(2, '...', '2017-04-25 17:37:19', 1, 'admin2', '', '', 'test2@codefor.de', 1, 1, '2015-03-31 20:50:35'),
	(3, '...', '2017-04-25 17:37:19', 1, 'admin3', '', '', 'test3@codefor.de', 1, 1, '2015-03-31 20:50:35');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;

-- Dumping structure for table feinstaub.sensors_sensortype
CREATE TABLE IF NOT EXISTS `sensors_sensortype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  `uid` varchar(50) NOT NULL,
  `name` varchar(1000) NOT NULL,
  `manufacturer` varchar(1000) NOT NULL,
  `description` varchar(10000) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uid` (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8;

-- Dumping data for table feinstaub.sensors_sensortype: ~28 rows (approximately)
DELETE FROM `sensors_sensortype`;
/*!40000 ALTER TABLE `sensors_sensortype` DISABLE KEYS */;
INSERT INTO `sensors_sensortype` (`id`, `created`, `modified`, `uid`, `name`, `manufacturer`, `description`) VALUES
	(1, '2015-04-03 22:50:35', '2015-04-03 22:50:35', 'PPD42NS', 'PPD42NS', 'Shinyei', 'http://www.sca-shinyei.com/pdf/PPD42NS.pdf'),
	(2, '2015-04-03 22:50:51', '2015-04-03 22:50:51', 'GP2Y1010AU0F', 'GP2Y1010AU0F', 'Sharp', ''),
	(3, '2015-04-03 22:51:07', '2015-04-03 22:51:07', 'dsm501a', 'dsm501a', 'Samyoung S&C', 'http://www.samyoungsnc.com/products/3-1%20Specification%20DSM501.pdf'),
	(4, '2015-04-03 22:51:22', '2015-04-03 22:51:22', 'SHT10', 'SHT10', 'Sensirion AG', ''),
	(5, '2015-04-03 22:51:30', '2015-04-03 22:51:30', 'SHT11', 'SHT11', 'Sensirion AG', ''),
	(6, '2015-04-03 22:51:36', '2015-04-03 22:51:36', 'SHT15', 'SHT15', 'Sensirion AG', ''),
	(7, '2015-04-03 22:52:14', '2017-08-13 16:32:35', 'DHT11', 'DHT11', 'various', 'temperature, humidity'),
	(8, '2015-05-03 16:51:54', '2017-08-13 16:31:51', 'BMP180', 'BMP180', 'Bosch', 'temperature, pressure, connected via I2C'),
	(9, '2015-05-24 22:17:47', '2017-08-13 16:32:29', 'DHT22', 'DHT22', 'various', 'temperature, humidity'),
	(10, '2015-06-20 14:30:35', '2015-06-20 14:30:35', 'photoresistor', 'photoresistor', 'various', ''),
	(11, '2015-07-10 21:20:45', '2015-07-10 21:20:45', 'doorswitch', 'doorswitch', 'various', ''),
	(12, '2015-09-27 14:39:26', '2015-09-27 14:39:26', 'DS18S20', 'DS18S20', 'Dallas semiconductor', '1-wire temperature sensor'),
	(13, '2015-10-30 01:29:16', '2015-10-30 01:29:16', 'DS18B20', 'DS18B20', 'Dallas semiconductor', '1-wire temperature sensor'),
	(14, '2016-01-26 18:48:38', '2017-11-16 13:11:43', 'SDS011', 'SDS011', 'Nova Fitness', 'particulate matter, PM2.5, PM10'),
	(15, '2016-04-04 12:55:38', '2016-04-04 12:55:49', 'GPS-NEO-6M', 'GPS-NEO-6M', 'ublox', 'GPS device for position and time measurements'),
	(16, '2017-01-03 17:57:36', '2017-08-13 16:39:41', 'PMS3003', 'PMS3003', 'Plantower', 'particulate matter, PM1, PM2.5, PM10'),
	(17, '2017-01-27 08:58:03', '2017-08-13 16:31:33', 'BME280', 'BME280', 'Bosch', 'temperature, humidity, pressure, connected via I2C'),
	(18, '2017-02-19 15:52:06', '2017-11-16 13:11:54', 'SDS021', 'SDS021', 'Nova Fitness', 'particulate matter, PM2.5, PM10'),
	(19, '2017-08-13 16:30:13', '2017-08-13 16:33:16', 'HTU21D', 'HTU21D', 'Measurement Specialties', 'temperature, humidity, connected via I2C'),
	(20, '2017-08-13 16:32:13', '2017-08-13 16:32:13', 'BMP280', 'BMP280', 'Bosch', 'temperature, pressure, connected via I2C'),
	(21, '2017-08-13 16:39:57', '2017-08-13 16:39:57', 'PMS1003', 'PMS1003', 'Plantower', 'particulate matter, PM1, PM2.5, PM10'),
	(22, '2017-08-13 16:40:10', '2017-08-13 16:40:10', 'PMS7003', 'PMS7003', 'Plantower', 'particulate matter, PM1, PM2.5, PM10'),
	(23, '2017-09-13 15:42:39', '2017-09-13 15:42:39', 'PMS5003', 'PMS5003', 'Plantower', 'particulate matter, PM1, PM2.5, PM10'),
	(24, '2017-09-13 15:42:56', '2017-09-13 15:42:56', 'PMS6003', 'PMS6003', 'Plantower', 'particulate matter, PM1, PM2.5, PM10'),
	(25, '2017-11-16 13:11:21', '2017-11-16 13:12:01', 'HPM', 'HPM', 'Honeywell', 'particulate matter, PM2.5, PM10'),
	(26, '2018-01-30 16:59:14', '2018-01-30 16:59:14', 'SHT30', 'SHT30', 'Sensirion', ''),
	(27, '2018-01-30 16:59:27', '2018-01-30 16:59:27', 'SHT31', 'SHT31', 'Sensirion', ''),
	(28, '2018-01-30 16:59:41', '2018-01-30 16:59:41', 'SHT35', 'SHT35', 'Sensirion', '');
/*!40000 ALTER TABLE `sensors_sensortype` ENABLE KEYS */;

-- Dumping structure for table feinstaub.sensors_sensorlocation
CREATE TABLE IF NOT EXISTS `sensors_sensorlocation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  `location` longtext DEFAULT NULL,
  `timestamp` datetime NOT NULL,
  `description` longtext DEFAULT NULL,
  `indoor` tinyint(1) NOT NULL,
  `owner_id` int(11) DEFAULT NULL,
  `latitude` decimal(14,11) DEFAULT NULL,
  `longitude` decimal(14,11) DEFAULT NULL,
  `city` longtext DEFAULT NULL,
  `industry_in_area` int(11) DEFAULT NULL,
  `oven_in_area` int(11) DEFAULT NULL,
  `postalcode` longtext DEFAULT NULL,
  `street_name` longtext DEFAULT NULL,
  `street_number` longtext DEFAULT NULL,
  `traffic_in_area` int(11) DEFAULT NULL,
  `country` longtext DEFAULT NULL,
  `altitude` decimal(14,8) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sensors_sensorlocation_5e7b1936` (`owner_id`),
  CONSTRAINT `sensors_sensorlocation_owner_id_01dfdd1d_fk_auth_user_id` FOREIGN KEY (`owner_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8002 DEFAULT CHARSET=utf8;

-- Dumping data for table feinstaub.sensors_sensorlocation: ~8,082 rows (approximately)
DELETE FROM `sensors_sensorlocation`;
/*!40000 ALTER TABLE `sensors_sensorlocation` DISABLE KEYS */;
INSERT INTO `sensors_sensorlocation` (`id`, `created`, `modified`, `location`, `timestamp`, `description`, `indoor`, `owner_id`, `latitude`, `longitude`, `city`, `industry_in_area`, `oven_in_area`, `postalcode`, `street_name`, `street_number`, `traffic_in_area`, `country`, `altitude`) VALUES
	(3, '2015-04-06 14:01:06', '2015-04-06 14:01:06', NULL, '2015-04-06 14:00:50', 'Hinterhof', 0, 2, 48.73275100000, 9.10254600000, 'Stuttgart - Vaihingen', NULL, NULL, '70563', 'Sternecker Str.', '6', NULL, 'DE', 452.42370000);
/*!40000 ALTER TABLE `sensors_sensorlocation` ENABLE KEYS */;

-- Dumping structure for table feinstaub.sensors_node
CREATE TABLE IF NOT EXISTS `sensors_node` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  `uid` varchar(50) NOT NULL,
  `description` longtext DEFAULT NULL,
  `location_id` int(11) NOT NULL,
  `owner_id` int(11) NOT NULL,
  `description_internal` longtext DEFAULT NULL,
  `email` varchar(254) DEFAULT NULL,
  `height` int(11) DEFAULT NULL,
  `sensor_position` int(11) DEFAULT NULL,
  `name` longtext DEFAULT NULL,
  `last_notify` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uid` (`uid`),
  KEY `sensors_node_e274a5da` (`location_id`),
  KEY `sensors_node_5e7b1936` (`owner_id`),
  CONSTRAINT `sensors_node_location_id_fed3caf3_fk_sensors_sensorlocation_id` FOREIGN KEY (`location_id`) REFERENCES `sensors_sensorlocation` (`id`),
  CONSTRAINT `sensors_node_owner_id_952b2ce4_fk_auth_user_id` FOREIGN KEY (`owner_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7879 DEFAULT CHARSET=utf8;

-- Dumping data for table feinstaub.sensors_node: ~7,852 rows (approximately)
DELETE FROM `sensors_node`;
/*!40000 ALTER TABLE `sensors_node` DISABLE KEYS */;
INSERT INTO `sensors_node` (`id`, `created`, `modified`, `uid`, `description`, `location_id`, `owner_id`, `description_internal`, `email`, `height`, `sensor_position`, `name`, `last_notify`) VALUES
	(1, '2015-08-07 23:00:21', '2015-08-07 23:00:21', 'esp8266-16630636', 'esp-12 (E)', 3, 2, NULL, 'testing@luftdaten.info', NULL, NULL, NULL, NULL);
/*!40000 ALTER TABLE `sensors_node` ENABLE KEYS */;


-- Dumping structure for table feinstaub.sensors_sensor
CREATE TABLE IF NOT EXISTS `sensors_sensor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  `description` longtext DEFAULT NULL,
  `sensor_type_id` int(11) NOT NULL,
  `node_id` int(11) NOT NULL,
  `pin` varchar(10) NOT NULL,
  `public` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sensors_sensor_node_id_5f5aa99a_uniq` (`node_id`,`pin`),
  KEY `sensors_sensor_7a592b3b` (`sensor_type_id`),
  KEY `sensors_sensor_c693ebc8` (`node_id`),
  CONSTRAINT `sensors_sensor_node_id_5a66f490_fk_sensors_node_id` FOREIGN KEY (`node_id`) REFERENCES `sensors_node` (`id`),
  CONSTRAINT `sensors_sensor_sensor_type_id_7c0ef1ec_fk_sensors_sensortype_id` FOREIGN KEY (`sensor_type_id`) REFERENCES `sensors_sensortype` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15775 DEFAULT CHARSET=utf8;

-- Dumping data for table feinstaub.sensors_sensor: ~15,628 rows (approximately)
DELETE FROM `sensors_sensor`;
/*!40000 ALTER TABLE `sensors_sensor` DISABLE KEYS */;
INSERT INTO `sensors_sensor` (`id`, `created`, `modified`, `description`, `sensor_type_id`, `node_id`, `pin`, `public`) VALUES
	(30, '2015-07-27 17:41:50', '2015-08-07 23:00:21', 'esp-12 (E)', 1, 1, '-', 0);
/*!40000 ALTER TABLE `sensors_sensor` ENABLE KEYS */;


/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
