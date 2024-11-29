WITH dt AS (
SELECT ta.place_id
      ,ta.place_name
      ,ta.comm_score
      ,ta.cover_image_url
      ,tl.location_name AS location
      ,ifnull((SELECT group_concat(tt.tag_name) 
               FROM   tbl_attraction_tags tat
               INNER JOIN tbl_tags tt
                     ON   tat.tag_id = tt.tag_id
               WHERE  tat.place_id = ta.place_id), ' ') AS tags
      ,ta.coordinate_type
      ,ta.latitude
      ,ta.longitude
      ,ta.address
      ,ta.description
      ,tu.first_name AS user_name
      ,ifnull(tar.content, ' ') AS content
      ,ifnull(tar.user_rating, ta.comm_score) AS user_rating
      ,ifnull(date_format(tar.create_date, '%Y-%m-%d %H:%i:%s'), '2018-01-01 00:00:00') AS create_time
FROM   tbl_attractions ta
LEFT OUTER JOIN tbl_locations tl
           ON   ta.location_id = tl.location_id
LEFT OUTER JOIN tbl_attraction_reviews tar
           ON   ta.place_id = tar.place_id
LEFT OUTER JOIN tbl_users tu
           ON   tar.user_id = tu.user_id
)
SELECT *
FROM   dt tbl
-- WHERE  tbl.user_name IS NULL
;

-- ------------------------------

WITH dt AS (
SELECT ta.place_id
      ,ta.place_name
      ,ta.comm_score
      ,ta.cover_image_url
      ,tl.location_name AS location
      ,ifnull((SELECT group_concat(tt.tag_name) 
               FROM   tbl_attraction_tags tat
               INNER JOIN tbl_tags tt
                     ON   tat.tag_id = tt.tag_id
               WHERE  tat.place_id = ta.place_id), ' ') AS tags
      ,ta.coordinate_type
      ,ta.latitude
      ,ta.longitude
      ,ta.address
      ,ta.description
      ,tu.user_name
      ,ifnull(tar.content, ' ') AS content
      ,ifnull(tar.user_rating, ta.comm_score) AS user_rating
      ,ifnull(date_format(tar.create_date, '%Y-%m-%d %H:%i:%s'), '2018-01-01 00:00:00') AS create_time
FROM   tbl_attractions ta
LEFT OUTER JOIN tbl_locations tl
           ON   ta.location_id = tl.location_id
LEFT OUTER JOIN tbl_attraction_reviews tar
           ON   ta.place_id = tar.place_id
LEFT OUTER JOIN tbl_users tu
           ON   tar.user_id = tu.user_id
)
SELECT *
FROM   dt tbl
-- WHERE  tbl.user_name IS NOT NULL
;

-- ------------------------------

WITH dt AS (
SELECT ta.place_id
      ,ta.place_name
      ,ta.comm_score
      ,ta.cover_image_url
      ,tl.location_name AS location
      ,ifnull((SELECT group_concat(tt.tag_name) 
               FROM   tbl_attraction_tags tat
               INNER JOIN tbl_tags tt
                     ON   tat.tag_id = tt.tag_id
               WHERE  tat.place_id = ta.place_id), ' ') AS tags
      ,ta.coordinate_type
      ,ta.latitude
      ,ta.longitude
      ,ta.address
      ,ta.description
      ,tu.user_name
      ,ifnull(tar.content, ' ') AS content
      ,ifnull(tar.user_rating, ta.comm_score) AS user_rating
      ,ifnull(date_format(tar.create_date, '%Y-%m-%d %H:%i:%s'), '2018-01-01 00:00:00') AS create_time
FROM   tbl_attractions ta
LEFT OUTER JOIN tbl_locations tl
           ON   ta.location_id = tl.location_id
LEFT OUTER JOIN tbl_attraction_reviews tar
           ON   ta.place_id = tar.place_id
LEFT OUTER JOIN tbl_users tu
           ON   tar.user_id = tu.user_id
)
SELECT tbl.place_id AS p_id
      ,tbl.place_name
      ,tbl.comm_score AS score
      ,tbl.address
      ,tbl.content
FROM   dt tbl
-- WHERE  tbl.user_name IS NOT NULL
;