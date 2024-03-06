--SE CREAZA BAZA DE DATE
CREATE DATABASE `proiect_final`;
--SE CREAZA TABELA acces
CREATE TABLE `proiect_final`.`acces` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Id_Persoana` int DEFAULT NULL,
  `Data` datetime DEFAULT NULL,
  `Sens` varchar(3) DEFAULT NULL,
  `Poarta` int DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ;
--SE CREAZA TABELA admins
CREATE TABLE `proiect_final`.`admins` (
  `id` int NOT NULL AUTO_INCREMENT,
  `mail` varchar(30) DEFAULT NULL,
  `password` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ;
--SE CREAZA TABELA persoane
CREATE TABLE `proiect_final`.`persoane` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Nume` varchar(50) DEFAULT NULL,
  `Prenume` varchar(50) DEFAULT NULL,
  `Companie` varchar(50) DEFAULT NULL,
  `IdManager` int DEFAULT NULL,
  `Email` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ;
--SE INSEREAZA 2 ELEMENTE IN TABELA admins
INSERT INTO `proiect_final`.`admins`  VALUES(Null,'00ntexar00@gmail.com','#nt-exar{0}');
INSERT INTO `proiect_final`.`admins`  VALUES(Null,'danutlazar128@gmail.com','LAzAR123');
--SE IINSEREAZA 8 ELEMENTE IN TABELA persoane
INSERT INTO `proiect_final`.`persoane`  VALUES(Null,'Lazar','Daniel','NT-Exar',0,'00ntexar00@gmail.com');
INSERT INTO `proiect_final`.`persoane`  VALUES(Null,'Preda','Alex','NT-Exar',1,'pred4alex@gmail.com');
INSERT INTO `proiect_final`.`persoane`  VALUES(Null,'Vaida','Ion','NT-Exar',1,'ionVD12@gmail.com');
INSERT INTO `proiect_final`.`persoane`  VALUES(Null,'Pop','Vasile','NT-Exar',1,'vaspopile5@gmail.com');
INSERT INTO `proiect_final`.`persoane`  VALUES(Null,'Ionescu','Andrei','NT-Exar',1,'ioneandre11@gmail.com');
INSERT INTO `proiect_final`.`persoane`  VALUES(Null,'Florescu','Iulian','NT-Exar',1,'floriuliscu90@gmail.com');
INSERT INTO `proiect_final`.`persoane`  VALUES(Null,'Danil','Stefan',	'NT-Exar',1,'danilstefann11@gmail.com');
INSERT INTO `proiect_final`.`persoane`  VALUES(Null,'Lazar','Iulian',	'NT-Exar',1,'lzriul43@gmail.com');