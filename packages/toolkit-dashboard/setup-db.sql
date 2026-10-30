-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS qfdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE qfdb;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    psw VARCHAR(255) NOT NULL,
    createdon DATETIME NOT NULL,
    roles VARCHAR(100),
    age VARCHAR(50),
    gender VARCHAR(50),
    country VARCHAR(100),
    isvalidated TINYINT(1) DEFAULT 0,
    isdel TINYINT(1) DEFAULT 0,
    -- Separate from the self-selected `roles` field: only settable manually/via admin-users.html
    isadmin TINYINT(1) NOT NULL DEFAULT 0,
    INDEX idx_email (email),
    INDEX idx_isdel (isdel)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Audit trail for DAT graph CRUD, used to support the manual Undo feature
CREATE TABLE IF NOT EXISTS dat_change_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_email VARCHAR(255) NOT NULL,
    dat_uri VARCHAR(500) NOT NULL,
    action VARCHAR(20) NOT NULL, -- create | update | delete | undo
    old_value MEDIUMTEXT,        -- JSON snapshot of properties before the action (NULL for create)
    new_value MEDIUMTEXT,        -- JSON snapshot of properties after the action (NULL for delete)
    undone_log_id INT NULL,      -- set on an 'undo' row: the log entry it reverted
    createdon DATETIME NOT NULL,
    INDEX idx_dat_uri (dat_uri),
    INDEX idx_createdon (createdon)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Audit trail for who granted/revoked admin rights (managed only via admin-users.html)
CREATE TABLE IF NOT EXISTS admin_role_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    actor_email VARCHAR(255) NOT NULL,   -- the super-admin who made the change
    target_email VARCHAR(255) NOT NULL,  -- the user whose isadmin flag changed
    new_isadmin TINYINT(1) NOT NULL,
    createdon DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
