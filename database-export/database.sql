CREATE DATABASE  IF NOT EXISTS `smartwekker` /*!40100 DEFAULT CHARACTER SET utf8 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `smartwekker`;
-- MySQL dump 10.13  Distrib 8.0.28, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: smartwekker
-- ------------------------------------------------------
-- Server version	8.0.28

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `actie`
--

DROP TABLE IF EXISTS `actie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `actie` (
  `actieID` int NOT NULL AUTO_INCREMENT,
  `beschrijving` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`actieID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `actie`
--

LOCK TABLES `actie` WRITE;
/*!40000 ALTER TABLE `actie` DISABLE KEYS */;
INSERT INTO `actie` VALUES (1,'LDR inlezen'),(2,'Kleur instellen'),(3,'RGB Ring Aan'),(4,'RGB Ring Uit'),(5,'RGB ring Brightness aanpassen'),(6,'RGB ring Auto Brightness Aan'),(7,'RGB ring Auto Brightness Uit');
/*!40000 ALTER TABLE `actie` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alarm`
--

DROP TABLE IF EXISTS `alarm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alarm` (
  `alarmID` int NOT NULL AUTO_INCREMENT,
  `naam` varchar(45) NOT NULL DEFAULT 'Alarm',
  `tijd` datetime NOT NULL,
  `actief` tinyint NOT NULL,
  `herhaal` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`alarmID`)
) ENGINE=InnoDB AUTO_INCREMENT=150 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alarm`
--

LOCK TABLES `alarm` WRITE;
/*!40000 ALTER TABLE `alarm` DISABLE KEYS */;
/*!40000 ALTER TABLE `alarm` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device`
--

DROP TABLE IF EXISTS `device`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `device` (
  `deviceID` int NOT NULL AUTO_INCREMENT,
  `naam` varchar(45) NOT NULL,
  `beschrijving` varchar(250) DEFAULT NULL,
  `meeteenheid` varchar(5) DEFAULT NULL,
  `aankoopkost` double NOT NULL,
  `type` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`deviceID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device`
--

LOCK TABLES `device` WRITE;
/*!40000 ALTER TABLE `device` DISABLE KEYS */;
INSERT INTO `device` VALUES (1,'Joytstick','Knop van de joystick',NULL,2.5,'Actuator'),(2,'LDR','Lichtsterke berekenen','%',0.3,'Sensor'),(3,'Gewicht','Het gewicht meten','g',3,'Sensor'),(4,'RGB Ring','Ring van ledjes',NULL,5,'Sensor');
/*!40000 ALTER TABLE `device` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `historiek`
--

DROP TABLE IF EXISTS `historiek`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `historiek` (
  `historiekID` int NOT NULL AUTO_INCREMENT,
  `datum` datetime NOT NULL,
  `waarde` varchar(25) DEFAULT NULL,
  `commentaar` varchar(250) DEFAULT NULL,
  `deviceID` int DEFAULT NULL,
  `actieID` int NOT NULL,
  PRIMARY KEY (`historiekID`,`actieID`),
  KEY `fk_History_Device_idx` (`deviceID`),
  KEY `fk_History_Actie1_idx` (`actieID`),
  CONSTRAINT `fk_History_Actie1` FOREIGN KEY (`actieID`) REFERENCES `actie` (`actieID`),
  CONSTRAINT `fk_History_Device` FOREIGN KEY (`deviceID`) REFERENCES `device` (`deviceID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historiek`
--

LOCK TABLES `historiek` WRITE;
/*!40000 ALTER TABLE `historiek` DISABLE KEYS */;
/*!40000 ALTER TABLE `historiek` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `slaap`
--

DROP TABLE IF EXISTS `slaap`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `slaap` (
  `slaapID` int NOT NULL AUTO_INCREMENT,
  `starttijd` datetime NOT NULL,
  `eindtijd` datetime NOT NULL,
  `effectievetijd` datetime DEFAULT NULL,
  PRIMARY KEY (`slaapID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `slaap`
--

LOCK TABLES `slaap` WRITE;
/*!40000 ALTER TABLE `slaap` DISABLE KEYS */;
/*!40000 ALTER TABLE `slaap` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-06-19 14:01:10
