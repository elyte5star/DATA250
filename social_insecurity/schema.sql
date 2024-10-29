-- --
-- Create tables
-- --

CREATE TABLE [Users] (
  id INTEGER NOT NULL,
  userid VARCHAR(60) NOT NULL UNIQUE,
  username VARCHAR(60) NOT NULL UNIQUE,
  first_name VARCHAR(60) NOT NULL,
  last_name VARCHAR(60) NOT NULL,
  [password] VARCHAR(255) NOT NULL,
  [creation_time] DATETIME NOT NULL,
  [modification_time] DATETIME NOT NULL,
  modified_by VARCHAR(60) NOT NULL DEFAULT 'NewAccount',
  active BOOLEAN NOT NULL DEFAULT 1,
  education VARCHAR(30) DEFAULT 'Unknown',
  employment VARCHAR(30) DEFAULT 'Unknown',
  music VARCHAR(30) DEFAULT 'Unknown',
  movie VARCHAR(30) DEFAULT 'Unknown',
  nationality VARCHAR(30) DEFAULT 'Unknown',
  birthday DATE DEFAULT 'Unknown',
  PRIMARY KEY(id,userid)
  
);

CREATE TABLE [Posts](
  id INTEGER PRIMARY KEY,
  u_id VARCHAR(60),
  content VARCHAR(300),
  [image] VARCHAR,
  [creation_time] DATETIME,
  FOREIGN KEY (u_id) REFERENCES [Users](userid)
);

CREATE TABLE [Friends](
  u_id VARCHAR(60) NOT NULL REFERENCES Users,
  f_id INTEGER NOT NULL REFERENCES Users,
  PRIMARY KEY(u_id, f_id),
  FOREIGN KEY (u_id) REFERENCES [Users](userid),
  FOREIGN KEY (f_id) REFERENCES [Users](userid)
);

CREATE TABLE [Comments](
  id INTEGER PRIMARY KEY,
  p_id INTEGER,
  u_id VARCHAR(60),
  comment VARCHAR(300),
  [creation_time] DATETIME,
  FOREIGN KEY (p_id) REFERENCES Posts(id),
  FOREIGN KEY (u_id) REFERENCES Users(userid)
);

-- --
-- Populate tables with test data
-- --

-- INSERT INTO Users (
--   id,
--   username,
--   userid,
--   first_name,
--   last_name,
--   [password],
--   creation_time,
--   modification_time,
--   modified_by  
-- )
-- VALUES (
--   "219dcf8f-3036-47fc-b961-c3d237431582",
--   'test',
--   '259dcf8f-3036-47fc-b961-c3d237431584',
--   'Jane',
--   'Doe',
--   'password123',
--   '13/01/2024',
--   '13/01/2024'
--   'test'

-- );