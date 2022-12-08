-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.4.19-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             12.2.0.6576
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for adms
CREATE DATABASE IF NOT EXISTS `adms` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE `adms`;

-- Dumping structure for table adms.tbl_accreditation_tasks
CREATE TABLE IF NOT EXISTS `tbl_accreditation_tasks` (
  `at_id` int(11) NOT NULL AUTO_INCREMENT,
  `at_task` text DEFAULT NULL,
  `at_remarks` text DEFAULT NULL,
  `date_added` datetime DEFAULT NULL,
  PRIMARY KEY (`at_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

-- Dumping data for table adms.tbl_accreditation_tasks: ~0 rows (approximately)

-- Dumping structure for table adms.tbl_accreditation_task_details
CREATE TABLE IF NOT EXISTS `tbl_accreditation_task_details` (
  `atd_id` int(11) NOT NULL AUTO_INCREMENT,
  `at_id` int(11) DEFAULT NULL,
  `doc_id` int(11) DEFAULT NULL,
  `atd_desc` text DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `date_added` datetime DEFAULT NULL,
  PRIMARY KEY (`atd_id`),
  KEY `at_id` (`at_id`),
  KEY `doc_id` (`doc_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `tbl_accreditation_task_details_ibfk_1` FOREIGN KEY (`at_id`) REFERENCES `tbl_accreditation_tasks` (`at_id`),
  CONSTRAINT `tbl_accreditation_task_details_ibfk_2` FOREIGN KEY (`doc_id`) REFERENCES `tbl_documents` (`doc_id`) ON DELETE SET NULL,
  CONSTRAINT `tbl_accreditation_task_details_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `tbl_user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;

-- Dumping data for table adms.tbl_accreditation_task_details: ~0 rows (approximately)

-- Dumping structure for table adms.tbl_documents
CREATE TABLE IF NOT EXISTS `tbl_documents` (
  `doc_id` int(11) NOT NULL AUTO_INCREMENT,
  `doc_type_id` int(11) DEFAULT NULL,
  `doc_name` varchar(150) DEFAULT NULL,
  `doc_desc` text DEFAULT NULL,
  `doc_file` text DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `date_added` datetime DEFAULT NULL,
  PRIMARY KEY (`doc_id`),
  KEY `doc_type_id` (`doc_type_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `tbl_documents_ibfk_1` FOREIGN KEY (`doc_type_id`) REFERENCES `tbl_document_types` (`doc_type_id`) ON DELETE CASCADE,
  CONSTRAINT `tbl_documents_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `tbl_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;

-- Dumping data for table adms.tbl_documents: ~0 rows (approximately)

-- Dumping structure for table adms.tbl_document_types
CREATE TABLE IF NOT EXISTS `tbl_document_types` (
  `doc_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `doc_type_title` varchar(150) DEFAULT NULL,
  `doc_type_desc` text DEFAULT NULL,
  `date_added` datetime DEFAULT NULL,
  PRIMARY KEY (`doc_type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

-- Dumping data for table adms.tbl_document_types: ~4 rows (approximately)
INSERT INTO `tbl_document_types` (`doc_type_id`, `doc_type_title`, `doc_type_desc`, `date_added`) VALUES
	(1, 'Accreditation Process Flow Chart', '', '2022-12-02 14:19:32'),
	(2, 'Accreditation Process Guidelindes for Institutions', '', '2022-12-02 22:47:45'),
	(6, 'Appointment as Commissioner Template', '', '2022-12-02 22:47:45'),
	(7, 'Standards and Criteria', '', '2022-12-02 22:47:45');

-- Dumping structure for table adms.tbl_user
CREATE TABLE IF NOT EXISTS `tbl_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fname` varchar(150) DEFAULT NULL,
  `mname` varchar(150) DEFAULT NULL,
  `lname` varchar(150) DEFAULT NULL,
  `username` varchar(150) DEFAULT NULL,
  `password` varchar(150) DEFAULT NULL,
  `category` varchar(150) DEFAULT NULL,
  `date_added` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

-- Dumping data for table adms.tbl_user: ~4 rows (approximately)
INSERT INTO `tbl_user` (`id`, `fname`, `mname`, `lname`, `username`, `password`, `category`, `date_added`) VALUES
	(1, 'Eduard RIno111', 'Questo', 'Carton', 'jag', 'sha256$srhW5avnCjLm7Tkj$0502c352f2f30fa5dfb8111d4c3e72b7c13d9f3da7f76bb3d72aabd5ba97977f', 'Admin', '2022-12-02 13:43:09'),
	(3, 'Jagwarthegreat', 'Questo', 'Carton', 'rin', 'sha256$srhW5avnCjLm7Tkj$0502c352f2f30fa5dfb8111d4c3e72b7c13d9f3da7f76bb3d72aabd5ba97977f', 'Admin', '2022-11-25 16:29:56'),
	(4, 'Kaye', 'N', 'Jacildo', 'k', 'sha256$M3gleJORbojiiJZa$9fa9bf27c354e5e782e95065b1619c9a055e431f345e96c32871fc96407eac75', 'Staff', '2022-11-28 14:22:45'),
	(5, 'jep', 'jep', 'jep', 'jep', 'sha256$B9R8kNibhLTUMID7$01913bf18355117e4fe44cb46088414b749b920628da446028d430998943d565', 'Staff', '2022-11-28 21:12:53');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
