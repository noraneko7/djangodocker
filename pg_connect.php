<?php
 $db = parse_url(getenv('DATABASE_URL'));
 $user = "admin";
 $password = 'adminpass';
 $dbh = new PDO($dsn,$user,$password);