-- MySQL dump 10.13  Distrib 5.5.28, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: aligilo
-- ------------------------------------------------------
-- Server version	5.5.28-0ubuntu0.12.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `ijk_landoj`
--

DROP TABLE IF EXISTS `ijk_landoj`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ijk_landoj` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `nomo` varchar(20) COLLATE utf8_esperanto_ci NOT NULL,
  `kodo` char(2) CHARACTER SET ascii NOT NULL COMMENT 'kodo laŭ ISO-3166-1',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=83 DEFAULT CHARSET=utf8 COLLATE=utf8_esperanto_ci COMMENT='La landoj, el kiuj povus veni la partoprenantoj';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ijk_landoj`
--

LOCK TABLES `ijk_landoj` WRITE;
/*!40000 ALTER TABLE `ijk_landoj` DISABLE KEYS */;
INSERT INTO `ijk_landoj` VALUES (7,'Sirio','SY'),(8,'Au^strio','AT'),(9,'C^inio','CN'),(10,'Belgio','BE'),(11,'Benino','BJ'),(12,'Britio','GB'),(13,'Danlando','DK'),(14,'Finnlando','FI'),(15,'Francio','FR'),(16,'Germanio','DE'),(17,'Hispanio','ES'),(18,'Hungario','HU'),(19,'Irlando','IE'),(20,'Irano','IR'),(21,'Italio','IT'),(22,'Jugoslavio','YU'),(23,'Kanado','CA'),(24,'Lih^tens^tejno','LI'),(25,'Luksemburgio','LU'),(26,'Litovio','LT'),(27,'Meksiko','MX'),(28,'Monako','MC'),(29,'Nederlando','NL'),(30,'Norvegio','NO'),(31,'Pollando','PL'),(32,'Portugalio','PT'),(33,'Rusio','RU'),(34,'San Marino','SM'),(35,'Slovakio','SK'),(36,'Svedio','SE'),(37,'Svislando','CH'),(38,'Urugvajo','UY'),(39,'Usono','US'),(40,'Vatikano','VA'),(41,'Andoro','AD'),(42,'C^eh^io','CZ'),(43,'Grekio','GR'),(44,'Kroatio','HR'),(45,'Malto','MT'),(46,'Slovenio','SI'),(47,'Alia Lando',''),(48,'Kongo','CD'),(49,'Ghanao','GH'),(50,'Kasah^stano','KZ'),(51,'Pakistanio','PK'),(52,'Romanio','RO'),(55,'Ukrainio','UA'),(56,'Nig^erio','NG'),(57,'Nepalo','NP'),(58,'Hindujo','IN'),(59,'Brazilo','BR'),(60,'Angolo','AO'),(61,'Ebur-Bordo','CI'),(62,'Israelo','IS'),(63,'Japanio','JP'),(64,'Suda Koreio','KR'),(65,'Makedonio','MK'),(66,'Togo','TG'),(67,'Argentinio','AR'),(69,'Bosnio','BA'),(70,'Bulgario','BG'),(72,'Latvio','LV'),(74,'Senegalo','SN'),(75,'Moldavujo','MD'),(76,'Malio','ML'),(77,'Katalunio',''),(78,'Alg^erio','DZ'),(79,'Serbio','RS'),(80,'Montenegro','ME'),(82,'Kubo','CU');
/*!40000 ALTER TABLE `ijk_landoj` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2012-12-07  7:08:43
