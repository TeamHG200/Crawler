create table if not exists svm_review (
  review_id integer primary key AUTOINCREMENT,
  game_id string not null,
  text string not null,
  score string not null,
  update_time TimeStamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ;

create table if not exists svm_words (
  review_id string primary key,
  game_id string not null,
  words string not null,
  emotion_words string not null,
  update_time TimeStamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ;

create table if not exists svm_feature (
  review_id string primary key,
  game_id string not null,
  feature string not null,
  feature_score string not null,
  update_time TimeStamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ;

create table if not exists svm_result (
  game_id string primary key ,
  good_review string not null,
  bad_review string not null,
  rate string not null,
  update_time TimeStamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ;
