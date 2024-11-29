-- 아래 script 를 순서대로 수행

-- Database 생성
CREATE DATABASE `recommend`; /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */ /*!80016 DEFAULT ENCRYPTION='N' */

-- temp table 생성
CREATE TABLE `place_info_temp` (
  `place_id` bigint DEFAULT NULL,
  `place_name` varchar(500) DEFAULT NULL,
  `comm_score` float DEFAULT NULL,
  `cover_image_url` varchar(500) DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  `tag_list` varchar(500) DEFAULT NULL,
  `coordinate_type` varchar(100) DEFAULT NULL,
  `latitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  `address` varchar(500) DEFAULT NULL,
  `description` longtext DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `place_review_temp` (
  `place_id` bigint DEFAULT NULL,
  `head_image` varchar(500) DEFAULT NULL,
  `user_name` varchar(100) DEFAULT NULL,
  `content` longtext DEFAULT NULL,
  `user_rating` float DEFAULT NULL,
  `create_time` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- * temp table 생성 후 temp_data_save.ipynb 수행 - 위의 temp table 에 데이터 생성

-- user_name 이 없는 데이터에 user_name 생성
WITH t_table AS (
SELECT rev.place_id
      ,rev.content
      ,rev.user_rating
      ,rev.create_time
      ,concat('Anonymous User', ROW_NUMBER() OVER (ORDER BY rev.create_time, rev.place_id)) AS user_name
FROM   (SELECT DISTINCT prt.place_id
              ,prt.content
              ,prt.user_rating
              ,prt.create_time
        FROM   place_review_temp prt
        WHERE  prt.user_name IS NULL
        ORDER BY prt.create_time) rev
)
UPDATE place_review_temp prt1
INNER JOIN t_table t
      ON   prt1.place_id = t.place_id
      AND  prt1.user_rating = t.user_rating
      AND  prt1.create_time = t.create_time
      AND  ifnull(prt1.content, '') = ifnull(t.content, '')
SET    prt1.user_name = t.user_name
;


-- 생성할 테이블
-- Location
CREATE TABLE `tbl_locations` (
    `location_id` int NOT NULL AUTO_INCREMENT,
    `location_name` varchar(100) NOT NULL,
    `update_date` datetime DEFAULT NULL,
    `updated_by` int DEFAULT NULL,
    PRIMARY KEY (`location_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Tag
CREATE TABLE `tbl_tags` (
    `tag_id` int NOT NULL AUTO_INCREMENT,
    `tag_name` varchar(100) NOT NULL,
    `update_date` datetime DEFAULT NULL,
    `updated_by` int DEFAULT NULL,
    PRIMARY KEY (`tag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Attractions
CREATE TABLE `tbl_attractions` (
    `place_id` int NOT NULL,
    `place_name` varchar(200) NOT NULL,
    `comm_score` float DEFAULT NULL,
    `cover_image_url` varchar(200) DEFAULT NULL,
    `location_id` int DEFAULT NULL,
    `coordinate_type` varchar(10) DEFAULT NULL,
    `latitude` float DEFAULT NULL,
    `longitude` float DEFAULT NULL,
    `address` varchar(300) DEFAULT NULL,
    `description` LONGTEXT DEFAULT NULL,
    `update_date` datetime DEFAULT NULL,
    `updated_by` int DEFAULT NULL,
    PRIMARY KEY (`place_id`),
    CONSTRAINT `tbl_attractions_location_id_fk` FOREIGN KEY (`location_id`) REFERENCES `tbl_locations` (`location_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Attraction tags
CREATE TABLE `tbl_attraction_tags` (
    `attr_tag_id` int NOT NULL AUTO_INCREMENT,
    `place_id` int NOT NULL,
    `tag_id` int NOT NULL,
    `update_date` datetime DEFAULT NULL,
    `updated_by` int DEFAULT NULL,
    PRIMARY KEY (`attr_tag_id`),
    CONSTRAINT `tbl_attraction_tags_place_id_fk` FOREIGN KEY (`place_id`) REFERENCES `tbl_attractions` (`place_id`),
    CONSTRAINT `tbl_attraction_tags_tag_id_fk` FOREIGN KEY (`tag_id`) REFERENCES `tbl_tags` (`tag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Users
CREATE TABLE `tbl_users` (
    `user_id` int NOT NULL AUTO_INCREMENT,
    `user_name` varchar(150) NOT NULL,
    `password` varchar(128) NOT NULL,
    `first_name` varchar(150) DEFAULT NULL,
    `last_name` varchar(150) DEFAULT NULL,
    `email` varchar(254) DEFAULT NULL,
    `create_date` datetime DEFAULT NULL,
    `last_login_date` datetime DEFAULT NULL,
    PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Reviews
CREATE TABLE `tbl_attraction_reviews` (
    `review_id` int NOT NULL AUTO_INCREMENT,
    `place_id` int NOT NULL,
    `user_id` int NOT NULL,
    `content` LONGTEXT DEFAULT NULL,
    `user_rating` float DEFAULT NULL,
    `create_date` datetime DEFAULT NULL,
    PRIMARY KEY (`review_id`),
    CONSTRAINT `tbl_attraction_reviews_place_id_fk` FOREIGN KEY (`place_id`) REFERENCES `tbl_attractions` (`place_id`),
    CONSTRAINT `tbl_attraction_reviews_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `tbl_users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 테이블에 데이터 입력
-- Users
INSERT INTO tbl_users (user_name, password, first_name, create_date, last_login_date)
SELECT concat('user_', ROW_NUMBER() OVER (ORDER BY ifnull(prt.user_name, 'Anonymous User'))) AS user_name
      ,sha2('user12345', 256) AS password
      ,ifnull(prt.user_name, 'Anonymous User') AS first_name
      ,now()
      ,now()
FROM   place_review_temp prt
GROUP BY ifnull(prt.user_name, 'Anonymous User')
;

-- Location
INSERT INTO tbl_locations (location_name, update_date, updated_by)
SELECT pit.location
      ,now() AS update_date
      ,-1 AS updated_by
FROM   place_info_temp pit
GROUP BY pit.location
ORDER BY location
;

-- Tag
INSERT INTO tbl_tags (tag_name, update_date, updated_by)
SELECT DISTINCT trim(t.tag) AS tag_name
      ,now() AS update_date
      ,-1 AS updated_by
FROM   (
SELECT substring(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), 1, regexp_instr(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), ',', 1, 1)-1) AS tag
FROM   place_info_temp pit
WHERE  pit.tag_list IS NOT NULL
UNION ALL
SELECT IF(regexp_instr(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), ',', 1, 2) != 0,
          substring(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''),
                    regexp_instr(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), ',', 1, 1)+2,
                    regexp_instr(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), ',', 1, 2)-regexp_instr(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), ',', 1, 1)-2),
          IF(regexp_instr(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), ',', 1, 1) != 0,
             substring(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''),
                       regexp_instr(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), ',', 1, 1)+2), ''))
FROM   place_info_temp pit
WHERE  pit.tag_list IS NOT NULL
UNION ALL
SELECT IF(regexp_instr(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), ',', 1, 3) != 0,
          substring(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''),
                    regexp_instr(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), ',', 1, 2)+2,
                    regexp_instr(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), ',', 1, 3)-regexp_instr(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), ',', 1, 2)-2),
          IF(regexp_instr(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), ',', 1, 2) != 0,
             substring(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''),
                       regexp_instr(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), ',', 1, 2)+2), ''))
FROM   place_info_temp pit
WHERE  pit.tag_list IS NOT NULL
UNION ALL
SELECT IF(regexp_instr(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), ',', 1, 4) != 0,
          substring(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''),
                    regexp_instr(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), ',', 1, 3)+2,
                    regexp_instr(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), ',', 1, 4)-regexp_instr(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), ',', 1, 3)-2),
          IF(regexp_instr(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), ',', 1, 3) != 0,
             substring(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''),
                       regexp_instr(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), ',', 1, 3)+2), ''))
FROM   place_info_temp pit
WHERE  pit.tag_list IS NOT NULL
UNION ALL
SELECT IF(regexp_instr(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), ',', 1, 4) != 0,
          substring(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''),
                    regexp_instr(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), ',', 1, 4)+2), '')
FROM   place_info_temp pit
WHERE  pit.tag_list IS NOT NULL
) t
WHERE  trim(t.tag) != ''
;

-- Attractions
DELETE FROM place_info_temp
WHERE  place_name IS NULL
;

INSERT INTO tbl_attractions (place_id, place_name, comm_score, cover_image_url, location_id, coordinate_type, latitude, longitude, address, description, update_date, updated_by)
SELECT DISTINCT pit.place_id
      ,pit.place_name
      ,pit.comm_score
      ,pit.cover_image_url
      ,tl.location_id
      ,pit.coordinate_type
      ,pit.latitude
      ,pit.longitude
      ,pit.address
      ,pit.description
      ,now() AS update_date
      ,-1 AS updated_by
FROM   place_info_temp pit
LEFT OUTER JOIN tbl_locations tl
           ON   pit.location = tl.location_name
;

-- Attraction tags
INSERT INTO tbl_attraction_tags (place_id, tag_id, update_date, updated_by)
SELECT pit.place_id
      ,tt.tag_id
      ,now() AS update_date
      ,-1 AS updated_by
FROM   place_info_temp pit
INNER JOIN tbl_tags tt
      ON   substring(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), 1, regexp_instr(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), ',', 1, 1)-1) = tt.tag_name
WHERE  pit.tag_list IS NOT NULL
UNION ALL
SELECT pit.place_id
      ,tt.tag_id
      ,now() AS update_date
      ,-1 AS updated_by
FROM   place_info_temp pit
INNER JOIN tbl_tags tt
      ON   IF(regexp_instr(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), ',', 1, 2) != 0,
              substring(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''),
                        regexp_instr(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), ',', 1, 1)+2,
                        regexp_instr(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), ',', 1, 2)-regexp_instr(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), ',', 1, 1)-2),
              IF(regexp_instr(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), ',', 1, 1) != 0,
                 substring(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''),
                           regexp_instr(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), ',', 1, 1)+2), '')) = tt.tag_name
WHERE  pit.tag_list IS NOT NULL
UNION ALL
SELECT pit.place_id
      ,tt.tag_id
      ,now() AS update_date
      ,-1 AS updated_by
FROM   place_info_temp pit
INNER JOIN tbl_tags tt
      ON   IF(regexp_instr(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), ',', 1, 3) != 0,
              substring(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''),
                        regexp_instr(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), ',', 1, 2)+2,
                        regexp_instr(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), ',', 1, 3)-regexp_instr(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), ',', 1, 2)-2),
              IF(regexp_instr(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), ',', 1, 2) != 0,
                 substring(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''),
                           regexp_instr(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), ',', 1, 2)+2), '')) = tt.tag_name
WHERE  pit.tag_list IS NOT NULL
UNION ALL
SELECT pit.place_id
      ,tt.tag_id
      ,now() AS update_date
      ,-1 AS updated_by
FROM   place_info_temp pit
INNER JOIN tbl_tags tt
      ON   IF(regexp_instr(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), ',', 1, 4) != 0,
              substring(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''),
                        regexp_instr(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), ',', 1, 3)+2,
                        regexp_instr(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), ',', 1, 4)-regexp_instr(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), ',', 1, 3)-2),
              IF(regexp_instr(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), ',', 1, 3) != 0,
                 substring(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''),
                           regexp_instr(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), ',', 1, 3)+2), '')) = tt.tag_name
WHERE  pit.tag_list IS NOT NULL
UNION ALL
SELECT pit.place_id
      ,tt.tag_id
      ,now() AS update_date
      ,-1 AS updated_by
FROM   place_info_temp pit
INNER JOIN tbl_tags tt
      ON   IF(regexp_instr(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), ',', 1, 4) != 0,
              substring(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''),
                        regexp_instr(regexp_replace(pit.tag_list, '[\'\\[\\]]', ''), ',', 1, 4)+2), '') = tt.tag_name
WHERE  pit.tag_list IS NOT NULL
ORDER BY place_id
;

-- Attraction reviews
INSERT INTO tbl_attraction_reviews (place_id, user_id, content, user_rating, create_date)
SELECT DISTINCT prt.place_id
      ,tu.user_id
      ,ifnull(prt.content, ' ') AS content
      ,prt.user_rating
      ,str_to_date(prt.create_time, '%Y-%m-%d %H:%i:%s') AS create_date
FROM   place_review_temp prt
INNER JOIN tbl_users tu
      ON   ifnull(prt.user_name, 'Anonymous User') = tu.first_name
;

CREATE INDEX tbl_users_n1 ON tbl_users (first_name);
CREATE INDEX tbl_tags_n1 ON tbl_tags (tag_name);
CREATE INDEX tbl_locations_n1 ON tbl_locations (location_name);
CREATE INDEX tbl_attractions_n1 ON tbl_attractions (place_name);
CREATE INDEX tbl_attraction_tags_n1 ON tbl_attraction_tags (place_id);
CREATE INDEX tbl_attraction_tags_n2 ON tbl_attraction_tags (tag_id);