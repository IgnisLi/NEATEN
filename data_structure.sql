
CREATE TABLE `agree_login` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `identifier` varchar(20) NOT NULL,
  `time` datetime NOT NULL,
  `success` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ;

CREATE TABLE `agree_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `identifier` varchar(20) NOT NULL,
  `voiceprint` blob NOT NULL,
  PRIMARY KEY (`id`)
) 
