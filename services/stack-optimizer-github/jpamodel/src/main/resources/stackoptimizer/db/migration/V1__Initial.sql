CREATE TABLE IF NOT EXISTS `optimization_parameters` (
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `location_uuid` varchar(50) NOT NULL,
    `parameter_name` varchar(50),
    `parameter_value` varchar(50),
    `value_from` varchar(50),
    `value_to` varchar(50),
    `value_type` varchar(50),
    `uom` varchar(50),
    `default_value` varchar(50),
    `description` varchar(50),
    `created_by` varchar(100) NOT NULL,
    `modified_by` varchar(100) NOT NULL,
    `created_on` datetime NOT NULL,
    `modified_on` datetime NOT NULL,
    PRIMARY KEY (`id`)
    );