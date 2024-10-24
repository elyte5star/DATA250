-- --
-- Create tables
-- --

CREATE TABLE [Users] (
  id INTEGER NOT NULL,
  userid VARCHAR(60) NOT NULL,
  username VARCHAR(60) NOT NULL,
  first_name VARCHAR(60) NOT NULL,
  last_name VARCHAR(60) NOT NULL,
  [password] VARCHAR(255) NOT NULL,
  [creation_time] DATETIME NOT NULL,
  [modification_time] DATETIME NOT NULL,
  education VARCHAR DEFAULT 'Unknown',
  employment VARCHAR DEFAULT 'Unknown',
  music VARCHAR DEFAULT 'Unknown',
  movie VARCHAR DEFAULT 'Unknown',
  nationality VARCHAR DEFAULT 'Unknown',
  birthday DATE DEFAULT 'Unknown',
  PRIMARY KEY(id,userid)
  
);

CREATE TABLE [Posts](
  id INTEGER PRIMARY KEY,
  u_id INTEGER,
  content INTEGER,
  [image] VARCHAR,
  [creation_time] DATETIME,
  FOREIGN KEY (u_id) REFERENCES [Users](userid)
);

CREATE TABLE [Friends](
  u_id INTEGER NOT NULL REFERENCES Users,
  f_id INTEGER NOT NULL REFERENCES Users,
  PRIMARY KEY(u_id, f_id),
  FOREIGN KEY (u_id) REFERENCES [Users](userid),
  FOREIGN KEY (f_id) REFERENCES [Users](userid)
);

CREATE TABLE [Comments](
  id INTEGER PRIMARY KEY,
  p_id INTEGER,
  u_id INTEGER,
  comment VARCHAR,
  [creation_time] DATETIME,
  FOREIGN KEY (p_id) REFERENCES Posts(id),
  FOREIGN KEY (u_id) REFERENCES Users(userid)
);

-- --
-- Populate tables with test data
-- --

INSERT INTO Users (
  id,
  username,
  userid,
  first_name,
  last_name,
  [password],
  creation_time,
  modification_time
)
VALUES (
  "219dcf8f-3036-47fc-b961-c3d237431582",
  'test',
  '259dcf8f-3036-47fc-b961-c3d237431584',
  'Jane',
  'Doe',
  'password123',
  '13/01/2024',
  '13/01/2024'

);