
create table if not exists svm_review (
  review_id integer primary key AUTOINCREMENT,
  game_id string not null,
  text string not null,
  score string not null,
  update_time TimeStamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ;

create table if not exists svm_feature (
  review_id string primary key,
  game_id string not null,
  feature string not null,
  feature_score string not null,
  update_time TimeStamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ;
