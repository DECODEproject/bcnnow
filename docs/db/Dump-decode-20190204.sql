-- MySQL dump 10.13  Distrib 5.7.25, for Linux (x86_64)
--
-- Host: localhost    Database: bcnnow
-- ------------------------------------------------------
-- Server version	5.7.25-0ubuntu0.16.04.2

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
-- Table structure for table `dataset`
--

DROP TABLE IF EXISTS `dataset`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dataset` (
  `id` int(11) NOT NULL,
  `typeof` varchar(45) NOT NULL DEFAULT 'public',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dataset`
--

LOCK TABLES `dataset` WRITE;
/*!40000 ALTER TABLE `dataset` DISABLE KEYS */;
INSERT INTO `dataset` VALUES (1,'public'),(2,'private'),(3,'public'),(4,'public'),(5,'public'),(6,'public'),(7,'public'),(8,'public'),(9,'public'),(10,'public');
/*!40000 ALTER TABLE `dataset` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dataset_community`
--

DROP TABLE IF EXISTS `dataset_community`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dataset_community` (
  `dataset_id` int(11) NOT NULL,
  `community_id` varchar(45) NOT NULL,
  PRIMARY KEY (`dataset_id`,`community_id`),
  CONSTRAINT `fk_dataset_community_1` FOREIGN KEY (`dataset_id`) REFERENCES `dataset` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dataset_community`
--

LOCK TABLES `dataset_community` WRITE;
/*!40000 ALTER TABLE `dataset_community` DISABLE KEYS */;
INSERT INTO `dataset_community` VALUES (4,'iot_community_1'),(5,'iot_community_1');
/*!40000 ALTER TABLE `dataset_community` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oauth2_client`
--

DROP TABLE IF EXISTS `oauth2_client`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `oauth2_client` (
  `client_id` varchar(48) DEFAULT NULL,
  `client_secret` varchar(120) DEFAULT NULL,
  `issued_at` int(11) NOT NULL,
  `expires_at` int(11) NOT NULL,
  `redirect_uri` text NOT NULL,
  `token_endpoint_auth_method` varchar(48) DEFAULT NULL,
  `grant_type` text NOT NULL,
  `response_type` text NOT NULL,
  `scope` text NOT NULL,
  `client_name` varchar(100) DEFAULT NULL,
  `client_uri` text,
  `logo_uri` text,
  `contact` text,
  `tos_uri` text,
  `policy_uri` text,
  `jwks_uri` text,
  `jwks_text` text,
  `i18n_metadata` text,
  `software_id` varchar(36) DEFAULT NULL,
  `software_version` varchar(48) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `ix_oauth2_client_client_id` (`client_id`),
  CONSTRAINT `oauth2_client_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oauth2_client`
--

LOCK TABLES `oauth2_client` WRITE;
/*!40000 ALTER TABLE `oauth2_client` DISABLE KEYS */;
INSERT INTO `oauth2_client` VALUES ('AzrWLH8xw1xGYoPBBt1lP4xl','V2CQt67jOXTpeV4BrDMumQOcka1HEpQmDWp72l1mnutz52j8',1542730153,0,'','client_secret_basic','password','','profile',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,1);
/*!40000 ALTER TABLE `oauth2_client` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oauth2_code`
--

DROP TABLE IF EXISTS `oauth2_code`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `oauth2_code` (
  `code` varchar(120) NOT NULL,
  `client_id` varchar(48) DEFAULT NULL,
  `redirect_uri` text,
  `response_type` text,
  `scope` text,
  `auth_time` int(11) NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `oauth2_code_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oauth2_code`
--

LOCK TABLES `oauth2_code` WRITE;
/*!40000 ALTER TABLE `oauth2_code` DISABLE KEYS */;
/*!40000 ALTER TABLE `oauth2_code` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oauth2_token`
--

DROP TABLE IF EXISTS `oauth2_token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `oauth2_token` (
  `client_id` varchar(48) DEFAULT NULL,
  `token_type` varchar(40) DEFAULT NULL,
  `access_token` varchar(255) NOT NULL,
  `refresh_token` varchar(255) DEFAULT NULL,
  `scope` text,
  `revoked` tinyint(1) DEFAULT NULL,
  `issued_at` int(11) NOT NULL,
  `expires_in` int(11) NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `access_token` (`access_token`),
  KEY `user_id` (`user_id`),
  KEY `ix_oauth2_token_refresh_token` (`refresh_token`),
  CONSTRAINT `oauth2_token_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oauth2_token`
--

LOCK TABLES `oauth2_token` WRITE;
/*!40000 ALTER TABLE `oauth2_token` DISABLE KEYS */;
INSERT INTO `oauth2_token` VALUES ('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','dDDOgSBDldPFdpgIN4vddjRpjY5TY8eVBRQIIFAA6b','JYNIQKzJ115MRH3CbJFokZ97tBBCFSL7oGIjjyqC677d0sgh','profile',0,1542730902,864000,1,1),('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','tKvGkY6N2By87zxhErWNft2V5MzanDVkGlJmmKSuXL','M3YLYqb1bcMtFM7cmvlXnU7j7P7ppysUPgJJVwOV9NJhx5Yo','profile',0,1542787563,864000,2,1),('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','dQwzbI0AnoBh3DLeKsbQfUBUJI6T8YSREAcj4Y14Qb','ml1s2D0gymiowLWTcBlDyqdh6SO5ZjJnWecY6NsUmPIGx1j3','profile',0,1542788129,864000,3,1),('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','lJeRgi985agb8gie9Ywxuf3LRzZjPx7CYkWSuiq3to','d7Nl6I6q4Chcf9k3uL58OkFxU01UIbxTFz1EmtmXG0uiUn2j','profile',0,1542788155,864000,4,1),('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','UmeKMqhGURst4iyaG9w7J6vHJzjbOdskQX2RcBl1xW','bk5jrxs2RvJOQM2ypbn3AEMCBfgkXgEr06UCGPfC2RTSUIBI','profile',0,1542788384,864000,5,1),('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','er1owIzdLeLtXoKmQqxvlZ06BHn4Ecp1B0pb3Aob6p','SKLYTQpfTzhwosjRjqA4dy6sm4TH6tl0i3aVntJKwBsbCiY8','profile',0,1542792187,864000,6,1),('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','HmqT4xPW6CXqAzBwiYqIlWYBGn7akrXDTQN6qCEes3','sea1wN8iS7GU4NWeNHIPeNjPTh8rLnSouBft67amz1YK3yhj','profile',0,1542792288,864000,7,1),('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','8GN3M4bDfeWYnKhAefBEa7UKbid3uYUIoOfKmC6wLp','5OZRNCPVdprLXVIcYtuaQISUi0jey8Ril1I5rK3H5IXXOrRU','profile',0,1542800689,864000,8,1),('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','PAMCaJiDdpZqpCerAMsDwk8SjjaHkdlxpvGR7OKUgK','sIXpmlpUj7uwwpbtKNicZEt15pGQLoi0lsRq8Dq9X0iR19il','profile',0,1543921885,864000,9,1),('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','lOkcCtrjZOQjWplj5W3xsigNcFsmkxCkMwdXgFVjmU','DPbsYZP6nxGvo3EUVUOu1b8SjIURej5I2TGyOgJC8Hg9Fwum','profile',0,1543924945,864000,10,1),('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','iIx2US7OUcXx6Atw3rJ6WdzRYnBvJ1cwFTG4H7N0Xp','FSmFHSlxzNPpx0zyDJbQ0oMLyfdQY17DgOK7AcYkR66b51Ir','profile',0,1543931276,864000,11,1),('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','Sm2kOHRvIuRnJUz0UOw4ci3MWkNyjt0kP1YFDCxe20','c0y8sFFS0YPV0n1m3whJwURxjD2aGNyBuAYMKCt6f2smtJP8','profile',0,1543931293,864000,12,1),('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','gs1p9pZP8xJ2Ahp4HEJ0AgQ2f03MPxdR9gg0qQz9SU','IxzitmzmGE0EVgpgRodsxYF1wIjVn6Dzf5ojLuwlrVWLL1wD','profile',0,1543931311,864000,13,1),('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','nzWvw5lcexQkdIxPZocGpbwImPDzligjPOEHGL2rQH','6d3au910CPfv2eDpPb4IcBmNtuXlNv6ruEr5wuklV3FTAbbo','profile',0,1543931376,864000,14,1),('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','tFFYh8mVz17H7rvuvXoLEYlLsV9LC1cu4KcYq4YSks','QslVexsMxFQQMi5YMDWcqBVZ4Em52Wh8PqED3fNbgnNugPHq','profile',0,1543931396,864000,15,1),('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','HBlQrk2u4F3wohwpOtJWSjyANGnrKVs5JXssl3rBSx','yRSICFkC9WZhpZ0VBzNngYfJfW5VV9tIMrtY9cJpuE5mOdk9','profile',0,1543932587,864000,16,1),('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','sTGWe1GPp5wk7duukd8Xj2hZWDXf3GGOntLfxu6ct7','TCWRHCAi0mn8aAH3Tdu0VqGq5ziLt4HXHTxro4CnfTlKwNjh','profile',0,1543933452,864000,17,1),('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','cFUCQbAFWdbAWoTp0u52vlcDlxIhm96x5luBEVhVAL','VU87J73Q5a7Hn1KhESyKsWrCOZSWr0TAY5DlhwMRvcU4FJ04','profile',0,1543934425,864000,18,1),('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','KRGSpz6qH025Fqlxlb3edlStC6fG4CeUVLcfHfDt6a','MelgzK6vF3V8i9a3Db2nKy47xNsz0r2DtlHJ2G4K4DkhXING','profile',0,1543934458,864000,19,1),('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','zYMe4mVejShIDavFGeYFwiuDZNskA2Wm5c4hxE8Czk','UGQBAX2mOjxXZqFht8ztiFzn7Hk24Y2FdG7VBwH3ta79wlZ8','profile',0,1543937415,864000,20,1),('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','9AHbkut6g9UibkQojAIRwnrY7Q3FY7fmeVTlZzzavg','owDldV0YiGUtxavDaNaK8CY0lf56LpLi6pdexkpncylETJOs','profile',0,1543937446,864000,21,1),('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','57b8D80R8vx2A8kgephmcmecaX5SsOxtmcDp9HP3QA','IblpCYKd0FM0kaREPFDgQSZ7aoBX36gYgZa6FhHTIaW14bpR','profile',0,1543937927,864000,22,1),('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','zKX5JLkpFFcABO6SQy8D4uCQcfNm2Cto9oGxNhC4w2','VzRjbNqA5SuNvOVOwYfSux8O4GfImjSXfOUJZRTjLLwckrOP','profile',0,1544718500,864000,23,1),('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','72FXhKfdaW8KG3zbvN4immJ1xWqnKehhQX3Yh0gDMK','oCX5jFfVVcUYMCaHhvoGvRojJ0wjD5vKkzbD2b7AzOXw1naT','profile',0,1544718773,864000,24,1),('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','VG3AkBinwgBGOKJYxaRIqo5N3M38OeskMcqRjmW05v','hEpIt4Y9dFV8i3PvAaoRJppHFK1l72O0xx9muZkp855fTddb','profile',0,1544772379,864000,25,1),('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','zdWg78XsO6wkKaCrJQ02iF7S9xDUHppiC4HzBKHTkd','PpudH8BNZedlWlbz9qMAvl9qP7gXVfRIGrt9iY5kqgWGNiUv','profile',0,1544778566,864000,26,1),('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','gbwZpHhp0UydysfyQezQlhQmv9WysdzVhli7lgvzb1','KK4R1OYG31vvvc24H5FK2l50ZIqRbKVNxbVnj0SDX8WJimWK','profile',0,1544786351,864000,27,1),('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','LGRd9s4Hslf6mJXhqiZCIL80yh4TFrYF4r1uSRTSDv','mw9BRTOuisVn1fXx4oUhqgYof77p1KogYUkTE6dgRNp43o0c','profile',0,1544794790,864000,28,1),('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','o3xbL6Orv8uXyWvbpt7ogTmd7rhBfJ0sqakRZXr8z9','9MFOGvp9v18EBCCNK14Y3Gcghj5YCzlxiRp6QkvhibA4XYdt','profile',0,1545046803,864000,29,2),('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','5RiryZWvivY7KCrTa6xECk145kEvqfkhmwWc8E4mp0','rJn7ooCkMOv959uofRUHRO6weoyKpXdoOgLwdYR0tEKiE7e9','profile',0,1545048989,864000,30,1),('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','e59gX9ZozAJEV82pULqO5z7ZNxAN5bugjQZFDxxxhd','d0a0x32H43gtyzsXLeNyz9nKc5T0o2HmbYZIDIFVrNEV4XNk','profile',0,1546437647,864000,31,4),('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','MK3adn5ek4m8kDRspKj7y1jDyGEL8gDJpSDGy4W3Ge','rA2dUPPOxWjqAGplkSlBJZONJtsTCxyrvWSzwJUw7GAtvM8A','profile',0,1546504477,864000,32,4),('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','73tfxCDCL4THiD31zTUtomRuZNHZLVirFrmehbHgGk','KNrB53B9leITmq1T5MdpVthz1HZWS0nIj49fX5XOSYiy98rK','profile',0,1546506807,864000,33,4),('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','SIzwCs9ONcKedwGK0wITAJ8xl7DETFbnE8Nsm15OWB','qdEHrQ6kgcy3KUzET6Tz6mHJraJZrar7CZHvzEXw99P7b3v9','profile',0,1546507004,864000,34,4),('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','ciNDrjFQLicpv0fCFe8seaQzYDXWeyZVY1FR0YnAWo','vQfFbK9c8mM138daDmCAGjuusjYGZaFr4eSaksbp1XthqNpf','profile',0,1546507039,864000,35,4),('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','oqNVaECLw2btz8ss6rPRJ6osAvBA4ReEHOyKenI4Ns','iO2SiBkj2vqNI0bVT9XBwu2rCbwSYUehf3VkMe8aTyhmzYQc','profile',0,1546512188,864000,36,4),('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','hd99fvTfEMj3DaL8dpjlmgEby0gSEC6Pkd6bLNHcUk','EWZFLz1tIXrgkQMHHaqPqeh3du6Owr4zYPHx9fhXOFQSGiA4','profile',0,1546512244,864000,37,4),('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','Di23GF25I0RqiIBxJFeQpmiNdWXQzoeE5bT4mrWsuA','FgYvkGoSxwOXhRcVg9Cw9NE2W4050NE3zNmZDdxarwvyEoEA','profile',0,1546513332,864000,38,4),('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','6J96jHb9PbUN1EhaqfoFZPrImoD8j9rBlWAG9QG2Vu','UNjU69s7ZT8h5K8ZjNXBHQrpnBXN86MQLRo5NLtJmCfD40eN','profile',0,1546514917,864000,39,7),('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','eMI7Gb2cabtXrtYj8Gb417pAlSNQ5ysVKsrYxiFr7V','eEeKfJsCtwBfFnWHJ3GTQZSwSfBi51ctAW9RbBTEirf5LiJb','profile',0,1546515068,864000,40,8),('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','QjzuHLeEJt48Wa3KkjlMqRY5D5Xa167K2snMsYm1y9','fR8AV8bpUwS2R2lHt7lc6hIpdmsnvnj10teD88Tn1srqavnm','profile',0,1548933036,864000,41,1),('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','2iz7TnhMJN8IvdGYHwrCMcu7BT4RHIjRdMs9IWOOiI','hTf1GHrbphdmjWHHrZGQJGm3gjWL2oRfJefp054MDTI6dZAa','profile',0,1548947868,864000,42,1),('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','UiZwkxyg0rpFC7xcdTywio5rO5yIj72np5U0Uv8YgX','dH811cmoVJIL85wwZJYCJXygUk6OZE7KXzfm5xVK4rhYnJcM','profile',0,1548948682,864000,43,1),('AzrWLH8xw1xGYoPBBt1lP4xl','Bearer','LVZpJwFc59BevbqXoMhATUedpzyrABKmfFPvWC7D1E','8hFdvXkbBwijj0dMi6hrbzQCmMeVhm4bZgCjLDWMTX4QmAFI','profile',0,1549005518,864000,44,1);
/*!40000 ALTER TABLE `oauth2_token` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(40) DEFAULT NULL,
  `password` varchar(65) DEFAULT NULL,
  `profile_name` varchar(45) DEFAULT NULL,
  `profile_title` varchar(45) DEFAULT NULL,
  `profile_city` varchar(45) DEFAULT NULL,
  `profile_age` varchar(45) DEFAULT NULL,
  `profile_area` varchar(45) DEFAULT NULL,
  `profile_community` varchar(45) DEFAULT NULL,
  `iot_user_id` varchar(45) DEFAULT NULL,
  `community_id` varchar(45) DEFAULT NULL,
  `login_method` varchar(45) NOT NULL DEFAULT 'internal',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `fk_user_1_idx` (`community_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'jordi0','ec654fac9599f62e79e2706abef23dfb7c07c08185aa86db4d8695f0b718d1b3','Jordi Allue','Barcelona','Barcelona','37','Guinardó','IOT',NULL,'iot_community_1','internal'),(2,'b024db1fac09dd6374c9df99','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'internal'),(3,'259c9ce1fd9baeacf996b14a',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'internal'),(4,'537cb7bfa0d5fc31dbc9f52f',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'iot'),(5,'5d4863ad40d03bc65cc5ed4e',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'iot'),(6,'601a1c7c82d46662c27e0d18',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'iot'),(7,'d583acfad93261798ff33fdc',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'iot'),(8,'04fd9e8d983c8e8f98acd002',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'iot');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-02-04 14:31:54
